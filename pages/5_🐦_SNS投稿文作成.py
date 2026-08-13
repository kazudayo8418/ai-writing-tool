import streamlit as st

from utils.auth import require_password
from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="SNS投稿文作成", page_icon="🐦", layout="wide")
require_password()
render_sidebar()

st.title("🐦 SNS投稿文作成")
st.caption("伝えたい内容から、媒体に合わせた投稿文の案を複数作成します。")

if not require_api_key():
    st.stop()

with st.form("sns_form"):
    content = st.text_area("投稿で伝えたい内容", height=150, placeholder="例：新しく出したハンドメイドアクセサリーの販売開始を告知したい")

    col1, col2, col3 = st.columns(3)
    with col1:
        platform = st.selectbox("媒体", ["X（Twitter）", "Instagram", "Threads", "Facebook", "LinkedIn"])
    with col2:
        tone = st.selectbox("トーン", ["親しみやすい", "熱量高め・ワクワク感", "落ち着いた・信頼感重視", "ユーモラス"])
    with col3:
        num_variants = st.slider("案の数", 1, 5, 3)

    col4, col5 = st.columns(2)
    with col4:
        use_hashtags = st.checkbox("ハッシュタグを含める", value=True)
    with col5:
        use_emoji = st.checkbox("絵文字を使う", value=True)

    submitted = st.form_submit_button("🐦 投稿文を作成", type="primary", use_container_width=True)

if submitted:
    if not content.strip():
        st.warning("投稿で伝えたい内容を入力してください。")
        st.stop()

    char_limit_note = "140字以内を目安に、" if platform == "X（Twitter）" else ""

    system_instruction = (
        "あなたはSNSマーケティングに詳しいコピーライターです。媒体ごとの雰囲気や文字数感覚に合わせて、"
        "読者の目を引く投稿文を作成してください。"
    )
    prompt = f"""次の内容でSNS投稿文を{num_variants}案作成してください。

【媒体】{platform}
【トーン】{tone}
【ハッシュタグ】{"文末に3〜5個程度含める" if use_hashtags else "含めない"}
【絵文字】{"適度に使う" if use_emoji else "使わない"}

{char_limit_note}案ごとに「案1」「案2」...と見出しをつけて出力してください。

【伝えたい内容】
{content}
"""

    generate_and_display(prompt, system_instruction, download_filename="sns_posts.txt")
