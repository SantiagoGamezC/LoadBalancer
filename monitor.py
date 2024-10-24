from flask import Flask, jsonify, render_template
import psutil
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    return jsonify({
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "nginx_status": check_nginx_status()
    })

def check_nginx_status():
    try: 
        response = os.popen("curl -s http://localhost/nginx_status").read()
        return response.strip() if response else "Not running"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
