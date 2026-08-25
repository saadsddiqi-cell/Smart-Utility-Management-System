import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
SENDER_EMAIL    = "utilitymanagementsystem786@gmail.com"      # replace with your gmail
SENDER_PASSWORD = "yoic epqa nvxs sgbk"        # replace with your 16-char app password

def send_alert_email(recipient_email, username, alerts):
    try:
        # Create email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "⚠️ UtilityHub — Active Alerts for Your Account"
        msg["From"]    = SENDER_EMAIL
        msg["To"]      = recipient_email

        # Build alert rows for email
        alert_rows = ""
        for priority, alert in alerts:
            color  = "#ef4444" if priority == 1 else "#f59e0b"
            label  = "CRITICAL 🚨" if priority == 1 else "WARNING ⚠️"
            alert_rows += f"""
            <tr>
                <td style="padding:12px 16px; border-bottom:1px solid #f0f4f8;">
                    <span style="color:{color}; font-weight:700; font-size:12px;">{label}</span><br>
                    <span style="color:#334155; font-size:13px;">{alert['message']}</span><br>
                    <span style="color:#94a3b8; font-size:11px;">📅 {alert['date']}</span>
                </td>
            </tr>
            """

        # HTML email body
        html = f"""
        <html>
        <body style="font-family: Inter, sans-serif; background: #f0f9ff; padding: 20px;">
            <div style="max-width:600px; margin:0 auto; background:#fff; border-radius:16px; overflow:hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.08);">

                <!-- Header -->
                <div style="background: linear-gradient(135deg, #0EA5E9, #10B981); padding: 32px; text-align:center;">
                    <h1 style="color:#fff; font-size:24px; margin:0;">⚡ UtilityHub</h1>
                    <p style="color:rgba(255,255,255,0.8); margin:8px 0 0;">Smart Utility Management System</p>
                </div>

                <!-- Body -->
                <div style="padding: 32px;">
                    <h2 style="color:#0F172A; font-size:20px; margin:0 0 8px;">Hello, {username}! 👋</h2>
                    <p style="color:#334155; font-size:14px; margin:0 0 24px;">
                        Your utility monitoring system has detected the following alerts for your account.
                        Please review them and take action if needed.
                    </p>

                    <!-- Alerts Table -->
                    <div style="background:#f8fafc; border-radius:12px; overflow:hidden; margin-bottom:24px;">
                        <div style="background:#0F172A; padding:12px 16px;">
                            <span style="color:#fff; font-size:13px; font-weight:600;">🔔 Active Alerts — Sorted by Priority</span>
                        </div>
                        <table style="width:100%; border-collapse:collapse;">
                            {alert_rows}
                        </table>
                    </div>

                    <!-- Action Button -->
                    <div style="text-align:center; margin-bottom:24px;">
                        <a href="http://127.0.0.1:5000/dashboard"
                           style="background:linear-gradient(135deg,#0EA5E9,#06B6D4); color:#fff; padding:14px 32px; border-radius:25px; text-decoration:none; font-weight:700; font-size:14px;">
                            View Your Dashboard →
                        </a>
                    </div>

                    <!-- Tips -->
                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:12px; padding:16px;">
                        <p style="color:#166534; font-size:13px; margin:0; font-weight:600;">💡 Tips to reduce usage:</p>
                        <ul style="color:#166534; font-size:12px; margin:8px 0 0; padding-left:16px;">
                            <li>Turn off appliances when not in use</li>
                            <li>Use energy-efficient appliances</li>
                            <li>Check for water or gas leaks immediately</li>
                        </ul>
                    </div>
                </div>

                <!-- Footer -->
                <div style="background:#f8fafc; padding:20px 32px; text-align:center; border-top:1px solid #e8eef5;">
                    <p style="color:#94a3b8; font-size:12px; margin:0;">
                        © 2024 UtilityHub — SSUET DSA Project<br>
                        Karachi, Pakistan
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())

        print(f"Alert email sent to {recipient_email}")
        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False