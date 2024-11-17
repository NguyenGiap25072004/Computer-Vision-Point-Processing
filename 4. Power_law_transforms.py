import struct
import math

# Hàm kiểm tra định dạng file
def detect_format(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(2)
        if header == b'BM':  # BMP định dạng
            return "BMP"
        elif header[:2] == b'P6':  # PPM định dạng
            return "PPM"
        else:
            raise ValueError("Định dạng ảnh không được hỗ trợ!")

# Đọc ảnh BMP (24-bit)
def read_bmp(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(14)
        dib_header = f.read(40)

        # Lấy thông tin cơ bản
        width = struct.unpack('<I', dib_header[4:8])[0]
        height = struct.unpack('<I', dib_header[8:12])[0]
        bit_count = struct.unpack('<H', dib_header[14:16])[0]
        compression = struct.unpack('<I', dib_header[16:20])[0]

        if bit_count != 24 or compression != 0:
            raise ValueError("Chỉ hỗ trợ ảnh BMP 24-bit không nén!")

        # Đọc dữ liệu pixel
        offset = struct.unpack('<I', header[10:14])[0]
        row_size = (width * 3 + 3) // 4 * 4
        f.seek(offset)
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                b, g, r = struct.unpack('BBB', f.read(3))
                row.append((r, g, b))
            f.read(row_size - width * 3)  # Bỏ padding
            pixels.append(row)
        return width, height, pixels

# Đọc ảnh PPM (P6)
def read_ppm(file_path):
    with open(file_path, 'rb') as f:
        header = f.readline().decode().strip()
        if header != "P6":
            raise ValueError("Chỉ hỗ trợ ảnh PPM dạng P6!")
        dimensions = f.readline().decode().strip().split()
        width, height = map(int, dimensions)
        max_val = int(f.readline().decode().strip())
        if max_val != 255:
            raise ValueError("Giá trị tối đa của ảnh không phải 255!")
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                r, g, b = struct.unpack('BBB', f.read(3))
                row.append((r, g, b))
            pixels.append(row)
        return width, height, pixels

# Ghi ảnh BMP (24-bit)
def write_bmp(file_path, width, height, pixels):
    with open(file_path, 'wb') as f:
        row_size = (width * 3 + 3) // 4 * 4
        padding = row_size - width * 3
        pixel_data_size = row_size * height
        file_size = 14 + 40 + pixel_data_size

        # Viết BMP Header
        f.write(b'BM')
        f.write(struct.pack('<I', file_size))
        f.write(b'\x00\x00')
        f.write(b'\x00\x00')
        f.write(struct.pack('<I', 54))  # Offset

        # Viết DIB Header
        f.write(struct.pack('<I', 40))  # Header size
        f.write(struct.pack('<I', width))
        f.write(struct.pack('<I', height))
        f.write(struct.pack('<H', 1))  # Planes
        f.write(struct.pack('<H', 24))  # Bits per pixel
        f.write(struct.pack('<I', 0))  # Compression
        f.write(struct.pack('<I', pixel_data_size))
        f.write(struct.pack('<I', 2835))  # X pixels per meter
        f.write(struct.pack('<I', 2835))  # Y pixels per meter
        f.write(struct.pack('<I', 0))  # Total colors
        f.write(struct.pack('<I', 0))  # Important colors

        # Viết dữ liệu pixel
        for row in pixels:
            for r, g, b in row:
                f.write(struct.pack('BBB', b, g, r))  # BMP lưu theo thứ tự BGR
            f.write(b'\x00' * padding)

# Ghi ảnh PPM (P6)
def write_ppm(file_path, width, height, pixels):
    with open(file_path, 'wb') as f:
        # Ghi header
        f.write(b"P6\n")
        f.write(f"{width} {height}\n".encode())
        f.write(b"255\n")
        # Ghi dữ liệu điểm ảnh
        for row in pixels:
            for r, g, b in row:
                f.write(struct.pack('BBB', r, g, b))

# Áp dụng Power Law Transformation
def apply_power_law_transform(width, height, pixels, gamma, c=1):
    new_pixels = []
    for row in pixels:
        new_row = []
        for r, g, b in row:
            r_new = int(c * ((r / 255) ** gamma) * 255)
            g_new = int(c * ((g / 255) ** gamma) * 255)
            b_new = int(c * ((b / 255) ** gamma) * 255)
            new_row.append((r_new, g_new, b_new))
        new_pixels.append(new_row)
    return new_pixels

# Hàm tổng hợp
def process_image(input_file, output_file, gamma):
    format_type = detect_format(input_file)
    if format_type == "BMP":
        width, height, pixels = read_bmp(input_file)
        new_pixels = apply_power_law_transform(width, height, pixels, gamma)
        write_bmp(output_file, width, height, new_pixels)
    elif format_type == "PPM":
        width, height, pixels = read_ppm(input_file)
        new_pixels = apply_power_law_transform(width, height, pixels, gamma)
        write_ppm(output_file, width, height, new_pixels)
    else:
        raise ValueError("Định dạng ảnh không được hỗ trợ!")

# Chạy chương trình
if __name__ == "__main__":
    input_file = "E:/Picture/bx.bmp"  # Hoặc input.ppm
    output_file = "output.bmp"  # Hoặc output.ppm
    gamma = 0.3  # Giá trị gamma (điều chỉnh độ sáng)
    
    process_image(input_file, output_file, gamma)
    print(f"Đã xử lý ảnh và lưu tại {output_file}")
