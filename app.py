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

# Main Content
st.markdown('<div class="main-header">🏦 PRA COREP Reporting Assistant</div>', unsafe_allow_html=True)
st.markdown("Ask questions about regulatory reporting and generate valid return data.")

# Input Query
query = st.text_area(
    "Describe your reporting scenario:",
    value="How should a UK bank report its Common Equity Tier 1 capital under PRA COREP Own Funds?",
    height=100
)

if st.button("Generate Report", type="primary"):
    with st.spinner("🔍 Analysing regulations and generating data..."):
        try:
            # Run Pipeline
            output: CorepOutput = pipeline.run(query)
            
            # Key Metrics Row
            st.markdown("### 📊 Key Capital Figures")
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.metric("CET1 Capital", f"£{output.own_funds.common_equity_tier_1:,.2f}m")
            with c2:
                st.metric("AT1 Capital", f"£{output.own_funds.additional_tier_1:,.2f}m")
            with c3:
                st.metric("Tier 2 Capital", f"£{output.own_funds.tier_2:,.2f}m")
            with c4:
                st.metric("Total Own Funds", f"£{output.own_funds.total_own_funds:,.2f}m")
            
            st.markdown("---")
            
            # Tabs for detailed view
            tab1, tab2, tab3 = st.tabs(["📝 Audit Log", "⚠️ Validations", "🔍 Raw Data"])
            
            with tab1:
                st.subheader("Decision Audit Log")
                
                audit_data = []
                for log in output.audit_log:
                    audit_data.append({
                        "Field": log.field,
                        "Value": log.value,
                        "Explanation": log.explanation,
                        "Rules": ", ".join(log.rule_ids)
                    })
                
                df_audit = pd.DataFrame(audit_data)
                st.dataframe(
                    df_audit, 
                    use_container_width=True,
                    column_config={
                        "Explanation": st.column_config.TextColumn("Reasoning", width="large"),
                        "Value": st.column_config.NumberColumn("Value (£m)")
                    }
                )
            
            with tab2:
                st.subheader("Validation Warnings")
                if output.warnings:
                    for warning in output.warnings:
                        st.warning(f"⚠️ {warning}")
                else:
                    st.success("✅ No validation warnings found. Data is compliant.")
            
            with tab3:
                st.subheader("JSON Structure")
                st.json(output.model_dump())
                
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
