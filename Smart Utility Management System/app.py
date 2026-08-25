from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db, get_connection
from models.user import load_users, login_user, register_user
from models.usage import simulate_usage, get_usage_linked_list, get_today_usage, get_chart_data, get_sorted_usage, search_usage_by_date
from models.alerts import generate_alerts, get_alerts_priority_queue
from models.network import find_shortest_route, find_affected_areas, get_all_areas
from models.recommendations import get_recommendations
from models.awareness import AWARENESS_CONTENT
from ml.forecast import get_all_forecasts
from dsa.tree import CityTree

from dsa.stack import Stack
# Global stack for recent alerts per session
recent_alerts_stack = Stack()

from models.translator import load_translations, translate

app = Flask(__name__)
app.secret_key = "smartutility2024"

@app.context_processor
def inject_translator():
    def _(key, default=None):
        lang = session.get("lang", "en")
        ht = load_translations(lang)
        result = translate(ht, key)
        return result if result != key else (default if default else key)
    return dict(_=_, lang=session.get("lang", "en"))

@app.route("/set_lang/<lang>", methods=["GET", "POST"])
def set_lang(lang):
    session["lang"] = lang
    return redirect(request.referrer or url_for("home"))

# Initialize database and load users on startup
init_db()
load_users()

# Landing page
@app.route("/")
def home():
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role     = request.form.get("role", "citizen")

        success, result = login_user(username, password, role)

        if success:
            session["username"] = username
            session["role"]     = result
            session["just_logged_in"] = True

            if result == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("dashboard"))
        else:
            error = result

    return render_template("login.html", error=error)

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    error   = None
    success = None

    if request.method == "POST":
        username         = request.form.get("username")
        password         = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role             = request.form.get("role")
        email            = request.form.get("email", "")
        phone            = request.form.get("phone", "")

        if password != confirm_password:
            error = "Passwords do not match!"
        else:
            ok, msg = register_user(username, password, role, email, phone)
            if ok:
                success = "Account created! You can now login."
            else:
                error = msg

    return render_template("register.html", error=error, success=success)

# Helper function to get dashboard data
def get_dashboard_data(user_id):
    simulate_usage(user_id)
    today  = get_today_usage(user_id)
    generate_alerts(user_id, today)
    alerts = get_alerts_priority_queue(user_id)

    # Send email only once per day
    if alerts:
        conn2   = get_connection()
        cursor2 = conn2.cursor()
        cursor2.execute("SELECT email FROM users WHERE id = %s", (user_id,))
        user_email = cursor2.fetchone()
        conn2.close()

        if user_email and user_email[0]:
            from models.email_sender import send_alert_email
            from models.alerts import check_email_sent_today

            # Only send if not sent today
            email_key = f"email_sent_{user_id}"
            if email_key not in session:
                send_alert_email(user_email[0], session["username"], alerts)
                session[email_key] = True

    elec_labels,  elec_data  = get_chart_data(user_id, "electricity")
    water_labels, water_data = get_chart_data(user_id, "water")
    gas_labels,   gas_data   = get_chart_data(user_id, "gas")

    recommendations = get_recommendations(today)

    return today, alerts, elec_labels, elec_data, water_labels, water_data, gas_labels, gas_data, recommendations


# Citizen dashboard
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
    user   = cursor.fetchone()
    conn.close()
    user_id = user[0]

    today, alerts, elec_labels, elec_data, water_labels, water_data, gas_labels, gas_data, recommendations = get_dashboard_data(user_id)

    ll      = get_usage_linked_list(user_id)
    history = ll.to_list()

    return render_template("dashboard.html",
        username       = session["username"],
        today          = today,
        alerts         = alerts,
        elec_labels    = elec_labels,
        elec_data      = elec_data,
        water_labels   = water_labels,
        water_data     = water_data,
        gas_labels     = gas_labels,
        gas_data       = gas_data,
        history        = history,
        sorted         = False,
        search_results = [],
        search_date    = "",
        recommendations = recommendations
    )

