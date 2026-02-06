"""
Streamlit Frontend for PRA COREP Reporting Assistant.
"""
import streamlit as st
import pandas as pd
import json

from pipeline import CorepPipeline
from models.corep import CorepOutput

# Page Config
st.set_page_config(
    page_title="PRA COREP Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box_shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Pipeline (Cached)
@st.cache_resource
def get_pipeline():
    return CorepPipeline()

try:
    pipeline = get_pipeline()
except Exception as e:
    st.error(f"Failed to initialize pipeline: {e}")
    st.stop()


# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/bank-building.png", width=80)
    st.title("Helper Tools")
    
    st.markdown("### ⚙️ Settings")
    model_name = st.text_input("Model Name", value="gemini-2.5-flash", disabled=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info(
        "This assistant helps interpret PRA COREP reporting rules "
        "and generates compliant data structures based on your input."
    )

# Helper: Rule Text Map
from knowledge_base.corpus import REGULATORY_CORPUS
CORPUS_MAP = {chunk["id"]: f"{chunk['source']} {chunk['paragraph']}: {chunk['text']}" for chunk in REGULATORY_CORPUS}

# Main Content
st.markdown('<div class="main-header">🏦 PRA COREP Reporting Assistant</div>', unsafe_allow_html=True)
st.markdown(
    "Describes your capital position and scenarios. "
    "The assistant will interpret PRA rules to check eligibility and compliance."
)

# Input Query
query = st.text_area(
    "Describe your reporting scenario:",
    value="I have £1,000m in paid-up ordinary shares, £200m in retained earnings, and £50m in intangible assets. I also issued £150m in perpetual bonds that are callable after 5 years.",
    height=120,
    help="Enter details about your capital instruments, reserves, and deductions."
)

if st.button("Generate Report", type="primary"):
    with st.spinner("🔍 Analysing regulations and generating data..."):
        try:
            # Run Pipeline
            output: CorepOutput = pipeline.run(query)
            
            # --- High Level Summary Metrics ---
            st.markdown("### 📊 Regulatory Capital Position")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("CET1 Capital", f"£{output.own_funds.common_equity_tier_1:,.2f}m")
            c2.metric("AT1 Capital", f"£{output.own_funds.additional_tier_1:,.2f}m")
            c3.metric("Tier 2 Capital", f"£{output.own_funds.tier_2:,.2f}m")
            c4.metric("Total Own Funds", f"£{output.own_funds.total_own_funds:,.2f}m")
            
            st.markdown("---")
            
            # --- Detailed Breakdown & Reasoning ---
            st.subheader("📝 Regulatory Analysis & Reasoning")
            
            # Sort audit log by specific order if possible
            # We want CET1 -> AT1 -> T2 -> Total
            
            for item in output.audit_log:
                # Create a readable card for each item
                with st.expander(f"🔹 {item.field.replace('_', ' ').title()} = £{item.value:,.2f}m", expanded=True):
                    st.markdown(f"**Reasoning:** {item.explanation}")
                    
                    if item.rule_ids:
                        st.markdown("**📜 Applied Regulatory Rules:**")
                        for rule_id in item.rule_ids:
                            rule_text = CORPUS_MAP.get(rule_id, "Rule text not found.")
                            st.info(f"**{rule_id}**: {rule_text}")

            # --- Validation Section ---
            if output.warnings:
                st.error("⚠️ Compliance Warnings Detected")
                for warning in output.warnings:
                    st.markdown(f"- {warning}")
            else:
                st.success("✅ All data passes basic validation checks.")

            # --- Raw Data Tab ---
            with st.expander("🔍 View Raw API Output (JSON)"):
                st.json(output.model_dump())
                
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
