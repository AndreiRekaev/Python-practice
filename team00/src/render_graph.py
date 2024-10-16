import argparse
import json
import matplotlib.pyplot as plt
import networkx as nx
import logging

from bokeh.plotting import figure, show, output_file, save, from_networkx
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool

logging.basicConfig(level=logging.INFO, format="%(message)s")

def load_graph(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return nx.readwrite.json_graph.node_link_graph(data)


def render_png(graph, output_path):
    plt.figure(figsize=(120, 120))
    in_degree = dict(graph.degree())
    node_size = [v*20 for v in in_degree.values()]

    pos = nx.spring_layout(graph, k=0.15, iterations=20)
    nx.draw(graph, pos, with_labels=False, node_size=node_size, node_color='skyblue', edge_color='gray', alpha=0.7)
    plt.savefig(output_path, format="PNG")
    plt.close()


def render_html(graph, output_path):
    pos = nx.spring_layout(graph, k=0.15, iterations=20)
    
    plot = figure(title="Interactive Graph Visualization", x_range=Range1d(-2, 2), y_range=Range1d(-2, 2))
    
    graph_renderer = from_networkx(graph, pos, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(radius=0.01, fill_color="skyblue")
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.5, line_width=1)

    hover_tool = HoverTool(tooltips=[("Node", "@index")])
    plot.add_tools(hover_tool)

    plot.renderers.append(graph_renderer)

    output_file(output_path)
    save(plot)



def main():
    parser = argparse.ArgumentParser(description="Render a Wikipedia page graph.")
    parser.add_argument('-f', '--format', choices=['png', 'html', 'both'], default='png', help="Output format: png, html, or both")
    args = parser.parse_args()

    graph = load_graph('wiki.json')
    if args.format in ['png', 'both']:
        render_png(graph, "wiki_graph.png")
        logging.info("PNG file is ready")
    if args.format in ['html', 'both']:
        render_html(graph, "wiki_graph.html")
        logging.info("HTML file is ready")
    

if __name__ == "__main__":
    main()