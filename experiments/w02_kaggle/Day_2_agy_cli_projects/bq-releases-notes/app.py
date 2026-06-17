import requests
import xml.etree.ElementTree as ET
from flask import Flask, render_template, jsonify

app = Flask(__name__)

BIGQUERY_FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"

def fetch_release_notes():
    response = requests.get(BIGQUERY_FEED_URL, timeout=10)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    notes = []
    # Handle Atom namespace if present
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', ns) + root.findall('entry'):
        title_elem = entry.find('atom:title', ns) or entry.find('title')
        content_elem = entry.find('atom:content', ns) or entry.find('content')
        title = title_elem.text if title_elem is not None else ''
        content = content_elem.text if content_elem is not None else ''
        notes.append({"title": title, "content": content})
    return notes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes')
def api_notes():
    try:
        notes = fetch_release_notes()
        return jsonify({"status": "ok", "notes": notes})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
