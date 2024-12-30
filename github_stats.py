import os
import subprocess
from datetime import datetime
from collections import Counter
from PIL import Image, ImageDraw, ImageFont


ROOT_DIR = "/apth/top/github/repos"
YEAR = 2024
OUTPUT_IMAGE = "git_stats.png"
CARD_WIDTH = 800
CARD_HEIGHT = 400
BACKGROUND_COLOR = "#f4f4f4"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
FONT_PATH = "/path/to/your/font"
FONT_SIZE = 24
TITLE_FONT_SIZE = 36
PADDING = 20

def get_git_stats(repo_path):
    """Get commit stats for a Git repository."""
    try:
        os.chdir(repo_path)

        result = subprocess.run(
            ["git", "log", "--since=2024-01-01", "--until=2024-12-31", "--pretty=format:%cd", "--date=iso"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        commit_dates = result.stdout.strip().split("\n") if result.stdout else []

        
        months = [datetime.fromisoformat(date).month for date in commit_dates]
        days = [datetime.fromisoformat(date).strftime('%A') for date in commit_dates]
        month_counter = Counter(months)
        day_counter = Counter(days)

        
        extensions = Counter()
        for root, _, files in os.walk(repo_path):
            for file in files:
                if not file.startswith("."):
                    _, ext = os.path.splitext(file)
                    extensions[ext] += 1
        primary_language = extensions.most_common(1)[0][0] if extensions else "Unknown"

        repo_name = os.path.basename(repo_path)
        return {
            "repo": repo_name,
            "commits": len(commit_dates),
            "most_active_month": month_counter.most_common(1)[0][0] if month_counter else None,
            "most_active_day": day_counter.most_common(1)[0][0] if day_counter else None,
            "top_language": primary_language,
        }

    except Exception as e:
        print(f"Error processing {repo_path}: {e}")
        return None

def collect_stats(root_dir):
    """Collect stats from all Git repositories under the root directory."""
    stats = []

    for dirpath, _, _ in os.walk(root_dir):
        if os.path.exists(os.path.join(dirpath, ".git")):
            print(f"Processing repository: {dirpath}")
            repo_stats = get_git_stats(dirpath)
            if repo_stats:
                stats.append(repo_stats)

    return stats

def aggregate_stats(stats):
    """Aggregate stats into global metrics."""
    total_commits = sum(repo["commits"] for repo in stats)
    overall_months = Counter(repo["most_active_month"] for repo in stats if repo["most_active_month"])
    overall_days = Counter(repo["most_active_day"] for repo in stats if repo["most_active_day"])
    overall_languages = Counter(repo["top_language"] for repo in stats if repo["top_language"])

    return {
        "total_commits": total_commits,
        "most_active_month": overall_months.most_common(1)[0][0] if overall_months else None,
        "most_active_day": overall_days.most_common(1)[0][0] if overall_days else None,
        "top_language": overall_languages.most_common(1)[0][0] if overall_languages else "Unknown",
    }

def create_global_card(aggregated_stats, output_image):
    """Create a single card image for global stats."""
    
    image = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    
    title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
    text_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    
    draw.rectangle(
        [(PADDING, PADDING), (CARD_WIDTH - PADDING, CARD_HEIGHT - PADDING)],
        fill=CARD_COLOR,
        outline="#e0e0e0",
    )


    draw.text(
        (PADDING * 2, PADDING * 2),
        f"Global Git Stats ({YEAR})",
        fill=TEXT_COLOR,
        font=title_font,
    )
    draw.text(
        (PADDING * 2, PADDING * 2 + 60),
        f"Total Commits: {aggregated_stats['total_commits']}",
        fill=TEXT_COLOR,
        font=text_font,
    )
    draw.text(
        (PADDING * 2, PADDING * 2 + 120),
        f"Most Active Month: {aggregated_stats['most_active_month']}",
        fill=TEXT_COLOR,
        font=text_font,
    )
    draw.text(
        (PADDING * 2, PADDING * 2 + 180),
        f"Most Active Day: {aggregated_stats['most_active_day']}",
        fill=TEXT_COLOR,
        font=text_font,
    )
    draw.text(
        (PADDING * 2, PADDING * 2 + 240),
        f"Top Language: {aggregated_stats['top_language']}",
        fill=TEXT_COLOR,
        font=text_font,
    )

    image.save(output_image)
    print(f"Global stats image saved as {output_image}")

def create_card(stats, output_image):
    """Create a card-style image with the stats."""
    
    card_count = len(stats)
    image_height = (CARD_HEIGHT + PADDING) * card_count + PADDING
    image = Image.new("RGB", (CARD_WIDTH, image_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    
    title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)
    text_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    y_offset = PADDING
    for stat in stats:
    
        draw.rectangle(
            [(PADDING, y_offset), (CARD_WIDTH - PADDING, y_offset + CARD_HEIGHT)],
            fill=CARD_COLOR,
            outline="#e0e0e0",
        )

    
        draw.text(
            (PADDING * 2, y_offset + PADDING),
            f"Repository: {stat['repo']}",
            fill=TEXT_COLOR,
            font=title_font,
        )
        draw.text(
            (PADDING * 2, y_offset + PADDING + 50),
            f"Commits: {stat['commits']}",
            fill=TEXT_COLOR,
            font=text_font,
        )
        draw.text(
            (PADDING * 2, y_offset + PADDING + 100),
            f"Most Active Month: {stat['most_active_month']}",
            fill=TEXT_COLOR,
            font=text_font,
        )
        draw.text(
            (PADDING * 2, y_offset + PADDING + 150),
            f"Most Active Day: {stat['most_active_day']}",
            fill=TEXT_COLOR,
            font=text_font,
        )
        draw.text(
            (PADDING * 2, y_offset + PADDING + 200),
            f"Top Language: {stat['top_language']}",
            fill=TEXT_COLOR,
            font=text_font,
        )

        y_offset += CARD_HEIGHT + PADDING

    
    image.save(output_image)
    print(f"Stats image saved as {output_image}")


def main():
    print(f"Collecting Git stats for year {YEAR}...")
    
    stats = collect_stats(ROOT_DIR)

    aggregated_stats = aggregate_stats(stats)

    print("\nGlobal Stats:")
    print(f"Total Commits: {aggregated_stats['total_commits']}")
    print(f"Most Active Month: {aggregated_stats['most_active_month']}")
    print(f"Most Active Day: {aggregated_stats['most_active_day']}")
    print(f"Top Language: {aggregated_stats['top_language']}")

    create_global_card(aggregated_stats, OUTPUT_IMAGE)

if __name__ == "__main__":
    main()