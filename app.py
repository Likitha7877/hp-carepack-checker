# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# from scraper_logic import run_warranty_check
# import os  # Required for reading PORT from environment

# app = Flask(__name__)
# CORS(app, origins=["https://arminfoserve.com/"])  # Enable cross-origin requests
# @app.route('/ping')
# def ping():
#     return 'pong'


# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/', methods=['POST'])
# def check_warranty():
#     try:
#         data = request.get_json()
#         print("📥 Received JSON:", data)

#         serial = data.get("serial")
#         product = data.get("product")
#         print(f"🔧 Serial: {serial}, Product: {product}")

#         result = run_warranty_check(serial, product)
#         print("✅ Warranty check result:", result)

#         return jsonify(result)

#     except Exception as e:
#         print("❌ Error during warranty check:", e)
#         return jsonify({"error": str(e)}), 500


# @app.route('/view-pack')
# def view_pack():
#     serial_number = request.args.get('serial', '')
#     product_number = request.args.get('product', '')
#     image_url = request.args.get('image_url', '')
#     return render_template("view_pack.html",
#                            serial_number=serial_number,
#                            product_number=product_number,
#                            image_url=image_url)

# # ✅ This enables iframe support across domains
# @app.after_request
# def allow_iframe(response):
#     response.headers['X-Frame-Options'] = 'ALLOWALL'
#     response.headers['Content-Security-Policy'] = "frame-ancestors *"
#     return response

# # ✅ Required for Render deployment
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))  # Render provides this PORT env variable
#     app.run(host="0.0.0.0", port=port, debug=True)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scraper_logic import run_warranty_check
from eosl_data import eosl_data  # ✅ EOSL data dictionary
import os  # Required for reading PORT from environment

app = Flask(__name__)
CORS(app, origins=["https://arminfoserve.com/"])  # Enable cross-origin requests


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def check_warranty():
    try:
        data = request.get_json()
        print("📥 Received JSON:", data)

        serial = data.get("serial")
        product = data.get("product")
        print(f"🔧 Serial: {serial}, Product: {product}")

        # Run main warranty logic
        result = run_warranty_check(serial, product)
        print("✅ Warranty check result:", result)

        # Extract product_number from result if not directly sent
        final_product = result.get("product_number") or product
        product_clean = final_product.strip().upper() if final_product else None

        # Debug: Check eosl_data keys
        print("📦 eosl_data keys include:", list(eosl_data.keys()))
        print(f"🔍 Looking up EOSL for: '{product_clean}'")

        # Lookup EOSL date
        if product_clean:
            eosl_date = eosl_data.get(product_clean)
            result['eosl_date'] = eosl_date
            print(f"📅 EOSL Date for {product_clean}: {eosl_date}")
        else:
            result['eosl_date'] = None
            print("⚠️ Product number not provided or found. EOSL not set.")

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


# ✅ This enables iframe support across domains
@app.after_request
def allow_iframe(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Content-Security-Policy'] = "frame-ancestors *"
    return response


# ✅ Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides this PORT env variable
    print("🗂️ eosl_data loaded:", eosl_data.get("2D9H6PA"))  # ⬅️ Test if this works at startup
    app.run(host="0.0.0.0", port=port, debug=True)
