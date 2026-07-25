"""
Shared Theme Manager
Supports:
- Dark / Light Mode
- Reusable Plotly Theme
- Shared CSS
- Floating Theme Toggle
"""

import streamlit as st

CURRENCY = "₹"

# ==========================================================
# Theme Definitions
# ==========================================================

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

        "plot_text": "#FAFAFA",
        "plot_grid": "#374151",
        "plot_axis": "#FAFAFA",
    },

    "light": {

        "bg": "#FAF6EF",
        "card_bg": "#FFFFFF",
        "card_border": "#D4D4D8",

        "sidebar_bg": "#FAF6EF",

        "text": "#171717",
        "subtext": "#525252",

        "input_bg": "#FFFFFF",
        "input_text": "#171717",
        "input_border": "#D4D4D8",

        "accent_1": "#EA580C",
        "accent_2": "#C2410C",

        "accent_hover_1": "#C2410C",
        "accent_hover_2": "#9A3412",

        "plotly_template": "plotly_white",

        "plot_text": "#171717",
        "plot_grid": "#D1D5DB",
        "plot_axis": "#171717",
    },
}


# ==========================================================
# Initialize Theme
# ==========================================================

def init_theme():

    if "theme" not in st.session_state:

        st.session_state.theme = "dark"

    return THEMES[st.session_state.theme]


# ==========================================================
# Rerun Compatibility
# ==========================================================

def _rerun():

    try:

        st.rerun()

    except AttributeError:

        st.experimental_rerun()


# ==========================================================
# Plotly Helper
# ==========================================================

def apply_plotly_theme(fig, theme):

    fig.update_layout(

        template=theme["plotly_template"],

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(

            color=theme["plot_text"],

            size=15

        ),

        title_font=dict(

            color=theme["plot_text"],

            size=24

        ),

        legend=dict(

            font=dict(

                color=theme["plot_text"]

            )

        ),

        xaxis=dict(

            title_font=dict(

                color=theme["plot_axis"]

            ),

            tickfont=dict(

                color=theme["plot_axis"]

            ),

            linecolor=theme["plot_axis"],

            showgrid=False,

            mirror=True

        ),

        yaxis=dict(

            title_font=dict(

                color=theme["plot_axis"]

            ),

            tickfont=dict(

                color=theme["plot_axis"]

            ),

            linecolor=theme["plot_axis"],

            gridcolor=theme["plot_grid"],

            zerolinecolor=theme["plot_grid"],

            mirror=True

        )

    )

    return fig

