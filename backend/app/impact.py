# Illustrative demo factors only. These are NOT official Sri Lankan lifecycle factors.
# Update with sourced local data before making scientific or environmental claims.

ADVICE = {
    "cardboard": "Keep it clean and dry. Flatten it and send it to a paper/cardboard recycling collection.",
    "glass": "Separate by type and colour where local facilities require it. Handle broken glass safely.",
    "metal": "Empty and rinse cans/containers, then send them to a metal recycling collection.",
    "paper": "Keep paper clean and dry. Recycle it where paper collection is available.",
    "plastic": "Check the resin/recycling mark and local collection rules. Empty and rinse before recycling.",
    "trash": "This image was classified as mixed or other waste. Check whether it can be separated into recyclable components."
}

# Demo relative scores, not measured emissions or guaranteed savings.
DEMO_IMPACT_POINTS = {
    "cardboard": 2.0,
    "glass": 1.5,
    "metal": 3.0,
    "paper": 1.8,
    "plastic": 2.2,
    "trash": 0.0
}

def get_recommendation(category: str):
    advice = ADVICE.get(category, ADVICE["trash"])
    points = DEMO_IMPACT_POINTS.get(category, 0.0)
    estimate = (
        f"Illustrative demo score: {points:.1f} points per item. "
        "This is a configurable educational estimate, not a measured CO2e value."
    )
    return advice, estimate
