# Mood Music Recommendation App

A Flask-based web application that detects user mood and recommends matching music playlists using the Jamendo API.

## Features
- **Mood Detection:** Analyzes input/emotions to determine mood.
- **Playlist Fetching:** Uses the Jamendo API to retrieve curated tracks based on tag mappings.
- **Fallback Support:** Includes pre-defined tracks for smooth offline/default behavior.

## Project Structure
```text
mood_music/
├── templates/          # HTML templates for the frontend interface
│   └── index.html
├── app.py             # Main Flask server application
├── mood_detector.py   # Emotion/mood detection logic
├── playlist_service.py # Jamendo API integration logic
└── requirements.txt   # Required Python libraries
