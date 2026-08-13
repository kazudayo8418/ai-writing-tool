import streamlit as st

from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="タイトル・キャッチコピー生成", page_icon="💡", layout="wide")
render_sidebar()

st.title("💡 タイトル・キャッチコピー生成")
st.caption("内容の概要から、目を引くタイトルやキャッチコピーの案を複数提案します。")

if not require_api_key():
    st.stop()

with st.form("title_form"):
    summary = st.text_area("内容の概要", height=150, placeholder="例：在宅ワーカー向けの、集中力を高める作業用BGMプレイリストを紹介する記事")

    col1, col2, col3 = st.columns(3)
    with col1:
        kind = st.selectbox(
            "種類",
            ["ブログ・note記事タイトル", "キャッチコピー", "YouTube動画タイトル", "商品名・セールスコピー", "メールの件名"],
        )
    with col2:
        tone = st.selectbox("トーン", ["興味を引く・煽り気味", "信頼感重視・誠実", "シンプル・端的", "ユーモラス"])
    with col3:
        num_variants = st.slider("案の数", 3, 15, 8)

    submitted = st.form_submit_button("💡 生成する", type="primary", use_container_width=True)

if submitted:
    if not summary.strip():
        st.warning("内容の概要を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは広告・編集の第一線で活躍するコピーライターです。誇大広告にならない範囲で、"
        "読み手の興味を引く、記憶に残るコピーを作成してください。"
    )
    prompt = f"""次の内容について、「{kind}」を{num_variants}案考えてください。

【トーン】{tone}
【内容の概要】
{summary}

番号付きリストで、案のみを簡潔に出力してください。"""

    generate_and_display(prompt, system_instruction, download_filename="titles.txt")
