# Khai Thác Luật Kết Hợp Trên Dữ Liệu Instacart

## 1. Giới Thiệu

Dự án phân tích dữ liệu giỏ hàng Instacart để tìm các nhóm sản phẩm thường được mua cùng nhau. Kết quả của dự án gồm dữ liệu đã xử lý, bảng phân tích hành vi mua hàng, tập phổ biến, luật kết hợp, phần cải tiến phương pháp và ứng dụng gợi ý sản phẩm bằng Streamlit.

## 2. Dataset

Dữ liệu sử dụng gồm 6 file nguồn:

| File | Nội dung |
|---|---|
| `orders.csv` | Thông tin đơn hàng, người dùng, thứ tự mua, ngày mua và giờ mua |
| `order_products__prior.csv` | Dữ liệu giỏ hàng chính dùng để khai thác luật kết hợp |
| `order_products__train.csv` | Dữ liệu phụ dùng để kiểm chứng kết quả |
| `products.csv` | Danh mục sản phẩm |
| `aisles.csv` | Nhóm hàng chi tiết |
| `departments.csv` | Nhóm hàng lớn |

## 3. Cấu Trúc Thư Mục

```text
app/
  streamlit_app.py

notebooks/
  00_core.ipynb
  01_data.ipynb
  02_eda.ipynb
  03_rules.ipynb
  04_improvement.ipynb
  05_app.ipynb

outputs/
  data/
  tables/
  figures/

requirements.txt
README.md
```

## 4. Thứ Tự Chạy Notebook

Chạy các notebook theo thứ tự sau:

| Thứ tự | Notebook | Nội dung chính |
|---|---|---|
| 1 | `00_core.ipynb` | Khai báo thư viện, cấu hình, class và hàm dùng chung |
| 2 | `01_data.ipynb` | Đọc dữ liệu, làm sạch, chuẩn hóa và xuất dữ liệu đã xử lý |
| 3 | `02_eda.ipynb` | Phân tích hành vi mua hàng và xuất biểu đồ |
| 4 | `03_rules.ipynb` | Khai thác tập phổ biến, sinh luật kết hợp và so sánh thuật toán |
| 5 | `04_improvement.ipynb` | Cải tiến luật bằng weighted rules, time-aware rules và kiểm chứng train |
| 6 | `05_app.ipynb` | Chuẩn bị dữ liệu cho ứng dụng và chạy Streamlit |

## 5. Kết Quả Đầu Ra

| Thư mục | Nội dung |
|---|---|
| `outputs/data/` | Dữ liệu trung gian dùng cho các bước sau |
| `outputs/tables/` | Bảng kết quả dùng cho báo cáo và ứng dụng |
| `outputs/figures/` | Biểu đồ phân tích hành vi mua hàng và luật kết hợp |

Các file quan trọng cho ứng dụng:

| File | Vai trò |
|---|---|
| `outputs/tables/frequent_products.csv` | Danh sách sản phẩm hiển thị trong bộ chọn |
| `outputs/tables/weighted_rules.csv` | Luật kết hợp đã xếp hạng bằng weighted score |
| `outputs/tables/time_aware_rules.csv` | Luật kết hợp theo giờ mua hàng |
| `outputs/tables/top_rules.csv` | Luật kết hợp cơ bản |

## 6. Chạy Ứng Dụng

Ứng dụng Streamlit được chạy từ `notebooks/05_app.ipynb`.

Trong notebook này, chạy cell khởi động Streamlit. Sau khi server chạy, mở địa chỉ:

```text
http://localhost:8501
```

File giao diện của ứng dụng nằm tại:

```text
app/streamlit_app.py
```

## 7. Chức Năng Ứng Dụng

| Trang | Chức năng |
|---|---|
| `Products` | Tìm sản phẩm và thêm vào giỏ hàng |
| `Recommendations` | Gợi ý sản phẩm dựa trên giỏ hàng hiện tại |

Trang `Recommendations` gồm hai chế độ:

| Chế độ | Ý nghĩa |
|---|---|
| `Basket-based` | Gợi ý theo luật kết hợp từ các sản phẩm đang có trong giỏ |
| `Time-aware` | Gợi ý theo luật kết hợp có xét thêm giờ mua hàng |

## 8. Thuật Toán Và Cải Tiến

| Nhóm | Nội dung |
|---|---|
| Khai thác luật | FP-Growth, Apriori, H-Mine, ECLAT |
| Đánh giá luật | `support`, `confidence`, `lift` |
| Cải tiến | Weighted rule ranking, time-aware rule strength |
| Kiểm chứng | So sánh luật khai thác từ prior với dữ liệu train |
