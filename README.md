# Đồ án Khai phá dữ liệu: Thuật toán ECLAT

## 1. Giới thiệu

Repository này chứa toàn bộ source code, notebook, dữ liệu và tài liệu phục vụ đồ án môn **Khai phá dữ liệu** với chủ đề **thuật toán ECLAT**.

ECLAT là thuật toán dùng để khai phá **frequent itemsets** trong dữ liệu giao dịch bằng cách biểu diễn dữ liệu ở dạng dọc thông qua **TID-list**. Từ các frequent itemsets thu được, đồ án tiếp tục sinh **association rules** và đánh giá các luật bằng các chỉ số như **support**, **confidence** và **lift**.

## 2. Mục tiêu đồ án

- Tìm hiểu bài toán khai phá tập phổ biến và luật kết hợp.
- Trình bày cơ sở lý thuyết của thuật toán ECLAT.
- Minh họa thuật toán ECLAT bằng ví dụ từng bước.
- Tiền xử lý dữ liệu giao dịch để phù hợp với bài toán khai phá luật kết hợp.
- Xây dựng demo chạy thuật toán ECLAT.
- Sinh frequent itemsets và association rules từ dữ liệu thực nghiệm.
- Đánh giá kết quả bằng support, confidence và lift.

## 3. Cấu trúc thư mục

```text
.
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── transactions_raw.csv
│   │   ├── customer_info.csv
│   │   └── product_info.csv
│   │
│   └── processed/
│       ├── transactions_cleaned.csv
│       └── baskets.csv
│
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   └── 02_chay_thuat_toan_eclat_va_danh_gia.ipynb
│
├── src/
│   ├── preprocess_clean_data.py
│   ├── eclat.py
│   ├── association_rules.py
│   └── utils.py
│
├── results/
│   ├── frequent_itemsets.csv
│   ├── association_rules.csv
│   ├── threshold_sensitivity.csv
│   └── figures/
│       ├── top_frequent_itemsets.png
│       ├── top_association_rules.png
│       └── support_sensitivity.png

```

## 4. Mô tả các thư mục chính

### `data/raw/`

Chứa dữ liệu gốc được tải từ nguồn dữ liệu ban đầu. Dữ liệu trong thư mục này không nên chỉnh sửa trực tiếp.

Ví dụ:

- `transactions_raw.csv`: dữ liệu giao dịch gốc.
- `customer_info.csv`: thông tin khách hàng, nếu bộ dữ liệu có.
- `product_info.csv`: thông tin sản phẩm, nếu bộ dữ liệu có.

### `data/processed/`

Chứa dữ liệu đã được làm sạch và chuyển đổi để phục vụ thuật toán ECLAT.

Ví dụ:

- `transactions_cleaned.csv`: dữ liệu sau khi loại bỏ bản ghi lỗi, dữ liệu thiếu hoặc giao dịch không hợp lệ.
- `baskets.csv`: dữ liệu dạng basket, trong đó mỗi dòng tương ứng với một giao dịch và danh sách item trong giao dịch đó.

### `notebooks/`

Chứa các notebook dùng để trình bày quá trình xử lý và chạy demo.

- `01_data_preprocessing.ipynb`: đọc dữ liệu, làm sạch dữ liệu và tạo dữ liệu dạng basket.
- `02_chay_thuat_toan_eclat_va_danh_gia.ipynb`: chạy thuật toán ECLAT, sinh association rules, thử nghiệm ngưỡng support và phân tích kết quả.

### `src/`

Chứa source code chính của đồ án.

- `preprocess_clean_data.py`: xử lý dữ liệu thô và tạo dữ liệu đã làm sạch.
- `eclat.py`: triển khai thuật toán ECLAT.
- `association_rules.py`: sinh luật kết hợp từ frequent itemsets.
- `utils.py`: các hàm hỗ trợ dùng chung.

### `results/`

Chứa kết quả sau khi chạy demo.

- `frequent_itemsets.csv`: danh sách frequent itemsets tìm được.
- `association_rules.csv`: danh sách luật kết hợp được sinh ra.
- `threshold_sensitivity.csv`: bảng so sánh số lượng itemsets/rules khi thay đổi `min_support`.
- `figures/`: các biểu đồ hoặc hình minh họa kết quả thực nghiệm.


## 5. Cài đặt môi trường

Yêu cầu cài đặt Python 3.9 trở lên.

Cài đặt các thư viện cần thiết:

```text
pandas
numpy
matplotlib
jupyter
```

Tùy cách triển khai, nhóm có thể bổ sung thêm thư viện khác.

## 6. Cách chạy demo

### Bước 1: Tiền xử lý dữ liệu

```bash
python src/preprocess_clean_data.py
```

Sau bước này, dữ liệu đã xử lý sẽ được lưu trong thư mục:

```text
data/processed/
```

### Bước 2: Chạy thuật toán ECLAT

```bash
python src/eclat.py
```

Kết quả frequent itemsets sẽ được lưu tại:

```text
results/frequent_itemsets.csv
```

Mặc định script đọc từ `data/processed/transactions_cleaned.csv` để giữ nguyên tên sản phẩm gốc, kể cả các sản phẩm có dấu phẩy trong mô tả. Nếu muốn đọc file basket đã tạo sẵn, có thể truyền:

```bash
python src/eclat.py --input data/processed/baskets.csv
```

### Bước 3: Sinh luật kết hợp

```bash
python src/association_rules.py
```

Kết quả association rules sẽ được lưu tại:

