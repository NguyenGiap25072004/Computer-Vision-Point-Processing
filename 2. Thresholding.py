# Hàm đọc ảnh từ file (giả sử ảnh là file .ppm hoặc định dạng nhị phân đơn giản)
def read_image(file_path):
    with open(file_path, 'rb') as f:
        header = f.readline().decode().strip()
        if header != 'P6':  # Kiểm tra định dạng PPM đơn giản
            raise ValueError("Chỉ hỗ trợ ảnh PPM dạng P6!")
        dimensions = f.readline().decode().strip().split()
        width, height = map(int, dimensions)
        max_val = int(f.readline().decode().strip())
        if max_val != 255:
            raise ValueError("Giá trị tối đa không phải 255!")
        
        # Đọc dữ liệu điểm ảnh
        pixels = list(f.read())
        return width, height, pixels

# Hàm ghi ảnh sau xử lý ra file
def write_image(file_path, width, height, pixels):
    with open(file_path, 'wb') as f:
        f.write(b'P6\n')
        f.write(f"{width} {height}\n".encode())
        f.write(b'255\n')
        f.write(bytearray(pixels))

# Hàm áp dụng Thresholding
def apply_thresholding(width, height, pixels, threshold):
    new_pixels = []
    for i in range(0, len(pixels), 3):  # 3 bytes cho mỗi pixel RGB
        # Tính giá trị xám (gray) của pixel
        gray = int(0.299 * pixels[i] + 0.587 * pixels[i + 1] + 0.114 * pixels[i + 2])
        # So sánh với ngưỡng threshold
        value = 255 if gray >= threshold else 0
        new_pixels.extend([value, value, value])  # RGB đều giống nhau (ảnh xám)
    return new_pixels

# Chạy thử chương trình
if __name__ == "__main__":
    # Đường dẫn tới ảnh gốc và ảnh kết quả
    input_file = "E:/Dowload/moon.ppm"  # Đổi tên file cho phù hợp
    output_file = "output.ppm"
    
    # Đọc ảnh từ file
    width, height, pixels = read_image(input_file)
    
    # Áp dụng thuật toán Thresholding với ngưỡng 128
    threshold = 128
    new_pixels = apply_thresholding(width, height, pixels, threshold)
    
    # Ghi ảnh sau xử lý ra file
    write_image(output_file, width, height, new_pixels)
    print(f"Đã lưu ảnh sau xử lý tại: {output_file}")
