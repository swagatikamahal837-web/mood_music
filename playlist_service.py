import requests

JAMENDO_CLIENT_ID = '709fa152'

# Tag mapping for Jamendo API query
MOOD_TAG_MAP = {
    'happy': 'pop',
    'sad': 'chill',
    'angry': 'rock',
    'neutral': 'ambient',
    'surprise': 'funk',
    'fear': 'meditation',
    'disgust': 'groove',
}

# Unique fallback tracks for ALL 7 emotions
DEFAULT_TRACKS = {
    'happy': {
        'title': 'Upbeat Pop Sunshine',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888420/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
    'neutral': {
        'title': 'Ambient Relaxing Sound',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888432/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
    'sad': {
        'title': 'Melancholy Chill Melodies',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888425/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
    'angry': {
        'title': 'Energetic Rock Beat',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888410/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
    'surprise': {
        'title': 'Funky Surprise Jam',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888415/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
    'fear': {
        'title': 'Calming Ambient Therapy',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888430/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
    'disgust': {
        'title': 'Smooth Groove Sound',
        'artist': 'Jamendo Artist',
        'audio_url': 'https://mp3d.jamendo.com/download/track/1888418/mp32/',
        'image': (
            'https://usercontent.jamendo.com?type=album&id=322797&width=300'
        ),
    },
}


def get_playlist_for_mood(mood):
  """Queries Jamendo API based on detected mood and falls back to unique default tracks."""
  clean_mood = str(mood).lower().strip()
  tag = MOOD_TAG_MAP.get(clean_mood, 'ambient')

  url = f'https://api.jamendo.com/v3.0/tracks/?client_id={JAMENDO_CLIENT_ID}&format=json&limit=5&fuzzytags={tag}&boost=popularity_month'

  try:
    response = requests.get(url, timeout=4, verify=False)
    data = response.json()

    results = data.get('results', [])
    if results:
      track = results[0]
      return {
          'title': track.get('name', 'Unknown Title'),
          'artist': track.get('artist_name', 'Jamendo Artist'),
          'audio_url': track.get('audio'),
          'image': track.get(
              'album_image',
              'https://usercontent.jamendo.com?type=album&id=322797&width=300',
          ),
      }
  except Exception as e:
    print(f'Jamendo API Warning/Error: {e}')

  # Return specific default track for the emotion
  return DEFAULT_TRACKS.get(clean_mood, DEFAULT_TRACKS['neutral'])