def normalize(x, min_val, max_val):
    return (x - min_val) / (max_val - min_val) if max_val != min_val else 0
