import streamlit as st
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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

def visualize_html_structure(structure):
    G = nx.DiGraph()
    for parent, children in structure.items():
        for child, count in children.items():
            G.add_edge(parent, child, weight=count)
    
    pos = nx.spring_layout(G, seed=42)  # Define the layout
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=5000, node_color='skyblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(plt)



# Render HTML structure as a tree graph
def render_tree_graph(structure, max_depth=3, max_children=10):
    graph = nx.DiGraph()
    root_node = '[document]'
    graph.add_node(root_node, label='[document]')
    q = deque([root_node])

    while q:
        parent_node = q.popleft()
        children = structure.get(parent_node, {})
        print("Parent Node:", parent_node)
        print("Children:", children)
        for child, count in children.items():
            child_node = f"{parent_node}-{child}"
            graph.add_node(child_node, label=f"{child} [{count}]")
            graph.add_edge(parent_node, child_node, label=f"{count}")
            q.append(child_node)

    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')
    nx.draw(graph, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=8)
    plt.title("HTML Structure Overview")
    st.pyplot(plt)
    
def render_node(graph, structure, parent_node='[document]', depth=0, max_depth=3, max_children=10):
    if depth > max_depth or parent_node not in structure:
        return
    children_count = sum(structure[parent_node].values())
    if children_count > max_children:
        graph.add_node(parent_node, label=f"{parent_node} [{children_count} children]")
    else:
        for child, count in structure[parent_node].items():
            if isinstance(child, str):  # Check if it's a tag name
                continue
            child_node = f"{parent_node}-{child}"
            graph.add_node(child_node, label=f"{child} [{count}]")
            graph.add_edge(parent_node, child_node, label=f"{count}")
            render_node(graph, structure, parent_node=child_node, depth=depth + 1, max_depth=max_depth, max_children=max_children)


def main():
    st.set_page_config(page_title="HTML Semantic Analyzer", layout="wide")
    st.title("HTML Semantic Analyzer")

    st.header("Controls")
    url = st.text_input("Webpage URL:")
    show_structure = st.checkbox("Show HTML Structure", value=True)
    max_depth = st.slider("Max Depth", min_value=1, max_value=10, value=3, step=1)
    max_children = st.slider("Max Children", min_value=1, max_value=100, value=10, step=1)

    if url:
        with st.spinner('Fetching and parsing HTML...'):
            html_content = fetch_html(url)
            
            if html_content:
                st.subheader("Extracted HTML Content")
                st.text_area("HTML Content", html_content, height=200, max_chars=None)

                try:
                    structure = extract_html_structure(html_content)

                    st.subheader("HTML Structure Overview")
                    if show_structure:
                        visualize_html_structure(structure)

                except Exception as e:
                    st.error(f"Error analyzing HTML: {e}")

if __name__ == "__main__":
    main()
