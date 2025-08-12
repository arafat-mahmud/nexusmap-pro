import os
from dotenv import load_dotenv
from linkedin_api import Linkedin
import networkx as nx
import requests
import json

load_dotenv()

class NetworkBuilder:
    def __init__(self):
        self.graph = nx.Graph()
        
    def from_linkedin_official(self):
        """
        Safe LinkedIn integration using official API
        Requires LinkedIn Developer App setup
        """
        access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        if not access_token:
            print("⚠️ LinkedIn access token not found. Please set up LinkedIn Developer App first.")
            return self._create_sample_linkedin_network()
        
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            # Get user profile
            profile_response = requests.get(
                'https://api.linkedin.com/v2/people/~', 
                headers=headers
            )
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                user_name = f"{profile.get('localizedFirstName', 'You')} {profile.get('localizedLastName', '')}"
                
                self.graph.add_node(user_name, 
                                  size=25, 
                                  title="LinkedIn Professional", 
                                  group="Central")
                
                # Note: LinkedIn API v2 has limited connection access
                # This is a demo implementation
                return self.graph
            else:
                print("⚠️ LinkedIn API access failed. Using sample data.")
                return self._create_sample_linkedin_network()
                
        except Exception as e:
            print(f"⚠️ LinkedIn API error: {e}. Using sample data.")
            return self._create_sample_linkedin_network()
    
    def from_linkedin_unsafe(self):
        """
        UNSAFE: Using email/password (NOT RECOMMENDED)
        This method is kept for educational purposes only
        LinkedIn will likely ban your account for this!
        """
        print("⚠️ WARNING: Using email/password method is NOT SAFE!")
        print("⚠️ LinkedIn may ban your account!")
        print("⚠️ Use from_linkedin_official() instead!")
        
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')
        
        if not email or not password or email == "your@email.com":
            print("⚠️ LinkedIn credentials not provided. Using sample data.")
            return self._create_sample_linkedin_network()
        
        try:
            api = Linkedin(email, password)
            profile = api.get_profile()
            
            self.graph.add_node("You", 
                              size=25, 
                              title=profile.get('headline', 'LinkedIn Professional'), 
                              group="Central")
            
            connections = api.get_connections()
            for conn in connections[:10]:  # Limit to avoid rate limits
                self.graph.add_node(conn.get('name', 'Unknown'), 
                                  size=10, 
                                  title=conn.get('headline', 'Professional'),
                                  group=conn.get('company', {}).get('name', 'Other'))
                self.graph.add_edge("You", conn.get('name', 'Unknown'))
            
            return self.graph
            
        except Exception as e:
            print(f"⚠️ LinkedIn login failed: {e}")
            return self._create_sample_linkedin_network()
    
    def _create_sample_linkedin_network(self):
        """
        Creates a sample LinkedIn-style network for demonstration
        """
        print("📊 Creating sample LinkedIn network...")
        
        self.graph.add_node("You", 
                          size=25, 
                          title="Data Scientist & Network Analyst", 
                          group="Central")
        
        # Sample connections with realistic LinkedIn data
        sample_connections = [
            {"name": "Sarah Johnson", "title": "Product Manager at Tech Corp", "company": "Tech Corp"},
            {"name": "Mike Chen", "title": "Software Engineer at StartupXYZ", "company": "StartupXYZ"},
            {"name": "Dr. Emily Davis", "title": "Data Science Lead at BigTech", "company": "BigTech"},
            {"name": "Alex Rodriguez", "title": "Marketing Director at MediaCo", "company": "MediaCo"},
            {"name": "Jennifer Liu", "title": "UX Designer at DesignStudio", "company": "DesignStudio"},
            {"name": "David Park", "title": "DevOps Engineer at CloudInc", "company": "CloudInc"},
            {"name": "Rachel Green", "title": "Business Analyst at FinanceGroup", "company": "FinanceGroup"},
            {"name": "Tom Wilson", "title": "CTO at Innovation Labs", "company": "Innovation Labs"}
        ]
        
        for conn in sample_connections:
            self.graph.add_node(conn["name"], 
                              size=10, 
                              title=conn["title"],
                              group=conn["company"])
            self.graph.add_edge("You", conn["name"])
        
        # Add some inter-connections
        self.graph.add_edge("Sarah Johnson", "Mike Chen")
        self.graph.add_edge("Dr. Emily Davis", "David Park")
        self.graph.add_edge("Alex Rodriguez", "Jennifer Liu")
        
        return self.graph
    
    def from_github(self, username):
        """
        Enhanced GitHub network analysis
        Gets followers, following, and collaborators
        """
        print(f"📊 Analyzing GitHub network for: {username}")
        
        headers = {}
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            headers['Authorization'] = f'token {github_token}'
            print("🔑 Using GitHub token for enhanced API access")
        
        try:
            # Get user info
            user_url = f"https://api.github.com/users/{username}"
            user_response = requests.get(user_url, headers=headers)
            user_data = user_response.json()
            
            self.graph.add_node(username, 
                              size=30, 
                              title=f"GitHub: {user_data.get('name', username)}\n{user_data.get('bio', 'Developer')}",
                              group="Central",
                              followers=user_data.get('followers', 0),
                              following=user_data.get('following', 0))
            
            # Get followers
            followers_url = f"https://api.github.com/users/{username}/followers"
            followers_response = requests.get(followers_url, headers=headers)
            
            if followers_response.status_code == 200:
                followers = followers_response.json()
                print(f"📈 Found {len(followers)} followers")
                
                for follower in followers[:20]:  # Limit to avoid API limits
                    self.graph.add_node(follower['login'], 
                                      size=8,
                                      title=f"GitHub: {follower['login']}\nFollower",
                                      group="Follower")
                    self.graph.add_edge(username, follower['login'], 
                                       relationship="follower")
            
            # Get following
            following_url = f"https://api.github.com/users/{username}/following"
            following_response = requests.get(following_url, headers=headers)
            
            if following_response.status_code == 200:
                following = following_response.json()
                print(f"👥 Found {len(following)} following")
                
                for followed in following[:20]:  # Limit to avoid API limits
                    if followed['login'] not in self.graph.nodes():
                        self.graph.add_node(followed['login'], 
                                          size=8,
                                          title=f"GitHub: {followed['login']}\nFollowing",
                                          group="Following")
                        self.graph.add_edge(username, followed['login'], 
                                           relationship="following")
            
            # Get repositories and collaborators
            repos_url = f"https://api.github.com/users/{username}/repos"
            repos_response = requests.get(repos_url, headers=headers)
            
            if repos_response.status_code == 200:
                repos = repos_response.json()
                print(f"📚 Analyzing {len(repos)} repositories")
                
                # Get collaborators from top repos
                for repo in repos[:5]:  # Top 5 repos
                    if repo['owner']['login'] == username:  # Only own repos
                        collab_url = f"https://api.github.com/repos/{username}/{repo['name']}/collaborators"
                        collab_response = requests.get(collab_url, headers=headers)
                        
                        if collab_response.status_code == 200:
                            collaborators = collab_response.json()
                            for collab in collaborators:
                                if collab['login'] != username:  # Exclude self
                                    if collab['login'] not in self.graph.nodes():
                                        self.graph.add_node(collab['login'], 
                                                          size=12,
                                                          title=f"GitHub: {collab['login']}\nCollaborator",
                                                          group="Collaborator")
                                    self.graph.add_edge(username, collab['login'], 
                                                       relationship="collaborator",
                                                       repo=repo['name'])
            
            print(f"✅ Network built: {len(self.graph.nodes())} nodes, {len(self.graph.edges())} connections")
            return self.graph
            
        except Exception as e:
            print(f"⚠️ GitHub API error: {e}")
            # Fallback to basic follower data
            return self._github_basic_fallback(username)
    
    def _github_basic_fallback(self, username):
        """Fallback method for basic GitHub data"""
        url = f"https://api.github.com/users/{username}/followers"
        response = requests.get(url)
        
        if response.status_code == 200:
            followers = response.json()
            
            self.graph.add_node(username, 
                              size=25, 
                              title=f"GitHub: {username}",
                              group="Central")
            
            for follower in followers[:10]:
                self.graph.add_node(follower['login'], 
                                  size=10,
                                  title=f"GitHub: {follower['login']}",
                                  group="Follower")
                self.graph.add_edge(username, follower['login'])
        
        return self.graph