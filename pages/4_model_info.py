import streamlit as st
from common_theme import init_theme, inject_css, theme_toggle

st.set_page_config(page_title="Model Info", page_icon="🧠", layout="wide")

theme = init_theme()
inject_css(theme)
theme_toggle()

with st.sidebar:
    st.title("🛍️ Customer Segmentation")

st.markdown('<div class="section-title">🧠 Model Info</div>', unsafe_allow_html=True)

st.info(
    "This is a placeholder page. Move your existing model-details "
    "logic here (algorithm, features, training info) — it already "
    "inherits the shared light/dark theme, sidebar styling, and the "
    "sun/moon toggle from Homepage.py."
)