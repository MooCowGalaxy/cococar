from clamp import clamp


def remap_range(val, old_min, old_max, new_min, new_max, limit=True):
    proportion = (val - old_min) / (old_max - old_min)

    if limit:
        proportion = clamp(proportion, 0, 1)

    return new_min + proportion * (new_max - new_min)
