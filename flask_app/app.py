from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)
metrics = PrometheusMetrics(app)

compute_counter = Counter('compute_requests_total', 'Total number of compute requests')

@app.route('/')
def home():
    return """
        <h1>Hello World from Prateek</h1>
        <p><a href='/compute'>Go to Compute</a></p>
    """

@app.route('/compute')
def compute():
    compute_counter.inc()
    a, b = 0, 1
    total = 0
    while a <= 55000:
        total += a
        a, b = b, a + b
    return f"<h1>Fibonacci sum up to 55000: {total}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
