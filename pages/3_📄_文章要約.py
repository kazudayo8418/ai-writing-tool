import streamlit as st

from utils.auth import require_password
from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
require_password()
render_sidebar()

st.title("📄 文章要約")
st.caption("長い文章を、指定した長さ・形式で要約します。")

if not require_api_key():
    st.stop()

with st.form("summary_form"):
    source_text = st.text_area("要約したい文章", height=280, placeholder="ここに要約したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox(
            "要約の長さ",
            ["一文で", "3行程度", "100字程度", "300字程度", "元の文章の半分程度"],
        )
    with col2:
        style = st.selectbox("出力形式", ["自然な文章", "箇条書き", "要点＋詳細の2段構成"])

    submitted = st.form_submit_button("📄 要約する", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.warning("要約したい文章を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは文章要約の専門家です。原文の意味や重要なニュアンスを損なわず、"
        "指定された長さと形式に忠実に要約してください。"
    )
    prompt = f"""次の文章を要約してください。

【要約の長さ】{length}
【出力形式】{style}

【原文】
{source_text}
"""

    generate_and_display(prompt, system_instruction, download_filename="summary.txt")
