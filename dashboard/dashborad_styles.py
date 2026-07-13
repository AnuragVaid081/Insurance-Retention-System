import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* Hide Streamlit default elements */

        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        
        /* Main page */

        .stApp{
            background-color:#0F1117;
        }

        .block-container{
            padding-top:2rem;
            padding-left:2rem;
            padding-right:2rem;
        }

        /* Sidebar */

        section[data-testid="stSidebar"]{
            background-color:#14171F;
            border-right:1px solid #2C313C;
        }

       /* KPI Cards */

    div[data-testid="stMetric"] {
        background: #1A1D24 !important;
        border: 1px solid #2C313C !important;
        border-radius: 14px;
        padding: 18px;
    }

    /* Metric Label */

    div[data-testid="stMetricLabel"] p {
        color: #CBD5E1 !important;
        font-size: 14px;
    }

    /* Metric Value */


        div[data-testid="stMetricValue"]{
            color:#FACC15;
            font-weight:bold;
        }

        /* Headers */

        h1,h2,h3{
            color:#F8FAFC;
        }

        p,label{
            color:#CBD5E1;
        }

        /* Dataframe */

        div[data-testid="stDataFrame"]{
            border-radius:12px;
            border:1px solid #2C313C;
        }

        </style>
        """,
        unsafe_allow_html=True
    )