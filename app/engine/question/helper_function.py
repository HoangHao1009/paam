def _get_duplicates(lst):
    duplicates = []
    seen = set()
    for item in lst:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates
