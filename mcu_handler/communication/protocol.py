def parse_status(line: str):
    """
    Exempelrad från Arduino: 'DIST 123 ESTOP 0'
    Returnerar dict med keys: distance_cm, estop
    """
    if not line:
        return None

    parts = line.split()
    status = {}
    try:
        for i in range(0, len(parts), 2):
            key = parts[i]
            val = parts[i+1]
            if key == "DIST":
                status["distance_cm"] = int(val)
            elif key == "ESTOP":
                status["estop"] = bool(int(val))
            else:
                status[key.lower()] = val
        return status
    except Exception as e:
        print("Protocol parse error:", e)
        return None
