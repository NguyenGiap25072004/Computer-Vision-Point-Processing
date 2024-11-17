# Computer-Vision-Point-Processing
Cải thiện hình ảnh qua xử lý điểm (Image Enhancement Point Processing)
- Cải thiện hình ảnh trong miền không gian cơ bản:
   + Các phép cải thiện hình ảnh trong miền không gian chủ yếu có thể được rút gọn thành dạng g(x,y) = T[f(x,y)]
   + trong đó f(x,y) là hình ảnh đầu vào, g(x,y) là hình ảnh đã được xử lý, và T là một toán tử được định nghĩa trên một vùng lân cận của (x,y).
- Point processing
   + Các phép toán miền không gian đơn giản nhất xảy ra khi vùng lân cận đơn giản chỉ là chính pixel đó.
   + Trong trường hợp này, T được gọi là hàm biến đổi mức xám hoặc phép toán xử lý điểm. Các phép toán xử lý điểm có dạng: s = T(r)
   + trong đó s đề cập đến giá trị pixel của hình ảnh đã được xử lý và r đề cập đến giá trị pixel của hình ảnh gốc.

1. Negative images (hình ảnh âm)
- Hình ảnh âm rất hữu ích trong việc cải thiện các chi tiết trắng hoặc xám nằm trong các vùng tối của một bức ảnh.
- s = intensity(max) - r

2. Thresholding (ngưỡng)
- Các biến đổi ngưỡng đặc biệt hữu ích cho việc phân đoạn, trong đó chúng ta muốn tách biệt một đối tượng quan tâm khỏi nền.
- s = { 1.0 r > threshold or 0.0 r <= threshold

3. Logarithmic transformation (biến đổi Logarit)
- Dạng tổng quát của phép biến đổi logarit là: s = c ∗ log 1 + r
- Trong đó c là hằng số, r bị giới hạn trong khoảng [0,255], ta có thể chọn c để giới hạn output s. Với c = 255/log(256) , s ∈ [0, 255].
- Phép biến đổi Logarithmic Transformations ánh xạ một phạm vi hẹp các giá trị mức xám thấp trong ảnh đầu vào thành một phạm vi rộng hơn các giá trị đầu ra. Điều ngược lại đúng với các giá trị cao của các mức đầu vào.
- Chúng ta sử dụng phép biến đổi log để mở rộng giá trị của các dark pixel trong một ảnh trong khi nén các giá trị mức cao hơn.
- Nó nén phạm vi động của các ảnh có sự biến đổi lớn về giá trị pixel.
- Phép biến đổi log nghịch đảo thực hiện biến đổi ngược lại.
- Các hàm log đặc biệt hữu ích khi các giá trị mức xám đầu vào có thể có một phạm vi giá trị cực kỳ lớn.
- s = c ∗ log(1 + r)
- Ta thường lấy c = 1

4. Power law transforms (biến đổi theo luật công suất)
- Biến đổi theo luật công suất có dạng sau: s = c ∗ r ^ γ
- Ánh xạ một phạm vi hẹp các giá trị dark input thành một phạm vi rộng hơn các giá trị output, và điều ngược lại đúng với các giá trị cao hơn.
- Thay đổi γ tạo ra một họ đường cong.
- s = c ∗ r ^ γ
- Ta thường lấy c = 1
- Mức thang xám phải nằm trong [0.0, 1.0]

5. Grey level slicing (cắt mức xám)
- Tự tìm hiểu

6. Bit plane slicing (cắt mặt phẳng bit)
- Giá trị pixel là một số nguyên được tạo thành từ một dãy nhị phân 8 bits. Ý tưởng của bit-plane slicing là: thay vì biểu diễn ảnh bằng giá trị của các pixel, ta biểu diễn nó bằng 8 tầng ảnh, mỗi tầng tương ứng với mỗi bit.
- Thường thì bằng cách cách ly các bit cụ thể của giá trị pixel trong một hình ảnh, chúng ta có thể làm nổi bật các khía cạnh thú vị của hình ảnh đó.
   + Các bit bậc cao thường chứa hầu hết thông tin hình ảnh quan trọng.
   + Các bit bậc thấp chứa các chi tiết tinh tế (subtle details).












