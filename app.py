
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

        # 🧱 Prevent further processing if an error occurred
        if "error" in result:
            return jsonify(result)

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
        has_post_warranty = any("post warranty" in pack.get("title", "").lower() for pack in care_packs)
        if has_post_warranty:
            warranty_message = """
            <p style="font-size: 16px; color: #1F48F0; font-family: Poppins, sans-serif;">
            The warranty will start from the date of purchase.
            </p>
            """
        else:
            warranty_message = f"""
            <p style="font-size: 16px; color: #1F48F0; font-family: Poppins, sans-serif;">
            The warranty will start from the date of expiry: 
            <strong>{result.get('end_date')}</strong>
            </p>
            """
        has_post_warranty = any("post warranty" in pack.get("title", "").lower() for pack in care_packs)
        has_adp = any("accidental damage protection" in pack.get("title", "").lower() for pack in care_packs)
        

        # ✅ Generate care pack rows
        rows = ""
        product_name = result.get("product_name", "").lower()
        for pack in care_packs:
            title = pack.get("title", "")
            price = pack.get("price", "")
            url = pack.get("url", "")
            if "accidental damage protection add on for 3 years extended warranty" in title.lower():
                if "pavilion" in product_name:
                    price = "10500"
                elif "14s" in product_name or "15s" in product_name:
                    price = "8500"
                elif "victus" in product_name:
                    price = "10500"
                elif "omen" in product_name or "envy" in product_name:
                    price = "12500"
                elif "spectre" in product_name:
                    price = "18500"
            note_html = ""
            if (
                'accidental damage protection' in title.lower()
                and has_post_warranty
                and has_adp
                ):
                end_date = result.get("end_date", "")
                note_html = f"""
                <div style='font-size: 12px; color: #C00000; margin-top: 4px;'>
                Note: The ADP warranty will expire with the current plan on <strong>{end_date}</strong>.
                </div>
                """
            rows += f"""
            <tr style='background-color: #fff;'>
            <td style='padding: 8px; color:#00208E;'>
            {title}
            {note_html}
            </td>
            <td style='padding: 8px; color:#00208E;'>&#8377;{price}</td>
            <td style='padding: 8px; color:#00208E;'>
            <a href='{url}' style='color: #0033A0; text-decoration: underline;'>BUY NOW</a>
            </td>
            </tr>
            """


        care_pack_html = f"""
        <h3 style="color: #1F48F0; font-size: 26px;font-family: Roboto Slab,sans-serif; margin-top: 30px;">Compatible Care Packs:</h3>
        <table cellpadding="10" cellspacing="0" border="1" style="border-collapse: collapse; width: 100%; font-size: 14px; border:1px solid #BAC3FF; font-family: Roboto Slab, sans-serif;">
            <thead>
                <tr style="background-color: #F0EFFF; color: #0033A0; text-align: left;">
                    <th style="padding: 8px;">Plan</th>
                    <th style="padding: 8px;">Price</th>
                    <th style="padding: 8px;">Buy Now</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """

        # ✅ Email Header with Logos
        email_header = """
       <table style="width: 100%; margin-bottom: 20px;background:#FBFBFF;height:75px;">
       <tr>
       <td style="width: 50%; text-align: left;">
       <img src="https://arminfoserve.com/wp-content/uploads/2025/07/Group-482268-1.png" alt="HP Logo" style="height: 43px;">
       </td>
       <td style="width: 50%; text-align: right;">
       <img src="https://arminfoserve.com/wp-content/uploads/2025/07/Group-1000003567-1.png" alt="ARM Infoserve Logo" style="height: 43px;">
       </tr>
       </table>
       """

        html_content = f"""
        <div style="max-width: 700px; margin: auto; font-family: Poppins, sans-serif; color: #000; line-height: 1.5; border: none; padding: 20px;">
          {email_header}
          <h3 style="margin-bottom: 5px; font-family: Poppins, sans-serif;font-weight:bold;text-transform: uppercase;">Hi {name},</h3>
          <p style="font-size:16px;font-family: Poppins,sans-serif;">
            Thank you for contacting <strong>ARM Infoserve India</strong>, the authorised HP Warranty Extension partner.</p>
            <p style="font-size:16px;font-family: Poppins,sans-serif;">We are delighted to support you with the warranty extension of your <strong>{result.get("product_name")}</strong>.
          </p>

          <div style="background-color: #FBFBFF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #d0dfff;">
            <h4 style="margin: 0 0 10px; color: #00115A;font-weight:Bold;font-family: Poppins,sans-serif;font-size:16px;">User Details</h4>
            <table style="width: 100%; font-size: 14px;">
              <tr><td style="padding: 4px 0;width:150px; color:#00115A;font-weight:500; font-size:16px;font-family: Poppins,sans-serif;">Name</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;"> {name}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-weight:500;font-family: Poppins,sans-serif;">Email</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E;"> {email}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">Phone Number</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;"> {number}</td></tr>
            </table>
          </div>

          <div style="background-color: #FBFBFF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #ddd;">
            <h4 style="margin: 0 0 10px; color: #00115A;font-weight:Bold;font-family: Poppins,sans-serif;font-size:16px;">Product Details</h4>
             <table style="width: 100%; font-size: 14px;">
              <tr><td style="padding: 4px 0;width:150px; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">Status</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;">{result.get("status")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">Product Name</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;">{result.get("product_name")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">Start Date</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;">{result.get("start_date")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">End Date</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;">{result.get("end_date")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">Serial Number</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;">{result.get("serial")}</td></tr>
              <tr><td style="padding: 4px 0; color:#00115A;font-size:16px;font-family: Poppins,sans-serif;font-weight:500;">Product Number</td><td style="font-size:16px;font-family: Poppins,sans-serif;color:#00208E ;">{result.get("product_number")}</td></tr>
            </table>
          </div>

          {care_pack_html}
          {warranty_message}

          <h3 style="font-family: Poppins, sans-serif;font-size:16px;">Terms and Conditions</h3>
          <ul style="font-family: Poppins, sans-serif; line-height: 1.6;font-size:16px;">
              <li>To avail ON-SITE support, please log a complaint at the HP Service Toll-free number <strong>18002587170</strong>.</li>
              <li>The warranty extension covers all hardware parts except the battery, adapter, and physical damage (unless accidental damage protection is included).</li>
              <li>You will receive a certificate of Care Pack from HP within 2 to 3 days of order confirmation.</li>
              <li>Payment for the warranty extension is required in full in advance.</li>
              <li>Kindly make the payment in favour of ARM Infoserve India Pvt. Ltd.</li>
              <li>The principal company, HP, will provide reliable support and assistance.</li>
              <li>Under Battery Protection Support pack or ADP + Battery Protection Support pack only 1 Time Battery Replacement will be allowed if the original purchased Battery life drops below 50% of Charging Capacity of if a Battery cell failure has occurred before the 50% limit is reached.</li>
              <li>Please note that HP's service, support, and warranty commitments do not cover claims resulting from the following:
              <ol type="a" style="margin-top: 8px;">
              <li>Improper use, inadequate site preparation, environmental conditions, or non-compliance with applicable guidelines.</li>
              <li>Unauthorised modifications, improper system maintenance, or calibration not performed by HP or authorised by HP.</li>
              <li>Failure or functional limitations of non-HP software or products that impact systems receiving HP support or service</li
              </ol>
              </li>
              </ol>
              </ul>

          <p style="font-family:Poppins, sans-serif; font-size:16px;">
            For any questions, contact <strong>info@arminfoserve.com</strong> or <strong>9560207904</strong>.
          </p>

          <h3 style="font-family: Poppins, sans-serif;font-size:16px;">Alternative Payment Options:</h3>
          <ul style="font-family: Poppins, sans-serif; line-height: 1.6; font-size:16px;">
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
            cc=["vemulalikitha2002@gmail.com"],
            html=html_content
        )

        # Attach QR Code only
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            qr_path = os.path.join(base_dir, "static", "ARM QR Code.jpg")
            if os.path.exists(qr_path):
                with open(qr_path, "rb") as f:
                    msg.attach("ARM QR Code.jpg", "image/jpeg", f.read())
        except Exception as qr_error:
            print("⚠️ QR attachment error:", qr_error)

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

