def check_attributes(data: dict, checklist: list):
    for item in checklist:
        if not item in data:
            return False
    
    return True