```text
results/association_rules.csv
```

Script cũng tạo thêm file kết luận ngắn:

```text
results/eclat_summary.md
```

### Bước 4: Chạy bằng notebook

Có thể chạy lần lượt các notebook trong thư mục `notebooks/`:

```text
01_data_preprocessing.ipynb
02_chay_thuat_toan_eclat_va_danh_gia.ipynb
```

## 7. Tham số chính

Các tham số có thể điều chỉnh trong quá trình chạy demo:

- `min_support`: ngưỡng support tối thiểu để xác định frequent itemsets.
- `min_confidence`: ngưỡng confidence tối thiểu để giữ lại association rules.
- `min_lift`: ngưỡng lift tối thiểu để chọn các luật có ý nghĩa hơn.

Ví dụ:

```python
MIN_SUPPORT = 0.02
MIN_CONFIDENCE = 0.5
MIN_LIFT = 1.0
```

Các giá trị này có thể thay đổi tùy theo kích thước dữ liệu và mục tiêu phân tích.

## 8. Kết quả đầu ra

Sau khi chạy demo, đồ án cần có các kết quả chính sau:

- Danh sách frequent itemsets.
- Danh sách association rules.
- Giá trị support, confidence và lift của từng luật.
- Một số nhận xét về các item thường xuất hiện cùng nhau.
- Biểu đồ hoặc bảng minh họa kết quả nếu cần.

Với bộ dữ liệu đã tiền xử lý hiện tại và tham số:

```python
MIN_SUPPORT = 0.02
MIN_CONFIDENCE = 0.5
MIN_LIFT = 1.0
```

Kết quả thực nghiệm hiện tại:

- Tổng số transaction: `19,952`.
- Số item riêng biệt: `4,042`.
- Số frequent itemsets tìm được: `376`.
- Số association rules thỏa ngưỡng: `60`.
- Item phổ biến nhất: `WHITE HANGING HEART T-LIGHT HOLDER` với support khoảng `11.33%`.
- Tập item đi cùng nhau phổ biến nhất: `JUMBO BAG RED RETROSPOT` và `JUMBO BAG PINK POLKADOT` với support khoảng `4.13%`.
- Luật có lift cao nhất: `ROSES REGENCY TEACUP AND SAUCER | GREEN REGENCY TEACUP AND SAUCER -> PINK REGENCY TEACUP AND SAUCER`, confidence khoảng `70.57%`, lift khoảng `18.38`.

Notebook đánh giá cũng thử các ngưỡng `min_support = 0.015, 0.02, 0.025, 0.03`. Kết quả này dùng để giải thích lựa chọn `min_support = 0.02`: ngưỡng này tạo ra số lượng luật vừa đủ phân tích, không quá ít như ngưỡng cao và không quá nhiều mẫu hiếm như ngưỡng thấp.

Kết luận: các sản phẩm cùng dòng thiết kế hoặc cùng mục đích sử dụng có xu hướng được mua chung rõ rệt. Các luật có lift lớn hơn `1` cho thấy việc mua nhóm sản phẩm tiền đề làm tăng xác suất mua sản phẩm kết quả so với mức trung bình, vì vậy có thể dùng để gợi ý bán kèm, sắp xếp sản phẩm gần nhau hoặc tạo combo khuyến nghị.

## 9. Nguồn dữ liệu

Nguồn dữ liệu sử dụng trong đồ án cần được ghi rõ trong báo cáo cuối.

Ví dụ nguồn dữ liệu có thể dùng:

- UCI Machine Learning Repository.
- Kaggle.
- Bộ dữ liệu giao dịch do nhóm tự tổng hợp, nếu có nguồn rõ ràng.

Khi sử dụng dữ liệu, cần ghi lại:

- Tên bộ dữ liệu.
- Link tải dữ liệu.
- Ngày truy cập.
- Các trường dữ liệu được sử dụng để tạo transaction và item.

## 10. Phân công công việc

| Thành viên | Vai trò chính | Công việc phụ trách |
|---|---|---|
| Thành viên 1 | Trưởng nhóm, tổng hợp báo cáo | Chương 1, kết luận, format báo cáo, kiểm tra đạo văn, tổng hợp slide |
| Thành viên 2 | Lý thuyết khai phá luật kết hợp | Itemset, frequent itemset, support, confidence, lift |
| Thành viên 3 | Thuật toán ECLAT | TID-list, vertical format, equivalence class, ví dụ minh họa từng bước |
| Thành viên 4 | Dữ liệu và tiền xử lý | Chọn dataset, làm sạch dữ liệu, tạo transaction/basket |
| Thành viên 5 | Demo và kết quả | Chạy ECLAT, sinh association rules, xuất kết quả, chuẩn bị demo |

## 11. Ghi chú khi nộp bài

Trước khi nộp, cần kiểm tra đủ các thành phần sau:

- Báo cáo `.docx` và `.pdf`.
- Slide thuyết trình.
- Source code hoặc notebook demo.
- Dữ liệu gốc hoặc link dữ liệu.
- Dữ liệu đã xử lý nếu có.
- Kết quả frequent itemsets và association rules.
- README hướng dẫn cài đặt và chạy demo.
- File kiểm tra đạo văn nếu giảng viên yêu cầu.

## 12. Tác giả

Nhóm thực hiện: `[Tên nhóm hoặc tên các thành viên]`

Môn học: **Khai phá dữ liệu**

Chủ đề: **Thuật toán ECLAT trong khai phá tập phổ biến và luật kết hợp**
