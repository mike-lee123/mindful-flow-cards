# 念流．心境 Mindful Flow：正念牌卡抽牌

隨機抽出一張正念牌卡，同時顯示字義卡（牌義、覺察微練習、自我提問、今日肯定語、彩繪冥想）。

## 檔案結構

```
streamlit-app/
├── app.py               主程式
├── cards.json           50 張牌的文字資料（可直接編輯）
├── cards/               牌卡圖片 01.jpg ~ 50.jpg、back.jpg
├── requirements.txt     相依套件
└── .streamlit/
    └── config.toml      深青金色主題
```

## 本機執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 部署到 Streamlit Community Cloud（免費）

1. 在 GitHub 建立一個公開的 repository，例如 `mindful-flow-cards`
2. 把這個資料夾內的所有檔案上傳到 repository 根目錄（包含 `.streamlit` 資料夾）
3. 到 https://share.streamlit.io 用 GitHub 帳號登入
4. 按 **Create app** → **Deploy a public app from GitHub**
5. 填入：
   - Repository：`你的帳號/mindful-flow-cards`
   - Branch：`main`
   - Main file path：`app.py`
   - App URL：自訂網址，例如 `mindful-flow`，網址就會是 `https://mindful-flow.streamlit.app`
6. 按 **Deploy**，約 1～3 分鐘完成

## 修改內容

- 修改字義：編輯 `cards.json`，推送到 GitHub 後，網站會自動更新
- 更換圖片：替換 `cards/` 內同名的 jpg 檔
