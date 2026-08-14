import streamlit as st

from utils.auth import require_password
from utils.ui import render_sidebar

st.set_page_config(
    page_title="AIライティングツール",
    page_icon="✍️",
    layout="wide",
)

require_password()
render_sidebar()

st.markdown(
    "<div style='color:#4F46E5; font-weight:700; letter-spacing:0.04em; "
    "font-size:0.85rem; text-transform:uppercase; margin-bottom:4px;'>"
    "AI WRITING SUITE</div>",
    unsafe_allow_html=True,
)
st.title("✍️ AIライティングツール")
st.caption("Gemini APIを使った、オールインワン文章作成アシスタントです。")

st.markdown("#### 左のメニューから使いたいツールを選んでください")
st.write("")

tools = [
    ("📝", "ブログ・Note記事作成", "テーマとキーワードから、構成付きの記事を自動生成します。"),
    ("📧", "メール返信作成", "受信メールの内容を貼り付けるだけで、返信文の下書きを作成します。"),
    ("📄", "文章要約", "長い文章を、指定した長さ・スタイルで要約します。"),
    ("✨", "リライト・校正", "文章の誤字脱字をチェックし、トーンや文体を調整します。"),
    ("🐦", "SNS投稿文作成", "X（Twitter）やInstagramなど、媒体に合わせた投稿文を作成します。"),
    ("💡", "タイトル・キャッチコピー生成", "記事や商品の魅力が伝わるタイトル案を複数提案します。"),
    ("🌐", "文章翻訳", "自然な言い回しを意識して、文章を多言語に翻訳します。"),
]

cols = st.columns(2)
for i, (icon, name, desc) in enumerate(tools):
    with cols[i % 2]:
        st.markdown(
            f"""<div class="tool-card">
                <div class="tool-badge">{icon}</div>
                <div class="tool-name">{name}</div>
                <p class="tool-desc">{desc}</p>
            </div>""",
            unsafe_allow_html=True,
        )
