from flask import Flask, request, jsonify

app = Flask(__name__)

ip_scores = {
        "192.168.7.150": 2
}

def score_ip(ip_address):
    return ip_scores.get(ip_address, 1)

@app.route('/score_ip', methods=['GET'])
def score_ip_route():
    ip_address = request.args.get('ip')
    if not ip_address:
        return jsonify({'error': 'IP address is required'}), 400

    score = score_ip(ip_address)
    return jsonify({'ip': ip_address, 'score': score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
