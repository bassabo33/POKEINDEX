
from pathlib import Path

import openpyxl
import streamlit as st


# ============================================================
#                     Excel 資料讀取
# ============================================================

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

        # 從 E 欄讀取到 U 欄
        # E=0, F=1, I=4, L=7, O=10, R=13, U=16

        for values in ws.iter_rows(
            min_row=2,
            min_col=5,
            max_col=21,
            values_only=True
        ):

            name = values[0]

            if name is None or str(name).strip() == "":
                continue

            row_data = {
                "name": str(name).strip(),

                "F": values[1],
                "I": values[4],
                "L": values[7],
                "O": values[10],
                "R": values[13],
                "U": values[16],
            }

            data.append(row_data)

        return data

    finally:
        workbook.close()
