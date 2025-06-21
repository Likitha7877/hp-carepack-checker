from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from eosl_data import eosl_data

printer_mapping = {}

product_page_mapping = {
    "U8LH8E": "u8lh8e-hp-laptop-14-15-series-2-years-additional-warranty-extension",
    "U8LJ4E": "u8lj4e-hp-laptop-14-15-series-2-years-additional-warranty-extension-adp",
    "U8LH7PE": "u8lh7pe-hp-14-15-series-1-year-post-warranty",
    "U8LH9E": "u8lh9e-hp-laptop-14-15-series-factory-warranty-add-on-accidental-damage-protection",
    "UB5R2E": "ub5r2e-hp-14-15-series-2-years-additional-warranty-with-one-time-battery-replacement",
    "U9WX1E": "u9wx1e-hp-3-year-adp",
    "U8LH3E": "u8lh3e-hp14-15-2-year-warranty-extension",
    "UN008E": "un008e-hp-laptop-14-15-series-1-year-additional-warranty-extension-with-accidental-damage-protection",
    "UB5R2E-U9WX1E": "ub5r2e-u9wx1e-hp-14-15-series-2-years-additional-warranty-with-one-time-battery-replacement-and-adp",
    "U0H90E": "u0h90e-hp-pavilion-2-years-additional-warranty-extension",
    "U0H96E": "u0h96e-hp-pavilion-factory-warranty-add-on-accidental-damage-protection",
    "UN009E": "un009e-hp-pavilion-1-year-warranty-extension-adp",
    "U6WD1E": "u6wd1e-hp-pavilion-2-year-warranty-with-accidental-damage-protection-adp",
    "U0H93PE": "u0h93pe-hp-pavilion-1-year-post-warranty",
    "UN006E": "un006e-hp-pavilion-1-year-additional-warranty-extension",
    "UB5R3E": "ub5r3e-hp-pavilion-2-years-additional-warranty-with-one-time-battery-replacement",
    "U6WD2E": "u6wd2e-hp-envy-omen-2-years-additional-warranty-extension-with-accidental-damage-protection-adp",
    "UN010E": "un010e-hp-envy-omen-1-year-additional-warranty-extension-with-accidental-damage-protection-adp",
    "U0H91E": "u0h91e-hp-envy-omen-2-years-additional-warranty-extension",
    "U6WC9E": "u6wc9e-hp-envy-omen-factory-warranty-add-on-with-accidental-damage-protection",
    "UB5R4E": "ub5r4e-hp-envy-omen-2-years-additional-warranty-with-one-time-battery-replacement",
    "UN082PE": "un082pe-hp-envy-omen-1-year-post-warranty",
    "UN007E": "un007e-hp-envy-omen-1-year-additional-warranty-extension",
    "UB5R4E-U9WX1E": "ub5r4e-u9wx1e-hp-envy-omen-2-years-additional-warranty-with-one-time-battery-replacement-and-adp",
    
    
}

