import streamlit as st
from pipeline import run_research_pipeline


# Page Config
st.set_page_config(
    page_title="Multi Agent Research System",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 Multi-Agent Research Agent")
st.markdown(
    "Search → Read → Write → Critic"
)

# Input
topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Future of Generative AI"
)

# Run Button
if st.button("Generate Research"):

    if not topic.strip():
        st.warning("Please enter a topic")
        st.stop()

    with st.spinner("Running Multi-Agent Pipeline..."):

        try:
            result = run_research_pipeline(topic)

            st.success("Research Completed")

            # Search Results
            with st.expander(
                "🔎 Search Results",
                expanded=False
            ):
                st.write(result["search_results"])

            # Scraped Content
            with st.expander(
                "📄 Scraped Content",
                expanded=False
            ):
                st.write(result["scraped_content"])

            # Report
            st.subheader("📝 Final Report")
            st.markdown(result["report"])

            # Feedback
            st.subheader("🧠 Critic Feedback")
            st.markdown(result["feedback"])

            # Download
            st.download_button(
                label="⬇ Download Report",
                data=result["report"],
                file_name="research_report.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")