import os
from dotenv import load_dotenv
from linkedin_api import Linkedin
import networkx as nx
import requests

load_dotenv()

class NetworkBuilder:
    def __init__(self):
        self.graph = nx.Graph()
        
    def from_linkedin(self):
        api = Linkedin(os.getenv('LINKEDIN_EMAIL'), os.getenv('LINKEDIN_PASSWORD'))
        profile = api.get_profile()
        
        self.graph.add_node("You", 
                          size=25, 
                          title=profile['headline'], 
                          image=profile['displayPictureUrl'])
        
        connections = api.get_connections()
        for conn in connections:
            self.graph.add_node(conn['name'], 
                              size=10, 
                              title=conn['headline'],
                              group=conn['company']['name'] if 'company' in conn else 'Other')
            self.graph.add_edge("You", conn['name'], 
                               value=conn['connectionStrength'] if 'connectionStrength' in conn else 1)
        return self.graph
    
    def from_github(self, username):
        url = f"https://api.github.com/users/{username}/followers"
        response = requests.get(url).json()
        
        self.graph.add_node(username, 
                          size=25, 
                          title=f"GitHub: {username}",
                          group="Central")
        
        for follower in response:
            self.graph.add_node(follower['login'], 
                              size=10,
                              title=f"GitHub: {follower['login']}",
                              group="Follower")
            self.graph.add_edge(username, follower['login'])
        return self.graph