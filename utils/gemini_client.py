"""Gemini APIとのやり取りをまとめた共通モジュール。"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_OPTIONS = {
    "Gemini 3.5 Flash（高速・おすすめ）": "gemini-3.5-flash",
    "Gemini 3.1 Pro（高精度）": "gemini-3.1-pro-preview",
    "Gemini 3.5 Flash-Lite（最速・軽量）": "gemini-3.5-flash-lite",
}
DEFAULT_MODEL_LABEL = "Gemini 3.5 Flash（高速・おすすめ）"


def get_api_key() -> str | None:
    """st.secrets → 環境変数 → セッション入力 の優先順でAPIキーを取得する。"""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key

    return st.session_state.get("gemini_api_key")


def get_client() -> genai.Client | None:
    api_key = get_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def get_selected_model() -> str:
    label = st.session_state.get("model_label", DEFAULT_MODEL_LABEL)
    return MODEL_OPTIONS.get(label, MODEL_OPTIONS[DEFAULT_MODEL_LABEL])


def generate_stream(prompt: str, system_instruction: str | None = None, temperature: float = 0.8):
    """Gemini APIにストリーミングでリクエストし、テキストチャンクを順次yieldする。"""
    client = get_client()
    if client is None:
        raise RuntimeError("APIキーが設定されていません。サイドバーから設定してください。")

    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )

    stream = client.models.generate_content_stream(
        model=get_selected_model(),
        contents=prompt,
        config=config,
    )
    for chunk in stream:
        if chunk.text:
            yield chunk.text
