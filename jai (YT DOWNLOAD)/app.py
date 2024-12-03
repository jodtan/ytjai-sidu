import os
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

# Initialize Flask app
app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_info', methods=['POST'])
def fetch_info():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Use yt-dlp to fetch video information
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        # Prepare response with title, thumbnail, and formats
        video_info = {
            "title": info.get('title', 'Unknown Title'),
            "thumbnail": info.get('thumbnail', ''),
            "formats": [
                {
                    "format_id": f.get('format_id'),
                    "format": f"{f.get('ext', 'unknown')} - {f.get('format_note', 'N/A')}"
                }
                for f in info['formats'] if f.get('ext') in ['mp4', 'mp3']
            ]
        }
        return jsonify(video_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    format_id = request.json.get('format_id')

    if not url or not format_id:
        return jsonify({"error": "Missing URL or format ID"}), 400

    try:
        ydl_opts = {
            'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            'format': format_id,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            file_path = ydl.prepare_filename(info)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
