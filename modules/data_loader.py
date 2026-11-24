# C=0, D=1, E=2, F=3, I=6, L=9, O=12, R=15, U=18

for values in ws.iter_rows(
    min_row=2,
    min_col=3,
    max_col=21,
    values_only=True
):

    name = values[2]

    if name is None or str(name).strip() == "":
        continue

    row_data = {
        "C": values[0],
        "name": str(name).strip(),
        "F": values[3],
        "I": values[6],
        "L": values[9],
        "O": values[12],
        "R": values[15],
        "U": values[18],
    }

    data.append(row_data)
