from flask import Flask, request, jsonify
from collections import defaultdict
import time
import numpy as np
import tensorflow as tf

app = Flask(__name__)

model = tf.keras.models.load_model('scoring_model.h5')

ip_request_times = defaultdict(list)

# Function to get the score of an IP address based on request frequency
def score_ip(ip_address):
    current_time = time.time()
    request_times = ip_request_times[ip_address]

    # Remove requests older than 60 seconds
    ip_request_times[ip_address] = [t for t in request_times if t > current_time - 60]

    # Add the current request time
    ip_request_times[ip_address].append(current_time)

    # Count how many requests in the last 60 seconds
    request_count = len(ip_request_times[ip_address])

    # Adjust score based on request count
    input_data = np.array([[request_count]])

    predicted_score = model.predict(input_data)[0][0]

    return int(round(predicted_score))

@app.route('/score_ip', methods=['GET'])
def score_ip_route():
    ip_address = request.args.get('ip')
    if not ip_address:
        return jsonify({'error': 'IP address is required'}), 400

    # Get the updated score based on request frequency
    score = score_ip(ip_address)
    return jsonify({'ip': ip_address, 'score': score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
