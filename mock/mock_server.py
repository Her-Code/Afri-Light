from flask import Flask, jsonify, request
import random

app = Flask(__name__)

@app.route('/api/mtn/payment', methods=['POST'])
def mtn_payment():
    data = request.get_json()
    return jsonify({
        'provider': 'MTN',
        'status': 'success',
        'transaction_id': f"MTN-{random.randint(1000, 9999)}",
        'amount': data.get('amount'),
        'recipient': data.get('recipient')
    }), 200

@app.route('/api/airtel/payment', methods=['POST'])
def airtel_payment():
    data = request.get_json()
    return jsonify({
        'provider': 'Airtel',
        'status': 'success',
        'transaction_id': f"AIR-{random.randint(1000, 9999)}",
        'amount': data.get('amount'),
        'recipient': data.get('recipient')
    }), 200

@app.route('/api/mpesa/payment', methods=['POST'])
def mpesa_payment():
    data = request.get_json()
    return jsonify({
        'provider': 'Safaricom M-Pesa',
        'status': 'success',
        'transaction_id': f"MPS-{random.randint(1000, 9999)}",
        'amount': data.get('amount'),
        'recipient': data.get('recipient')
    }), 200

# Error simulation route
@app.route('/api/mtn/payment/fail', methods=['POST'])
def mtn_payment_fail():
    return jsonify({
        'error': 'Insufficient funds',
        'status': 'failed'
    }), 400

if __name__ == '__main__':
    app.run(port=5001, debug=True)
