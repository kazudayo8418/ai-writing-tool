"""各ページ共通のサイドバー・UI部品。"""
import streamlit as st

from utils.gemini_client import DEFAULT_MODEL_LABEL, MODEL_OPTIONS, generate_stream, get_api_key


def render_sidebar():
    """APIキー設定・モデル選択の共通サイドバーを描画する。"""
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
