import streamlit as st

from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="ブログ・Note記事作成", page_icon="📝", layout="wide")
render_sidebar()

st.title("📝 ブログ・Note記事作成")
st.caption("テーマやキーワードを入力すると、見出し付きの記事案を作成します。")

if not require_api_key():
    st.stop()

with st.form("blog_form"):
    topic = st.text_input("記事のテーマ・タイトル案", placeholder="例：初心者向けの家庭菜園の始め方")
    keywords = st.text_input("含めたいキーワード（カンマ区切り・任意）", placeholder="例：プランター, 初心者, 費用")
    audience = st.text_input("想定読者（任意）", placeholder="例：これから家庭菜園を始めたい30代の会社員")

    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox("文体・トーン", ["丁寧・親しみやすい", "専門的・信頼感重視", "カジュアル・フランク", "エモーショナル・共感重視"])
    with col2:
        length = st.selectbox("文字数の目安", ["短め（600字程度）", "標準（1200字程度）", "長め（2000字程度）"])
    with col3:
        platform = st.selectbox("投稿先", ["ブログ全般", "note", "はてなブログ", "企業オウンドメディア"])

    include_outline = st.checkbox("見出し（H2/H3）構成にする", value=True)
    extra = st.text_area("追加の指示（任意）", placeholder="例：体験談を交えて、最後にCTAを入れてほしい")

    submitted = st.form_submit_button("✍️ 記事を生成", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("記事のテーマを入力してください。")
        st.stop()

    system_instruction = (
        "あなたはプロのWebライター兼編集者です。SEOと読みやすさの両方を意識し、"
        "自然な日本語で記事を執筆してください。誇張しすぎた表現や事実に基づかない断定は避けてください。"
    )
    prompt = f"""次の条件でブログ記事を執筆してください。

テーマ: {topic}
キーワード: {keywords or "指定なし"}
想定読者: {audience or "指定なし"}
文体・トーン: {tone}
文字数の目安: {length}
投稿先媒体: {platform}
見出し構成: {"H2/H3の見出しを使い、構成をはっきりさせる" if include_outline else "見出しは使わず、自然な段落構成にする"}
追加の指示: {extra or "特になし"}

Markdown形式で、タイトル・導入文・本文・まとめの流れで出力してください。"""

    generate_and_display(prompt, system_instruction, download_filename="blog_article.md")
