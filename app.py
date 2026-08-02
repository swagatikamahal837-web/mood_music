import base64
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from mood_detector import detect_emotion as detect_mood
from playlist_service import get_playlist_for_mood

app = Flask(__name__)

# Ensure an upload folder exists if handling temporary file storage
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
  """Renders the main home page with a default track."""
  default_mood = 'neutral'
  track_data = get_playlist_for_mood(default_mood)

  return render_template('index.html', mood=default_mood, track=track_data)


@app.route('/detect', methods=['POST'])
def detect():
  """Handles image file upload or webcam base64 payload, extracts the single mood

  string safely, and fetches matching music.
  """
  detected_mood = 'neutral'

  # 1. Handle JSON base64 payload from webcam (JS fetch)
  if request.is_json:
    data = request.get_json()
    base64_str = data.get('image', '')
    if base64_str:
      detection_result = detect_mood(base64_str)

      # Unpack tuple if detect_emotion returned (mood, metadata)
      if isinstance(detection_result, (tuple, list)):
        detected_mood = detection_result[0]
      else:
        detected_mood = detection_result

      detected_mood = str(detected_mood).lower().strip()
      track_data = get_playlist_for_mood(detected_mood)

      return jsonify(
          {'status': 'success', 'mood': detected_mood, 'track': track_data}
      )

  # 2. Handle standard form file upload
  if 'image' in request.files:
    file = request.files['image']
    if file.filename != '':
      image_bytes = file.read()
      base64_str = base64.b64encode(image_bytes).decode('utf-8')

      detection_result = detect_mood(base64_str)

      if isinstance(detection_result, (tuple, list)):
        detected_mood = detection_result[0]
      else:
        detected_mood = detection_result

      detected_mood = str(detected_mood).lower().strip()
      track_data = get_playlist_for_mood(detected_mood)

      return render_template(
          'index.html', mood=detected_mood, track=track_data
      )

  return redirect(url_for('index'))


@app.route('/api/get_track/<mood>', methods=['GET'])
def api_get_track(mood):
  """API Endpoint: Returns track metadata JSON for a given mood string."""
  track_data = get_playlist_for_mood(mood)
  if track_data:
    return jsonify({'status': 'success', 'mood': mood, 'track': track_data})
  return jsonify(
      {'status': 'error', 'message': 'No track found for this mood'}
  ), 404


if __name__ == '__main__':
  # Uses port 5001 to avoid conflicts with macOS AirPlay on port 5000
  app.run(debug=True, port=5001)