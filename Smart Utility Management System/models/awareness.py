AWARENESS_CONTENT = {
    "electricity": [
        {
            "title": "Use Natural Light",
            "content": "Open blinds and curtains during the day to use natural sunlight instead of turning on lights. This simple step can save significant energy."
        },
        {
            "title": "Unplug Idle Electronics",
            "content": "Devices draw power even when turned off. Unplug chargers, TVs, and computers when not in use, or use a smart power strip."
        },
        {
            "title": "Optimize Cooling",
            "content": "Set your AC to 24°C (75°F) for an optimal balance of comfort and energy savings. Clean the filters regularly to ensure efficiency."
        }
    ],
    "water": [
        {
            "title": "Fix Leaks Promptly",
            "content": "A dripping faucet can waste up to 3,000 gallons of water a year. Fixing leaks is the most cost-effective way to save water."
        },
        {
            "title": "Shorter Showers",
            "content": "Reducing your shower time by just 2 minutes can save up to 5 gallons of water per shower. Consider installing a low-flow showerhead."
        },
        {
            "title": "Turn Off the Tap",
            "content": "Don't let the water run while brushing your teeth, shaving, or washing your face. This can save up to 200 gallons a month."
        }
    ],
    "gas": [
        {
            "title": "Lower Water Heater Temp",
            "content": "Lowering your water heater temperature to 120°F (49°C) reduces energy waste and prevents scalding."
        },
        {
            "title": "Cook Efficiently",
            "content": "Cover pots when cooking to retain heat and reduce cooking time. Match the pot size to the burner to prevent gas waste."
        },
        {
            "title": "Seal Leaks",
            "content": "Ensure doors and windows are properly sealed to keep warm air inside, reducing the need for gas heating during winter."
        }
    ]
}

def get_awareness_tips(utility_type):
    return AWARENESS_CONTENT.get(utility_type, [])
