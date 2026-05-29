# 🎬 Movie & Series Recommendation System

A command-line application to search, explore, and get personalized recommendations for movies and TV series using the OMDB API.

## Features

✨ **Smart Recommendations**
- 🎯 Mood-based suggestions (happy, sad, romantic, scared, energetic, relaxed)
- 🔥 Popular titles across Netflix, Prime Video, Disney+, HBO Max, and Hulu
- 💥 Curated action categories (Marvel, DC, Spy, War, Action)

🔍 **Search & Explore**
- Detailed information about any movie or series
- IMDb ratings and plot summaries
- Genre classification and mood analysis
- Streaming platform availability

💾 **Smart Caching**
- Automatic caching of search results
- Faster repeated queries
- JSON-based persistence

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Key**
   - Get a free API key from [OMDB API](https://www.omdbapi.com/apikey.aspx)
   - Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your OMDB API key:
   ```
   OMDB_API_KEY=your_api_key_here
   ```

## Usage

### Run the application
```bash
python main.py
```

### Main Menu Options

#### 1. Check Movie/Series Details
- Search for any movie or TV series
- View detailed information including:
  - Title and type
  - IMDb rating
  - Genres
  - Available streaming platforms
  - Plot summary
  - Mood classification

#### 2. Get Recommendations
- **Mood-based**: Get suggestions based on your current mood
  - Happy, Sad, Romantic, Scared, Energetic, Relaxed
- **Popular**: Browse trending and popular titles
- **Action Special**: Explore curated action categories
  - Marvel, DC, Spy, War, Action

### Example Workflow

```
🎬 Hollywood Movie & Series Recommendation System
==============================================================
1. 🔍 Check movie/series details
2. 🎯 Get movie/series suggestions
3. ❌ Exit
==============================================================

Choose option (1/2/3): 2

📽️  What do you want to watch? (movie/series): movie

🎯 Options:
1. Mood based recommendations
2. Popular titles
3. Action special categories

Choose option (1/2/3): 1

😊 Available moods: happy, sad, romantic, scared, energetic, relaxed

Enter mood: happy
```

## Database Structure

### POPULAR_TITLES
Contains curated collections of:
- **Movies**: 30+ titles from Netflix, Prime Video, and other platforms
- **Series**: 30+ popular TV series

### ACTION_CATEGORIES
Specialized collections:
- **Marvel**: All MCU movies
- **DC**: DC Universe films
- **Spy**: Spy thrillers and espionage films
- **War**: War and military dramas
- **Action**: Transformers, Fast & Furious, Jurassic franchises, and more

### MOOD_KEYWORDS
Maps moods to genres for intelligent recommendations:
- Happy → Comedy, Adventure, Family, Fantasy
- Sad → Drama, Biography, Romance
- Romantic → Romance, Drama, Musical
- Scared → Horror, Thriller, Mystery
- Energetic → Action, Thriller, Crime, Sci-Fi
- Relaxed → Comedy, Slice of Life, Family

## API Integration

### OMDB API
- Provider: [OMDB API](https://www.omdbapi.com/)
- Free tier: 1,000 requests/day
- Used for: Title search, ratings, plot summaries, genre data

## Caching System

The application maintains `streaming_cache.json` to:
- Cache API responses for faster lookups
- Store streaming platform information
- Reduce API calls and improve performance

## Project Structure

```
movie-recommendation-system/
│
├── main.py              # Main application logic
├── data.py              # Movie and series databases
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OMDB_API_KEY=your_api_key_here
```

The application will use the default API key if `.env` is not present (limited functionality).

## Troubleshooting

### Issue: "API Error" message
- Check your internet connection
- Verify OMDB API key is valid
- Ensure you haven't exceeded API rate limits

### Issue: "Title not found"
- The title might not be in the OMDB database
- Try searching with a slightly different name
- Check IMDb directly for correct spelling

### Issue: Cache corrupted
- Delete `streaming_cache.json`
- The application will recreate it on next run

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Enhancement Ideas
- Add more movie/series to databases
- Implement user ratings and reviews
- Add watch history tracking
- Support for multiple API providers
- Web interface using Flask/Django
- Discord bot integration

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Credits

- **OMDB API**: For movie and series data
- **Movie & TV Data**: Community-sourced and verified

## Support

If you encounter any issues or have suggestions:
- Open an issue on GitHub
- Contact the maintainers

## Roadmap

- [ ] Add user authentication
- [ ] Implement user preferences and saved lists
- [ ] Add advanced filtering options
- [ ] Support for TV series episodes
- [ ] Mobile app version
- [ ] Integration with streaming service APIs
- [ ] Machine learning-based recommendations

---

**Made with ❤️ for movie and series lovers everywhere!**

