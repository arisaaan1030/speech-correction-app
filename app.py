import streamlit as st
import google.generativeai as genai
import os

# APIキーを環境変数 or Streamlit Secrets から取得
API_KEY = os.getenv("GEMINI_API_KEY", st.secrets["GEMINI_API_KEY"])
genai.configure(api_key=API_KEY)

# Streamlit UIの設定
st.set_page_config(page_title="音声入力補正ツール", page_icon="✨", layout="centered")

# ヘッダー部分を装飾
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎤 音声入力補正ツール</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>音声入力の誤変換を修正し、自然な文章に補正！</p>", unsafe_allow_html=True)

# プロンプトの種類を選択するドロップダウンメニュー
prompt_options = {
    "標準補正": "以下の日本語の誤変換を修正し、前後の文脈を考慮して適切な表現にしてください。\n{input_text}",
    "最小限補正（文体を保持）": "以下の日本語の文章について、語彙や文体を変えず、同音異義語や誤変換された漢字だけを修正してください。句読点は必要な箇所にのみ追加し、文の構造や口調はできるだけ維持してください。必要最小限の修正のみに留めて、文脈に合わない誤変換を正して自然な文章にしてください。\n{input_text}",
    "専門用語を正しく補正": "以下の日本語の誤変換を修正し、投資・金融関連の専門用語を適切に表記し、文脈に合った文章にしてください。\n{input_text}",
    "フォーマルな文章へ変換": "以下の日本語の誤変換を修正し、投資・金融に関する専門的な記事として適切なフォーマルな文章に整えてください。また、文章の流れが自然になるように句読点を追加してください。\n{input_text}",
}

# **文脈を考慮した誤変換補正用プロンプト**
advanced_prompt = """
以下の日本語の誤変換を修正し、適切な句読点を追加してください。
特に、同音異義語（例：「球場」→「休場」）や、誤変換の可能性がある単語を適切に修正してください。

【入力】:
{input_text}

【出力】:
誤変換の可能性がある単語:
- 元の単語: {wrong_word}
- 修正後の単語: {corrected_word}

修正後の文章:
{corrected_text}
"""

# **ドロップダウンメニューを追加**
selected_prompt = st.selectbox("📝 プロンプトの種類を選択", list(prompt_options.keys()))

# **入力テキストエリア**
input_text = st.text_area("🎙️ 音声入力の文章を入力してください", "")

# **「補正する」ボタン**
if st.button("✨ 補正する"):
    if input_text.strip():
        # **ユーザーが選んだプロンプトを適用**
        if selected_prompt in prompt_options:
            prompt = prompt_options[selected_prompt].replace("{input_text}", input_text)
        else:
            prompt = advanced_prompt.replace("{input_text}", input_text)

        # **Gemini APIの呼び出し**
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # **補正後の文章を表示**
        corrected_text = response.text
        st.subheader("✅ 修正後の文章")
        st.write(corrected_text)

        # **コピー用のボタンを追加**
        st.code(corrected_text, language="text")  # 修正後の文章をコードブロックで表示
        st.button("📋 クリップボードにコピー", key="copy_button")

    else:
        st.warning("⚠️ 文章を入力してください！")
