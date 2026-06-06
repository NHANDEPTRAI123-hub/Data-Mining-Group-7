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
- Item phổ biến nhất: WHITE HANGING HEART T-LIGHT HOLDER (support = 11.33%, 2260 transaction).
- Tập item đi cùng nhau phổ biến nhất: JUMBO BAG RED RETROSPOT | JUMBO BAG PINK POLKADOT (support = 4.13%, 825 transaction).
- Luật có lift cao nhất: ROSES REGENCY TEACUP AND SAUCER | GREEN REGENCY TEACUP AND SAUCER -> PINK REGENCY TEACUP AND SAUCER (confidence = 70.57%, lift = 18.38).
- Luật có support lớn nhất: JUMBO BAG PINK POLKADOT -> JUMBO BAG RED RETROSPOT (support = 4.13%, confidence = 67.73%, lift = 6.46).

## Nhận xét
Nhóm nhận thấy các sản phẩm cùng dòng thiết kế hoặc cùng mục đích sử dụng thường xuất hiện chung trong giỏ hàng.
Khi đọc kết quả, nhóm cần xét đồng thời support và lift: lift cao cho biết mối liên hệ nổi bật, còn support cao cho thấy luật xuất hiện trên nhiều giao dịch hơn.
Các luật kết hợp chỉ phản ánh mẫu đồng xuất hiện trong dữ liệu, không khẳng định quan hệ nhân quả giữa các sản phẩm.
