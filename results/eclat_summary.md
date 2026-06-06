# Kết luận thực nghiệm ECLAT

## Tham số chạy
- Số transaction: 19952
- Số item riêng biệt: 4042
- Min support: 0.02 (400 transaction)
- Min confidence: 0.5
- Min lift: 1.0

## Kết quả chính
- Số frequent itemsets tìm được: 376
- Số association rules thỏa ngưỡng: 60
- Cấu trúc frequent itemsets theo kích thước: 1-itemset: 295, 2-itemset: 78, 3-itemset: 3.
- Item phổ biến nhất: WHITE HANGING HEART T-LIGHT HOLDER (support = 11.33%, 2260 transaction).
- Tập item đi cùng nhau phổ biến nhất: JUMBO BAG RED RETROSPOT | JUMBO BAG PINK POLKADOT (support = 4.13%, 825 transaction).
- Luật có lift cao nhất: ROSES REGENCY TEACUP AND SAUCER | GREEN REGENCY TEACUP AND SAUCER -> PINK REGENCY TEACUP AND SAUCER (confidence = 70.57%, lift = 18.38).
- Luật có support lớn nhất: JUMBO BAG PINK POLKADOT -> JUMBO BAG RED RETROSPOT (support = 4.13%, confidence = 67.73%, lift = 6.46).

## Nhận xét kết quả
Nhóm nhận thấy các sản phẩm cùng dòng thiết kế hoặc cùng mục đích sử dụng thường xuất hiện chung trong giỏ hàng.
Khi đọc kết quả, nhóm cần xét đồng thời support và lift: lift cao cho biết mối liên hệ nổi bật, còn support cao cho thấy luật xuất hiện trên nhiều giao dịch hơn.
Các luật kết hợp chỉ phản ánh mẫu đồng xuất hiện trong dữ liệu, không khẳng định quan hệ nhân quả giữa các sản phẩm.

## Kết luận về thuật toán ECLAT
ECLAT phù hợp với bài toán này vì dữ liệu sau tiền xử lý đã ở dạng basket. Khi chuyển sang dạng dọc item -> TID-list, support của itemset được tính bằng phép giao TID-list thay vì quét lại toàn bộ bảng giao dịch nhiều lần.
Với min_support = 0.02, thuật toán tìm được 376 frequent itemsets và 60 luật kết hợp. Số lượng này đủ để phân tích nhưng vẫn kiểm soát được, cho thấy ngưỡng support có vai trò quyết định trong việc giữ kết quả vừa gọn vừa có ý nghĩa.
Các frequent itemsets chỉ mở rộng đến kích thước 3, trong đó phần lớn là 1-itemset và 2-itemset. Điều này cho thấy trên bộ Online Retail, các mẫu mua chung nổi bật chủ yếu là cặp hoặc bộ ba sản phẩm, không phải các nhóm sản phẩm rất lớn xuất hiện lặp lại thường xuyên.
Hạn chế chính của ECLAT là khi min_support đặt quá thấp hoặc số item quá lớn, số phép giao TID-list và bộ nhớ lưu TID-list có thể tăng nhanh. Vì vậy thuật toán cần được dùng cùng bước tiền xử lý tốt và lựa chọn ngưỡng support hợp lý.

## Bổ sung từ thử nghiệm ngưỡng support
- Khi giảm min_support từ 0.02 xuống 0.015, số frequent itemsets tăng từ 376 lên 699 và số association rules tăng từ 60 lên 174. Điều này cho thấy ECLAT sinh thêm nhiều mẫu khi nới ngưỡng, nhưng kết quả cũng dễ nhiễu hơn.
- Khi tăng min_support lên 0.03, số frequent itemsets giảm còn 140 và số association rules còn 13. Kết quả gọn hơn nhưng có thể bỏ sót các quan hệ mua kèm ở nhóm sản phẩm nhỏ.
- Vì vậy, kết luận về thuật toán là ECLAT hoạt động tốt trên dữ liệu basket đã làm sạch, nhưng chất lượng đầu ra phụ thuộc mạnh vào cách chọn min_support. Ngưỡng 0.02 là mức cân bằng cho bộ dữ liệu này.
