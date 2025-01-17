from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def post_json():
    name = request.json.get("name")
    return jsonify({"name_received": name})

if __name__ == "__main__":
		app.run()
                