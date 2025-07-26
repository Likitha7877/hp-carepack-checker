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
# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# from scraper_logic import run_warranty_check
# from eosl_data import eosl_data  # ✅ EOSL data dictionary
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

#         # Run main warranty logic
#         result = run_warranty_check(serial, product)
#         print("✅ Warranty check result:", result)

#         # Extract product_number from result if not directly sent
#         final_product = result.get("product_number") or product
#         product_clean = final_product.strip().upper() if final_product else None

#         # Debug: Check eosl_data keys
#         # print("📦 eosl_data keys include:", list(eosl_data.keys()))
#         # print(f"🔍 Looking up EOSL for: '{product_clean}'")

#         # Lookup EOSL date
#         if product_clean:
#             eosl_date = eosl_data.get(product_clean)
#             result['eosl_date'] = eosl_date
#             # print(f"📅 EOSL Date for {product_clean}: {eosl_date}")
#         else:
#             result['eosl_date'] = None
#             print("⚠️ Product number not provided or found. EOSL not set.")

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
#     print("🗂️ eosl_data loaded:", eosl_data.get("2D9H6PA"))  # ⬅️ Test if this works at startup
#     app.run(host="0.0.0.0", port=port, debug=True)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from scraper_logic import run_warranty_check
from eosl_data import eosl_data
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://arminfoserve.com/"])

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)


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

        result = run_warranty_check(serial, product)
        print("✅ Warranty check result:", result)

        final_product = result.get("product_number") or product
        product_clean = final_product.strip().upper() if final_product else None

        if product_clean:
            eosl_date = eosl_data.get(product_clean)
            result['eosl_date'] = eosl_date
        else:
            result['eosl_date'] = None
            print("⚠️ Product number not provided or found. EOSL not set.")

        return jsonify(result)

    except Exception as e:
        print("❌ Error during warranty check:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        name = data.get("name")
        phone = data.get("phone")
        serial = data.get("serial")
        heading = data.get("headingText", "Not specified")

        if not (name and phone and serial):
            return jsonify({"error": "All fields are required"}), 400

        msg = Message(f"Reminder Form: {heading}", recipients=["aayushi@arminfoserve.com"])
        msg.html = f"""
        <h2>{heading}</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Serial Number:</strong> {serial}</p>
        """
        mail.send(msg)

        return jsonify({"message": "✅ Thank you! We will remind you in time."})
    except Exception as e:
        print("❌ Failed to send email:", e)
        return jsonify({"error": "Failed to send email"}), 500


@app.route("/send_email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        number = data.get("number")
        result = data.get("result")

        if not (name and email and number and result):
            return jsonify({"message": "❌ Missing data"}), 400

        care_packs = result.get("care_packs", [])
        is_post_warranty = any("post warranty" in pack.get("title", "").lower() for pack in care_packs)

        if is_post_warranty:
            warranty_message = "<p>The warranty will start from the date of purchase.</p>"
        else:
            warranty_message = f"<p>The warranty will start from the date of expiry: <strong>{result.get('end_date')}</strong></p>"

        care_pack_html = f"""
        <h3 style="color: #1F48F0; font-size: 16px; margin-top: 30px;">Compatible Care Packs:</h3>
        <table cellpadding="10" cellspacing="0" border="1" style="border-collapse: collapse; width: 100%; font-size: 14px; border:1px solid #BAC3FF; font-family: Roboto Slab, sans-serif;">
            <thead>
                <tr style="background-color: #F0EFFF; color: #0033A0; text-align: left;">
                    <th style="padding: 8px;">Plan</th>
                    <th style="padding: 8px;">Price</th>
                    <th style="padding: 8px;">Buy Now</th>
                </tr>
            </thead>
            <tbody>
                {''.join([
                    f"""
                    <tr style="background-color: #fff;">
                        <td style="padding: 8px; color:#00208E;">{pack['title']}</td>
                        <td style="padding: 8px;color:#00208E;">₹{pack['price']}</td>
                        <td style="padding: 8px;color:#00208E;"><a href="{pack['url']}" style="color: #0033A0;  text-decoration: underline;">BUY NOW</a></td>
                    </tr>
                    """ for pack in care_packs
                ])}
            </tbody>
        </table>
        """

        html_content = f"""
        <div style="max-width: 700px; margin: auto; font-family: Roboto Slab, sans-serif; color: #000; line-height: 1.5; border: 1px solid #ddd; padding: 20px;">
          <h3 style="margin-bottom: 5px;">Hi {name},</h3>
          <p style="padding-bottom:8px;font-size:16px;font-family: Poppins,sans-serif">
            Thank you for contacting <strong>ARM Infoserve India</strong>, the authorised HP Warranty Extension partner.<br>
            We are delighted to support you with the warranty extension of your <strong>{result.get("product_name")}</strong>.
          </p>

          <!-- User Details Block -->
          <div style="background-color: #FBFBFF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #d0dfff;">
            <h4 style="margin: 0 0 10px; color: #00115A;">User Details</h4>
            <table style="width: 100%; font-size: 14px;">
              <tr><td style="padding: 4px 0;  color:#00115A;">Name</td><td>: {name}</td></tr>
              <tr><td style="padding: 4px 0;  color:#00115A;">Email</td><td>: {email}</td></tr>
              <tr><td style="padding: 4px 0;  color:#00115A;">Phone Number</td><td>: {number}</td></tr>
            </table>
          </div>

          <!-- Warranty Info Block -->
          <div style="background-color: #FBFBFF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #ddd;">
             <table style="width: 100%; font-size: 14px;">
              <tr><td style="padding: 4px 0; color:#00115A;">Product Status</td><td>: {result.get("status")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;">Product Name</td><td>: {result.get("product_name")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;">Start Date</td><td>: {result.get("start_date")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;">End Date</td><td>: {result.get("end_date")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;">Serial Number</td><td>: {result.get("serial")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;;">Product Number</td><td>: {result.get("product_number")}</td></tr>
            </table>
          </div>

          {care_pack_html}
          {warranty_message}

          <h3>Terms and Conditions</h3>
          <ul style="font-family: Poppins, sans-serif; line-height: 1.6;">
              <li>To avail ON-SITE support, please log a complaint at the HP Service Toll-free number <strong>18002587170</strong>.</li>
              <li>The warranty extension covers all hardware parts except the battery, adapter, and physical damage (unless accidental damage protection is included).</li>
              <li>In the case of accidental damage protection, physical damage is also covered except for battery and adapter.</li>
              <li>Care Pack certificate will be issued by HP within <strong>2 to 3 days</strong> of order confirmation.</li>
              <li>Full advance payment is required.</li>
              <li>Pay in favour of <strong>ARM Infoserve India Pvt. Ltd.</strong></li>
              <li>HP provides the warranty support.</li>
              <li>Damage due to improper use, site conditions, or unauthorized maintenance is not covered.</li>
              <li>Failures due to non-HP software or products are also excluded.</li>
          </ul>

          <p style="font-family: Roboto Slab, sans-serif;">
              For questions, contact <strong>info@arminfoserve.com</strong> or <strong>9560207904</strong>.
          </p>

          <h3>Alternative Payment Options:</h3>
          <ul style="font-family: Poppins, sans-serif; line-height: 1.6;">
              <li>UPI/Cards/Netbanking: <a href="https://rzp.io/l/BHvzhDKEeb" target="_blank">https://rzp.io/l/BHvzhDKEeb</a></li>
              <li><strong>Bank Transfer:</strong><br>
                  Bank: ICICI Bank<br>
                  Account Name: <strong>ARM INFOSERVE INDIA PVT. LTD.</strong><br>
                  Account No.: 054251000009<br>
                  Type: CURRENT ACCOUNT/OD ACCOUNT<br>
                  IFSC: ICIC0000542
              </li>
              <li><strong>UPI:</strong> MSARMINFOSERVEINDIAPVTLTD.eazypay@icici (QR Code attached)</li>
          </ul>
        </div>
        """

        msg = Message(
            subject="Quotation for warranty extension.",
            recipients=[email],
            cc=["aayushi@arminfoserve.com", "abhay@arminfoserve.com"],
            html=html_content
        )

        # Attach QR Code
        base_dir = os.path.dirname(os.path.abspath(__file__))
        qr_path = os.path.join(base_dir, "static", "ARM QR Code.jpg")

        if os.path.exists(qr_path):
            with open(qr_path, "rb") as f:
                msg.attach("ARM QR Code.jpg", "image/jpeg", f.read())
        else:
            print("❌ QR file not found")

        mail.send(msg)
        return jsonify({"message": "✅ Quotation sent to your email."})

    except Exception as e:
        print("❌ Send email error:", e)
        return jsonify({"message": "❌ Failed to send email"}), 500



@app.route('/view-pack')
def view_pack():
    serial_number = request.args.get('serial', '')
    product_number = request.args.get('product', '')
    image_url = request.args.get('image_url', '')
    return render_template("view_pack.html",
                           serial_number=serial_number,
                           product_number=product_number,
                           image_url=image_url)


@app.after_request
def allow_iframe(response):
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    response.headers['Content-Security-Policy'] = "frame-ancestors *"
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
