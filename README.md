# Đồ án Khai phá dữ liệu: Thuật toán ECLAT

## 1. Giới thiệu

Repository này chứa notebook, dữ liệu đã xử lý và kết quả thực nghiệm phục vụ đồ án môn **Khai phá dữ liệu** với chủ đề **thuật toán ECLAT**.

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
│   │   └── Online Retail.xlsx
│   │
│   └── processed/
│       ├── transactions_cleaned.csv
│       ├── stockcode_description_map.csv
│       └── baskets.csv
│
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   └── 02_chay_thuat_toan_eclat_va_danh_gia.ipynb
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

- `Online Retail.xlsx`: dữ liệu giao dịch gốc dùng trong đồ án.

### `data/processed/`

Chứa dữ liệu đã được làm sạch và chuyển đổi để phục vụ thuật toán ECLAT.

Ví dụ:

- `transactions_cleaned.csv`: dữ liệu sau khi loại bỏ bản ghi lỗi, dữ liệu thiếu hoặc giao dịch không hợp lệ.
- `stockcode_description_map.csv`: bảng ánh xạ mã sản phẩm sang tên sản phẩm.
- `baskets.csv`: dữ liệu dạng basket, trong đó mỗi dòng tương ứng với một giao dịch và cột `Items` là JSON list các sản phẩm trong giao dịch đó.

### `notebooks/`

Chứa các notebook dùng để trình bày quá trình xử lý và chạy demo.

- `01_data_preprocessing.ipynb`: đọc dữ liệu, làm sạch dữ liệu và tạo dữ liệu dạng basket.
- `02_chay_thuat_toan_eclat_va_danh_gia.ipynb`: chạy thuật toán ECLAT, sinh association rules, thử nghiệm ngưỡng support và phân tích kết quả.

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
openpyxl
jupyter
```

Tùy cách triển khai, nhóm có thể bổ sung thêm thư viện khác.

## 6. Cách chạy demo

Đồ án chạy trực tiếp bằng notebook. Có thể mở Jupyter Notebook hoặc JupyterLab rồi chạy lần lượt:

```text
01_data_preprocessing.ipynb
02_chay_thuat_toan_eclat_va_danh_gia.ipynb
```

Notebook `01_data_preprocessing.ipynb` tạo dữ liệu đã làm sạch và file basket trong `data/processed/`.

Notebook `02_chay_thuat_toan_eclat_va_danh_gia.ipynb` đọc `data/processed/baskets.csv`, chạy ECLAT, sinh luật kết hợp và lưu kết quả vào `results/`.

Cột `Items` trong `baskets.csv` được lưu dưới dạng JSON list để giữ nguyên tên sản phẩm gốc, kể cả sản phẩm có dấu phẩy trong mô tả.

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
- Notebook demo.
- Dữ liệu gốc hoặc link dữ liệu.
- Dữ liệu đã xử lý nếu có.
- Kết quả frequent itemsets và association rules.
- README hướng dẫn cài đặt và chạy demo.
- File kiểm tra đạo văn nếu giảng viên yêu cầu.

## 12. Tác giả

Nhóm thực hiện: `[Tên nhóm hoặc tên các thành viên]`

Môn học: **Khai phá dữ liệu**

Chủ đề: **Thuật toán ECLAT trong khai phá tập phổ biến và luật kết hợp**
