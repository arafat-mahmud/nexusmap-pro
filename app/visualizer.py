from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx

class Visualizer:
    @staticmethod
    def create_interactive(graph, filename="output/network.html"):
        net = Network(height="800px", 
                     width="100%",
                     bgcolor="#0E1117",
                     font_color="white")
        
        net.from_nx(graph)
        net.save_graph(filename)
        return filename
    
    @staticmethod
    def create_static(graph, filename="output/network.png"):
        # Create a more LinkedIn-worthy visualization
        plt.figure(figsize=(12, 8), facecolor='white')
        plt.subplots_adjust(top=0.85)
        
        pos = nx.spring_layout(graph, k=3, iterations=50)
        
        # Get node sizes based on degree (more connections = bigger node)
        degrees = dict(graph.degree())
        node_sizes = [degrees[node] * 300 + 200 for node in graph.nodes()]
        
        # Create color map based on node groups
        node_colors = []
        for node in graph.nodes():
            if graph.nodes[node].get('group') == 'Central':
                node_colors.append('#FF6B6B')  # Red for central
            else:
                node_colors.append('#4ECDC4')  # Teal for others
        
        # Draw the network
        nx.draw_networkx_nodes(graph, pos, 
                              node_color=node_colors,
                              node_size=node_sizes,
                              alpha=0.8,
                              edgecolors='black',
                              linewidths=1)
        
        nx.draw_networkx_edges(graph, pos,
                              edge_color='#666666',
                              alpha=0.6,
                              width=2)
        
        nx.draw_networkx_labels(graph, pos,
                               font_size=8,
                               font_weight='bold',
                               font_color='black')
        
        # Add title and stats
        total_nodes = len(graph.nodes())
        total_edges = len(graph.edges())
        density = nx.density(graph)
        
        plt.title('🚀 My Professional Network Analysis - NexusMapPro\n' + 
                 f'📊 {total_nodes} connections • {total_edges} relationships • {density:.2f} density',
                 fontsize=16, fontweight='bold', pad=20)
        
        # Add branding
        plt.figtext(0.99, 0.01, '#NexusMapPro #DataVisualization #NetworkAnalysis', 
                   ha='right', va='bottom', fontsize=10, style='italic', color='#666')
        
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor='white')
        plt.close()
        return filename