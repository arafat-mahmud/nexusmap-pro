import networkx as nx

class SocialPostGenerator:
    @staticmethod
    def generate_stats(graph):
        # Find the central node (the one with the highest degree)
        degrees = dict(graph.degree())
        central_node = max(degrees, key=degrees.get)
        
        centrality_scores = nx.degree_centrality(graph)
        
        stats = {
            'total_connections': len(graph.nodes()) - 1,
            'clusters': nx.number_connected_components(graph),
            'density': nx.density(graph),
            'centrality': centrality_scores[central_node],
            'central_node': central_node
        }
        return stats
    
    @staticmethod
    def generate_post(stats):
        # Create more engaging content with better storytelling
        density_insight = "highly connected" if stats['density'] > 0.3 else "diverse and spread out"
        centrality_insight = "central hub" if stats['centrality'] > 0.8 else "well-connected node"
        
        return f"""
🚀 I just decoded my professional network and the results are fascinating! 

📊 THE BREAKDOWN:
🔗 {stats['total_connections']} professional connections
🌐 {stats['clusters']} distinct network cluster{'s' if stats['clusters'] != 1 else ''}
� Network density: {stats['density']:.2f} ({density_insight})
🎯 My position: {stats['centrality']:.2f} centrality ({centrality_insight})

💡 KEY INSIGHT: My network is {density_insight}, showing {'strong industry focus' if stats['density'] > 0.3 else 'diverse cross-industry reach'}!

🛠️ Built with #NexusMapPro - a data visualization tool I created to decode professional networks.

What would YOUR network reveal? 🤔

#DataVisualization #NetworkAnalysis #CareerGrowth #DataScience #LinkedIn #ProfessionalNetworking #TechCommunity

---
🔥 Want to map your own network? Drop a comment and I'll share the code!
"""