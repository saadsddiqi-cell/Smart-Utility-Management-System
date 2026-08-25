def get_recommendations(today):
    tips = []
    
    # Electricity threshold (e.g. 20 kWh per day)
    if today['electricity'] > 20:
        tips.append({
            "type": "electricity",
            "message": "Your electricity usage is above average. Consider switching to LED bulbs and turning off unused appliances.",
            "priority": "high"
        })
    else:
        tips.append({
            "type": "electricity",
            "message": "Great job! Your electricity usage is within normal limits.",
            "priority": "low"
        })
        
    # Water threshold (e.g. 300 Litres per day)
    if today['water'] > 300:
        tips.append({
            "type": "water",
            "message": "High water consumption detected. Check for leaks in plumbing and consider shorter showers.",
            "priority": "high"
        })
    else:
        tips.append({
            "type": "water",
            "message": "Your water consumption is optimal. Keep it up!",
            "priority": "low"
        })
        
    # Gas threshold (e.g. 10 m3 per day)
    if today['gas'] > 10:
        tips.append({
            "type": "gas",
            "message": "Your gas usage is elevated. Ensure your water heater and stove are operating efficiently.",
            "priority": "high"
        })
    else:
        tips.append({
            "type": "gas",
            "message": "Your gas usage is perfectly normal.",
            "priority": "low"
        })
        
    return tips
