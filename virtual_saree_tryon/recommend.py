def suggest_blouse_styles(fabric_type, palette, occasion):
    return [
        {"name": "V-neck blouse", "why": "Elegant and simple."},
        {"name": "Boat neck blouse", "why": "Modern touch."},
        {"name": "Sweetheart with elbow sleeves", "why": "Photogenic for festive looks."}
    ]

def suggest_jewellery(palette, occasion, fabric_type):
    return [
        {"name": "Gold jhumkas", "why": "Matches festive look."},
        {"name": "Simple studs", "why": "Perfect for daily wear."}
    ]

def look_bundle_cards(blouses, jewels):
    return "\\n".join(["Blouse: "+blouses[0]['name'], "Jewellery: "+jewels[0]['name']])
