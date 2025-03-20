import streamlit as st
from web_scraper import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# Set page config
st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🕸️",
    layout="wide",
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("🕸️ AI Web Scraper")
st.subheader("Extract specific information from any website using AI")

# Input section
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input("Enter Website URL", placeholder="https://example.com")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        scrape_button = st.button("🔍 Scrape Website", use_container_width=True)

# Progress tracker
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# Step 1: Scrape the Website
if scrape_button and url:
    st.session_state.current_step = 1
    
    with st.spinner("Scraping the website..."):
        # Scrape the website
        try:
            dom_content = scrape_website(url)
            
            if dom_content.startswith("Error"):
                st.error(dom_content)
            else:
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)
                
                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content
                st.session_state.url = url
                
                # Display success message
                st.success(f"Successfully scraped {url}")
                
                # Display the DOM content in an expandable text box
                with st.expander("View Extracted Content"):
                    st.text_area("Website Content", cleaned_content, height=300)
                
                # Update progress
                st.session_state.current_step = 2
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Step 2: Ask Questions About the DOM Content
if st.session_state.current_step >= 2:
    st.markdown("---")
    st.subheader("📝 Extract Information")
    
    # Check if we have content to parse
    if "dom_content" in st.session_state:
        parse_description = st.text_area(
            "Describe what information you want to extract",
            placeholder="Examples:\n- Extract all product prices and names\n- Find contact information\n- Summarize the main content\n- List all article headings",
            height=100
        )
        
        parse_button = st.button("🤖 Extract Information", use_container_width=True)
        
        if parse_button:
            if parse_description:
                with st.spinner("Analyzing the content..."):
                    try:
                        # Parse the content
                        dom_chunks = split_dom_content(st.session_state.dom_content)
                        parsed_result = parse_with_ollama(dom_chunks, parse_description)
                        
                        # Check if there's an error message
                        if parsed_result.startswith("Error parsing content:"):
                            st.error(parsed_result)
                        else:
                            # Display the results
                            st.markdown("### Results")
                            st.markdown(parsed_result)
                            
                            # Provide download option
                            st.download_button(
                                label="Download Results",
                                data=parsed_result,
                                file_name="extracted_data.txt",
                                mime="text/plain"
                            )
                    except Exception as e:
                        st.error(f"An error occurred during parsing: {str(e)}")
            else:
                st.warning("Please describe what information you want to extract.")

# Add footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>AI Web Scraper | Built with Streamlit and Ollama</p>
</div>
""", unsafe_allow_html=True)