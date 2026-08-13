"""アプリ全体の簡易パスワードゲート。"""
import os

import streamlit as st


def get_app_password() -> str | None:
    try:
        if "APP_PASSWORD" in st.secrets:
            return st.secrets["APP_PASSWORD"]
    except Exception:
        pass
    return os.environ.get("APP_PASSWORD")


def require_password():
    """APP_PASSWORDが設定されている場合のみ、ログインを要求する。"""
    password = get_app_password()
    if not password:
        return

    if st.session_state.get("authenticated"):
        return

    st.title("🔒 ログイン")
    st.caption("このアプリを利用するにはパスワードが必要です。")
    entered = st.text_input("パスワード", type="password")
    if st.button("ログイン", type="primary"):
        if entered == password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("パスワードが違います。")
    st.stop()
