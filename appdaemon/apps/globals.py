HOME_NAME = "House"
MOTD = f"We bid you welcome to the {HOME_NAME}!"
# All rooms have their own log file, the house/global one is defined here. Note that these are defined in appdaemon.yaml.
HOME_LOG = "house_log"

def decimal_to_octet_proportional(value):
    if not (-1.0 <= value <= 1.0):
        raise ValueError("Decimal value must be between -1.0 and 1.0")

    # Convert the decimal value to a proportional 8-bit (octet) value
    eight_bit_value = int(value * 255)

    # Clamp the value to the 8-bit range
    eight_bit_value = max(min(eight_bit_value, 255), -255)

    return eight_bit_value

def decimal_to_custom_range_proportional(value, min_value, max_value):
    if not (-1.0 <= value <= 1.0):
        raise ValueError("Decimal value must be between -1.0 and 1.0")

    # Calculate the range between min_value and max_value
    range_width = max_value - min_value

    # Adjust the value from the range of -1.0 to 1.0 to the custom range
    proportional_value = int((value + 1.0) / 2.0 * range_width + min_value)

    # Clamp the value to the custom range
    proportional_value = max(min(proportional_value, max_value), min_value)

    return proportional_value

def angle_to_octet_proportional(angle):
    # One full rotation (360 degrees) corresponds to 255.
    return int(round(angle * 255 / 360))

def angle_to_custom_range_proportional(angle, min_value, max_value):
    # One full rotation (360 degrees) corresponds to the full range from min_value to max_value.
    range_width = max_value - min_value
    proportional_value = int(round(abs(angle) / 360 * range_width))
    # If the angle is negative (rotation to the left), the delta should also be negative.
    # If the angle is positive (rotation to the right), the delta should be positive.
    return proportional_value if angle >= 0 else -proportional_value
