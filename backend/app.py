from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from yolov4 import detect_cars
from algo import optimize_traffic

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('videos')
    if len(files) != 4:
        return jsonify({'error': 'Please upload exactly 4 videos'}), 400

    video_paths = []
    for i, file in enumerate(files):
        print(f"Attempting to save video {i}")
        video_path = os.path.join('uploads', f'video_{i}.mp4')
        file.save(video_path)
        video_paths.append(video_path)
        print(f"Video {i} saved at {video_path}")

    num_cars_list = []
    for video_file in video_paths:
        num_cars = detect_cars(video_file)
        print(f"Processed {video_file}, detected {num_cars} cars")
        num_cars_list.append(num_cars)

    result = optimize_traffic(num_cars_list)
    print(f"Optimization result: {result}")

    return jsonify(result)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