# Sort by amount (Merge Sort)
@app.route("/sort_usage")
def sort_usage():
    if "username" not in session:
        return redirect(url_for("login"))

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
    user   = cursor.fetchone()
    conn.close()
    user_id = user[0]

    today, alerts, elec_labels, elec_data, water_labels, water_data, gas_labels, gas_data, recommendations = get_dashboard_data(user_id)

    sorted_history = get_sorted_usage(user_id)

    return render_template("dashboard.html",
        username       = session["username"],
        today          = today,
        alerts         = alerts,
        elec_labels    = elec_labels,
        elec_data      = elec_data,
        water_labels   = water_labels,
        water_data     = water_data,
        gas_labels     = gas_labels,
        gas_data       = gas_data,
        history        = sorted_history,
        sorted         = True,
        search_results = [],
        search_date    = "",
        recommendations = recommendations
    )

# Search by date (Binary Search)
@app.route("/search_usage")
def search_usage():
    if "username" not in session:
        return redirect(url_for("login"))

    target_date = request.args.get("date", "")

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
    user   = cursor.fetchone()
    conn.close()
    user_id = user[0]

    today, alerts, elec_labels, elec_data, water_labels, water_data, gas_labels, gas_data, recommendations = get_dashboard_data(user_id)

    ll      = get_usage_linked_list(user_id)
    history = ll.to_list()

    search_results = search_usage_by_date(user_id, target_date) if target_date else []

    return render_template("dashboard.html",
        username       = session["username"],
        today          = today,
        alerts         = alerts,
        elec_labels    = elec_labels,
        elec_data      = elec_data,
        water_labels   = water_labels,
        water_data     = water_data,
        gas_labels     = gas_labels,
        gas_data       = gas_data,
        history        = history,
        sorted         = False,
        search_results = search_results,
        search_date    = target_date,
        recommendations = recommendations
    )

# Network Map (Graph + Dijkstra + BFS)
@app.route("/network", methods=["GET", "POST"])
def network():
    if "username" not in session:
        return redirect(url_for("login"))

    areas       = get_all_areas()
    path        = []
    distance    = -1
    affected    = []
    from_area   = ""
    to_area     = ""
    outage_area = ""
    action      = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "dijkstra":
            from_area = request.form.get("from_area")
            to_area   = request.form.get("to_area")
            path, distance = find_shortest_route(from_area, to_area)

        elif action == "bfs":
            outage_area = request.form.get("outage_area")
            affected    = find_affected_areas(outage_area)

    return render_template("network.html",
        username    = session["username"],
        areas       = areas,
        path        = path,
        distance    = distance,
        affected    = affected,
        from_area   = from_area,
        to_area     = to_area,
        outage_area = outage_area,
        action      = action
    )


# Utility Details page
@app.route("/utility/<utype>")
def utility_page(utype):
    if "username" not in session:
        return redirect(url_for("login"))
        
    if utype not in ["electricity", "water", "gas"]:
        return redirect(url_for("dashboard"))
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return redirect(url_for("login"))
        
    user_id = user[0]
    
    labels, data = get_chart_data(user_id, utype)
    tips = AWARENESS_CONTENT.get(utype, [])
    
    return render_template("utility.html",
        username=session["username"],
        utype=utype,
        labels=labels,
        data=data,
        awareness_tips=tips
    )

# AI Forecast page
@app.route("/forecast")
def forecast():
    if "username" not in session:
        return redirect(url_for("login"))

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (session["username"],))
    user   = cursor.fetchone()
    conn.close()

    user_id   = user[0]
    forecasts = get_all_forecasts(user_id)

    return render_template("forecast.html",
        username  = session["username"],
        forecasts = forecasts
    )


# City Tree page
@app.route("/tree")
def tree():
    if "username" not in session:
        return redirect(url_for("login"))

    ct        = CityTree()
    root      = ct.build_karachi_tree()
    tree_dict = ct.to_dict()
    traversal = ct.preorder(root)
    areas     = ct.get_all_areas()

    return render_template("tree.html",
        username  = session["username"],
        tree_dict = tree_dict,
        traversal = traversal,
        areas     = areas
    )



