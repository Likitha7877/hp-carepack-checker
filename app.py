# from flask import Flask, render_template, request, jsonify
# from scraper_logic import run_warranty_check
 


# app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template("index.html")
# #
# @app.route('/check-warranty', methods=['POST'])
# def check_warranty():
#     data = request.json
#     serial = data.get("serial")
#     product = data.get("product")
#     result = run_warranty_check(serial, product)
#     # print("🟡 Result from scraper_logic:", result)  # Add this line


#     return jsonify(result)


# @app.route('/view-pack')
# def view_pack():
#     serial_number = request.args.get('serial', '')
#     product_number = request.args.get('product', '')
#     image_url = request.args.get('image_url', '')
#     return render_template("view_pack.html",
#                            serial_number=serial_number,
#                            product_number=product_number,
#                            image_url=image_url)


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os  # Required for reading PORT from environment
import time  # Used for simulating delay
from scraper_logic import run_warranty_check  # Temporarily commented out

app = Flask(__name__)
CORS(app, origins=["https://arminfoserve.com/"])  # Enable cross-origin requests

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/')
def index():
    print("🟢 GET / route hit")
    return render_template("index.html")

@app.route('/', methods=['POST'])
def check_warranty():
    try:
        print("📨 Received POST request to /")

        data = request.get_json()
        print("📥 Received JSON:", data)

        serial = data.get("serial")
        product = data.get("product")
        print(f"🔧 Serial: {serial}, Product: {product}")

        # Temporary: simulate long response
        time.sleep(5)
        result = {"mock": "response", "serial": serial, "product": product}

        # When ready to re-enable:
        result = run_warranty_check(serial, product)

        print("✅ Warranty check result (mock):", result)
        return jsonify(result)

    except Exception as e:
        print("❌ Error during warranty check:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/view-pack')
def view_pack():
    serial_number = request.args.get('serial', '')
    product_number = request.args.get('product', '')
    image_url = request.args.get('image_url', '')
    return render_template("view_pack.html",
                           serial_number=serial_number,
                           product_number=product_number,
                           image_url=image_url)

# ✅ Enable iframe support
@app.after_request
def allow_iframe(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Content-Security-Policy'] = "frame-ancestors *"
    return response

# ✅ Entry point for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides this PORT env variable
    app.run(host="0.0.0.0", port=port, debug=True)
