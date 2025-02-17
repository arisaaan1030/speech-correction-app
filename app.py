import streamlit as st
import google.generativeai as genai

# APIキーの設定
API_KEY = "AIzaSyD_u65YIMj_Iw9TQ4NrJcSMx5tXGscn8jE"
genai.configure(api_key=API_KEY)

# Streamlit UIの設定
st.set_page_config(page_title="音声入力補正ツール", page_icon="✨", layout="centered")

# ヘッダー部分を装飾
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎤 音声入力補正ツール</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>音声入力の誤変換を修正し、自然な文章に補正！</p>", unsafe_allow_html=True)

# プロンプトの種類を選択するドロップダウンメニュー
prompt_options = {
    "標準補正": "以下の日本語の誤変換を修正し、適切に句読点を追加してください。\n{input_text}",
    "専門用語を正しく補正": "以下の日本語の誤変換を修正し、投資・金融関連の専門用語が正しく表記されるようにしてください。\n{input_text}",
    "フォーマルな文章へ変換": "以下の日本語の誤変換を修正し、投資・金融に関する専門的な記事として適切なフォーマルな文章に整えてください。\n{input_text}",
    "SNS向けに整える": "以下の日本語の誤変換を修正し、SNS投稿として適切なテンションを維持しつつ、句読点を適切に追加してください。\n{input_text}"
}

# **ドロップダウンメニューを追加**
selected_prompt = st.selectbox("📝 プロンプトの種類を選択", list(prompt_options.keys()))

# **入力テキストエリア**
input_text = st.text_area("🎙️ 音声入力の文章を入力してください", "")

# **「補正する」ボタン**
if st.button("✨ 補正する"):
    if input_text.strip():
        # **ユーザーが選んだプロンプトを適用**
        prompt = prompt_options[selected_prompt].replace("{input_text}", input_text)
        
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