def inject_css(theme):

    st.markdown(f"""
<style>

/* ==========================================================
   Streamlit Branding
========================================================== */

#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

[data-testid="stToolbar"],
[data-testid="stAppToolbar"] {{
    visibility:hidden;
}}

header,
header[data-testid="stHeader"],
header[data-testid="stAppHeader"] {{
    background:transparent;
}}

/* ==========================================================
   Sidebar Collapse Button
========================================================== */

[data-testid="collapsedControl"],
[data-testid="stExpandSidebarButton"] {{

    visibility:visible !important;

    color:{theme["text"]} !important;

}}

[data-testid="collapsedControl"] svg,
[data-testid="stExpandSidebarButton"] svg {{

    fill:{theme["text"]} !important;

}}

/* ==========================================================
   Root Variables
========================================================== */

:root,
.stApp {{

    --primary-color:{theme["accent_1"]};

    --background-color:{theme["bg"]};

    --secondary-background-color:{theme["card_bg"]};

    --text-color:{theme["text"]};

}}

/* ==========================================================
   Main Background
========================================================== */

.stApp{{
    background:{theme["bg"]};
    color:{theme["text"]};
}}

.block-container{{
    max-width:1300px;
    padding-top:2rem;
    padding-bottom:2rem;
}}

/* ==========================================================
   Hero
========================================================== */

.hero{{

    background:
        linear-gradient(
            135deg,
            {theme["accent_1"]},
            {theme["accent_2"]}
        );

    padding:35px;

    border-radius:18px;

    color:white;

    margin-bottom:30px;

    box-shadow:
        0px 10px 35px rgba(0,0,0,.25);

}}

.hero h1{{
    font-size:46px;
    margin-bottom:5px;
}}

.hero p{{
    font-size:18px;
    opacity:.9;
}}

/* ==========================================================
   Typography
========================================================== */

.section-title{{
    font-size:30px;
    font-weight:700;
    color:{theme["text"]};
    margin-top:20px;
    margin-bottom:20px;
}}

h1,h2,h3,h4,h5,h6,
p,span,label,
.stMarkdown,
.stCaption{{
    color:{theme["text"]};
}}

/* ==========================================================
   Metric Cards
========================================================== */

.metric-card{{

    background:{theme["card_bg"]};

    border:1px solid {theme["card_border"]};

    border-radius:16px;

    padding:20px;

    color:{theme["text"]};

}}

div[data-testid="stMetricValue"],
div[data-testid="stMetricLabel"]{{
    color:{theme["text"]};
}}

/* ==========================================================
   Inputs
========================================================== */

.stNumberInput input,
.stTextInput input{{

    background:{theme["input_bg"]} !important;

    color:{theme["input_text"]} !important;

    border:1px solid {theme["input_border"]} !important;

}}

.stNumberInput button{{

    background:{theme["input_bg"]} !important;

    color:{theme["input_text"]} !important;

}}

div[data-baseweb="select"] > div{{

    background:{theme["input_bg"]} !important;

    color:{theme["input_text"]} !important;

    border:1px solid {theme["input_border"]} !important;

}}

.stSlider label,
.stNumberInput label,
.stSelectbox label{{
    color:{theme["text"]} !important;
}}

/* ==========================================================
   Buttons
========================================================== */

div.stButton > button{{

    width:100%;

    height:60px;

    border-radius:15px;

    font-size:20px;

    font-weight:bold;

    border:none;

    color:white;

    background:
        linear-gradient(
            90deg,
            {theme["accent_1"]},
            {theme["accent_2"]}
        );

}}

div.stButton > button:hover{{

    background:
        linear-gradient(
            90deg,
            {theme["accent_hover_1"]},
            {theme["accent_hover_2"]}
        );

}}

/* ==========================================================
   Sidebar
========================================================== */

section[data-testid="stSidebar"]{{
    background:{theme["sidebar_bg"]};
}}

section[data-testid="stSidebar"] *{{
    color:{theme["text"]} !important;
}}

section[data-testid="stSidebarNav"] a span,
section[data-testid="stSidebarNav"] a p{{
    color:{theme["text"]} !important;
}}

section[data-testid="stSidebarNav"] a:hover span{{
    color:{theme["accent_1"]} !important;
}}

/* ==========================================================
   Plotly
========================================================== */

/* Light Mode */

.js-plotly-plot .plotly .xtick text,
.js-plotly-plot .plotly .ytick text,
.js-plotly-plot .plotly .gtitle,
.js-plotly-plot .plotly .xtitle,
.js-plotly-plot .plotly .ytitle,
.js-plotly-plot .plotly .legendtext{{
    fill:{theme["plot_text"]} !important;
}}

/* ==========================================================
   Theme Toggle
========================================================== */

div[data-testid="stMain"] div[data-testid="stButton"]:first-of-type{{

    position:fixed;

    top:8px;

    right:5px;

    z-index:999999;

    width:40px;

}}

div[data-testid="stMain"] div[data-testid="stButton"]:first-of-type button{{

    width:40px;

    height:40px;

    min-height:40px;

    padding:0;

    border-radius:50%;

    border:1px solid {theme["card_border"]};

    background:{theme["card_bg"]};

    color:{theme["text"]};

    display:flex;

    justify-content:center;

    align-items:center;

}}

div[data-testid="stMain"] div[data-testid="stButton"]:first-of-type button:hover{{

    border-color:{theme["accent_1"]};

}}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Theme Toggle
# ==========================================================

def theme_toggle():
    """
    Floating Light / Dark Toggle

    Place this immediately after:

        theme = init_theme()
        inject_css(theme)

    on every page.
    """

    current = st.session_state.get("theme", "dark")

    icon = "☀️" if current == "dark" else "🌙"

    if st.button(
        icon,
        key="theme_toggle_btn",
        help="Switch Theme",
    ):

        st.session_state.theme = (
            "light"
            if current == "dark"
            else "dark"
        )

        _rerun()


# ==========================================================
# Plotly Theme Helper
# ==========================================================

def style_plotly(fig):
    """
    Automatically styles any Plotly figure
    according to the active theme.
    """

    theme = THEMES[st.session_state.theme]

    fig.update_layout(

        template=theme["plotly_template"],

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color=theme["plot_text"],
            size=15
        ),

        title_font=dict(
            color=theme["plot_text"],
            size=24
        ),

        legend=dict(
            font=dict(
                color=theme["plot_text"]
            )
        ),

        xaxis=dict(

            title_font=dict(
                color=theme["plot_axis"]
            ),

            tickfont=dict(
                color=theme["plot_axis"]
            ),

            linecolor=theme["plot_axis"],

            mirror=True,

            showgrid=False

        ),

        yaxis=dict(

            title_font=dict(
                color=theme["plot_axis"]
            ),

            tickfont=dict(
                color=theme["plot_axis"]
            ),

            gridcolor=theme["plot_grid"],

            zerolinecolor=theme["plot_grid"],

            linecolor=theme["plot_axis"],

            mirror=True

        )

    )

    return fig


# ==========================================================
# Plotly Bar Helper
# ==========================================================

def style_bar(bar):

    theme = THEMES[st.session_state.theme]

    bar.update(

        textfont=dict(

            color=theme["plot_text"],

            size=15

        )

    )

    return bar


# ==========================================================
# Colors
# ==========================================================

def get_segment_color(segment):

    colors = {

        "High Value Customer": "#16A34A",

        "Budget Customer": "#2563EB",

    }

    return colors.get(segment, "#9CA3AF")


# ==========================================================
# Success Card
# ==========================================================

def success_card(title, value):

    st.markdown(
        f"""
<div style="

background:{THEMES[st.session_state.theme]['card_bg']};

padding:18px;

border-radius:14px;

border:1px solid {THEMES[st.session_state.theme]['card_border']};

text-align:center;

">

<h4 style="margin:0;color:{THEMES[st.session_state.theme]['subtext']};">

{title}

</h4>

<h2 style="margin-top:10px;color:{THEMES[st.session_state.theme]['text']};">

{value}

</h2>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Divider
# ==========================================================

def divider():

    st.markdown(
        """
<hr style="
border:0;
height:1px;
background:#374151;
margin-top:30px;
margin-bottom:30px;
">
""",
        unsafe_allow_html=True,
    )