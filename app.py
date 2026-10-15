"""《念流．心境 Mindful Flow》正念牌卡抽牌 — Streamlit 版

執行：streamlit run app.py
資料：cards.json（50 張牌的牌名、牌義、微練習、自我提問、肯定語）
圖片：cards/01.jpg ~ cards/50.jpg、cards/back.jpg
"""

import base64
import html
import json
import secrets
import time
from pathlib import Path

import streamlit as st

BASE = Path(__file__).parent
# 圖片可放在 cards/ 資料夾，或直接放在 app.py 旁邊
CARD_DIR = BASE / "cards" if (BASE / "cards" / "back.jpg").exists() else BASE

st.set_page_config(page_title="念流．心境 抽牌", page_icon="🎴", layout="centered")


# ── 資料 ──────────────────────────────────────────────
@st.cache_data
def load_data():
    data = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
    return data["suits"], data["cards"]


@st.cache_data
def img_b64(name: str) -> str:
    return base64.b64encode((CARD_DIR / name).read_bytes()).decode()


SUITS, CARDS = load_data()
pad = lambda n: f"{n:02d}"
esc = html.escape

# ── 狀態 ──────────────────────────────────────────────
ss = st.session_state
ss.setdefault("current", None)  # 目前顯示的牌號
ss.setdefault("animate", False)  # 下一次顯示是否播放翻牌動畫
ss.setdefault("history", [])  # 最近抽到的牌號


def random_card() -> int:
    """真隨機抽牌，避免與上一張重複。"""
    while True:
        no = secrets.randbelow(len(CARDS)) + 1
        if no != ss.current:
            return no


def show_card(no: int, animate: bool = True):
    ss.current = no
    ss.animate = animate


def remember(no: int):
    ss.history = ([no] + [n for n in ss.history if n != no])[:6]


