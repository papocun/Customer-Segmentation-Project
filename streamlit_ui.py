import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Homepage",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Theme State
# ---------------------------------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

THEMES = {
    "dark": {
        "bg": "#0E1117",
        "card_bg": "#1A1D26",
        "card_border": "#2B2F3A",
        "sidebar_bg": "#161A23",
        "text": "#FAFAFA",
        "subtext": "#9CA3AF",
        "input_bg": "#1A1D26",
        "input_text": "#FAFAFA",
        "input_border": "#2B2F3A",
        "accent_1": "#2563EB",
        "accent_2": "#1D4ED8",
        "accent_hover_1": "#1D4ED8",
        "accent_hover_2": "#1E40AF",
        "plotly_template": "plotly_dark",
    },
    "light": {
        "bg": "#F5F7FA",
        "card_bg": "#FFFFFF",
        "card_border": "#E2E8F0",
        "sidebar_bg": "#FFFFFF",
        "text": "#111827",
        "subtext": "#4B5563",
        "input_bg": "#FFFFFF",
        "input_text": "#111827",
        "input_border": "#CBD5E1",
        "accent_1": "#2563EB",
        "accent_2": "#1D4ED8",
        "accent_hover_1": "#1D4ED8",
        "accent_hover_2": "#1E40AF",
        "plotly_template": "plotly_white",
    },
}

theme = THEMES[st.session_state.theme]

# Currency symbol used everywhere in the dashboard
CURRENCY = "₹"

# ---------------------------------------------------------
# Custom CSS (driven by theme dict, not hardcoded)
# ---------------------------------------------------------

st.markdown(f"""
<style>

/* Hide Streamlit Branding */
#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

/* Streamlit's own CSS variables drive native widget colors
   (number input, select box, slider, etc). Overriding these
   is what actually fixes light-mode visibility. */
:root, .stApp {{
    --primary-color: {theme['accent_1']};
    --background-color: {theme['bg']};
    --secondary-background-color: {theme['card_bg']};
    --text-color: {theme['text']};
}}

.stApp{{
    background:{theme['bg']};
    color:{theme['text']};
}}

/* Main Container */
.block-container{{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1300px;
}}

/* Hero Card */
.hero{{
    background:linear-gradient(135deg,{theme['accent_1']},{theme['accent_2']});
    padding:35px;
    border-radius:18px;
    color:white;
    box-shadow:0px 8px 30px rgba(0,0,0,.25);
    margin-bottom:25px;
}}

.hero h1{{
    font-size:46px;
    margin-bottom:5px;
}}

.hero p{{
    font-size:18px;
    opacity:.9;
}}

/* Section Title */
.section-title{{
    font-size:28px;
    font-weight:700;
    margin-top:15px;
    margin-bottom:20px;
    color:{theme['text']};
}}

/* Card */
.metric-card{{
    background:{theme['card_bg']};
    padding:20px;
    border-radius:15px;
    border:1px solid {theme['card_border']};
    text-align:center;
    color:{theme['text']};
}}

/* General text / headings / labels visibility across both themes */
h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stCaption {{
    color:{theme['text']};
}}

div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] {{
    color:{theme['text']};
}}

/* ---- Native input widgets (Number Input, Selectbox, Slider) ---- */

.stNumberInput input,
.stTextInput input {{
    background-color:{theme['input_bg']} !important;
    color:{theme['input_text']} !important;
    border:1px solid {theme['input_border']} !important;
}}

.stNumberInput button {{
    background-color:{theme['input_bg']} !important;
    color:{theme['input_text']} !important;
    border:1px solid {theme['input_border']} !important;
}}

div[data-baseweb="select"] > div {{
    background-color:{theme['input_bg']} !important;
    color:{theme['input_text']} !important;
    border:1px solid {theme['input_border']} !important;
}}

/* Dropdown menu portal renders outside .stApp, needs its own rule */
div[data-baseweb="popover"] ul, div[data-baseweb="menu"] {{
    background-color:{theme['input_bg']} !important;
    color:{theme['input_text']} !important;
}}

div[data-baseweb="popover"] li:hover {{
    background-color:{theme['card_border']} !important;
}}

.stSlider label, .stNumberInput label, .stSelectbox label {{
    color:{theme['text']} !important;
}}

/* Slider track / thumb numbers */
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"],
.stSlider div[role="slider"] {{
    color:{theme['text']} !important;
}}

/* Info / success boxes */
div[data-testid="stAlert"] {{
    background-color:{theme['card_bg']} !important;
    color:{theme['text']} !important;
}}

/* Button */
div.stButton>button{{
    width:100%;
    height:60px;
    font-size:20px;
    font-weight:bold;
    border-radius:15px;
    background:linear-gradient(90deg,{theme['accent_1']},{theme['accent_2']});
    color:white;
    border:none;
}}

div.stButton>button:hover{{
    background:linear-gradient(90deg,{theme['accent_hover_1']},{theme['accent_hover_2']});
    color:white;
}}

/* Sidebar */
section[data-testid="stSidebar"]{{
    background:{theme['sidebar_bg']};
}}

section[data-testid="stSidebar"] * {{
    color:{theme['text']} !important;
}}

/* Sidebar multipage navigation: force Title Case + readable color */
section[data-testid="stSidebarNav"] a span,
section[data-testid="stSidebarNav"] a p {{
    text-transform: capitalize !important;
    color:{theme['text']} !important;
}}

section[data-testid="stSidebarNav"] a:hover span,
section[data-testid="stSidebarNav"] a:hover p {{
    color:{theme['accent_1']} !important;
}}

/* ---- Floating Sun/Moon theme toggle, fixed top-right ---- */
.st-key-theme_toggle_container {{
    position: fixed;
    top: 14px;
    right: 30px;
    z-index: 9999;
    width: 50px !important;
}}

.st-key-theme_toggle_container div.stButton>button {{
    width:46px;
    height:46px;
    min-height:46px;
    border-radius:50%;
    font-size:20px;
    padding:0;
    display:flex;
    align-items:center;
    justify-content:center;
    background:{theme['card_bg']};
    border:1px solid {theme['card_border']};
    color:{theme['text']};
    box-shadow:0px 4px 14px rgba(0,0,0,.15);
}}

.st-key-theme_toggle_container div.stButton>button:hover {{
    background:{theme['card_border']};
}}

</style>
""", unsafe_allow_html=True)

