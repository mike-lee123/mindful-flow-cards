"""《念流．心境 Mindful Flow》網站入口

執行：streamlit run app.py
頁面：
  draw.py     抽牌（原本的首頁）
  journey.py  心境旅程（停 → 覺 → 抽 → 練 → 探 → 收）
"""

import streamlit as st

st.set_page_config(page_title="念流．心境", page_icon="🎴", layout="centered")

pages = [
    st.Page("draw.py", title="抽牌", icon="🎴", url_path="draw", default=True),
    st.Page("journey.py", title="心境旅程", icon="🌦️", url_path="journey"),
]
st.navigation(pages, position="top").run()
