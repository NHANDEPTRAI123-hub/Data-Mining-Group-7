import pandas as pd
import os

def preprocess_data():
    # Đảm bảo đường dẫn chạy đúng từ thư mục gốc của project
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == 'src':
        os.chdir('..')

    raw_data_path = 'data/raw/Online Retail.xlsx'
    processed_transactions_path = 'data/processed/transactions_cleaned.csv'
    baskets_path = 'data/processed/baskets.csv'

    print(f"Đang đọc dữ liệu từ: {raw_data_path} ...")
    df = pd.read_excel(raw_data_path)

    print("Bắt đầu làm sạch dữ liệu...")
    # Xoá khoảng trắng trùng lặp ở Description
    df['Description'] = df['Description'].str.strip()

    # Loại bỏ các hàng bị thiếu InvoiceNo
    df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
    df['InvoiceNo'] = df['InvoiceNo'].astype('str')

    # Loại bỏ các giao dịch bị hủy (InvoiceNo chứa 'C')
    df = df[~df['InvoiceNo'].str.contains('C')]

    # Loại bỏ các giao dịch có Quantity <= 0
    df = df[df['Quantity'] > 0]

    # Loại bỏ các hàng thiếu Description
    df.dropna(axis=0, subset=['Description'], inplace=True)

    print(f"Số lượng bản ghi giao dịch sau khi làm sạch: {df.shape[0]}")

    # Đảm bảo thư mục lưu trữ đã tồn tại
    os.makedirs('data/processed', exist_ok=True)

    print("Đang lưu dữ liệu giao dịch đã làm sạch...")
    df.to_csv(processed_transactions_path, index=False)
    print(f"Đã lưu thành công tại: {processed_transactions_path}")

    print("Chuyển đổi định dạng giỏ hàng (Baskets)...")
    # Nhóm theo giao dịch để tạo giỏ hàng cho từng hóa đơn
    baskets = df.groupby('InvoiceNo')['Description'].apply(list).reset_index()

    # Chuyển list thành chuỗi các mặt hàng cách nhau bởi dấu phẩy
    baskets['Items'] = baskets['Description'].apply(lambda x: ','.join(x))
    baskets.drop('Description', axis=1, inplace=True)

    baskets.to_csv(baskets_path, index=False)
    print(f"Đã lưu file giỏ hàng thành công tại: {baskets_path}")

if __name__ == "__main__":
    preprocess_data()
