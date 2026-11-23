import streamlit as st

from modules.data_loader import load_dex_data
from modules.generator import generate_string, MODE_CONFIG

st.set_page_config(
    page_title="Pokémon GO String Generator",
    page_icon="🎮",
    layout="wide",
)

st.title("Pokémon GO String Generator")
st.caption("依照 Excel DEX 工作表的排名資料，篩選寶可夢並產生遊戲內搜尋字串。")

EXCEL_PATH = "data/PVP_collection.xlsx"

# ------------------------------------------------------------
# Sidebar：資料管理
# ------------------------------------------------------------
with st.sidebar:
    st.header("資料管理")
    st.write("資料來源：`data/PVP_collection.xlsx`")
    if st.button("重新載入 Excel", use_container_width=True):
        load_dex_data.clear()
        st.session_state.pop("generated_result", None)
        st.rerun()

# ------------------------------------------------------------
# 條件設定
# ------------------------------------------------------------
mode = st.selectbox(
    "選擇遊戲模式",
    options=list(MODE_CONFIG.keys()),
    index=0,
)

config = MODE_CONFIG[mode]
limit_label = "CP 限制" if config["limit_type"] == "cp" else "排名限制"

default_value = config["default"]
limit_value = st.number_input(
    limit_label,
    min_value=0,
    max_value=100000,
    value=default_value,
    step=1,
    help=f"{mode} 的預設值為 {default_value}，可自行修改。",
    key=f"limit_{mode}",
)

if config["status"] == "pending":
    st.warning(
        "PVE 的資料來源與篩選欄位尚未確認。"
        "目前先保留 PVE 選項及 CP 限制輸入框，但暫不執行產生，"
        "避免誤用尚未確認的 Excel 欄位。"
    )
else:
    st.caption(
        f"資料來源：DEX 工作表｜篩選欄位：{config['column']} 欄｜"
        f"中文名稱：E 欄｜條件：{config['column']} > {int(limit_value)}"
    )

# ------------------------------------------------------------
# 產生字串
# ------------------------------------------------------------
generate_clicked = st.button(
    "產生字串",
    type="primary",
    use_container_width=True,
    disabled=(config["status"] == "pending"),
)

if generate_clicked:
    try:
        dex_data = load_dex_data(EXCEL_PATH)
        names = generate_string(
            rows=dex_data,
            mode=mode,
            limit=int(limit_value),
        )
        st.session_state["generated_result"] = {
            "mode": mode,
            "limit": int(limit_value),
            "names": names,
            "string": "&".join(names),
        }
    except FileNotFoundError:
        st.error(f"找不到 Excel 檔案：{EXCEL_PATH}")
    except Exception as exc:
        st.error(f"讀取或處理 Excel 時發生錯誤：{exc}")

# ------------------------------------------------------------
# 結果
# ------------------------------------------------------------
result = st.session_state.get("generated_result")

if result:
    st.divider()
    st.subheader("產生結果")

    # 若切換模式但尚未重新產生，不顯示舊模式結果造成誤解
    if result["mode"] != mode:
        st.info("目前顯示的是上一次產生的結果。請按「產生字串」更新。")
    else:
        st.success(
            f"完成：{len(result['names']):,} 個不重複名稱｜"
            f"{result['mode']}｜限制值：{result['limit']}"
        )

    if result["string"]:
        st.markdown("**字串（使用 `&` 串接）**")
        st.code(result["string"], language=None)
        st.caption("點擊字串區塊右上角的複製圖示，即可複製整段字串。")

        with st.expander(f"查看篩選後名稱清單（{len(result['names']):,} 筆）"):
            st.write("、".join(result["names"]))
    else:
        st.warning("沒有符合條件的資料，因此沒有產生字串。")
else:
    st.info("請選擇遊戲模式、設定限制值，再按「產生字串」。")

st.divider()
st.caption(
    "目前已完成：超級聯盟、高級聯盟、大師聯盟、小小盃。"
    "PVE 待確認資料來源後再啟用。"
)