# Best-effort relabel of the first sidebar nav entry to "Homepage".
# (Multipage nav labels normally come from filenames; renaming the
# entry file itself to Homepage.py is the cleaner long-term fix —
# this JS patch just covers it live in the browser.)
components.html("""
<script>
function relabelNav(){
    const doc = window.parent.document;
    const navLinks = doc.querySelectorAll('[data-testid="stSidebarNav"] a');
    navLinks.forEach(link => {
        const label = link.querySelector('span') || link.querySelector('p');
        if (label && label.textContent.trim().toLowerCase() === 'streamlit ui') {
            label.textContent = 'Homepage';
        }
    });
}
relabelNav();
const observer = new MutationObserver(relabelNav);
observer.observe(window.parent.document.body, {childList: true, subtree: true});
</script>
""", height=0, width=0)

# ---------------------------------------------------------
# Floating theme toggle (sun / moon, top-right corner)
# ---------------------------------------------------------

with st.container(key="theme_toggle_container"):
    icon = "☀️" if st.session_state.theme == "dark" else "🌙"
    if st.button(icon, key="theme_toggle_btn", help="Toggle light / dark mode"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.title("🛍️ Customer Segmentation")

    st.markdown("---")

    st.subheader("📊 Model")

    st.success("KMeans Clustering")

    st.write("Version : **1.0**")

    st.markdown("---")

    st.subheader("⚙️ Tech Stack")

    st.write("""
- FastAPI
- Streamlit
- MongoDB
- Scikit-Learn
- KMeans
- Plotly
""")

    st.markdown("---")

    st.subheader("📌 Features")

    st.write("""
✅ Income

✅ Total Spending

✅ Purchases

✅ Recency

✅ Website Visits

✅ Promotions

✅ Children
""")

    st.markdown("---")

    st.info("Built with ❤️ by Divyanshu")

# ---------------------------------------------------------
# Hero Section
# ---------------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🛍️ Customer Segmentation Dashboard</h1>

<p>
AI-Powered Customer Analytics using Machine Learning
</p>

</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">📋 Customer Information</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Customer Input Section
# ---------------------------------------------------------

left_col, right_col = st.columns(2, gap="large")

with left_col:

    st.markdown("#### 💰 Financial Information")

    income = st.number_input(
        "Annual Income",
        min_value=0.0,
        value=52000.0,
        step=1000.0,
        help="Customer yearly income"
    )

    total_spending = st.number_input(
        "Total Spending",
        min_value=0.0,
        value=700.0,
        step=50.0,
        help="Total customer spending"
    )

    total_purchases = st.number_input(
        "Total Purchases",
        min_value=0,
        value=10,
        step=1,
        help="Number of purchases"
    )

    recency = st.slider(
        "📅 Days Since Last Purchase",
        0,
        100,
        42,
        help="Lower value means more recent purchase"
    )


with right_col:

    st.markdown("#### 🌐 Customer Behaviour")

    web_visits = st.slider(
        "Website Visits",
        0,
        20,
        5,
        help="Monthly website visits"
    )

    promotions = st.slider(
        "Promotions Accepted",
        0,
        10,
        2,
        help="Accepted promotional offers"
    )

    children = st.selectbox(
        "Children",
        [0, 1, 2, 3, 4],
        help="Number of children"
    )

st.write("")
st.write("")

# ---------------------------------------------------------
# Input Summary Cards
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Customer Summary</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("💰 Income", f"{CURRENCY}{income:,.0f}")

with m2:
    st.metric("💵 Spending", f"{CURRENCY}{total_spending:,.0f}")

with m3:
    st.metric("🛒 Purchases", total_purchases)

with m4:
    st.metric("🌐 Visits", web_visits)

st.write("")
st.write("")

predict_btn = st.button("🚀 Predict Customer Segment")

# ==========================================================
# Prediction Helper
# ==========================================================

API_URL = "http://127.0.0.1:8000/predict"


def get_customer_profile(segment):
    profiles = {
        "High Value Customer": {
            "income": "High",
            "spending": "High",
            "loyalty": "Excellent",
            "color": "🟢",
            "strategies": [
                "Offer premium memberships",
                "Provide exclusive loyalty rewards",
                "Recommend high-value products"
            ]
        },
        "Budget Customer": {
            "income": "Moderate",
            "spending": "Low",
            "loyalty": "Average",
            "color": "🟡",
            "strategies": [
                "Send discount coupons",
                "Bundle related products",
                "Promote seasonal offers"
            ]
        }
    }

    return profiles.get(
        segment,
        {
            "income": "-",
            "spending": "-",
            "loyalty": "-",
            "color": "⚪",
            "strategies": []
        },
    )


# ==========================================================
# Session state to persist last prediction across reruns
# (theme toggle / other widget changes no longer wipe it out)
# ==========================================================

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# ==========================================================
# Prediction
# ==========================================================

if predict_btn:

    payload = {
        "Income": income,
        "Total_Spending": total_spending,
        "Total_Purchases": total_purchases,
        "Recency": recency,
        "NumWebVisitsMonth": web_visits,
        "Total_Promo_Accepted": promotions,
        "Children": children,
    }

    try:

        with st.spinner("🔍 Analyzing customer..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=15
            )

        response.raise_for_status()

        result = response.json()

        cluster = result["cluster"]
        segment = result["segment"]
        description = result["description"]

        profile = get_customer_profile(segment)

        st.session_state.last_prediction = {
            "cluster": cluster,
            "segment": segment,
            "description": description,
            "profile": profile,
        }

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Unable to connect to FastAPI.\n\nRun:\n\nuvicorn app:app --reload"
        )

        st.stop()

    except requests.exceptions.Timeout:

        st.error("❌ Request timed out.")

        st.stop()

    except Exception as e:

        st.error(str(e))

        st.stop()

