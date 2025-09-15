from flask import Flask, jsonify, render_template_string
import time
from time import sleep
import threading
from collections import defaultdict, deque
from datetime import datetime
import json

app = Flask(__name__)

# Store request counts per second
request_counts = defaultdict(int)
request_history = deque(maxlen=60)  # Keep last 60 seconds
lock = threading.Lock()

# Middleware to count requests
@app.before_request
def count_request():
    current_second = int(time.time())
    with lock:
        request_counts[current_second] += 1

def update_history():
    """Background thread to update request history every second"""
    while True:
        current_second = int(time.time())
        with lock:
            # Get count for the previous second (to ensure complete data)
            count = request_counts.get(current_second - 1, 0)
            request_history.append({
                'timestamp': current_second - 1,
                'count': count
            })
        time.sleep(1)

# Start background thread
history_thread = threading.Thread(target=update_history, daemon=True)
history_thread.start()

# API endpoint to get request data
@app.route('/api/requests')
def get_requests():
    with lock:
        data = list(request_history)
    return jsonify(data)

# Test endpoints to generate some traffic
@app.route('/api/test')
def test_endpoint():
    return jsonify({'message': 'Test endpoint hit!', 'timestamp': time.time()})

@app.route('/api/ping')
def ping():
    return jsonify({'status': 'pong'})

@app.route('/api/data/<int:item_id>')
def get_data(item_id):
    return jsonify({'item_id': item_id, 'data': f'Sample data for item {item_id}'})

@app.route('/api/delay/<int:delay>')
def delay(delay):
    sleep(delay / 1000)
    return "OK"


# Main dashboard route
@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTTP Request Monitor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            min-width: 150px;
            margin: 10px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .chart-container {
            position: relative;
            height: 400px;
            margin-bottom: 30px;
        }
        .controls {
            text-align: center;
            margin-bottom: 20px;
        }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
            font-size: 14px;
        }
        button:hover {
            background: #0056b3;
        }
        .test-endpoints {
            background: #e9ecef;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .test-endpoints h3 {
            margin-top: 0;
            color: #333;
        }
        .endpoint-button {
            background: #28a745;
            margin: 5px;
            padding: 8px 15px;
            font-size: 12px;
        }
        .endpoint-button:hover {
            background: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 HTTP Request Monitor</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="current-rps">0</div>
                <div class="stat-label">Current RPS</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-requests">0</div>
                <div class="stat-label">Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avg-rps">0</div>
                <div class="stat-label">Avg RPS (60s)</div>
            </div>
        </div>

        <div class="controls">
            <button onclick="toggleUpdates()">Pause Updates</button>
            <button onclick="clearData()">Clear Data</button>
        </div>

        <div class="chart-container">
            <canvas id="requestChart"></canvas>
        </div>

        <div class="test-endpoints">
            <h3>Test Endpoints (click to generate traffic):</h3>
            <button class="endpoint-button" onclick="hitEndpoint('/api/test')">/api/test</button>
            <button class="endpoint-button" onclick="hitEndpoint('/api/ping')">/api/ping</button>
            <button class="endpoint-button" onclick="hitEndpoint('/api/data/123')">/api/data/123</button>
            <button class="endpoint-button" onclick="generateLoad()">Generate Load (10 req/s)</button>
        </div>
    </div>

    <script>
        let chart;
        let isUpdating = true;
        let loadInterval = null;

        // Initialize chart
        function initChart() {
            const ctx = document.getElementById('requestChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Requests per Second',
                        data: [],
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Requests per Second'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true
                        }
                    }
                }
            });
        }

        // Update chart with new data
        function updateChart() {
            if (!isUpdating) return;

            fetch('/api/requests')
                .then(response => response.json())
                .then(data => {
                    const labels = data.map(item => {
                        const date = new Date(item.timestamp * 1000);
                        return date.toLocaleTimeString();
                    });
                    const values = data.map(item => item.count);

                    chart.data.labels = labels;
                    chart.data.datasets[0].data = values;
                    chart.update('none');

                    // Update stats
                    updateStats(data);
                })
                .catch(error => console.error('Error fetching data:', error));
        }

        // Update statistics
        function updateStats(data) {
            if (data.length === 0) return;

            const currentRps = data[data.length - 1]?.count || 0;
            const totalRequests = data.reduce((sum, item) => sum + item.count, 0);
            const avgRps = data.length > 0 ? (totalRequests / data.length).toFixed(1) : 0;

            document.getElementById('current-rps').textContent = currentRps;
            document.getElementById('total-requests').textContent = totalRequests;
            document.getElementById('avg-rps').textContent = avgRps;
        }

        // Toggle updates
        function toggleUpdates() {
            isUpdating = !isUpdating;
            const button = event.target;
            button.textContent = isUpdating ? 'Pause Updates' : 'Resume Updates';
        }

        // Clear chart data
        function clearData() {
            chart.data.labels = [];
            chart.data.datasets[0].data = [];
            chart.update();
            
            document.getElementById('current-rps').textContent = '0';
            document.getElementById('total-requests').textContent = '0';
            document.getElementById('avg-rps').textContent = '0';
        }

        // Hit test endpoint
        function hitEndpoint(endpoint) {
            fetch(endpoint)
                .then(response => response.json())
                .then(data => console.log('Response:', data))
                .catch(error => console.error('Error:', error));
        }

        // Generate continuous load
        function generateLoad() {
            if (loadInterval) {
                clearInterval(loadInterval);
                loadInterval = null;
                event.target.textContent = 'Generate Load (10 req/s)';
                event.target.style.background = '#28a745';
            } else {
                loadInterval = setInterval(() => {
                    const endpoints = ['/api/test', '/api/ping', '/api/data/' + Math.floor(Math.random() * 1000)];
                    const randomEndpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
                    hitEndpoint(randomEndpoint);
                }, 100); // 10 requests per second
                event.target.textContent = 'Stop Load';
                event.target.style.background = '#dc3545';
            }
        }

        // Initialize everything
        document.addEventListener('DOMContentLoaded', function() {
            initChart();
            updateChart(); // Initial load
            setInterval(updateChart, 1000); // Update every second
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("🚀 Starting HTTP Request Monitor...")
    print("📊 Dashboard available at: http://localhost:5000")
    print("📡 API endpoint: http://localhost:5000/api/requests")
    print("🧪 Test endpoints: /api/test, /api/ping, /api/data/<id>")
    app.run(debug=True, host='0.0.0.0', port=5000)
