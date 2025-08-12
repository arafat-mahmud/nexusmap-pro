from app.network_builder import NetworkBuilder
from app.visualizer import Visualizer
from app.social_post_generator import SocialPostGenerator


def main():
    print("🛠️ Building your professional network...")
    print("📊 Choose your network source:")
    print("1. GitHub (Safe & Comprehensive)")
    print("2. LinkedIn Sample (Demo)")
    print("3. LinkedIn Official API (Requires setup)")

    builder = NetworkBuilder()

    # Configuration - change this to switch between sources
    network_source = (
        "github"  # Options: "github", "linkedin_sample", "linkedin_official"
    )
    username = "arafat-mahmud"  # Your GitHub username

    if network_source == "github":
        print(f"🔍 Analyzing GitHub network for: {username}")
        graph = builder.from_github(username)
    elif network_source == "linkedin_sample":
        print("📊 Creating LinkedIn-style sample network...")
        graph = builder._create_sample_linkedin_network()
    elif network_source == "linkedin_official":
        print("🔗 Connecting to LinkedIn Official API...")
        graph = builder.from_linkedin_official()
    else:
        print("⚠️ Unknown source, using GitHub...")
        graph = builder.from_github(username)

    print("🎨 Generating visualizations...")
    html_file = Visualizer.create_interactive(graph)
    png_file = Visualizer.create_static(graph)

    print("📊 Analyzing network...")
    stats = SocialPostGenerator.generate_stats(graph)
    post = SocialPostGenerator.generate_post(stats)

    print("\n🔥 YOUR LINKEDIN POST COPY 🔥")
    print(post)
    print(f"\n📁 Files saved to: {html_file} and {png_file}")


if __name__ == "__main__":
    main()
