import streamlit as st

from utils.ui import generate_and_display, render_sidebar, require_api_key

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")
render_sidebar()

st.title("📧 メール返信作成")
st.caption("受信したメールと返信の要点を入力すると、返信文の下書きを作成します。")

if not require_api_key():
    st.stop()

with st.form("mail_form"):
    original_mail = st.text_area("受信したメールの本文", height=200, placeholder="返信元のメール本文を貼り付けてください")
    key_points = st.text_area("返信で伝えたい要点", height=120, placeholder="例：提案内容は了承。ただし納期は来月末に変更してほしい")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["丁寧なビジネス文書", "フォーマル（社外・目上向け）", "フレンドリー（社内・親しい相手向け）", "簡潔・要点のみ"])
    with col2:
        sender_name = st.text_input("署名する名前（任意）", placeholder="例：山田太郎")

    submitted = st.form_submit_button("✉️ 返信文を作成", type="primary", use_container_width=True)

if submitted:
    if not original_mail.strip() or not key_points.strip():
        st.warning("受信メールの本文と、伝えたい要点の両方を入力してください。")
        st.stop()

    system_instruction = (
        "あなたは日本語ビジネスメールの作成に長けたアシスタントです。"
        "失礼のない自然な言い回しで、簡潔かつ分かりやすい返信文を作成してください。"
    )
    prompt = f"""以下の受信メールに対する返信メールの本文を作成してください。

【受信メール】
{original_mail}

【返信で伝えたい要点】
{key_points}

【トーン】
{tone}

【署名】
{f"最後に「{sender_name}」の名前で締めくくってください。" if sender_name.strip() else "署名部分は「（署名）」とプレースホルダーにしてください。"}

宛名・書き出しの挨拶・本文・結びの挨拶・署名の順で、そのままコピーして使えるメール文面を出力してください。"""

    generate_and_display(prompt, system_instruction, download_filename="reply_mail.txt")
