from pathlib import Path
from typing import List
from ..models import AnalysisResult

def generate_graph(results: List[AnalysisResult], output_path: Path):
    # Find dependencies analyzer result
    graph_data = None
    for res in results:
        if res.analyzer_name == "dependencies":
            graph_data = res.details.get("nx_graph")
            break
            
    if not graph_data:
        raise ValueError("Dependencies analysis result not found or graph missing.")
        
    try:
        import graphviz
    except ImportError:
        raise ImportError("graphviz python package is required for graph generation (pip install graphviz)")

    dot = graphviz.Digraph(comment="Architecture Dependency Graph", format="svg")
    dot.attr(rankdir='LR', size='8,5')
    
    dot.attr('node', shape='box', style='filled', color='lightblue2', fontname='Helvetica')
    dot.attr('edge', color='gray50')

    # Add nodes and edges
    for node in graph_data.nodes():
        dot.node(node, node)
        
    for edge in graph_data.edges():
        dot.edge(edge[0], edge[1])

    # Save to file
    # render outputs to {output_path}.svg or similar depending on the extensions,
    # so we give it the stem.
    stem = output_path.with_suffix('')
    dot.render(str(stem), cleanup=True)
