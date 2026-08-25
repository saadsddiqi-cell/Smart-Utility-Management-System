# Binary Search — searches consumption records by date

def binary_search(records, target_date):
    # Binary search requires sorted list
    # Sort by date first (ascending)
    sorted_records = sorted(records, key=lambda x: x["date"])

    low  = 0
    high = len(sorted_records) - 1

    results = []

    # Find any matching record
    while low <= high:
        mid = (low + high) // 2
        current_date = str(sorted_records[mid]["date"])

        if current_date == target_date:
            # Found one match — now collect all matches for this date
            results.append(sorted_records[mid])

            # Check left side for more matches
            left = mid - 1
            while left >= 0 and str(sorted_records[left]["date"]) == target_date:
                results.append(sorted_records[left])
                left -= 1

            # Check right side for more matches
            right = mid + 1
            while right < len(sorted_records) and str(sorted_records[right]["date"]) == target_date:
                results.append(sorted_records[right])
                right += 1

            return results  # found!

        elif current_date < target_date:
            low = mid + 1   # search right half
        else:
            high = mid - 1  # search left half

    return []  # not found