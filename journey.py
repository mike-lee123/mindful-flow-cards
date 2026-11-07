"""心境旅程：以念流．心境牌卡為核心的正念練習小遊戲（試用版）

遊戲本體是 journey.html，完全在使用者的瀏覽器中執行；
使用者寫下的文字不會傳到伺服器。牌卡資料讀自 cards.json，
圖片由 Streamlit 靜態檔案功能提供（static/cards/，見 .streamlit/config.toml）。
"""

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent


@st.cache_data
def journey_html() -> str:
    cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))["cards"]
    keep = ("no", "title", "suit", "action", "affirmation", "question")
    data = json.dumps([{k: c[k] for k in keep} for c in cards], ensure_ascii=False)
    html = (BASE / "journey.html").read_text(encoding="utf-8").replace("__CARDS__", data)
    # 嵌入設定：圖片走靜態路徑、深色主題、iframe 自動高度
    flags = '<script>window.MF_EMBED = true; window.MF_IMG_BASE = "app/static/cards/";</script>'
    return flags + html


components.html(journey_html(), height=1100, scrolling=True)
