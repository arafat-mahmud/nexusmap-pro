from app.network_builder import NetworkBuilder
from app.visualizer import Visualizer
from app.social_post_generator import SocialPostGenerator


def main():
    print("🛠️ Building your professional network...")

    builder = NetworkBuilder()
    # Use your GitHub username
    graph = builder.from_github("sidra3921")  # Changed to your username

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
