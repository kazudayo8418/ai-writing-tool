import streamlit as st

from utils.auth import require_password
from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="文章翻訳", page_icon="🌐", layout="wide")
require_password()
render_sidebar()

st.title("🌐 文章翻訳")
st.caption("自然な言い回しを意識して、文章を翻訳します。")

if not require_api_key():
    st.stop()

with st.form("translate_form"):
    source_text = st.text_area("翻訳したい文章", height=220, placeholder="ここに翻訳したい文章を入力してください")

    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox(
            "翻訳先言語",
            ["英語", "中国語（簡体字）", "中国語（繁体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語", "日本語", "その他（下に入力）"],
        )
        custom_lang = ""
        if target_lang == "その他（下に入力）":
            custom_lang = st.text_input("言語名を入力", placeholder="例：タイ語")
    with col2:
        tone = st.selectbox("トーン", ["自然な文章", "フォーマル・ビジネス向け", "カジュアル・会話調"])

    submitted = st.form_submit_button("🌐 翻訳する", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.warning("翻訳したい文章を入力してください。")
        st.stop()

    lang = custom_lang.strip() if target_lang == "その他（下に入力）" else target_lang
    if not lang:
        st.warning("翻訳先の言語を入力してください。")
        st.stop()

    system_instruction = (
        "あなたはプロの翻訳者です。直訳ではなく、ネイティブスピーカーが読んで自然な表現に翻訳してください。"
    )
    prompt = f"""次の文章を「{lang}」に翻訳してください。トーンは「{tone}」でお願いします。
翻訳結果のみを出力し、余計な説明は付けないでください。

【原文】
{source_text}
"""

    generate_and_display(prompt, system_instruction, download_filename="translation.txt")
