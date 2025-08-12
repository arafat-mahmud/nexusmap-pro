import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import pandas as pd
import base64
import io
from PIL import Image
import json
import requdef analyze_github_user(username):
    """Analyze a GitHub user's network"""
    try:
        builder = NetworkBuilder()
        graph = builder.from_github(username)
        return graph, True, None
    except Exception as e:
        return None, False, str(e)

def analyze_linkedin_profile(profile_url):
    """Analyze a LinkedIn profile URL"""
    try:
        # Extract username from profile URL
        if "linkedin.com/in/" in profile_url:
            username = profile_url.split("linkedin.com/in/")[-1].strip("/").split("?")[0]
            
            # Try to get additional profile info if possible (optional enhancement)
            try:
                import requests
                from bs4 import BeautifulSoup
                
                # Note: This is a demonstration only - a real implementation would use LinkedIn's API
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                # Note: This is not actually making a real request - it's just simulating what could be done
                # with official LinkedIn API access
                profile_data = {
                    'username': username,
                    'display_name': username.replace(".", " ").replace("-", " ").replace("_", " ").title(),
                    'headline': 'Professional on LinkedIn',
                    'company': 'LinkedIn',
                }
                
            except Exception as e:
                # Fall back to just username information
                profile_data = {
                    'username': username,
                    'display_name': username.replace(".", " ").replace("-", " ").replace("_", " ").title(),
                }
            
            # Create a personalized demo with the username
            graph = create_personalized_linkedin_demo(username)
            return graph, True, profile_data
        else:
            return None, False, "Invalid LinkedIn profile URL"
    except Exception as e:
        return None, False, str(e)ort sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.network_builder import NetworkBuilder
from app.visualizer import Visualizer
from app.social_post_generator import SocialPostGenerator

# Page configuration
st.set_page_config(
    page_title="NexusMap Pro - Network Analyzer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

def create_interactive_network_plotly(graph):
    """Create an interactive network visualization using Plotly"""
    # Get positions using spring layout
    pos = nx.spring_layout(graph, k=3, iterations=50)
    
    # Extract node and edge information
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Node info
        node_info = graph.nodes[node]
        connection_type = node_info.get('connection_type', '')
        if connection_type:
            node_text.append(f"{node}<br>{node_info.get('title', 'Professional')}<br>Connection: {connection_type}")
        else:
            node_text.append(f"{node}<br>{node_info.get('title', 'Professional')}")
        
        # Color coding based on group
        group = node_info.get('group', 'Other')
        if group == 'Central':
            node_color.append('#FF6B6B')  # Red for central node
            node_size.append(25)
        elif group == 'Follower':
            node_color.append('#4ECDC4')  # Teal for followers
            node_size.append(15)
        elif group == 'Following':
            node_color.append('#45B7D1')  # Blue for following
            node_size.append(15)
        elif node_info.get('connection_type') == '2nd':
            node_color.append('#FFA500')  # Orange for 2nd degree connections
            node_size.append(10)
        else:
            # Get color based on industry for 1st degree connections
            industry = group
            industry_colors = {
                'Tech': '#4287f5',
                'Finance': '#41c871',
                'Healthcare': '#f54242',
                'Education': '#9941f5',
                'Consulting': '#f5a142',
                'Marketing': '#42f5e9',
                'Design': '#f542d4',
                'Engineering': '#42f578',
                'Sales': '#f5d742',
                'Human Resources': '#8c7ae6',
                'Product': '#c56cf0',
                'Research': '#3ae374',
                'Operations': '#32ff7e'
            }
            node_color.append(industry_colors.get(industry, '#7158e2'))  # Default purple if industry not found
            node_size.append(15)
        elif group == 'Collaborator':
            node_color.append('#96CEB4')
            node_size.append(20)
        else:
            node_color.append('#FECA57')
            node_size.append(12)
    
    # Create edges
    edge_x = []
    edge_y = []
    
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create the plot
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.8, color='#888'),
        hoverinfo='none',
        mode='lines'
    ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line=dict(width=1, color='#444')
        )
    ))
    
    # Add legend with markers for connection types
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=15, color='#FF6B6B'),
        name='You (Central)'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#4ECDC4'),
        name='Follower'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#45B7D1'),
        name='Following'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=8, color='#FFA500'),
        name='2nd Degree Connection'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#96CEB4'),
        name='Collaborator'
    ))
    
    # Add a few industry color examples to the legend
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#4287f5'),
        name='Tech Industry'
    ))
    
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#41c871'),
        name='Finance Industry'
    ))
    
    # Set layout
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        title="Your Professional Network Visualization",
        title_font_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[ dict(
            text="Interactive Network - Hover over nodes for details",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002 ) ],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white'
    )
    
    return fig

