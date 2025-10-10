def autodetect_sensor_location(filename):
    """
    Try to infer sensor location from filename.
    """
    fname = filename.lower()
    patterns = {
        "leftankle": ["la", "leftankle", "lankle"],
        "rightankle": ["ra", "rightankle", "rankle"],
        "lumbar": ["l5", "lumbar", "lowerback", "waist"],
        "leftwrist": ["lw", "leftwrist", "lwrist"],
        "rightwrist": ["rw", "rightwrist", "rwrist"],
        "chest": ["chest", "sternum"],
        "thoracic": ["c7", "upperback"],
    }

    for canon_name, keywords in patterns.items():
        for kw in keywords:
            if kw in fname:
                return canon_name
    return None  # could not detect