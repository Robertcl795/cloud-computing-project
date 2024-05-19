import streamlit as st
import requests
from bs4 import BeautifulSoup

# Fetch HTML
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        return html_content
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

# Extract HTML structure
def extract_html_structure(html_content):
    if html_content is None:
        st.error("HTML content is empty.")
        return {}

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        st.error(f"Error parsing HTML: {e}")
        return {}

    structure = {'[document]': {}}  # Initialize with root node
    
    # Function to recursively extract structure
    def extract_structure_recursive(tag, parent):
        nonlocal structure
        if hasattr(tag, 'children'):
            tag_name = tag.name
            if parent not in structure:
                structure[parent] = {}
            if tag_name not in structure[parent]:
                structure[parent][tag_name] = 1
            else:
                structure[parent][tag_name] += 1
            for child in tag.children:
                if hasattr(child, 'name'):
                    extract_structure_recursive(child, tag_name)
    
    # Start extraction from the root HTML tag
    extract_structure_recursive(soup.html, '[document]')
    
    st.write("HTML structure:", structure)
    return structure