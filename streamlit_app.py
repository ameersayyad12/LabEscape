# streamlit_app.py

import streamlit as st
from get_papers.fetch import fetch_and_process_papers

st.set_page_config(
    page_title="LabEscape – Real-World PubMed Research",
    page_icon="🧪",
    layout="wide"
)

# Zoom the entire page by 1.2x (like browser zoom)
st.markdown("""
    <style>
        .main {
            transform: scale(1.2);
            transform-origin: top left;
        }
    </style>
""", unsafe_allow_html=True)



# ✅ Dark-safe branding with better spacing and emojis
st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-size: 48px;">🧪 <span style="color:#2b90d9;">LabEscape</span></h1>
        <h4 style="color: #aaa; margin-top: -20px;">Escape the academic bubble — find real-world research</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# 🔍 Search box
st.markdown("### 🔎 Enter a PubMed Search Query")
query = st.text_input("", "cancer drug resistance", label_visibility="collapsed")
debug = st.checkbox("Show debug output")

st.markdown("---")

if st.button("🚀 Find Non-Academic Papers"):
    with st.spinner("🔄 Fetching from PubMed..."):
        try:
            df = fetch_and_process_papers(query, debug=debug)

            if df is None or df.empty:
                st.warning("⚠️ No non-academic authors found. Try a different query.")
            else:
                st.success(f"✅ {len(df)} paper(s) found with industry-affiliated authors.")
                st.markdown("### 📄 Filtered Results")
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    "filtered_papers.csv",
                    "text/csv",
                    help="Download filtered results"
                )
        except Exception as e:
            st.error(f"❌ Error: {e}")

# 📘 About section (safe and clean)
st.markdown("---")
with st.expander("ℹ️ About LabEscape"):
    st.markdown("""
    **LabEscape** helps you surface PubMed papers with authors from **non-academic institutions** like:
    - Biotech & Pharma companies
    - Clinical research orgs
    - Independent R&D labs

    🧠 Ideal for:
    - Competitive intelligence
    - Trend analysis
    - Biotech due diligence

    **How it works:**
    - Queries PubMed using E-utilities API
    - Parses affiliations from XML
    - Filters out academic institutions using heuristics

    💡 Built with Python, Streamlit, Typer, and Pandas
    """)
