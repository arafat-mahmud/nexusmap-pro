import networkx as nx

class SocialPostGenerator:
    @staticmethod
    def generate_stats(graph):
        # Find the central node (the one with the highest degree)
        degrees = dict(graph.degree())
        central_node = max(degrees, key=degrees.get)
        
        centrality_scores = nx.degree_centrality(graph)
        
        # Analyze network composition
        groups = {}
        for node, data in graph.nodes(data=True):
            group = data.get('group', 'Unknown')
            groups[group] = groups.get(group, 0) + 1
        
        # Get relationship types if available
        relationships = {}
        for u, v, data in graph.edges(data=True):
            rel_type = data.get('relationship', 'connection')
            relationships[rel_type] = relationships.get(rel_type, 0) + 1
        
        stats = {
            'total_connections': len(graph.nodes()) - 1,
            'clusters': nx.number_connected_components(graph),
            'density': nx.density(graph),
            'centrality': centrality_scores[central_node],
            'central_node': central_node,
            'groups': groups,
            'relationships': relationships,
            'total_relationships': len(graph.edges())
        }
        return stats
    
    @staticmethod
    def generate_post(stats):
        # Create more engaging content with better storytelling
        density_insight = "highly connected" if stats['density'] > 0.3 else "diverse and spread out"
        centrality_insight = "central hub" if stats['centrality'] > 0.8 else "well-connected node"
        
        # Analyze network composition
        top_groups = sorted(stats['groups'].items(), key=lambda x: x[1], reverse=True)[:3]
        group_breakdown = ", ".join([f"{count} {group.lower()}" for group, count in top_groups if group != "Central"])
        
        # Relationship insights
        rel_breakdown = ""
        if 'relationships' in stats and stats['relationships']:
            top_rels = sorted(stats['relationships'].items(), key=lambda x: x[1], reverse=True)[:2]
            rel_breakdown = f"\n🤝 Connection types: {', '.join([f'{count} {rel}s' for rel, count in top_rels])}"
        
        return f"""
🚀 I just decoded my professional network and the results are fascinating! 

📊 THE BREAKDOWN:
🔗 {stats['total_connections']} professional connections
🌐 {stats['clusters']} distinct network cluster{'s' if stats['clusters'] != 1 else ''}
📈 Network density: {stats['density']:.2f} ({density_insight})
🎯 My position: {stats['centrality']:.2f} centrality ({centrality_insight}){rel_breakdown}
👥 Network composition: {group_breakdown if group_breakdown else "diverse professional mix"}

💡 KEY INSIGHT: My network is {density_insight}, showing {'strong industry focus' if stats['density'] > 0.3 else 'diverse cross-industry reach'}!

🛠️ Built with #NexusMapPro - a data visualization tool I created to decode professional networks.

What patterns would YOUR network reveal? 🤔

#DataVisualization #NetworkAnalysis #CareerGrowth #DataScience #LinkedIn #ProfessionalNetworking #TechCommunity #GitHub

---
🔥 Want to map your own network? Drop a comment and I'll share the code!
"""