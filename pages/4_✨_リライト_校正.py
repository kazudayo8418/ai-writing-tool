import streamlit as st

from utils.auth import require_password
from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="リライト・校正", page_icon="✨", layout="wide")
require_password()
render_sidebar()

st.title("✨ 文章リライト・校正")
st.caption("誤字脱字のチェックや、文体・トーンの変換を行います。")

if not require_api_key():
    st.stop()

with st.form("rewrite_form"):
    source_text = st.text_area("元の文章", height=250, placeholder="校正・リライトしたい文章を貼り付けてください")

    mode = st.selectbox(
        "変換の種類",
        [
            "誤字脱字・文法だけを直す（校正）",
            "より分かりやすく書き直す",
            "丁寧なビジネス文体にする",
            "カジュアルな文体にする",
            "簡潔に短くする",
            "より詳しく具体的にする",
        ],
    )
    extra = st.text_input("追加の指示（任意）", placeholder="例：専門用語はできるだけ使わないでほしい")

    submitted = st.form_submit_button("✨ 変換する", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.warning("元の文章を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは日本語の編集・校正のプロです。原文の意図を保ったまま、指定された種類の変換を行ってください。"
        "校正の場合は変更箇所が分かるよう簡潔な補足を末尾に添えてください。"
    )
    prompt = f"""次の文章を「{mode}」という方針で変換してください。
追加の指示: {extra or "特になし"}

【元の文章】
{source_text}
"""

    generate_and_display(prompt, system_instruction, download_filename="rewritten.txt")
