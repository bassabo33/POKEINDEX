
from pathlib import Path

import streamlit as st

from modules.data_loader import load_dex_data
from modules.generator import MODE_CONFIG, generate_string


# ============================================================
#                     基本設定
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
EXCEL_PATH = BASE_DIR / "data" / "PVP_collection.xlsx"

st.set_page_config(
    page_title="PVP String Generator",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
#                     頁面標題
# ============================================================

st.title("⚡ Pokémon GO PVP String Generator")
st.caption("依照 Excel 資料篩選寶可夢，產生可複製的搜尋字串")


# ============================================================
#                     Excel 資料讀取
# ============================================================

if not EXCEL_PATH.exists():
    st.error(f"找不到 Excel 檔案：{EXCEL_PATH}")
    st.stop()

if "generated_names" not in st.session_state:
    st.session_state.generated_names = []

if "generated_string" not in st.session_state:
    st.session_state.generated_string = ""

if "generated_mode" not in st.session_state:
    st.session_state.generated_mode = ""


# ============================================================
#                     Sidebar
# ============================================================

with st.sidebar:
    st.header("資料設定")

    st.write("Excel 檔案：")
    st.code(EXCEL_PATH.name)

    if st.button("重新載入 Excel", use_container_width=True):
        load_dex_data.clear()
        st.session_state.generated_names = []
        st.session_state.generated_string = ""
        st.rerun()


# ============================================================
#                     載入資料
# ============================================================

try:
    file_mtime = EXCEL_PATH.stat().st_mtime

    dex_data = load_dex_data(
        str(EXCEL_PATH),
        file_mtime
    )

except Exception as e:
    st.error(f"Excel 讀取失敗：{e}")
    st.stop()

if not dex_data:
    st.warning("Excel 中沒有讀取到有效資料。")
    st.stop()


# ============================================================
#                     篩選模式
# ============================================================

st.subheader("篩選設定")

mode = st.selectbox(
    "選擇篩選模式",
    options=list(MODE_CONFIG.keys())
)

config = MODE_CONFIG[mode]

limit = st.number_input(
    config["limit_label"],
    min_value=0,
    max_value=100000,
    value=config["default"],
    step=1,
    key=f"limit_{mode}"
)


# ============================================================
#                     產生字串
# ============================================================

if st.button("產生搜尋字串", type="primary", use_container_width=True):

    names = generate_string(
        dex_data,
        mode,
        limit
    )

    result = "&".join(names)

    st.session_state.generated_names = names
    st.session_state.generated_string = result
    st.session_state.generated_mode = mode


# ============================================================
#                     輸出結果
# ============================================================

st.divider()

st.subheader("產生結果")

if st.session_state.generated_mode:

    st.write(
        f"目前模式：**{st.session_state.generated_mode}**"
    )

    st.write(
        f"符合條件的寶可夢數量：**{len(st.session_state.generated_names)}**"
    )

    if st.session_state.generated_string:

        st.caption("搜尋字串（可直接複製）")

        st.code(
            st.session_state.generated_string,
            language=None
        )

        with st.expander("查看篩選出的寶可夢清單"):

            for index, name in enumerate(
                st.session_state.generated_names,
                start=1
            ):
                st.write(f"{index}. {name}")

    else:
        st.warning("沒有找到符合條件的寶可夢。")

else:
    st.info("請設定篩選條件，然後按下「產生搜尋字串」。")
