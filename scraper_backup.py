from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up browser
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# Step 1: Load page
driver.get("https://support.hp.com/in-en/check-warranty")
print("🔄 Opened HP Warranty Check page")

# Step 2: Accept cookies
try:
    cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All Cookies')]")))
    cookie_btn.click()
    print("🍪 Accepted cookies")
except:
    print("🍪 No cookie popup")

try:
    # Step 3: Ask for serial number
    serial_number = input("Enter your HP Serial Number: ").strip()

    # Step 4: Fill serial number
    serial_input = wait.until(EC.presence_of_element_located((By.ID, "inputtextpfinder")))
    serial_input.clear()
    serial_input.send_keys(serial_number)

    # Step 5: Click submit
    submit_btn = driver.find_element(By.CLASS_NAME, "button-box")
    driver.execute_script("arguments[0].removeAttribute('disabled')", submit_btn)
    submit_btn.click()
    print("🚀 Submitted serial number")

    # Step 6: Wait for reload
    time.sleep(4)

    # Step 7: Check if product number is required
    product_required = driver.find_elements(By.XPATH, "//p[contains(@class, 'errorTxt') and contains(text(), 'cannot be identified')]")

    if product_required:
        print("⚠️ Product number is required.")
        product_number = input("Enter your HP Product Number: ").strip()

        # Step 8: Enter product number
        product_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.productNumField.input-box")))
        product_input.clear()
        product_input.send_keys(product_number)

        # Step 9: Submit again
        submit_btn = driver.find_element(By.ID, "FindMyProductNumber")
        driver.execute_script("arguments[0].removeAttribute('disabled')", submit_btn)
        submit_btn.click()
        print("🔁 Resubmitted with product number")
        time.sleep(5)  # wait for final reload

    # Step 10: Use JS to extract product name
    time.sleep(2)
    try:
        print("🔍 Using JavaScript to fetch product name...")
        product_name_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-info-text h2"))
        )
        product_name = driver.execute_script("return arguments[0].innerText;", product_name_el).strip()
        if product_name:
            print(f"\n✅ Product Name: {product_name}")
        else:
            print("❌ Found element but product name is still blank.")
    except Exception as e:
        print(f"❌ Failed to extract product name via JavaScript: {e}")
        product_name = ""

    # Step 10.1: Extract Product Number using JavaScript innerText from serial-product-no block
    import re

    try:
        print("🔎 Fetching Product Number using JavaScript...")
        container = driver.find_element(By.CSS_SELECTOR, "div.serial-product-no")
        inner_text = driver.execute_script("return arguments[0].innerText;", container).strip()
        print(f"📝 Raw serial-product-no innerText: '{inner_text}'")

        match = re.search(r"[Pp]roduct\s*:\s*(\S+)", inner_text)
        if match:
            extracted_product_number = match.group(1).strip()
            print(f"🆔 Product Number: {extracted_product_number}")
        else:
            print("❌ Could not extract Product Number from innerText.")
            extracted_product_number = ""
    except Exception as e:
        print(f"❌ Failed to extract Product Number via JavaScript: {e}")
        extracted_product_number = ""


    # Step 11: Extract and prioritize Care Pack > Factory Warranty
    info_sections = driver.find_elements(By.CLASS_NAME, "info-section")
    warranty_data = None
    carepack_found = False
    factory_found = False

    for section in info_sections:
        items = section.find_elements(By.CLASS_NAME, "info-item")
        section_data = {}

        for item in items:
            try:
                label = item.find_element(By.CLASS_NAME, "label").text.strip()
                value = item.find_element(By.CLASS_NAME, "text").text.strip()
                section_data[label] = value
            except:
                continue

        # Debug: Print block content
        print("---- Warranty Block ----")
        print(f"Coverage type: {section_data.get('Coverage type')}")
        print(f"Service type:  {section_data.get('Service type')}")
        print(f"Status:        {section_data.get('Status')}")
        print("------------------------")

        coverage_type = section_data.get("Coverage type", "").strip().lower()
        service_type = section_data.get("Service type", "").strip().lower()
        status = section_data.get("Status", "").strip().lower()

        # Step 11.1: Prioritize Active Care Pack
        if coverage_type == "care pack":
            warranty_data = section_data
            carepack_found = True
            break  # Use this, skip everything else

        # Step 11.2: Fallback - Factory warranty with valid service type
        if (
            not carepack_found and
            coverage_type == "factory warranty" and
            any(keyword in service_type for keyword in [
                "hardware maintenance", 
                "hardware replacement"
            ])
        ):
            warranty_data = section_data
            factory_found = True

    # Step 12: Show matched warranty info
    if carepack_found:
        print("\n📋 Active Care Pack Details:")
    elif factory_found:
        print("\n📋 Factory Warranty Details:")
    else:
        print("\n⚠️ No valid care pack or factory warranty found.")

    if warranty_data:
        print(f"Start Date: {warranty_data.get('Start date')}")
        print(f"End Date:   {warranty_data.get('End date')}")
        print(f"Status:     {warranty_data.get('Status')}")

except Exception as e:
    print("❌ Error:", str(e))

finally:
    driver.quit()