def analyze_github_user(username):
    """Analyze GitHub user network"""
    try:
        builder = NetworkBuilder()
        graph = builder.from_github(username)
        return graph, True, None
    except Exception as e:
        return None, False, str(e)

def create_linkedin_sample():
    """Create sample LinkedIn network"""
    builder = NetworkBuilder()
    graph = builder._create_sample_linkedin_network()
    return graph

def create_personalized_linkedin_demo(username):
    """Create a personalized LinkedIn demo based on username"""
    import random
    
    graph = nx.Graph()
    
    # Create personalized central node - handle URLs or usernames
    if "linkedin.com/in/" in username:
        # Extract just the username from URL
        username = username.split("linkedin.com/in/")[-1].strip("/").split("?")[0]
    
    # Clean up username for display
    display_name = username.replace(".", " ").replace("-", " ").replace("_", " ").title()
    
    # Add user as central node
    graph.add_node("You", 
                  size=30, 
                  title=f"{display_name}\nProfessional Network",
                  group="Central")
    
    # Create more realistic connections based on username
    industries = ["Tech", "Finance", "Healthcare", "Education", "Consulting", "Marketing", "Design", 
                 "Engineering", "Sales", "Human Resources", "Product", "Research", "Operations"]
    companies = ["TechCorp", "DataInc", "InnovateLabs", "FutureWorks", "SmartSolutions", "NextGen", 
                "ProAnalytics", "GlobalTech", "InnovateAI", "CloudSystems", "FinTech Solutions", 
                "HealthTech", "EduTech", "ConsultGroup"]
    
    # Generate connections that feel personalized but realistic
    random.seed(hash(username) % 1000)  # Consistent results for same username
    
    # Generate primary connections (direct connections)
    primary_connections = []
    num_primary = random.randint(15, 25)  # More realistic LinkedIn connection count
    
    first_names = ["Sarah", "Mike", "Emily", "Alex", "Jennifer", "David", "Rachel", "Tom", "Lisa", "Chris",
                  "Mohammed", "Aisha", "Wei", "Priya", "Carlos", "Sofia", "Jamal", "Elena", "Ahmed", "Zoe"]
    last_names = ["Johnson", "Chen", "Davis", "Rodriguez", "Liu", "Park", "Green", "Wilson", "Brown", "Taylor",
                 "Patel", "Nguyen", "Garcia", "Kim", "Singh", "Muller", "Williams", "Martinez", "Lee", "Khan"]
    
    for i in range(num_primary):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        company = random.choice(companies)
        industry = random.choice(industries)
        
        titles = [
            f"Senior {industry} Manager at {company}",
            f"Lead {industry} Analyst at {company}",
            f"{industry} Director at {company}",
            f"Principal {industry} Consultant at {company}",
            f"{industry} Product Manager at {company}",
            f"{industry} Specialist at {company}",
            f"Head of {industry} at {company}",
            f"{industry} Engineer at {company}",
            f"VP of {industry} at {company}"
        ]
        
        connection_type = "1st"
        if random.random() < 0.2:  # 20% chance of being a follower
            connection_type = "Follower"
        
        primary_connections.append({
            "name": name,
            "title": random.choice(titles),
            "company": company,
            "industry": industry,
            "type": connection_type
        })
    
    # Add primary connections to graph
    for conn in primary_connections:
        node_size = 12
        if conn["type"] == "Follower":
            group = "Follower"
        else:
            group = conn["industry"]
        
        graph.add_node(conn["name"], 
                      size=node_size, 
                      title=conn["title"],
                      group=group,
                      connection_type=conn["type"])
        
        graph.add_edge("You", conn["name"])
    
    # Add some 2nd-degree connections (connections of connections)
    secondary_connections = []
    num_secondary = random.randint(5, 10)
    
    for i in range(num_secondary):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        company = random.choice(companies)
        industry = random.choice(industries)
        
        titles = [
            f"Senior {industry} Manager at {company}",
            f"Lead {industry} Analyst at {company}",
            f"{industry} Director at {company}",
            f"Principal {industry} Consultant at {company}",
            f"{industry} Product Manager at {company}"
        ]
        
        # Connect to a random primary connection
        connected_to = random.choice(primary_connections)["name"]
        
        secondary_connections.append({
            "name": name,
            "title": random.choice(titles),
            "company": company,
            "industry": industry,
            "connected_to": connected_to
        })
    
    # Add secondary connections
    for conn in secondary_connections:
        graph.add_node(conn["name"], 
                      size=8,  # Smaller size for 2nd degree
                      title=conn["title"],
                      group=conn["industry"],
                      connection_type="2nd")
        
        graph.add_edge(conn["connected_to"], conn["name"])
    
    # Add inter-connections among primary connections for realism
    primary_names = [conn["name"] for conn in primary_connections]
    num_inter_connections = random.randint(num_primary // 3, num_primary // 2)
    
    for i in range(num_inter_connections):
        if len(primary_names) >= 2:
            conn1, conn2 = random.sample(primary_names, 2)
            if not graph.has_edge(conn1, conn2):
                graph.add_edge(conn1, conn2)
    
    return graph

def analyze_linkedin_profile(profile_url_or_username):
    """
    Analyze LinkedIn profile (currently creates realistic demo)
    In production, this would connect to LinkedIn API
    """
    try:
        # Extract username from URL or use directly
        if "linkedin.com/in/" in profile_url_or_username:
            username = profile_url_or_username.split("linkedin.com/in/")[-1].strip("/")
        else:
            username = profile_url_or_username
        
        # For now, create a realistic demo
        # In production, this would use LinkedIn API
        graph = create_personalized_linkedin_demo(username)
        return graph, True, None
        
    except Exception as e:
        return None, False, str(e)
    """Create a personalized LinkedIn demo based on username"""
    builder = NetworkBuilder()
    graph = nx.Graph()
    
    # Create personalized central node
    display_name = username.replace(".", " ").replace("-", " ").replace("_", " ").title()
    
    graph.add_node("You", 
                  size=30, 
                  title=f"{display_name}\nData Scientist & Network Analyst", 
                  group="Central")
    
    # Create personalized connections based on username
    industries = ["Tech", "Finance", "Healthcare", "Education", "Consulting", "Marketing", "Design"]
    companies = ["TechCorp", "DataInc", "InnovateLabs", "FutureWorks", "SmartSolutions", "NextGen", "ProAnalytics"]
    
    # Generate connections that feel personalized
    import random
    random.seed(hash(username) % 1000)  # Consistent results for same username
    
    connections = []
    for i in range(8, 15):  # Variable number of connections
        first_names = ["Sarah", "Mike", "Emily", "Alex", "Jennifer", "David", "Rachel", "Tom", "Lisa", "Chris"]
        last_names = ["Johnson", "Chen", "Davis", "Rodriguez", "Liu", "Park", "Green", "Wilson", "Brown", "Taylor"]
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        company = random.choice(companies)
        industry = random.choice(industries)
        
        titles = [
            f"Senior {industry} Manager at {company}",
            f"Lead {industry} Analyst at {company}",
            f"{industry} Director at {company}",
            f"Principal {industry} Consultant at {company}",
            f"{industry} Product Manager at {company}"
        ]
        
        connections.append({
            "name": name,
            "title": random.choice(titles),
            "company": company,
            "industry": industry
        })
    
    # Add connections to graph
    for conn in connections:
        graph.add_node(conn["name"], 
                      size=12, 
                      title=conn["title"],
                      group=conn["industry"])
        graph.add_edge("You", conn["name"])
    
    # Add some inter-connections for realism
    connection_names = [conn["name"] for conn in connections]
    for i in range(2, 4):  # Add 2-3 inter-connections
        if len(connection_names) >= 2:
            conn1, conn2 = random.sample(connection_names, 2)
            graph.add_edge(conn1, conn2)
    
    return graph

def display_network_stats(stats):
    """Display network statistics in a nice format"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔗 Connections</h3>
            <h2>{}</h2>
        </div>
        """.format(stats['total_connections']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 Clusters</h3>
            <h2>{}</h2>
        </div>
        """.format(stats['clusters']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Density</h3>
            <h2>{:.2f}</h2>
        </div>
        """.format(stats['density']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Centrality</h3>
            <h2>{:.2f}</h2>
        </div>
        """.format(stats['centrality']), unsafe_allow_html=True)

def create_stats_charts(stats, graph):
    """Create additional charts for network analysis"""
    
    # Group composition chart
    if 'groups' in stats and stats['groups']:
        groups_df = pd.DataFrame(list(stats['groups'].items()), columns=['Group', 'Count'])
        groups_df = groups_df[groups_df['Group'] != 'Central']  # Exclude central node
        
        if not groups_df.empty:
            fig_pie = px.pie(groups_df, values='Count', names='Group', 
                            title="Network Composition by Group")
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Relationship types chart
    if 'relationships' in stats and stats['relationships']:
        rel_df = pd.DataFrame(list(stats['relationships'].items()), columns=['Relationship', 'Count'])
        fig_bar = px.bar(rel_df, x='Relationship', y='Count', 
                        title="Connection Types Distribution")
        st.plotly_chart(fig_bar, use_container_width=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌐 NexusMap Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Decode Your Professional Network with Data Science</p>', unsafe_allow_html=True)
    
    # Sidebar for input
    st.sidebar.header("🔍 Network Analysis")
    
    # Network source selection
    network_source = st.sidebar.selectbox(
        "Choose your network source:",
        ["GitHub", "LinkedIn", "LinkedIn Demo", "Sample Analysis"]
    )
    
    # Initialize session state
    if 'graph' not in st.session_state:
        st.session_state.graph = None
    if 'stats' not in st.session_state:
        st.session_state.stats = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Input based on source
    if network_source == "GitHub":
        st.sidebar.markdown("### GitHub Analysis")
        username = st.sidebar.text_input("Enter GitHub Username:", placeholder="e.g., octocat")
        
        if st.sidebar.button("🚀 Analyze Network", type="primary"):
            if username:
                with st.spinner("🔍 Analyzing your GitHub network..."):
                    graph, success, error = analyze_github_user(username)
                    
                    if success and graph:
                        st.session_state.graph = graph
                        st.session_state.stats = SocialPostGenerator.generate_stats(graph)
                        st.session_state.analysis_complete = True
                        st.success(f"✅ Successfully analyzed {username}'s network!")
                    else:
                        st.error(f"❌ Error analyzing network: {error}")
            else:
                st.warning("⚠️ Please enter a GitHub username")
    
    elif network_source == "LinkedIn":
        st.sidebar.markdown("### LinkedIn Analysis")
        st.sidebar.info("🔗 Enter your LinkedIn profile URL or email to analyze your professional network.")
        
        # LinkedIn input options
        linkedin_input_type = st.sidebar.radio(
            "Choose input method:",
            ["Profile URL", "Email (Demo Mode)"]
        )
        
        if linkedin_input_type == "Profile URL":
            linkedin_url = st.sidebar.text_input(
                "LinkedIn Profile URL:", 
                placeholder="https://linkedin.com/in/yourname"
            )
            
            if st.sidebar.button("🔗 Analyze LinkedIn Network", type="primary"):
                if linkedin_url:
                    # Process LinkedIn URL
                    if "linkedin.com/in/" in linkedin_url:
                        with st.spinner("🔍 Analyzing your LinkedIn network..."):
                            graph, success, profile_data = analyze_linkedin_profile(linkedin_url)
                            
                            if success and graph:
                                st.session_state.graph = graph
                                st.session_state.stats = SocialPostGenerator.generate_stats(graph)
                                st.session_state.analysis_complete = True
                                
                                # Display success with profile name
                                if isinstance(profile_data, dict) and 'display_name' in profile_data:
                                    display_name = profile_data['display_name']
                                else:
                                    # Extract username for display
                                    username = linkedin_url.split("linkedin.com/in/")[-1].strip("/").split("?")[0]
                                    display_name = username.replace(".", " ").replace("-", " ").replace("_", " ").title()
                                
                                st.success(f"✅ Successfully analyzed {display_name}'s LinkedIn network!")
                                st.info("📝 Note: This is a realistic demo visualization based on your profile URL. For full LinkedIn data access, official API integration is required.")
                            else:
                                error_msg = profile_data if isinstance(profile_data, str) else "Unknown error"
                                st.error(f"❌ Error analyzing LinkedIn profile: {error_msg}")
                    else:
                        st.error("❌ Please enter a valid LinkedIn profile URL that includes 'linkedin.com/in/'")
                else:
                    st.warning("⚠️ Please enter your LinkedIn profile URL")
        
        else:  # Email Demo Mode
            linkedin_email = st.sidebar.text_input(
                "LinkedIn Email (Demo):", 
                placeholder="your.email@example.com"
            )
            
            if st.sidebar.button("🎭 Generate LinkedIn Demo", type="primary"):
                if linkedin_email:
                    with st.spinner("🎨 Creating personalized LinkedIn demo..."):
                        # Create personalized demo based on email
                        username = linkedin_email.split("@")[0]
                        graph = create_personalized_linkedin_demo(username)
                        st.session_state.graph = graph
                        st.session_state.stats = SocialPostGenerator.generate_stats(graph)
                        st.session_state.analysis_complete = True
                        st.success("✅ Personalized LinkedIn demo created!")
                        st.info("📝 This is a realistic demo showing what your actual LinkedIn analysis would look like.")
                else:
                    st.warning("⚠️ Please enter an email address")
    
    elif network_source == "LinkedIn Demo":
        st.sidebar.markdown("### LinkedIn Demo")
        st.sidebar.info("This creates a realistic LinkedIn-style network for demonstration.")
        
        if st.sidebar.button("🎭 Generate Demo Network", type="primary"):
            with st.spinner("🎨 Creating LinkedIn demo network..."):
                graph = create_linkedin_sample()
                st.session_state.graph = graph
                st.session_state.stats = SocialPostGenerator.generate_stats(graph)
                st.session_state.analysis_complete = True
                st.success("✅ Demo network created!")
    
    else:  # Sample Analysis
        st.sidebar.markdown("### Sample Analysis")
        st.sidebar.info("View a pre-built network analysis example.")
        
        if st.sidebar.button("📊 Load Sample", type="primary"):
            with st.spinner("📈 Loading sample analysis..."):
                graph = create_linkedin_sample()
                st.session_state.graph = graph
                st.session_state.stats = SocialPostGenerator.generate_stats(graph)
                st.session_state.analysis_complete = True
                st.success("✅ Sample loaded!")
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.graph:
        
        # Network Statistics
        st.header("📊 Network Analysis Results")
        display_network_stats(st.session_state.stats)
        
        # Two columns for visualization and insights
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🌐 Interactive Network Visualization")
            fig = create_interactive_network_plotly(st.session_state.graph)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💡 Key Insights")
            
            density = st.session_state.stats['density']
            centrality = st.session_state.stats['centrality']
            
            if density > 0.3:
                density_insight = "highly connected"
                density_desc = "Your network shows strong clustering and tight-knit connections."
            else:
                density_insight = "diverse and spread out"
                density_desc = "Your network spans across diverse groups and industries."
            
            if centrality > 0.8:
                centrality_insight = "central hub"
                centrality_desc = "You're at the center of your network with high influence."
            else:
                centrality_insight = "well-connected node"
                centrality_desc = "You have good connections but share influence with others."
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>🎯 Network Position</h4>
                <p>You're a <strong>{centrality_insight}</strong> in your network.</p>
                <p>{centrality_desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>🌐 Network Structure</h4>
                <p>Your network is <strong>{density_insight}</strong>.</p>
                <p>{density_desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional Charts
        st.header("📈 Detailed Analysis")
        create_stats_charts(st.session_state.stats, st.session_state.graph)
        
        # LinkedIn Post Generation
        st.header("🔥 LinkedIn Post Generator")
        
        post = SocialPostGenerator.generate_post(st.session_state.stats)
        
        st.markdown("""
        <div class="success-box">
            <h4>📝 Your LinkedIn-Ready Post:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("LinkedIn Post Copy:", value=post, height=300)
        
        # Download buttons
        st.header("📁 Download Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Download Network Data"):
                # Create downloadable network data
                nodes_data = []
                for node, data in st.session_state.graph.nodes(data=True):
                    nodes_data.append({
                        'node': node,
                        'group': data.get('group', 'Unknown'),
                        'title': data.get('title', ''),
                        'size': data.get('size', 10)
                    })
                
                df = pd.DataFrame(nodes_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="network_data.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Download Statistics"):
                stats_json = json.dumps(st.session_state.stats, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=stats_json,
                    file_name="network_stats.json",
                    mime="application/json"
                )
        
        with col3:
            st.info("💡 Tip: Save the visualization by right-clicking and selecting 'Save as PNG'")
    
    else:
        # Welcome message
        st.markdown("""
        ## 🚀 Welcome to NexusMap Pro!
        
        **Decode your professional network with the power of data science.**
        
        ### 🎯 What you can do:
        - 📊 **Analyze GitHub Networks** - See your followers, following, and collaborators
        - 🔗 **Analyze LinkedIn Profiles** - Enter your LinkedIn URL or email for personalized analysis
        - 🎭 **Try LinkedIn Demo** - Experience realistic professional network analysis
        - 📈 **Get Insights** - Understand your network position and influence
        - 🔥 **Generate Posts** - Create LinkedIn-ready content about your network
        
        ### 🔍 How it works:
        1. Choose your network source from the sidebar
        2. Enter your username, LinkedIn URL, or email
        3. Get instant network analysis and visualizations
        4. Share your insights on LinkedIn!
        
        **Get started by selecting an option from the sidebar! →**
        """)
        
        # Feature showcase
        st.header("✨ Features")
        
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            ### 🌐 Interactive Visualizations
            - Explore your network interactively
            - Hover for detailed information
            - Beautiful, professional charts
            """)
        
        with feature_col2:
            st.markdown("""
            ### 📊 Deep Analytics
            - Network density analysis
            - Centrality measurements
            - Connection type breakdown
            """)
        
        with feature_col3:
            st.markdown("""
            ### 🔥 Social Ready
            - Auto-generated LinkedIn posts
            - Professional insights
            - Downloadable results
            """)

if __name__ == "__main__":
    main()
