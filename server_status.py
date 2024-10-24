from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    stats = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage
            }

    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
