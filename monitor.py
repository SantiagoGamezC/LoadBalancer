from flask import Flask, jsonify, render_template
import psutil
import os
import requests

app = Flask(__name__)

def backend_servers_status(server_url):
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: server returned status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

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

    nginx_status_ouput = check_nginx_status()

    backend_servers = [
            "http://192.168.7.157:8081/status",
            "http://192.168.7.158:8082/status",
            "http://192.168.7.157:8083/status"
            ]
    
    backend_stats = {}
    for server in backend_servers:
        backend_stats[server] = backend_servers_status(server)


    return jsonify({
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "nginx_status": check_nginx_status(),
        "backend_stats": backend_stats
    })

def check_nginx_status():
    try: 
        response = os.popen("curl -s http://localhost/nginx_status").read()
        return response.strip() if response else "Not running"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
