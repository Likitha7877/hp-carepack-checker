import pandas as pd

# Load the Excel file
df = pd.read_excel("Printer product number cp mapping.xlsx")

# Clean up column names
df.columns = [col.strip() for col in df.columns]

# Just to confirm script is running
print("Welcome to HP Care Pack Finder!")

# Get product number input from user
product_number = input("Enter your HP Product Number: ").strip().upper()

# Search for this product number in the mapping
match = df[df['Prod Nbr'].str.upper().str.strip() == product_number]

if not match.empty:
    product_model = match.iloc[0]['Product Model Description']
    cp_3yr = match.iloc[0]['3 yr CP Part']
    woo_3yr = int(match.iloc[0]['Woocommerce URL'])

    print(f"\n🖨️ Product: {product_model}")
    print(f"✅ 3-Year Care Pack: {cp_3yr}")
    print(f"🛒 Add to Cart: https://armserve.co.in/?add-to-cart={woo_3yr}")
else:
    print(f"\n❌ No care pack found for product number: {product_number}")
