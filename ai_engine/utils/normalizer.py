import numpy as np

def normalize(value, min_val=0, max_val=100):
    if value is None:
        return 0
    return max(min(float(value), max_val), min_val)


def safe_float(x):
    if isinstance(x, (np.integer, np.floating)):
        return float(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def clean_dict(obj):
    if isinstance(obj, dict):
        return {k: clean_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_dict(i) for i in obj]
    else:
        return safe_float(obj)