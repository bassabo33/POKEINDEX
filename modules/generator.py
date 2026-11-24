def generate_list(data, mode, limit):

    selected_rows = []

    for row in data:

        if not is_matched(row, mode, limit):
            continue

        selected_rows.append({
            "C": row.get("C"),
            "E": row.get("name"),
        })

    return selected_rows
