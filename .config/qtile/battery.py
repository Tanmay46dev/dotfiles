def get_battery_icon(percentage: str) -> str:
    percentage = int(percentage)
    if percentage == 0:
        return ""

    if percentage <= 25:
        return ""

    if percentage <= 50:
        return ""

    if percentage <= 75:
        return ""

    if percentage <= 100:
        return ""

