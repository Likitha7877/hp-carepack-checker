
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
    serial = request.args.get("serial")
    product = request.args.get("product")
    return render_template("index.html", serial=serial, product=product)

# @app.route('/')
# def index():
#     return render_template("index.html")



@app.route('/', methods=['POST'])
def check_warranty():
    try:
        data = request.get_json()
        print("📥 Received JSON:", data)

        serial = data.get("serial")
        product = data.get("product")
        role = data.get("role", "guest")  # guest | customer | hp_partner

        print(f"🔧 Serial: {serial}, Product: {product}, Role: {role}")

        # ✅ CALL ONLY ONCE
        result = run_warranty_check(serial, product)

        if "error" in result:
            return jsonify(result)

        # ✅ PARTNER PRICE MAP
        PARTNER_PRICES = {
            "UJ217E": 6490,
            "U4813PE": 5310,
            "U6417E": 8732,
            "U8LH8E": 4750,
            "U8LJ4E": 10148,
            "UN008E": 6962,
            "UB5R2E": 8260,
            "U8LH3E": 4130,
            "U8LH9E": 2950,
            "U8LH9E":2950,
            "U8LH7PE":5310,
            "U0H90E":8909,
            "U6WD1E":13570,
            "UN009E": 8496,
            "UB5R3E": 10620,
            "UN006E": 5310,
            "U0H96E": 4540,
            "U0H93PE": 8437,
            "U0H91E": 13924,
            "U6WD2E": 20650,
            "UN010E": 12930,
            "UB5R4E": 18880,
            "UN007E": 7080,
            "U6WC9E": 4750,
            "UN082PE": 13924,
            "U0H92E": 17110,
            "U6WD3E": 24190,
            "UM952E": 8850,
            "UN011E": 15930,
            "U6WD0E": 7080,
            "UB5R5E": 21830,
            "U0H94PE": 20650,
            # "U9WX1E": 6962,
            "UN062PE": 7552,
            "UB5R2E-U9WX1E": 14041,
            "UB5R3E-U9WX1E": 16401,
            "UB5R4E-U9WX1E": 23482,
            "UB5R5E-U9WX1E": 25842,
            "U9BA7E": 3245,
            "U9BA3E": 2832,
            "U9AZ7E": 3422,
            "U9BA9E": 7198,
            "U9EE7E": 6490,
            "U9EE8E": 9145,
            "UB5U0E": 11092,
            # // "U9EF4E": 1,
            "U9BB1PE": 3835,
            "UK703E": 5546,
            "U86DVE": 5664,
            "UK726E": 7552,
            "UK718E": 11446,
            "U86DXE": 9912,
            # // "U86E0E": 1,
            "UB8B3E": 13747,
            "UK744E": 7552,
            "UK749E": 5546,
            "UB8B6E": 12272,
            "UK738PE": 6018,
            "U4391E": 8732,
            "UC282E": 13452,
            "U7861E": 8496,
            "UC279E": 7198,
            "UB5T7E": 15812,
            "U4416PE": 8732,
            "U85DWE": 8260,
            "U7876E": 19352,
            "UB0E2E": 11092,
            "UB0E6E": 16992,
            "U6578E": 3717,
            # // "U10N3E": 1,
            "U7923E": 6372,
            "U7925E": 7552,
            "U0A83E": 6372,
            "UF360E": 5782,
            "UF361E": 8142,
            "U11C2E": 9912,
            "U0A84E": 3658,
            "U7897E": 3186,
            "U7899E": 4071,
            "U10N7E": 3481,
            "U0A85E": 5192,
            "UF236E": 7552,
            "U11BTE": 4012,
            "U11BVE": 5192,
            "U11BWE": 6372,
            "U5864PE": 3835,
            "U10N2PE": 3835,
            "U7935E": 2537,
            "U4925PE": 2124,
            "U7937E": 4366,
            "U4936PE": 4071,
            "U7944E": 9912,
            "U7942E": 6372,
            "U1G57E": 9204,
            "U1G39E": 7847,
            "U1G37E": 5546,
            "U02BSE": 8437,
            "U10KHE": 16992,
            "U60ZBE": 7670,
            "U60ZCE": 12980,
            "U60ZWE": 15930,
            "U60ZXE": 25370,
            "U61E2E": 13629,
            "U85S0E": 3540,
            "U7936E": 3245,
            "U7934E": 1947,
            "UC9A2E": 7670,
            "UD0N9E": 21240,
            "UC9A5E": 11210,
            "U8TQ9E": 14221,
            "UA5C0E": 3245,
            "U5AD9E": 43133,
            "UZ276E": 16305,
            "UZ277E": 12749,
            "UZ275E": 13270,
            "UG467E": 6411,
            "U04THE": 11091,
            "UZ299E": 6071,
            "UC4X9E": 9800,
            "U04SKE": 9648,
            "UC4X7E": 9601,
            "U6M74E": 9426,
            "UZ287E": 9274,
            "UC4X5E": 8353,
            "UB4W7E": 5538,
            "UZ260E": 8326,
            "UG482E": 5495,
            "UZ298E": 5204,
            "UZ297E": 5204,
            "UC4Y1E": 5204,
            "U62F5E": 5204,
            "UZ289E": 5204,
            "UG468E": 7327,
            "U6M72E": 4987,
            "U6M85E": 6938,
            "U42GXPE": 5109,
            "UZ272E": 4510,
            "UB4X9E": 4515,
            "U04TKE": 4357,
            "UZ296E": 4337,
            "UG470E": 4215,
            "U9MW4PE": 14408,
            "U8TM2E": 5140,
            "UG350E": 3864,
            "UZ295E": 3903,
            "UZ303E": 4770,
            "U34XRE": 7200,
            "UB4Z1E": 3772,
            "U04SME": 3630,
            "UG349E": 3469,
            "UZ304E": 3469,
            "UH267E": 4119,
            "UH773E": 3154,
            "UQ463E": 3469,
            "U1G24PE": 7269,
            "UG348E": 2602,
            "UG347E": 2602,
            "UG337E": 2602,
            "U35PFE": 3829,
            "UG481E": 2313,
            "U57D7E": 2313,
            "U62F3E": 2207,
            "UB4V5E": 2206,
            "UG062E": 1995,
            "UG346E": 1995,
            "UG338E": 1735,
            "UG361E": 1735,
            "UG334E": 1518,
            "U9NR3PE": 1558,



        }

        # ✅ APPLY PARTNER PRICING
        for pack in result.get("care_packs", []):
            sku = pack.get("part")

            try:
                regular_price = int(pack.get("price", 0))
            except ValueError:
                regular_price = 0

            final_price = regular_price
            is_partner_price = False

            if role == "hp_partner" and sku in PARTNER_PRICES:
                final_price = PARTNER_PRICES[sku]
                is_partner_price = True

            pack["regular_price"] = regular_price
            pack["price"] = final_price
            pack["is_partner_price"] = is_partner_price

        # ✅ EOSL LOGIC (UNCHANGED)
        final_product = result.get("product_number") or product
        product_clean = final_product.strip().upper() if final_product else None

        if product_clean:
            result["eosl_date"] = eosl_data.get(product_clean)
        else:
            result["eosl_date"] = None

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
            price = pack.get("price")
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
            cc=["aayushi@arminfoserve.com","abhay@arminfoserve.com"],
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

