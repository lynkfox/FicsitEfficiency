

def calculate_item_per_minute(item_count: int, time: int) -> float:

    return (60*item_count)/time


def calculate_components_per_minute(components: dict, time: int) -> dict:

    return { key:calculate_item_per_minute(value, time) for key, value in components.items()}