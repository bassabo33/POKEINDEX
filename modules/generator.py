
# ============================================================
#                     篩選模式設定
# ============================================================

MODE_CONFIG = {

    "超級聯盟": {
        "column": "F",
        "operator": ">",
        "default": 500,
        "limit_label": "排名限制（F 欄）",
        "limit_type": "rank",
    },

    "高級聯盟": {
        "column": "L",
        "operator": ">",
        "default": 300,
        "limit_label": "排名限制（L 欄）",
        "limit_type": "rank",
    },

    "大師聯盟": {
        "column": "O",
        "operator": ">",
        "default": 100,
        "limit_label": "排名限制（O 欄）",
        "limit_type": "rank",
    },

    "PVE": {
        "column": "I",
        "operator": "<",
        "default": 2800,
        "limit_label": "CP 上限（I 欄）",
        "limit_type": "cp",
    },

    "小小盃": {
        "column": "R",
        "operator": ">",
        "default": 200,
        "limit_label": "排名限制（R 欄）",
        "limit_type": "rank",
    },
}


# ============================================================
#                     數值轉換
# ============================================================

def to_number(value):

    if value is None or isinstance(value, bool):
        return None

    try:
        value = str(value).replace(",", "").strip()

        if value == "":
            return None

        return float(value)

    except (ValueError, TypeError):
        return None


# ============================================================
#                     判斷是否符合篩選條件
# ============================================================

def is_matched(row, mode, limit):

    if mode not in MODE_CONFIG:
        return False

    config = MODE_CONFIG[mode]

    column = config["column"]
    operator = config["operator"]

    if mode == "PVE":

        cp_value = to_number(row.get("I"))

        max_type = str(
            row.get("U") or ""
        ).strip().upper()

        condition_1 = (
            cp_value is not None
            and cp_value < limit
        )

        condition_2 = (
            max_type == "MAX"
        )

        return condition_1 and condition_2

    value = to_number(row.get(column))

    if value is None:
        return False

    if operator == ">":
        return value > limit

    elif operator == "<":
        return value < limit

    return False


# ============================================================
#                  產生搜尋字串（去除重複）
# ============================================================

def generate_string(data, mode, limit):

    selected_names = []
    seen_names = set()

    for row in data:

        if not is_matched(row, mode, limit):
            continue

        name = str(row.get("name") or "").strip()

        if not name:
            continue

        if name not in seen_names:
            selected_names.append(name)
            seen_names.add(name)

    return selected_names


# ============================================================
#               產生下方清單（保留重複）
# ============================================================

def generate_list(data, mode, limit):

    selected_rows = []

    for row in data:

        if not is_matched(row, mode, limit):
            continue

        selected_rows.append({
            "D": row.get("D"),
            "E": row.get("name"),
        })

    return selected_rows