# ── 樣式 ──────────────────────────────────────────────
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap" rel="stylesheet">
<style>
:root {
  --night:#17262A; --table:#1F3337; --edge:#2C464B; --gold:#D9B864; --gold-dim:#A88B45;
  --mist:#C8D5D1; --mist-dim:#8FA3A0; --paper:#FBF7EE; --ink:#2B2A28;
  --serif:"Noto Serif TC","PMingLiU",serif; --sans:"Noto Sans TC","Microsoft JhengHei",sans-serif;
  --latin:"Cormorant Garamond",Georgia,serif;
}
.stApp { background: radial-gradient(ellipse 90% 50% at 50% 0%, #24403F 0%, transparent 70%), var(--night); }
.stApp, .stApp p, .stApp label, .stApp span:not([data-testid="stIconMaterial"]) { color: var(--mist); font-family: var(--sans); }
.block-container { max-width: 980px; padding-top: 2.2rem; }
header[data-testid="stHeader"] { background: transparent; }
.mf-head { text-align:center; margin-bottom: 1.2rem; }
.mf-eyebrow { font-family:var(--latin); letter-spacing:.32em; color:var(--gold-dim); font-size:15px; text-transform:uppercase; }
.mf-title { font-family:var(--serif); font-weight:700; color:var(--gold); font-size:clamp(32px,6vw,46px); letter-spacing:.18em; margin:.2rem 0; }
.mf-lede { color:var(--mist-dim); font-size:15px; max-width:34em; margin:0 auto; }
.mf-table { background:linear-gradient(180deg,var(--table),#1A2C30); border:1px solid var(--edge);
  border-radius:24px; padding:28px 16px 20px; text-align:center; }
.mf-fan { position:relative; height:230px; max-width:460px; margin:0 auto; }
.mf-fan img { position:absolute; left:50%; bottom:0; width:120px; margin-left:-60px; border-radius:9px;
  box-shadow:0 10px 24px rgba(0,0,0,.35); transform-origin:50% 160%; transform:rotate(var(--r)); }
.mf-fan.shuffle img { animation: mfShuffle .9s ease-in-out infinite; animation-delay: var(--d); }
@keyframes mfShuffle { 0%,100% { transform:rotate(var(--r)) translateY(0); }
  50% { transform:rotate(calc(var(--r) * -0.6)) translateY(-26px); } }
.mf-breath { font-family:var(--serif); color:var(--gold); font-size:24px; letter-spacing:.35em; min-height:2em; margin-top:14px; }
.mf-prompt { color:var(--mist); margin-top:14px; }
.mf-card { perspective:1600px; }
.mf-card img { width:100%; border-radius:14px; box-shadow:0 24px 50px rgba(0,0,0,.45); display:block; }
.mf-card.flip img { animation: mfFlip 1.1s cubic-bezier(.65,0,.35,1) both; }
@keyframes mfFlip { 0% { transform:rotateY(90deg) scale(.92); opacity:.2; } 100% { transform:rotateY(0) scale(1); opacity:1; } }
.mf-meaning { background:var(--paper); border-radius:18px; padding:28px 26px; outline:3px solid var(--suit);
  outline-offset:-12px; box-shadow:0 24px 50px rgba(0,0,0,.35); }
.mf-meaning.rise { animation: mfRise .7s .6s both; }
@keyframes mfRise { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:none; } }
.mf-meaning * { color:var(--ink) !important; }
.mf-mhead { display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; padding:0 4px; }
.mf-mhead span { color:var(--suit) !important; }
.mf-no { font-family:var(--latin) !important; font-size:20px; letter-spacing:.08em; }
.mf-suit { font-family:var(--serif) !important; font-size:15px; letter-spacing:.2em; }
.mf-mtitle { font-family:var(--serif) !important; font-weight:700; font-size:clamp(28px,5vw,38px);
  letter-spacing:.14em; text-align:center; margin:10px 0 0; line-height:1.3; }
.mf-en { display:block; font-family:var(--latin) !important; font-style:italic; font-size:18px; color:var(--suit) !important; }
.mf-rule { text-align:center; color:var(--suit) !important; margin:8px 0 6px; letter-spacing:1em; }
.mf-sec { margin:14px 4px 0; }
.mf-label { display:block; font-size:13px; letter-spacing:.24em; font-weight:500; color:var(--suit) !important; }
.mf-sec p { margin:2px 0 0; line-height:1.75; font-size:16px; }
.mf-quote { background:var(--tint); border-radius:12px; padding:14px 16px; margin-top:16px;
  font-family:var(--serif) !important; font-size:19px; text-align:center; }
.mf-art p { font-size:14px; color:#5E574C !important; }
.mf-h2 { font-family:var(--serif); color:var(--gold); font-size:24px; letter-spacing:.16em; text-align:center; margin:2.4rem 0 .6rem; }
.mf-thumb { font-size:13px; color:var(--mist-dim); text-align:center; }
div.stButton > button { border-radius:999px; letter-spacing:.15em; border:1px solid var(--gold); }
div.stButton > button[kind="primary"] { background:var(--gold); color:var(--night); font-weight:500; }
div.stButton > button[kind="primary"]:hover { background:#E8CC80; color:var(--night); }
div.stButton > button[kind="secondary"] { background:transparent; color:var(--gold); }
button[data-baseweb="tab"] p { color:var(--mist) !important; }
@media (prefers-reduced-motion: reduce) { .mf-card.flip img, .mf-meaning.rise, .mf-fan.shuffle img { animation:none; } }</style>
""",
    unsafe_allow_html=True,
)


# ── 元件 ──────────────────────────────────────────────
def fan_html(shuffle: bool, breath: str = "", prompt: str = "") -> str:
    back = img_b64("back.jpg")
    imgs = "".join(
        f'<img src="data:image/jpeg;base64,{back}" style="--r:{r}deg;--d:{i * 0.08}s" alt="">'
        for i, r in enumerate([-24, -16, -8, 0, 8, 16, 24])
    )
    cls = "mf-fan shuffle" if shuffle else "mf-fan"
    return (
        f'<div class="mf-table"><div class="{cls}">{imgs}</div>'
        f'<div class="mf-breath">{esc(breath)}</div>'
        f'<div class="mf-prompt">{esc(prompt)}</div></div>'
    )


def card_html(c: dict, animate: bool) -> str:
    b64 = img_b64(f"{pad(c['no'])}.jpg")
    cls = "mf-card flip" if animate else "mf-card"
    return f'<div class="{cls}"><img src="data:image/jpeg;base64,{b64}" alt="第 {c["no"]} 張：{esc(c["title"])}"></div>'


def meaning_html(c: dict, animate: bool) -> str:
    s = SUITS[c["suit"]]
    en = f'<span class="mf-en">{esc(c["en"])}</span>' if c.get("en") else ""
    cls = "mf-meaning rise" if animate else "mf-meaning"
    return f"""
<div class="{cls}" style="--suit:{s['accent']};--tint:{s['tint']}">
  <div class="mf-mhead"><span class="mf-no">No. {pad(c['no'])}</span><span class="mf-suit">{s['symbol']} {esc(s['name'])}</span></div>
  <div class="mf-mtitle">{esc(c['title'])}{en}</div>
  <div class="mf-rule">— {s['symbol']} —</div>
  <div class="mf-sec"><span class="mf-label">牌義</span><p>{esc(c['meaning'])}</p></div>
  <div class="mf-sec"><span class="mf-label">覺察微練習</span><p>{esc(c['action'])}</p></div>
  <div class="mf-sec"><span class="mf-label">自我提問</span><p>{esc(c['question'])}</p></div>
  <div class="mf-quote">「{esc(c['affirmation'])}」</div>
  <div class="mf-sec mf-art"><span class="mf-label">彩繪冥想</span>
    <p>{esc(c['art'])} 抽到這張牌後，可以拿出線稿版，一邊上色一邊回到呼吸。</p></div>
</div>"""


def share_text(c: dict) -> str:
    s = SUITS[c["suit"]]
    return "\n".join(
        [
            f"《念流．心境》No.{pad(c['no'])} {c['title']}（{s['symbol']} {s['name']}）",
            f"牌義：{c['meaning']}",
            f"覺察微練習：{c['action']}",
            f"自我提問：{c['question']}",
            f"今日肯定語：{c['affirmation']}",
        ]
    )


# ── 頁面 ──────────────────────────────────────────────
st.markdown(
    """<div class="mf-head">
  <div class="mf-eyebrow">Mindful Flow · 50 Cards</div>
  <div class="mf-title">念流．心境</div>
  <p class="mf-lede">帶著一個想問的事或此刻的心情，抽一張牌。它不預言未來，而是陪你看見當下需要的提醒。</p>
</div>""",
    unsafe_allow_html=True,
)

stage = st.empty()
draw_clicked = st.button(
    "抽一張牌" if ss.current is None else "再抽一張",
    type="primary",
    width="stretch",
)

if draw_clicked:
    # 洗牌 + 呼吸引導，約 3 秒
    for word in ["吸　氣", "吐　氣", "吸　氣", "吐　氣"]:
        stage.markdown(fan_html(True, word, "跟著節奏，慢慢呼吸⋯⋯"), unsafe_allow_html=True)
        time.sleep(0.8)
    no = random_card()
    remember(no)
    show_card(no, animate=True)

if ss.current is None:
    stage.markdown(
        fan_html(False, "", "靜下來，深呼吸三次，在心裡默想你想問的事。準備好了，就按下方按鈕抽一張牌。"),
        unsafe_allow_html=True,
    )
else:
    card = CARDS[ss.current - 1]
    animate = ss.animate
    ss.animate = False
    with stage.container():
        left, right = st.columns([5, 7], gap="large")
        with left:
            st.markdown(card_html(card, animate), unsafe_allow_html=True)
        with right:
            st.markdown(meaning_html(card, animate), unsafe_allow_html=True)
            with st.expander("複製字義（可貼到 LINE 或筆記）"):
                st.code(share_text(card), language=None, wrap_lines=True)

# 最近抽到
if ss.history:
    st.caption("最近抽到")
    cols = st.columns(len(ss.history))
    for col, no in zip(cols, ss.history):
        c = CARDS[no - 1]
        if col.button(f"{SUITS[c['suit']]['symbol']} {c['title']}", key=f"h{no}", width="stretch"):
            show_card(no, animate=True)
            st.rerun()

# 全部牌卡一覽
st.markdown('<div class="mf-h2">全部牌卡</div>', unsafe_allow_html=True)
tab_keys = ["all", "spade", "heart", "diamond", "club", "core"]
tab_labels = ["全部"] + [f"{SUITS[k]['symbol']} {SUITS[k]['name']}" for k in tab_keys[1:]]
for key, tab in zip(tab_keys, st.tabs(tab_labels)):
    with tab:
        items = [c for c in CARDS if key == "all" or c["suit"] == key]
        per_row = 5
        for i in range(0, len(items), per_row):
            cols = st.columns(per_row)
            for col, c in zip(cols, items[i : i + per_row]):
                with col:
                    st.image(str(CARD_DIR / f"{pad(c['no'])}.jpg"), width="stretch")
                    if st.button(f"{pad(c['no'])} {c['title']}", key=f"{key}-{c['no']}", width="stretch"):
                        show_card(c["no"], animate=True)
                        st.rerun()

st.markdown(
    '<p style="text-align:center;color:#8FA3A0;font-size:13px;margin-top:2rem">念流．心境 Mindful Flow　·　點選任一張牌，可直接查看它的字義卡</p>',
    unsafe_allow_html=True,
)
