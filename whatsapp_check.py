import sys
import io
import os
os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_SSL_VERIFY'] = '0'
import contextlib
sys.stdout.reconfigure(encoding='utf-8')
from scraper_logic import run_warranty_check
from partner_prices import PARTNER_PRICES
from eosl_data import eosl_data

def format_price(price):
    try:
        p = int(price)
        return "{:,}".format(p)
    except:
        return str(price)

def no_packs_message(result, eosl_date):
    """Message when no care packs are available - picks the right reason."""
    if eosl_date:
        return "This product has reached End of Service Life (EOSL: " + str(eosl_date) + ") and is no longer eligible for a warranty extension."

    status = str(result.get('status', '')).lower()
    remaining = result.get('remaining_days')

    if 'active' in status:
        msg = "Good news - your warranty is currently *Active*"
        if remaining not in (None, '', 'N/A'):
            msg += " with *" + str(remaining) + " days* remaining"
        msg += " (valid until " + str(result.get('end_date', 'N/A')) + ")."
        msg += "\n\nNo additional Care Packs are needed right now. If you need any assistance, feel free to contact us!"
        return msg

    if 'expir' in status:
        # Coverage expiring/expired but EOSL date unknown - post-warranty
        # eligibility cannot be determined automatically.
        return ("Your coverage is expiring soon (valid until " + str(result.get('end_date', 'N/A')) + "). "
                "The EOSL date for this product is not available in our data yet, so our team will "
                "check the post-warranty Care Pack options for you and get back to you soon.")

    return "No compatible Care Packs are currently available for this product. Please contact us for assistance."

def check_serial(serial, product="", is_partner=False):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        result = run_warranty_check(serial, product)

    if "error" in result:
        return "Sorry, we could not find warranty information for serial number " + serial + ". Please check the number and try again."

    start_date = result.get('start_date', 'N/A')
    end_date = result.get('end_date', 'N/A')

    # EOSL lookup - same as website (app.py)
    final_product = result.get("product_number") or product
    product_clean = final_product.strip().upper() if final_product else None
    eosl_date = eosl_data.get(product_clean) if product_clean else None

    if start_date == end_date:
        return "*" + result.get('product_name', 'Your Product') + "*\n\nThis product has reached End of Service Life (EOSL) and is no longer eligible for a warranty extension."

    care_packs = result.get('care_packs', [])

    if is_partner:
        # Partner format: SKU | Plan | Price+GST
        msg = "*" + result.get('product_name', 'Your Product') + "*\n\n"
        if care_packs:
            msg += "*Available Care Packs:*\n"
            for cp in care_packs:
                sku = cp.get('part', '')
                title = cp.get('title', '')
                partner_price = PARTNER_PRICES.get(sku)
                if partner_price:
                    price_ex_gst = round(partner_price / 1.18)
                    price_str = "Rs." + format_price(price_ex_gst) + "+GST"
                else:
                    price_str = "Price on request"
                msg += sku + " | " + title + " | " + price_str + "\n"

            has_post_warranty = any("post warranty" in cp.get('title', '').lower() for cp in care_packs)
            if has_post_warranty:
                msg += "\nThe warranty will start from the date of purchase."
            else:
                msg += "\nCare Pack Start Date: " + str(end_date)
            if eosl_date:
                msg += "\nEOSL Date: " + str(eosl_date)
        else:
            msg += no_packs_message(result, eosl_date)

    else:
        # Customer format: full info with links
        msg = "*Warranty Information for " + result.get('product_name', 'Your Product') + "*\n\n"
        msg += "Start Date: " + str(start_date) + "\n"
        msg += "End Date: " + str(end_date) + "\n"
        msg += "Status: " + str(result.get('status', 'N/A')) + "\n"
        msg += "Remaining Days: " + str(result.get('remaining_days', 'N/A')) + "\n"
        if eosl_date:
            msg += "EOSL Date: " + str(eosl_date) + "\n"
        msg += "\n"
        if care_packs:
            msg += "*Available Care Packs:*\n"
            for cp in care_packs:
                msg += "- " + cp.get('title', '') + ": " + cp.get('url', '') + "\n"
        else:
            msg += no_packs_message(result, eosl_date)

    return msg

if __name__ == "__main__":
    serial = sys.argv[1]
    is_partner = len(sys.argv) > 2 and sys.argv[2] == "partner"
    print(check_serial(serial, is_partner=is_partner))
