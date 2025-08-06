# occgpu/utils.py
import os

def validate_proportion(value):
    try:
        f = float(value)
        if f <= 0 or f > 1:
            raise ValueError
        return f
    except (ValueError, TypeError):
        raise ValueError(f"Proportion must be a float in (0, 1], got '{value}'")

def validate_positive_int(value):
    try:
        i = int(value)
        if i <= 0:
            raise ValueError
        return i
    except (ValueError, TypeError):
        raise ValueError(f"GPU nums must be a positive integer, got '{value}'")

def get_env_or(default_key, default_value, validator):

    env_value = os.getenv(default_key)
    if env_value is None:
        return default_value

    try:
        return validator(env_value)
    except ValueError as e:
        print(f"Warning: {e} Using default {default_value}.")
        return default_value