import pandas as pd
import os

ITEM_SEPARATOR = " ||| "

def preprocess_data():
    # Ensure the working directory is the project root
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == 'src':
        os.chdir('..')

    raw_data_path = 'data/raw/Online Retail.xlsx'
    processed_transactions_path = 'data/processed/transactions_cleaned.csv'
    baskets_path = 'data/processed/baskets.csv'
    mapping_path = 'data/processed/stockcode_description_map.csv'

    print(f"Reading data from: {raw_data_path} ...")
    df = pd.read_excel(raw_data_path)

    print("Starting data cleaning...")
    
    # Drop rows with missing Description
    df.dropna(axis=0, subset=['Description'], inplace=True)
    
    # Convert Description to string and remove leading/trailing whitespaces
    df['Description'] = df['Description'].astype(str).str.strip()

    # Drop rows with missing InvoiceNo
    df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
    df['InvoiceNo'] = df['InvoiceNo'].astype('str')

    # Remove cancelled transactions (InvoiceNo contains 'C')
    df = df[~df['InvoiceNo'].str.contains('C')]

    # Keep only transactions with Quantity > 0
    df = df[df['Quantity'] > 0]

    # Convert StockCode to string and keep only valid product codes using regex
    # Valid codes: 5 digits optionally followed by 1 letter (e.g., '85123', '85123A')
    df['StockCode'] = df['StockCode'].astype('str')
    df = df[df['StockCode'].str.match(r'^\d{5}[a-zA-Z]?$')]

    print(f"Number of transaction records after cleaning: {df.shape[0]}")

    # Ensure processed directory exists
    os.makedirs('data/processed', exist_ok=True)

    print("Saving cleaned transaction data...")
    df.to_csv(processed_transactions_path, index=False)
    print(f"Successfully saved to: {processed_transactions_path}")

    # Create StockCode -> Description mapping table
    print("Creating StockCode -> Description mapping table...")
    mapping = df.groupby('StockCode')['Description'].first().reset_index()
    mapping.to_csv(mapping_path, index=False)
    print(f"Mapping table saved to: {mapping_path}")

    print("Converting to basket format...")
    # Group by transaction, get unique list of product names for each invoice
    baskets = df.groupby('InvoiceNo')['Description'].apply(
        lambda x: ITEM_SEPARATOR.join(sorted(set(x)))
    ).reset_index()
    baskets.columns = ['InvoiceNo', 'Items']

    baskets.to_csv(baskets_path, index=False)
    print(f"Successfully saved basket file to: {baskets_path}")
    print(f"Total number of baskets: {baskets.shape[0]}")

if __name__ == "__main__":
    preprocess_data()
