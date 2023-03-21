import os
from flask import Flask, request, jsonify
import urllib.request
import io
from PIL import Image
import imagehash

app = Flask(__name__)
port = int(os.environ.get('PORT', 8022))

@app.route('/images-hash-filter', methods=['POST'])
def hash_images():
    post_data = request.get_json()
    urls = post_data['urls']

    images = []
    hashes = []

    for url in urls:
        if not url:
            continue

        try:
            image = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
        except (OSError, urllib.error.URLError):
            # Skip the current URL if it's not a valid image file
            continue

        hash = imagehash.average_hash(image)

        is_duplicate = False
        for h in hashes:
            if hash - h < 15:  # adjust threshold as needed
                is_duplicate = True
                break

        if not is_duplicate:
            images.append(url)
            hashes.append(hash)

    return jsonify({'result': images})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)