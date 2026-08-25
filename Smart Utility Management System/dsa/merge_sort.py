# Merge Sort — sorts consumption records by amount (highest first)

def merge_sort(records):
    if len(records) <= 1:
        return records

    # Split list in half
    mid   = len(records) // 2
    left  = merge_sort(records[:mid])
    right = merge_sort(records[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j  = 0

    # Compare and merge
    while i < len(left) and j < len(right):
        # Sort by amount — highest first
        if left[i]["amount"] >= right[j]["amount"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result