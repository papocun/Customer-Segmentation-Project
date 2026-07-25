import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

from common_theme import init_theme, inject_css, theme_toggle, CURRENCY

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Homepage",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

theme = init_theme()
inject_css(theme)
theme_toggle()

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

prediction = st.session_state.last_prediction

if prediction:

    cluster = prediction["cluster"]
    segment = prediction["segment"]
    description = prediction["description"]
    profile = prediction["profile"]

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