# Pull whatever the latest prediction is (persists across reruns)
prediction = st.session_state.last_prediction

if prediction:

    cluster = prediction["cluster"]
    segment = prediction["segment"]
    description = prediction["description"]
    profile = prediction["profile"]

    # ======================================================
    # Prediction Dashboard
    # ======================================================

    st.markdown("---")

    st.markdown(
        """
        <div class='section-title'>
        🎯 Prediction Dashboard
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.2, 1], gap="large")

    # ------------------------------------------------------
    # LEFT PANEL
    # ------------------------------------------------------

    with left:

        st.success(f"{profile['color']} {segment}")

        st.write(description)

        st.write("")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Income Level", profile["income"])

        with c2:
            st.metric("Spending", profile["spending"])

        with c3:
            st.metric("Loyalty", profile["loyalty"])

        st.write("")

        st.subheader("📢 Recommended Marketing Strategy")

        for item in profile["strategies"]:
            st.markdown(f"✅ {item}")

    # ------------------------------------------------------
    # RIGHT PANEL
    # ------------------------------------------------------

    with right:

        st.markdown("### 📊 Model Output")

        st.metric("Cluster", cluster)
        st.metric("Segment", segment)
        st.metric("Website Visits", web_visits)
        st.metric("Promotions", promotions)
        st.metric("Children", children)

# ==========================================================
# Customer Analytics Dashboard
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div class='section-title'>
        📈 Customer Analytics
    </div>
    """,
    unsafe_allow_html=True,
)

