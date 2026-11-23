from typing import Any


MODE_CONFIG = {
    "超級聯盟": {
        "column": "F",
        "default": 500,
        "limit_type": "rank",
        "status": "ready",
    },
    "高級聯盟": {
        "column": "L",
        "default": 300,
        "limit_type": "rank",
        "status": "ready",
    },
    "大師聯盟": {
        "column": "O",
        "default": 100,
        "limit_type": "rank",
        "status": "ready",
    },
    "PVE": {
        "column": None,
        "default": 2800,
        "limit_type": "cp",
        "status": "pending",
    },
    "小小盃": {
        "column": "R",
        "default": 200,
        "limit_type": "rank",
        "status": "ready",
    },
}


def _to_number(value: Any) -> float | None:
    """將 Excel 儲存格內容轉成數字；空值或非數字回傳 None。"""
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def generate_string(
    rows: list[dict[str, Any]],
    mode: str,
    limit: int,
) -> list[str]:
    """
    根據模式與限制值篩選 DEX 資料。

    規則：
    1. 篩選指定排名欄位 > limit。
    2. 讀取 E 欄中文名稱。
    3. 忽略空白名稱。
    4. 去重並保留 Excel 原始順序。
    5. 回傳名稱清單；由 app.py 使用 & 串接。
    """
    if mode not in MODE_CONFIG:
        raise ValueError(f"不支援的模式：{mode}")

    config = MODE_CONFIG[mode]
    if config["status"] != "ready":
        raise ValueError(f"{mode} 的資料來源尚未設定。")

    column = config["column"]
    selected_names: list[str] = []
    seen: set[str] = set()

    for row in rows:
        rank_value = _to_number(row.get(column))
        if rank_value is None or rank_value <= limit:
            continue

        raw_name = row.get("name")
        if raw_name is None:
            continue

        name = str(raw_name).strip()
        if not name or name in seen:
            continue

        seen.add(name)
        selected_names.append(name)

    return selected_names
