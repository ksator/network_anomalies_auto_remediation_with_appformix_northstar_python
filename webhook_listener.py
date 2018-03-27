from flask import Flask, jsonify, abort, make_response, request
import northstar_rest_calls
import push_to_git

app = Flask(__name__)

@app.route('/northstar/device_maintenance', methods=['POST'])
def node_in_maintenance():
 if request.headers['Content-Type'] != 'application/json':
        abort(400, message="Expected Content-Type = application/json")
 data = request.json
 #dev = data["device"]
 dev='10.49.124.59'
 northstar_rest_calls.put_device_in_maintenance(dev)
 return jsonify({'device in maintenance ': dev}), 201

@app.route('/junos/collect_data', methods=['POST'])
def collect_commands():
 if request.headers['Content-Type'] != 'application/json':
        abort(400, message="Expected Content-Type = application/json")
 data = request.json
 #dev = data["device"]
 dev='10.49.124.59'
 push_to_git.collect_and_push(dev)
 return jsonify({'collected data on device ': dev}), 201


app.run(
    debug=True,
    port=int("12345"),
    host="0.0.0.0"
    )

