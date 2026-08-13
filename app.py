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

st.title("✍️ AIライティングツール")
st.caption("Gemini APIを使った、個人用のオールインワン文章作成アシスタントです。")

st.markdown("### 左のメニューから使いたいツールを選んでください")

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
        with st.container(border=True):
            st.markdown(f"#### {icon} {name}")
            st.write(desc)

st.divider()
st.markdown(
    """
##### 初回セットアップ
1. [Google AI Studio](https://aistudio.google.com/apikey) でGemini APIキーを無料で発行
2. 左のサイドバーの「⚙️ 設定」にAPIキーを入力
   （毎回入力したくない場合は `.env` に `GEMINI_API_KEY=...` と書くか、`.streamlit/secrets.toml` に設定してください）
3. 左のメニューから使いたいツールを選んで実行
"""
)
