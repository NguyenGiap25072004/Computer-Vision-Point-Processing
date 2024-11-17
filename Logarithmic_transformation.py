import struct
import math

# Hàm đọc ảnh BMP (24-bit)
def read_bmp(file_path):
    with open(file_path, 'rb') as f:
        # Đọc header của BMP
        header = f.read(14)
        dib_header = f.read(40)

        # Lấy thông tin cơ bản
        file_size = struct.unpack('<I', header[2:6])[0]
        offset = struct.unpack('<I', header[10:14])[0]

        width = struct.unpack('<I', dib_header[4:8])[0]
        height = struct.unpack('<I', dib_header[8:12])[0]
        bit_count = struct.unpack('<H', dib_header[14:16])[0]
        compression = struct.unpack('<I', dib_header[16:20])[0]

        if bit_count != 24 or compression != 0:
            raise ValueError("Chỉ hỗ trợ ảnh BMP 24-bit không nén!")

        # Tìm số byte padding mỗi dòng
        row_size = (width * 3 + 3) // 4 * 4
        padding = row_size - width * 3

        # Đọc dữ liệu điểm ảnh
        f.seek(offset)
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                b, g, r = struct.unpack('BBB', f.read(3))  # BMP lưu theo thứ tự BGR
                row.append((r, g, b))
            f.read(padding)  # Bỏ qua padding
            pixels.append(row)

        return width, height, pixels

# Hàm ghi ảnh BMP (24-bit)
def write_bmp(file_path, width, height, pixels):
    with open(file_path, 'wb') as f:
        # Header BMP
        file_size = 14 + 40 + height * ((width * 3 + 3) // 4 * 4)
        offset = 14 + 40

        # Viết BMP Header
        f.write(b'BM')
        f.write(struct.pack('<I', file_size))
        f.write(b'\x00\x00')  # Reserved
        f.write(b'\x00\x00')  # Reserved
        f.write(struct.pack('<I', offset))

        # Viết DIB Header
        f.write(struct.pack('<I', 40))  # DIB Header size
        f.write(struct.pack('<I', width))
        f.write(struct.pack('<I', height))
        f.write(struct.pack('<H', 1))  # Planes
        f.write(struct.pack('<H', 24))  # Bits per pixel
        f.write(struct.pack('<I', 0))  # Compression
        f.write(struct.pack('<I', file_size - offset))  # Image size
        f.write(struct.pack('<I', 2835))  # X pixels per meter
        f.write(struct.pack('<I', 2835))  # Y pixels per meter
        f.write(struct.pack('<I', 0))  # Colors in color table
        f.write(struct.pack('<I', 0))  # Important color count

        # Viết dữ liệu pixel
        row_size = (width * 3 + 3) // 4 * 4
        padding = row_size - width * 3
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y][x]
                f.write(struct.pack('BBB', b, g, r))  # BMP lưu theo thứ tự BGR
            f.write(b'\x00' * padding)  # Thêm padding

# Hàm áp dụng Logarithmic Transformation
def apply_log_transform(width, height, pixels, c):
    new_pixels = []
    for row in pixels:
        new_row = []
        for r, g, b in row:
            # Áp dụng phép biến đổi logarit: s = c * log(1 + r)
            r_new = min(255, int(c * math.log(1 + r)))
            g_new = min(255, int(c * math.log(1 + g)))
            b_new = min(255, int(c * math.log(1 + b)))
            new_row.append((r_new, g_new, b_new))
        new_pixels.append(new_row)
    return new_pixels

# Chạy thử chương trình
if __name__ == "__main__":
    # Đường dẫn tới ảnh gốc và ảnh kết quả
    input_file = "E:/Picture/uni.bmp"  # Đường dẫn file BMP gốc
    output_file = "output.bmp"
    
    # Đọc ảnh từ file
    width, height, pixels = read_bmp(input_file)
    
    # Tính toán hằng số c
    c = 255 / math.log(256)
    
    # Áp dụng thuật toán Logarithmic Transformation
    new_pixels = apply_log_transform(width, height, pixels, c)
    
    # Ghi ảnh sau xử lý ra file
    write_bmp(output_file, width, height, new_pixels)
    print(f"Đã lưu ảnh sau xử lý tại: {output_file}")
