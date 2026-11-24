
from pathlib import Path

import openpyxl
import streamlit as st


@st.cache_data
def load_dex_data(file_path: str, file_mtime: float):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"找不到 Excel：{file_path}")

    workbook = openpyxl.load_workbook(
        file_path,
        read_only=True,
        data_only=True
    )

    try:
        if "DEX" not in workbook.sheetnames:
            raise ValueError("Excel 中找不到 DEX 工作表")

        ws = workbook["DEX"]
        data = []

        # D=0, E=1, F=2, I=5, L=8, O=11, R=14, U=17

        for values in ws.iter_rows(
            min_row=2,
            min_col=4,
            max_col=21,
            values_only=True
        ):

            name = values[1]

            if name is None or str(name).strip() == "":
                continue

            row_data = {
                "D": values[0],
                "name": str(name).strip(),
                "F": values[2],
                "I": values[5],
                "L": values[8],
                "O": values[11],
                "R": values[14],
                "U": values[17],
            }

            data.append(row_data)

        return data

    finally:
        workbook.close()
