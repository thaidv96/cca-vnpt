# Tổng quan bài toán
Dự báo nhu cầu sử dụng là một bài toán quan trọng của các nhà mạng. Từ việc đánh giá thực trạng và đưa ra dự báo về nhu cầu sử dụng của các thuê bao, các nhà mạng có thể đưa ra các chính sách khuyến nghị sản phẩm phù hợp với từng nhóm khách hàng.

# Mục tiêu của bài toán
## Mục tiêu
Mục tiêu của bài toán là dự báo khoảng tiêu dùng về lưu lượng data, lưu lượng thoại nội mạng và ngoại mạng của khách hàng nằm một trong bốn mức sau:

- Không sử dụng

- Sử dụng ít

- Sử dụng trung bình

- Sử dụng nhiều

## Input
Dữ liệu về lưu lượng sử dụng data, lưu lượng thoại nội mạng và ngoại mạng. Tuy nhiên, chỉ xét dữ liệu thoại của các cuộc gọi đi (vì các cuộc gọi đến không phát sinh cước thoại).
## Output
Khoảng tiêu dùng của khách hàng trong tháng tiếp theo (nằm một trong các mức trên)
# Mục tiêu của bài toán

# Phương pháp thực hiện
## Tiền xử lý dữ liệu
- Bước 1: Trích rút các dữ liệu về lưu lượng sử dụng mạng, lưu lượng thoại nội mạng và ngoại mạng

- Bước 2: Chuyển đổi dữ liệu lưu lượng thoại từ bytes -> Metabytes (MB); dữ liệu lưu lượng thoại từ giây về phút.

- Bước 3: Chia lưu lượng sử dụng (data, thoại) thành các khoảng sử dụng (bins) như sau:

    + Không sử dụng (lưu lượng sử dụng bằng 0) => Kí hiệu là A

    + Sử dụng ít (0 < lưu lượng sử dụng <= quantile(1/3)) => Kí hiệu là B

    + Sử dụng trung bình (quantile(1/3) < lưu lượng sử dụng <= quantile(2/3)) => Kí hiệu là C

    + Sử dụng nhiều (lưu lượng sử dụng > quantile(2/3)) => Kí hiệu là D
## Các phương pháp sử dụng 
### Sử dụng tần suất sử dụng trong quá khứ
Phương pháp: Lấy hành vi sử dụng có tần suất xuất hiện lớn nhất trong quá khứ để dự báo cho tháng tiếp theo

test_df: tháng cuối cùng của tập dữ liệu (12/2020)

train_df: toàn bộ các dữ liệu lịch sử trừ tháng cuối cùng
### Moving Average
Công thức tính trung bình của một chuỗi số liệu với kích thước $s$ được biểu diễn như sau:

$\hat{y_i} = \dfrac{y_{i-1} + y_{i-2} + \ldots + y_{i-s}}{s}$

Trong đó: 

- $s$: kích thước cửa sổ

- $y_{i-1}, y_{i-2},\ldots$: chuỗi dữ liệu
### Simple Exponential Smoothing
Phương pháp: Giá trị dự báo tại thời điểm T+1 được tính bằng trung bình có trọng số của chuỗi quan sát trong khoảng thời gian T:

$\hat{y}_{T+1}|T = \alpha y_T + \alpha(1-\alpha)y_{T-1} + \alpha(1-\alpha)^2y_{T-2} + \ldots$

Trong đó:

- $0 < \alpha < 1$: smoothing parameter

- $y_T, y_{T-1}, \ldots$: chuỗi quan sát

### Thuật toán Apriori khai phá luật kết hợp
Phương pháp: 
# Kết quả & phân tích đánh giá

## Dự báo dựa vào tần suất sử dụng trong quá khứ
Sử dụng hành vi có tần suất xuất hiện lớn nhất trong quá khứ để dự báo cho tháng tiếp theo. Kết quả dự báo:

| Lưu lượng sử dụng data | Lưu lượng thoại nội mạng | Lưu lượng thoại ngoại mạng |
| --- | --- | --- |
| 64.4%| 62.4% | 59.4% |

## Moving Average với dữ liệu simple encoding
Encode các mức sử dụng A, B, C, D tương ứng thành các giá trị 0, 1, 2, 3. Sử dụng phương pháp Moving Average với window size = 3 tháng và 6 tháng để dự báo cho tháng tiếp theo. Kết quả được làm tròn xuống số nguyên gần nhất với kết quả. Kết quả dự báo được mô tả trong bảng dưới:


| Window size | Lưu lượng sử dụng data | Lưu lượng thoại nội mạng | Lưu lượng thoại ngoại mạng |
| --- | --- | --- | --- |
| 3 | 71.9% | 65.5% | 60.9% |
|6  | 65.3% |  61.8%| 47.7  |
## Moving Average với dữ liệu mean
Encode các mức sử dụng A, B, C, D tương ứng thành các giá trị trung bình của các nhóm. Sử dụng phương pháp Moving Average với window_size = 3 tháng để dự báo cho tháng tiếp theo. Kết quả dự báo được so sánh với các khoảng sử dụng ứng với từng nhóm (trong bước tiền xử lý) để ra kết quả khoảng sử dụng ứng với từng thuê bao. Kết quả dự báo được mô tả trong bảng dưới:

| Lưu lượng sử dụng data | Lưu lượng thoại nội mạng | Lưu lượng thoại ngoại mạng |
| --- | --- | --- |
| 69.9%| 43.4% | 43.4% |
## Moving Average với dữ liệu log mean encoding
Encode các mức sử dụng A, B, C, D tương ứng thành các giá trị logarit của trung bình các nhóm. Sử dụng phương pháp Moving Average với window_size = 3 tháng để dự báo cho tháng tiếp theo. Kết quả dự báo được so sánh với các khoảng sử dụng ứng với từng nhóm (trong bước tiền xử lý) để ra kết quả khoảng sử dụng ứng với từng thuê bao. Kết quả dự báo được mô tả trong bảng dưới:

| Lưu lượng sử dụng data | Lưu lượng thoại nội mạng | Lưu lượng thoại ngoại mạng |
| --- | --- | --- |
| 47.5%| 42.2% | 26.2% |
## Simple Exponential Smoothing với dữ liệu simple encoding
Encode các mức sử dụng A, B, C, D tương ứng thành các giá trị 0, 1, 2, 3. Sử dụng phương pháp Simple Exponential Smoothing với smoothing parameter = 0.4 và 0.6 để dự báo cho tháng tiếp theo. Kết quả được làm tròn xuống số nguyên gần nhất với kết quả. Kết quả dự báo được mô tả trong bảng dưới:

| Smoothing parameter | Lưu lượng sử dụng data | Lưu lượng thoại nội mạng | Lưu lượng thoại ngoại mạng |
| --- | --- | --- | --- |
| 0.4 | 53.4% | 49.6% | 47.8% |
|0.6  | 53.5% |  49.7%| 48%  |


Một số các hướng thử nghiệm tiếp theo:

- AutoRegression

- Association Rules and Apriori algorithm 