# Admin panel
@app.route("/admin")
def admin():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn   = get_connection()
    cursor = conn.cursor()

    # Get all users
    cursor.execute("SELECT id, username, role, email, phone FROM users")
    users = cursor.fetchall()

    # Get total usage stats
    cursor.execute("SELECT type, SUM(amount) FROM usage_data GROUP BY type")
    usage_stats = cursor.fetchall()

    # Get total alerts
    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    # Get usage per user
    cursor.execute('''
        SELECT u.username, ud.type, SUM(ud.amount)
        FROM usage_data ud
        JOIN users u ON u.id = ud.user_id
        GROUP BY u.username, ud.type
    ''')
    user_usage = cursor.fetchall()

    # Get recent system alerts for admin dashboard
    cursor.execute('''
        SELECT message, priority, date 
        FROM alerts 
        ORDER BY date DESC, id DESC 
        LIMIT 10
    ''')
    recent_alerts_rows = cursor.fetchall()

    conn.close()

    # Build usage dict
    usage_dict = {}
    for username, utype, amount in user_usage:
        if username not in usage_dict:
            usage_dict[username] = {"electricity": 0, "water": 0, "gas": 0}
        usage_dict[username][utype] = round(amount, 2)

    # Build stats dict
    stats = {"electricity": 0, "water": 0, "gas": 0}
    for utype, total in usage_stats:
        stats[utype] = round(total, 2)
    
    from dsa.priority_queue import MinHeap
    admin_heap = MinHeap()
    for msg, prio, d in recent_alerts_rows:
        admin_heap.insert(prio, {"message": msg, "priority": prio, "date": str(d)})
    
    admin_alerts = admin_heap.to_list()

    success_msg = session.pop("success", None)

    return render_template("admin.html",
        username     = session["username"],
        users        = users,
        stats        = stats,
        total_alerts = total_alerts,
        usage_dict   = usage_dict,
        total_users  = len(users),
        alerts       = admin_alerts,
        success      = success_msg
    )

# Admin send alert
@app.route("/admin/send_alert", methods=["POST"])
def admin_send_alert():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    message  = request.form.get("message")
    priority = int(request.form.get("priority", 2))

    conn   = get_connection()
    cursor = conn.cursor()

    # Get ALL users so the Admin also receives a copy of their own broadcast
    cursor.execute("SELECT id, username, email FROM users")
    all_users = cursor.fetchall()

    from datetime import date
    from models.email_sender import send_alert_email

    for user_id, username, email in all_users:
        # Save alert to database
        cursor.execute('''
            INSERT INTO alerts (user_id, message, priority, date)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, message, priority, date.today()))

        # Send email if available
        if email:
            send_alert_email(email, username, [(priority, {"message": message, "date": str(date.today())})])

    conn.commit()
    conn.close()

    # Set just_logged_in flag so the modal pops up immediately for the admin
    session["just_logged_in"] = True
    session["success"] = "Message has been sent to all citizens successfully!"

    return redirect(url_for("admin"))


# Admin upload CSV
@app.route("/admin/upload_csv", methods=["POST"])
def admin_upload_csv():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    
    if "csv_file" not in request.files:
        return redirect(url_for("admin"))
        
    file = request.files["csv_file"]
    if file.filename == "":
        return redirect(url_for("admin"))
        
    if file:
        try:
            content = file.read().decode('utf-8').splitlines()
            import csv
            reader = csv.DictReader(content)
            
            conn = get_connection()
            cursor = conn.cursor()
            
            for row in reader:
                try:
                    username = row.get('username')
                    utype = row.get('type')
                    amount = float(row.get('amount', 0))
                    date_val = row.get('date')
                    
                    if not username or not utype or not date_val:
                        continue

                    # Get user id
                    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                    user = cursor.fetchone()
                    if user:
                        user_id = user[0]
                        cursor.execute('''
                            INSERT INTO usage_data (user_id, type, amount, date)
                            VALUES (%s, %s, %s, %s)
                        ''', (user_id, utype, amount, date_val))
                except Exception as e:
                    continue
                    
            conn.commit()
            conn.close()
        except UnicodeDecodeError:
            # User uploaded a non-CSV file (e.g. image)
            pass
            
    return redirect(url_for("admin"))


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)