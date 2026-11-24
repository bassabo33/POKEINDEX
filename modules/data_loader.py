
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

        # 從 C 欄讀取到 U 欄
        #
        # C=0
        # E=2
        # F=3
        # I=6
        # L=9
        # O=12
        # R=15
        # U=18

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

        return data

    finally:
        workbook.close()
