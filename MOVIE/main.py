import requests
import json
import os
from data import POPULAR_TITLES, MOOD_KEYWORDS, ACTION_CATEGORIES

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "6c09d4a6")
BASE_URL = "http://www.omdbapi.com/"

CACHE_FILE = "streaming_cache.json"


def load_cache():
    """Load streaming cache from JSON file."""
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Warning: Could not load cache - {e}")
        return {}


def save_cache(cache):
    """Save streaming cache to JSON file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=4)
    except IOError as e:
        print(f"⚠️ Warning: Could not save cache - {e}")

STREAMING_CACHE = load_cache()


def get_streaming_platform(title):
    """Get streaming platform for a given title.
    Checks cache first, then searches through databases.
    """
    if title in STREAMING_CACHE:
        return STREAMING_CACHE[title]

    for block in [POPULAR_TITLES, ACTION_CATEGORIES]:
        for cat in block.values():
            if title in cat:
                STREAMING_CACHE[title] = cat[title]
                save_cache(STREAMING_CACHE)
                return cat[title]

    STREAMING_CACHE[title] = "Availability varies by region"
    save_cache(STREAMING_CACHE)
    return STREAMING_CACHE[title]

def fetch_by_title(title):
    """Fetch movie/series details from OMDB API.
    Returns dict with name, rating, genres, type, and plot.
    """
    try:
        params = {"t": title, "apikey": OMDB_API_KEY}
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if data.get("Response") == "True":
            try:
                rating = float(data.get("imdbRating", 0))
            except (ValueError, TypeError):
                rating = 0.0

            return {
                "name": data.get("Title"),
                "rating": rating,
                "genres": data.get("Genre", "Unknown"),
                "type": data.get("Type"),
                "plot": data.get("Plot", "N/A")
            }
    except requests.RequestException as e:
        print(f"❌ API Error: {e}")

    return None

def fetch_by_keyword(keyword, content_type):
    """Search OMDB for content by keyword and type.
    Returns list of matching items up to 10 results.
    """
    results = []
    try:
        params = {"s": keyword, "type": content_type, "apikey": OMDB_API_KEY}
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if data.get("Response") == "True":
            for item in data.get("Search", []):
                details = fetch_by_title(item["Title"])
                if details:
                    results.append(details)
                    if len(results) >= 10:
                        break
    except requests.RequestException as e:
        print(f"❌ API Error: {e}")

    return results

def get_badges(item, mode):
    """Generate badge labels for recommendation results."""
    badges = []

    if item["rating"] >= 8.5:
        badges.append("⭐ Top Rated")

    mode_badges = {
        "popular": "🔥 Trending",
        "action": "💥 Action Hit",
        "mood": "😊 Mood Pick"
    }

    if mode in mode_badges:
        badges.append(mode_badges[mode])

    return " | ".join(badges)

def print_result(item):
    """Print formatted result for a single item."""
    icon = "🎬" if item["type"] == "movie" else "📺"
    print(
        f"{icon} {item['name']:<30} ⭐ {item['rating']} | "
        f"{item['genres']:<25} | 📺 {item['platform']} | {item['badges']}"
    )

def show_next_batches(results):
    """Display results in batches of 5 with pagination."""
    if not results:
        print("❌ No results found.")
        return

    results.sort(key=lambda x: x["rating"], reverse=True)
    index = 0
    shown = 0

    # Show first batch
    for item in results[index:index + 5]:
        print_result(item)

    index += 5
    shown += 1

    # Show additional batches
    while index < len(results) and shown < 3:
        nxt = input("\nShow next 5? (y/n): ").lower()
        if nxt != "y":
            break

        for item in results[index:index + 5]:
            print_result(item)

        index += 5
        shown += 1

def recommendation_engine():
    """Main recommendation engine with multiple modes."""
    try:
        content_type = input("\n📽️  What do you want to watch? (movie/series): ").lower()
        if content_type not in ["movie", "series"]:
            print("❌ Invalid choice. Please enter 'movie' or 'series'.")
            return

        print("\n🎯 Options:")
        print("1. Mood based recommendations")
        print("2. Popular titles")
        print("3. Action special categories")

        choice = input("Choose option (1/2/3): ").strip()
        results = []

        if choice == "2":
            print(f"\n⏳ Fetching popular {content_type}s...")
            for title in POPULAR_TITLES[content_type]:
                data = fetch_by_title(title)
                if data:
                    data["platform"] = get_streaming_platform(title)
                    data["badges"] = get_badges(data, "popular")
                    results.append(data)

        elif choice == "3":
            print("\n🎬 Action categories:", ", ".join(ACTION_CATEGORIES.keys()))
            cat = input("Choose category: ").lower()

            if cat not in ACTION_CATEGORIES:
                print("❌ Invalid category.")
                return

            print(f"\n⏳ Fetching {cat} titles...")
            for title in ACTION_CATEGORIES[cat]:
                data = fetch_by_title(title)
                if data:
                    data["platform"] = get_streaming_platform(title)
                    data["badges"] = get_badges(data, "action")
                    results.append(data)

        elif choice == "1":
            print("\n😊 Available moods:", ", ".join(MOOD_KEYWORDS.keys()))
            mood = input("Enter mood: ").lower()

            if mood not in MOOD_KEYWORDS:
                print("❌ Invalid mood.")
                return

            print(f"\n⏳ Fetching {mood} recommendations...")
            for keyword in MOOD_KEYWORDS[mood]:
                for item in fetch_by_keyword(keyword, content_type):
                    item["platform"] = get_streaming_platform(item["name"])
                    item["badges"] = get_badges(item, "mood")
                    results.append(item)

        else:
            print("❌ Invalid option.")
            return

        # Remove duplicates
        results = list({i["name"]: i for i in results}.values())

        print("\n🎯 Recommendations\n")
        show_next_batches(results)

    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_movie_details():
    """Fetch and display detailed information about a specific title."""
    try:
        title = input("\n🔍 Enter movie/series name: ").strip()
        if not title:
            print("❌ Title cannot be empty.")
            return

        data = fetch_by_title(title)
        if not data:
            print("❌ Not found")
            return

        platform = get_streaming_platform(data["name"])
        moods = []

        for mood, genres in MOOD_KEYWORDS.items():
            for g in genres:
                if g.lower() in data["genres"].lower():
                    moods.append(mood)
                    break

        print("\n" + "="*60)
        print("🎬 Details")
        print("="*60)
        print(f"Name     : {data['name']}")
        print(f"Type     : {data['type'].upper()}")
        print(f"Rating   : ⭐ {data['rating']}/10")
        print(f"Genres   : {data['genres']}")
        print(f"Platform : 📺 {platform}")
        print(f"Moods    : {', '.join(moods) if moods else 'General'}")
        print(f"Plot     : {data['plot']}")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main application entry point."""
    print("\n" + "="*60)
    print("🎬 Hollywood Movie & Series Recommendation System")
    print("="*60)
    print("1. 🔍 Check movie/series details")
    print("2. 🎯 Get movie/series suggestions")
    print("3. ❌ Exit")
    print("="*60)

    choice = input("\nChoose option (1/2/3): ").strip()

    if choice == "1":
        check_movie_details()
    elif choice == "2":
        recommendation_engine()
    elif choice == "3":
        print("\n👋 Thank you for using Movie System!\n")
    else:
        print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}\n")