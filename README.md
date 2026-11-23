# Pokémon GO String Generator

## 功能

- 超級聯盟：DEX!F > 排名限制，讀取 DEX!E
- 高級聯盟：DEX!L > 排名限制，讀取 DEX!E
- 大師聯盟：DEX!O > 排名限制，讀取 DEX!E
- 小小盃：DEX!R > 排名限制，讀取 DEX!E
- PVE：保留模式與 CP 限制輸入，但因資料來源尚未確認，暫不執行。

符合條件的中文名稱會去除空值、去重（保留第一次出現順序），再以 `&` 串接。

## 本機執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Excel

請將 `PVP_collection.xlsx` 放在 `data/` 資料夾。
程式讀取 `DEX` 工作表，第一列視為標題，第二列開始讀取資料。

## 注意

若要部署到 GitHub / Streamlit Community Cloud，建議使用 Private Repository。
若 Excel 未來包含個人或公司機密資料，不要放進公開 Repository。
