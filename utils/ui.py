"""各ページ共通のサイドバー・UI部品。"""
import streamlit as st

from utils.gemini_client import DEFAULT_MODEL_LABEL, MODEL_OPTIONS, generate_stream, get_api_key

_CUSTOM_CSS = """
<style>
:root {
    --accent: #4F46E5;
    --accent-dark: #4338CA;
    --accent-soft: #EEF1FF;
    --ink: #1F2233;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #FAFAFC 0%, #F3F4FA 100%);
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #ECECF4;
}

[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.6);
}

h1, h2, h3 {
    color: var(--ink);
    letter-spacing: -0.01em;
}

h1 {
    font-weight: 800;
}

[data-testid="stCaptionContainer"] {
    color: #6B7280;
}

button[data-testid^="stBaseButton"] {
    border-radius: 10px !important;
    font-weight: 600;
    transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(31, 34, 51, 0.06);
}
button[data-testid^="stBaseButton"]:hover {
    transform: translateY(-1px);
}
button[data-testid*="primary"] {
    background: linear-gradient(135deg, var(--accent), #6366F1) !important;
    border: none !important;
    color: #fff !important;
}
button[data-testid*="primary"]:hover {
    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
}

.tool-card {
    border-radius: 14px;
    border: 1px solid #ECECF4;
    background: #FFFFFF;
    padding: 20px 22px;
    margin-bottom: 16px;
    transition: all 0.18s ease;
}
.tool-card:hover {
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.12);
    border-color: #C7D2FE;
    transform: translateY(-2px);
}
.tool-name {
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--ink);
    margin-bottom: 4px;
}
.tool-desc {
    color: #6B7280;
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 0;
}

[data-testid="stSidebarNav"] a {
    border-radius: 8px;
}
[data-testid="stSidebarNav"] a:hover {
    background: var(--accent-soft);
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    border-radius: 10px;
}

footer {visibility: hidden;}

.tool-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--accent-soft);
    font-size: 22px;
    margin-bottom: 8px;
}
</style>
"""


def inject_custom_css():
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)


def render_sidebar():
    """APIキー設定・モデル選択の共通サイドバーを描画する。"""
    inject_custom_css()
    with st.sidebar:
        st.markdown("### ⚙️ 設定")

        if get_api_key():
            st.success("APIキー設定済み")
        else:
            st.warning("APIキー未設定")

        with st.expander("Gemini APIキー", expanded=not get_api_key()):
            key_input = st.text_input(
                "APIキーを入力",
                type="password",
                value=st.session_state.get("gemini_api_key", ""),
                help="Google AI StudioでAPIキーを発行できます。環境変数 GEMINI_API_KEY や "
                ".streamlit/secrets.toml に設定しておけば、ここでの入力は不要です。",
            )
            if key_input:
                st.session_state["gemini_api_key"] = key_input

        st.selectbox(
            "モデル",
            options=list(MODEL_OPTIONS.keys()),
            index=list(MODEL_OPTIONS.keys()).index(
                st.session_state.get("model_label", DEFAULT_MODEL_LABEL)
            ),
            key="model_label",
        )

        st.divider()
        st.page_link("app.py", label="🏠 ホームに戻る")


def require_api_key() -> bool:
    """APIキーが無ければ案内を表示してFalseを返す。"""
    if not get_api_key():
        st.info(
            "👈 左のサイドバーからGemini APIキーを入力してください。\n\n"
            "APIキーは https://aistudio.google.com/apikey から無料で取得できます。"
        )
        return False
    return True


def generate_and_display(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.8,
    download_filename: str = "output.txt",
    state_key: str = "last_result",
):
    """生成ボタン押下後の共通処理：ストリーミング表示＋ダウンロードボタン。"""
    st.markdown("#### 生成結果")
    try:
        with st.spinner("Geminiが生成中..."):
            result = st.write_stream(
                generate_stream(prompt, system_instruction=system_instruction, temperature=temperature)
            )
        st.session_state[state_key] = result
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return

    if st.session_state.get(state_key):
        st.download_button(
            "📥 テキストをダウンロード",
            data=st.session_state[state_key],
            file_name=download_filename,
            mime="text/plain",
        )
