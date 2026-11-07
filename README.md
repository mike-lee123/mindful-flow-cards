# 念流．心境 Mindful Flow：正念牌卡網站

網站有兩個分頁：

- **抽牌**：隨機抽出一張正念牌卡，同時顯示字義卡（牌義、覺察微練習、自我提問、今日肯定語、彩繪冥想）。
- **心境旅程**（試用版）：一段 1–5 分鐘的正念小旅程：停（心境天氣）→ 覺（情境）→ 抽（牌卡）→ 練（練習小徑）→ 探（回來看看）→ 收（心境花園）。遊戲在使用者的瀏覽器中執行，寫下的文字不會傳到伺服器；遇到危機語句或強度 8 分以上，會停下遊戲並顯示求助專線。

## 檔案結構

```
streamlit-app/
├── app.py               網站入口（兩個分頁的導覽）
├── draw.py              抽牌頁
├── journey.py           心境旅程頁（嵌入 journey.html）
├── journey.html         心境旅程遊戲本體（牌卡資料執行時從 cards.json 填入）
├── cards.json           50 張牌的文字資料（兩個分頁共用，可直接編輯）
├── static/cards/        牌卡圖片 01.jpg ~ 50.jpg、back.jpg（兩個分頁共用）
├── requirements.txt     相依套件
└── .streamlit/
    └── config.toml      深青金色主題；enableStaticServing 讓 static/ 可被網頁讀取
```

## 本機執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 部署到 Streamlit Community Cloud（免費）

Main file path 維持 `app.py`，已部署的網站推送更新後會自動套用新的分頁。

1. 在 GitHub 建立一個公開的 repository，例如 `mindful-flow-cards`
2. 把這個資料夾內的所有檔案上傳到 repository 根目錄（包含 `.streamlit` 與 `static` 資料夾）
3. 到 https://share.streamlit.io 用 GitHub 帳號登入
4. 按 **Create app** → **Deploy a public app from GitHub**
5. 填入：
   - Repository：`你的帳號/mindful-flow-cards`
   - Branch：`main`
   - Main file path：`app.py`
   - App URL：自訂網址，例如 `mindful-flow`，網址就會是 `https://mindful-flow.streamlit.app`
6. 按 **Deploy**，約 1～3 分鐘完成

## 修改內容

- 修改字義：編輯 `cards.json`，推送到 GitHub 後，兩個分頁都會自動更新
- 更換圖片：替換 `static/cards/` 內同名的 jpg 檔
- 修改心境旅程：編輯 `journey.html`。原始版本在《念流心境》專案的 `心境旅程/template.html`，兩邊請保持一致