product_title_mapping = {
   "U8LH8E": {
    "title": "HP Laptop 14/15 Series 2 Years Additional Warranty Extension",
    "price": "6000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/09/14-15s-2HW-1-2.webp",
    "tag"  : "Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U8LJ4E": {
    "title": "HP Laptop 14/15 Series 2 Years Additional Warranty Extension with Accidental Damage Protection",
    "price": "11500",
    "image": "https://arminfoserve.com/wp-content/uploads/2023/09/14-15s-2HWADP.png",
    "tag"  :"Smart Pick",
    "coverage":"in-warranty",
    "duration":"3 year"
    
  },
  "U8LH3E": {
    "title": "HP Laptop 14/15 Series 1 year Additional Warranty Extension",
    "price": "4000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-1HW-3.webp",
    "coverage": "in-warranty",
    "duration":"2 year"
    
  },
  "UN008E": {
    "title": "HP Laptop 14/15 Series 1 Year Additional Warranty Extension with Accidental Damage Protection",
    "price": "7500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-1HWADP.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U8LH9E": {
    "title": "HP Laptop 14/15 Series Factory Warranty add-on Accidental Damage Protection",
    "price": "4500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-ADP.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  "UB5R2E": {
    "title": "HP 14/15 Series 2 Years Additional Warranty with One-Time Battery Replacement",
    "price": "10000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U8LH7PE": {
    "title": "HP 14/15 Series 1 year Post Warranty",
    "price": "5500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
  "U0H90E": {
    "title": "HP Pavilion/Victus by HP 2 Years Additional Warranty Extension",
    "price": "9000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-2HW.webp",
    "tag":"Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U6WD1E": {
    "title": "HP Pavilion/Victus by HP 2-Year Warranty with Accidental Damage Protection (ADP)",
    "price": "15500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-2HWADP.webp",
    "tag":"Smart Pick",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UN006E": {
    "title": "HP Pavilion/Victus by HP 1-Year Additional Warranty Extension",
    "price": "5500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "UN009E": {
    "title": "HP Pavilion/Victus by HP 1-Year Warranty Extension with Accidental Damage Protection (ADP)",
    "price": "9500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-1HWADP.webp",
    "tag":"Customer favourite",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U0H96E": {
    "title": "HP Pavilion/Victus by HP Factory Warranty Add-On Accidental Damage Protection",
    "price": "4500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-ADP.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  "UB5R3E": {
    "title": "HP Pavilion/Victus by HP 2 Years Additional Warranty with One-Time Battery Replacement",
    "price": "12500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Pavilion-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "U0H93PE": {
    "title": "HP Pavilion/Victus by HP 1 year Post Warranty",
    "price": "8200",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/14-15s-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
    
  },
   "U0H91E": {
    "title": "HP Envy/Omen 2 Years Additional Warranty Extension",
    "price": "15500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HW.webp",
    "tag":"Essentials",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  
  "UN007E": {
    "title": "HP Envy/Omen 1 Year Additional Warranty Extension",
    "price": "8500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-1HW.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U6WD2E": {
    "title": "HP Envy/Omen 2 Years Additional Warranty Extension with Accidental Damage Protection",
    "price": "24500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HWADP.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UN010E": {
    "title": "HP Envy/Omen 1-year Additional Warranty Extension with Accidental Damage Protection",
    "price": "12500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-1HWADP.webp",
    "coverage":"in-warranty",
    "duration":"2 year"
  },
  "U6WC9E": {
    "title": "HP Envy/Omen Factory Warranty Add-On with Accidental Damage Protection",
    "price": "6500",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-ADP.webp",
    "coverage":"in-warranty",
    "duration":"1 year"
  },
  "UB5R4E": {
    "title": "HP Envy/Omen 2 Years Additional Warranty with One-Time Battery Replacement",
    "price": "23000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-2HWBATT.webp",
    "coverage":"in-warranty",
    "duration":"3 year"
  },
  "UN082PE": {
    "title": "HP Envy/Omen 1 year Post Warranty",
    "price": "14000",
    "image": "https://arminfoserve.com/wp-content/uploads/2024/01/Envy-PW.webp",
    "coverage":"post-warranty",
    "duration":"1 year"
  },
    "U9WX1E": {
        "title": "Accidental Damage Protection Add on for 3 years Extended Warranty",
        "price": "0",
        "image": "https://arminfoserve.com/wp-content/uploads/2024/09/14-15s-2HW-1-2.webp",
        "coverage": "in-warranty",
        "duration":"3 year"
    }
}

def calculate_remaining_days(end_date_str):
    try:
        end_date = datetime.strptime(end_date_str, "%B %d, %Y").date()
        today = datetime.today().date()

        if end_date < today:
            return "0 Days"

        total_days = (end_date - today).days
        years = total_days // 365
        months = (total_days % 365) // 30
        days = (total_days % 365) % 30

        parts = []
        if years > 0:
            parts.append(f"{years} Year{'s' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} Month{'s' if months > 1 else ''}")
        if days > 0:
            parts.append(f"{days} Day{'s' if days > 1 else ''}")

        return ", ".join(parts) if parts else "0 Days"
    except Exception:
        return "N/A"

def run_warranty_check(serial_number, product_number=None, eosl_data=eosl_data):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    wait = WebDriverWait(driver, 7)

    try:
        driver.get("https://support.hp.com/in-en/check-warranty")

        try:
            btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Accept All Cookies')]")
            ))
            btn.click()
        except Exception as e:
            print("Error while selecting cookies:", e)


        sn_input = wait.until(EC.presence_of_element_located((By.ID, "inputtextpfinder")))
        sn_input.clear()
        sn_input.send_keys(serial_number)

        submit = driver.find_element(By.CLASS_NAME, "button-box")
        driver.execute_script("arguments[0].removeAttribute('disabled')", submit)
        submit.click()
        time.sleep(5)
        
        need_pn = driver.find_elements(By.XPATH,
            "//p[contains(@class,'errorTxt') and contains(text(),'cannot be identified')]"
        )
        if need_pn:
            if not product_number:
                return {"error": "Please enter the product number."}
            pn_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.productNumField.input-box")))
            pn_input.clear()
            pn_input.send_keys(product_number)
            btn2 = driver.find_element(By.ID, "FindMyProductNumber")
            driver.execute_script("arguments[0].removeAttribute('disabled')", btn2)
            btn2.click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-info-text h2")))

        name_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-info-text h2")))
        product_name = driver.execute_script("return arguments[0].innerText;", name_el).strip()

        try:
            info = driver.find_element(By.CSS_SELECTOR, "div.serial-product-no")
            text = driver.execute_script("return arguments[0].innerText;", info)
            m = re.search(r"[Pp]roduct\s*:\s*(\S+)", text)
            extracted_product_number = m.group(1).strip() if m else ""
        except:
            extracted_product_number = ""

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.product-image")))
            img_el = driver.find_element(By.CSS_SELECTOR, "img.product-image")
            image_url = img_el.get_attribute("src")
        except:
            image_url = ""

        sections = driver.find_elements(By.CLASS_NAME, "info-section")
        warranty_data = None
        carepack_active = False

        for sec in sections:
            items = sec.find_elements(By.CLASS_NAME, "info-item")
            data = {}
            for it in items:
                try:
                    lbl = it.find_element(By.CLASS_NAME, "label").text.strip()
                    val = it.find_element(By.CLASS_NAME, "text").text.strip()
                    data[lbl] = val
                except Exception as e:
                    print("Error while extracting info-item:", e)


            cov = data.get("Coverage type", "").lower()
            sts = data.get("Status", "").lower()
            service_type = data.get("Service type", "").lower()

            if cov in ["care pack", "contract","bundled warranty"] and sts in ["active","coverage expiring","upcoming"] and service_type:
                warranty_data = data
                carepack_active = True
                break

            if not carepack_active and cov == "factory warranty" and any(
                k in service_type for k in ("hardware maintenance", "hardware replacement")
            ):
                warranty_data = data
        
        care_packs = []
        addon_text = None
        if carepack_active:
            addon_parts = []
            for sec in sections:
                items = sec.find_elements(By.CLASS_NAME, "info-item")
                for it in items:
                    try:
                        label = it.find_element(By.CLASS_NAME, "label").text.strip().lower()
                        if label in ["service level", "deliverables"]:
                            text_div = it.find_element(By.CLASS_NAME, "text")
                            text_content = text_div.text.strip().lower()
                            accidental_matches = re.findall(r"\b(accidental[^\n,]*)", text_content, re.IGNORECASE)
                            for match in accidental_matches:
                                cleaned = match.strip().title()
                                if cleaned not in addon_parts:
                                    addon_parts.append(cleaned)
                            defective_matches = re.findall(r"\b(defective[^\n,]*)", text_content, re.IGNORECASE)
                            for match in defective_matches:
                                cleaned = match.strip().title()
                                if cleaned not in addon_parts:
                                    addon_parts.append(cleaned)
                    except:
                        continue
            if addon_parts:
                addon_text = ", ".join(addon_parts)

     
         
        def carepack_duration(start_date, end_date):
            try:
                start_date_obj = datetime.strptime(start_date, "%B %d, %Y")
                end_date_obj = datetime.strptime(end_date, "%B %d, %Y")
                delta = relativedelta(end_date_obj, start_date_obj)
                return delta.years, delta.months
            except Exception as e:
                print("❌ Error parsing start/end date:", e)
                return None, None
                    
        start = datetime.strptime(warranty_data["Start date"], "%B %d, %Y")
        end_date_obj = datetime.strptime(warranty_data["End date"], "%B %d, %Y").date()
        span = relativedelta(end_date_obj, start)
        years, months = span.years, span.months

        def is_eligible_by_span(years,months,duration_str,addon_text,part_sku,plan_cov,warranty_status,product_number,eosl_data,end_date):
            dur          = duration_str.strip().lower()
            has_adp      = bool(addon_text and addon_text.strip())
            sku          = part_sku.upper()
            cov          = plan_cov.strip().lower()
            sts          = warranty_status.strip().lower()
            total_months = years * 12 + months
            today        = datetime.today().date()

            if 11 <= total_months < 15:
                if sku == "U9WX1E":
                    return False

                # Active/expiring: only in-warranty plans, any of 1/2/3 year
                if sts in ("active", "coverage expiring"):
                    if cov !="in-warranty":
                        return False
                    return dur in ("1 year","2 year","3 year")

                # Expired: now allow post-warranty or 3-year based on 2-yr anniversary proximity
                if sts == "expired":
                    # time until 2-year mark
                    two_year_ann = end_date + timedelta(days=730)
                    days_to_2yr  = (two_year_ann - today).days

                    if 0 < days_to_2yr < 90:
                        # within 3 months of 2-year mark
                        return (dur == "3 year") or (cov == "post-warranty")
                    if days_to_2yr >= 365:
                        # more than a year away from 2-year mark
                        return dur in ("2 year","3 year")
                return False

            # 15–23 months: 2- and 3-year plans (never add-on)
            elif 15 <= total_months < 23:
                return cov == "in-warranty" and sku != "U9WX1E" and dur in ("2 year", "3 year")

            # 23–35 months: only 3-year plans (never add-on)
            elif 23 <= total_months < 35:
                return cov == "in-warranty" and sku != "U9WX1E" and dur == "3 year"

            # ≥ 35 months: show both EOSL 1-year post-warranty **and** ADP add-on when valid
            elif total_months >= 35:
                # EOSL 1-year plan condition
                eosl_ok = False
                eosl_str = eosl_data.get(product_number)
                if eosl_str:
                    try:
                        eosl_date = datetime.strptime(eosl_str, "%d-%m-%Y").date()
                    except Exception:
                        pass
                    else:
                        days_remaining = (end_date - today).days
                        if (
                            eosl_date == today + timedelta(days=365)
                            and sts in ("active", "coverage expiring","expired")
                            and days_remaining < 90
                            and cov == "post-warranty"
                            and dur == "1 year"
                        ):
                            eosl_ok = True

                # ADP add-on condition
                adp_ok = (not has_adp) and (sku == "U9WX1E")

                # include either or both
                return eosl_ok or adp_ok

            return False

        def is_commercial_model(name: str) -> bool:
            kws = [
                "240","245","255","250","340","345","350","355",
                "elitedesk","prodesk","microtower",
                "probook","elitebook","zbook","pro"
            ]
            nl = name.lower()
            return any(kw in nl for kw in kws)
        def is_eligible_commercial_span(years, months, duration_str, plan_cov):
            total_months = years * 12 + months
            dur = duration_str.strip().lower().rstrip("s")
            cov = plan_cov.strip().lower()

            if 11 <= total_months < 15:
                return dur in ("1 year","2 year","3 year","5 year")
            if 15 <= total_months < 23:
                return dur in ("2 year","3 year","5 year")
            if 23 <= total_months < 35:
                return dur in ("3 year","5 year")
            if 35 <= total_months < 59:
                return dur == "5 year"
            if total_months >= 59:
                return cov == "post-warranty"
            return False




        # 1. Extract actual warranty data fields
        actual_start_date = warranty_data.get("Start date")
        actual_end_date = warranty_data.get("End date")
        actual_status = warranty_data.get("Status", "")
        actual_coverage_type = warranty_data.get("Coverage type", "")
        actual_coverage = warranty_data.get("Coverage", "")
        addon_parts = warranty_data.get("Add-on", "")
        years, months = carepack_duration(actual_start_date, actual_end_date)
        if years is None or months is None:
            return {"error": "Warranty dates could not be parsed."}
    
            
        if warranty_data and warranty_data.get("End date"):
            remaining_days = calculate_remaining_days(warranty_data.get("End date"))
        else:
            remaining_days = None

        name = product_name.lower()
        rules = [
            {
                "includes": ["hp laptop", "x360 14", "chromebook 11", "15", "15s"],
                "excludes": ["pavilion", "victus", "omen", "envy", "spectre", "x360", "chromebook", "notebook"],
                "parts": ["U8LH7PE", "U8LH8E", "U8LJ4E", "UN008E", "UB5R2E", "U8LH3E", "U8LH9E","U9WX1E"]
            },
            {
                "includes": ["pavilion"],
                "excludes": ["All-", "Desktop"],
                "parts": ["U0H90E", "U6WD1E", "UN009E", "UB5R3E", "UN006E", "U0H96E", "U0H93PE"]
            },
             
            {
                "includes": ["victus"],
                "excludes": ["all-"],
                "parts": ["U0H90E", "U6WD1E", "UN009E", "UB5R3E", "UN006E", "U0H96E", "U0H93PE"],
                    
            }, 
               {
                   "includes": ["omen"],
                   "excludes": ["All|desktop"],
                   "parts": ["U0H91E", "U6WD2E", "UN010E", "UB5R4E", "UN007E", "U6WC9E", "UN082PE"], 
                },
                {
                   "includes": ["envy"],
                   "excludes": ["all-"],
                   "parts": ["U0H91E", "U6WD2E", "UN010E", "UB5R4E", "UN007E", "U6WC9E", "UN082PE"], 
                }


        ]

        for rule in rules:
            includes_match = any(re.search(inc, name) for inc in rule["includes"])
            excludes_match = any(re.search(exc, name) for exc in rule["excludes"])
            if includes_match and not excludes_match:
                try:
                    start_date_str = warranty_data.get("Start date")
                    end_date_str = warranty_data.get("End date")
                    years, months = carepack_duration(start_date_str, end_date_str)

                except Exception as e:
                    print("❌ Error parsing warranty duration:", e)
                    years = None
                    months = None

                for part in rule["parts"]:
                    slug = product_page_mapping.get(part)
                    details = product_title_mapping.get(part, {})
                    title = details.get("title")
                    price = details.get("price")
                    image = details.get("image")
                    tag = details.get("tag")
                    coverage = details.get("coverage", "")
                    duration = details.get("duration", "")
                    status = warranty_data.get("Status", "")
                    coverage_type = warranty_data.get("Coverage type", "")
                    end_date = warranty_data.get("End date")
                    plan_cov      = details.get("coverage", "")
                    warranty_stat = warranty_data.get("Status", "")
                    product_num   = extracted_product_number
                    name_low = product_name.lower()
                    commercial = is_commercial_model(product_name)

                    
                    if is_commercial_model(product_name):
                        ok = is_eligible_commercial_span(years, months, duration, plan_cov)
                    else:
                        ok = is_eligible_by_span(years, months,duration, addon_text, part,plan_cov, warranty_stat,product_num, eosl_data,end_date_obj) 
                    if ok and slug:
                        care_packs.append({
                            "label": "Recommended Care Pack",
                            "part": part,
                            "title": title,
                            "price": price,
                            "image": image,
                            "tag": tag,
                            "url": f"https://arminfoserve.com/product/{slug}/"
                        })
                        
       
                if not care_packs:
                    actual_service_level = warranty_data.get("Service level", "")
                    actual_status = warranty_data.get("Status", "")
                    actual_coverage = warranty_data.get("Coverage", "")
                    actual_coverage_type = warranty_data.get("Coverage Type", "")
                    product_number = warranty_data.get("Product Number", "")
        

        current_date_str = datetime.today().strftime("%B %d, %Y")

        if warranty_data:
            return {
                "product_name": product_name,
                "product_number": extracted_product_number,
                "coverage_type": warranty_data.get("Coverage type"),
                "start_date": warranty_data.get("Start date"),
                "end_date": warranty_data.get("End date"),
                "status": warranty_data.get("Status"),
                "image_url": image_url,
                "remaining_days": remaining_days if remaining_days is not None else "N/A",
                "current_date": current_date_str,
                "care_packs": care_packs,
                "addon": addon_text
            }
        else:
            return {"error": "No valid warranty information found."}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()