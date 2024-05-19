# Render HTML structure as a tree graph
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

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