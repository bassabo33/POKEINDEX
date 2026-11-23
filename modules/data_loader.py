from pathlib import Path
from typing import Any

import openpyxl
import streamlit as st


@st.cache_data(show_spinner="正在讀取 Excel...")
def load_dex_data(excel_path: str, file_mtime: float | None = None) -> list[dict[str, Any]]:
    """
    讀取 DEX 工作表。
    使用 data_only=True 讀取 Excel 已儲存的計算結果，不在 Python 內重算公式。

    file_mtime 作為快取參數，檔案更新後可避免沿用舊快取。
    """
    path = Path(excel_path)
    if not path.exists():
        raise FileNotFoundError(path)

    workbook = openpyxl.load_workbook(
        path,
        read_only=True,
        data_only=True,
    )

    try:
        if "DEX" not in workbook.sheetnames:
            raise ValueError("Excel 中找不到 DEX 工作表。")

        worksheet = workbook["DEX"]
        rows: list[dict[str, Any]] = []

        # DEX 第 1 列為欄位標題，資料從第 2 列開始。
        # E 欄為繁體中文譯名。
        # F / L / O / R 分別為超級 / 高級 / 大師 / 小小盃的排名欄位。
        for row_number in range(2, worksheet.max_row + 1):
            name = worksheet.cell(row=row_number, column=5).value
            values = {
                "row_number": row_number,
                "name": name,
                "F": worksheet.cell(row=row_number, column=6).value,
                "L": worksheet.cell(row=row_number, column=12).value,
                "O": worksheet.cell(row=row_number, column=15).value,
                "R": worksheet.cell(row=row_number, column=18).value,
            }
            rows.append(values)

        return rows
    finally:
        workbook.close()
