import numpy as np
from sklearn.linear_model import LinearRegression
from database import get_connection

def get_forecast(user_id, utility_type, days_ahead=7):
    conn   = get_connection()
    cursor = conn.cursor()

    # Get last 14 days of data
    cursor.execute('''
        SELECT date, amount FROM usage_data
        WHERE user_id = %s AND type = %s
        ORDER BY date ASC
        LIMIT 14
    ''', (user_id, utility_type))

    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 3:
        return [], []

    # Prepare data for Linear Regression
    X = np.array(range(len(rows))).reshape(-1, 1)  # day numbers
    y = np.array([row[1] for row in rows])          # amounts

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 7 days
    future_X      = np.array(range(len(rows), len(rows) + days_ahead)).reshape(-1, 1)
    predictions   = model.predict(future_X)

    # Round and ensure no negative values
    predictions   = [round(max(0, p), 2) for p in predictions]

    # Generate future date labels
    from datetime import date, timedelta
    last_date  = rows[-1][0]
    if isinstance(last_date, str):
        from datetime import datetime
        last_date = datetime.strptime(last_date, "%Y-%m-%d").date()

    future_dates = [
        str(last_date + timedelta(days=i+1))
        for i in range(days_ahead)
    ]

    return future_dates, predictions

def get_all_forecasts(user_id):
    elec_dates,  elec_pred  = get_forecast(user_id, "electricity")
    water_dates, water_pred = get_forecast(user_id, "water")
    gas_dates,   gas_pred   = get_forecast(user_id, "gas")

    return {
        "electricity": {"dates": elec_dates,  "predictions": elec_pred},
        "water"      : {"dates": water_dates, "predictions": water_pred},
        "gas"        : {"dates": gas_dates,   "predictions": gas_pred}
    }