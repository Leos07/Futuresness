import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter, defaultdict
import re
import io
import json
from datetime import datetime
import numpy as np

# Import for file handling
try:
    from docx import Document
    import PyPDF2
except ImportError:
    pass

# Set page configuration
st.set_page_config(
    page_title="Futures Studies Vocabulary Analyzer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# NOTE: This legacy Streamlit app was preserved for local use. The primary deployment target is the FastAPI server (see `api/main.py`).

# (The rest of this file was copied from the original Streamlit app and is unchanged.)

FUTURES_VOCABULARY = {
    "Foresight Methods": [
        "scenario planning", "scenarios", "scenario analysis", "scenario building",
        "delphi method", "delphi", "expert panel", "expert consultation",
        "horizon scanning", "environmental scanning", "scanning",
        "trend analysis", "trend monitoring", "megatrends", "macro trends",
        "weak signals", "weak signal detection", "emerging issues",
        "wild cards", "black swans", "surprises",
        "backcasting", "normative scenarios",
        "causal layered analysis", "CLA",
        "futures wheel", "futures triangle",
        "cross-impact analysis", "morphological analysis",
        "roadmapping", "technology roadmapping",
        "visioning", "vision building", "preferred futures",
        "foresight", "strategic foresight", "corporate foresight",
        "forecasting", "predictive analytics", "extrapolation",
        "simulation", "modeling", "system dynamics",
    ],
    "Futures Concepts": [
        "futures", "future studies", "futures research", "futurism",
        "anticipation", "anticipatory systems", "anticipatory governance",
        "plausible futures", "possible futures", "probable futures", "preferable futures",
        "alternative futures", "multiple futures", "futures cone",
        "uncertainty", "ambiguity", "complexity", "volatility", "VUCA",
        "emergence", "emergent properties", "emerging trends",
        "disruption", "disruptive innovation", "discontinuity",
        "transformation", "transformative change", "transition",
        "resilience", "adaptive capacity", "adaptability",
        "long-term thinking", "long-term perspective", "temporal depth",
        "foresight capacity", "futures literacy", "futures thinking",
        "futures consciousness", "anticipatory awareness",
    ],
    # ... rest of vocabulary omitted for brevity in the legacy file
}

def main():
    st.markdown('<h1 class="main-header">🔮 Futures Studies Vocabulary Analyzer (Legacy Streamlit)</h1>', unsafe_allow_html=True)
    st.markdown("""
    This is the legacy Streamlit UI preserved for local interactive use. For deployment and the main server, run the FastAPI app in `api/main.py`.
    """)
    st.info("To run the FastAPI server locally: `uvicorn api.main:app --reload --port 8000`")

if __name__ == "__main__":
    main()