feature_names = [
    "Income",
    "Spending",
    "Purchases",
    "Recency",
    "Visits",
    "Promotions",
    "Children",
]

feature_values = [
    income,
    total_spending,
    total_purchases,
    recency,
    web_visits,
    promotions,
    children,
]

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=feature_names,
        y=feature_values,
        text=feature_values,
        textposition="outside",
        marker=dict(
            color=[
                "#3B82F6",
                "#10B981",
                "#F59E0B",
                "#EF4444",
                "#8B5CF6",
                "#06B6D4",
                "#EC4899",
            ]
        ),
    )
)

fig.update_layout(
    template=theme["plotly_template"],
    height=450,
    title="Customer Feature Overview",
    xaxis_title="Features",
    yaxis_title="Values",
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# Customer Snapshot
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div class='section-title'>
        📋 Customer Snapshot
    </div>
    """,
    unsafe_allow_html=True,
)

# Use 3 columns consistently so the "Family" card sits alongside
# the other two instead of a separate (buggy) row below.
snapshot1, snapshot2, snapshot3 = st.columns(3)

with snapshot1:

    st.info(
        f"""
### 💰 Financial

**Income:** {CURRENCY}{income:,.0f}

**Spending:** {CURRENCY}{total_spending:,.0f}

**Purchases:** {total_purchases}
"""
    )

with snapshot2:

    st.info(
        f"""
### 🌐 Behaviour

**Website Visits:** {web_visits}

**Recency:** {recency}

**Promotions:** {promotions}
"""
    )

with snapshot3:

    if prediction:
        st.info(f"""
### 👨‍👩‍👧 Family

**Children:** {children}

**Predicted Segment:**

**{prediction['segment']}**
""")
    else:
        st.info(
            f"""
### 👨‍👩‍👧 Family

**Children:** {children}

**Predicted Segment:**

_Run a prediction to see this_
"""
        )

# ==========================================================
# Download Prediction
# ==========================================================

if prediction:
    prediction_df = pd.DataFrame(
        {
            "Segment": [prediction["segment"]],
            "Cluster": [prediction["cluster"]],
            "Income": [income],
            "Total Spending": [total_spending],
            "Purchases": [total_purchases],
            "Recency": [recency],
            "Website Visits": [web_visits],
            "Promotions": [promotions],
            "Children": [children],
        }
    )

    csv = prediction_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Prediction Report",
        csv,
        file_name="customer_prediction.csv",
        mime="text/csv",
    )
else:
    st.caption("Run a prediction above to enable the download report button.")

# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;padding:20px;color:gray;">

### 🛍️ Customer Segmentation Dashboard

Built using

**FastAPI • Streamlit • Scikit-Learn • Plotly • MongoDB**

Made with ❤️ by Divyanshu

</div>
""",
    unsafe_allow_html=True,
)