from flask import Flask, jsonify, abort, make_response, request
import northstar_rest_calls

app = Flask(__name__)

@app.route('/northstar/device/maintenance', methods=['POST'])
def node_in_maintenance():
 if request.headers['Content-Type'] != 'application/json':
        abort(400, message="Expected Content-Type = application/json")
 data = request.json
 dev = data["device"]
 northstar_rest_calls.put_device_in_maintenance(dev)
 return jsonify({'device in maintenance ': dev}), 201

app.run(
    debug=True,
    port=int("12345"),
    host="0.0.0.0"
    )

