def read_image(file_path):
    """Đọc ảnh từ file BMP và trả về dữ liệu dưới dạng ma trận pixel."""
    with open(file_path, "rb") as f:
        data = f.read()

    # Header BMP có kích thước 54 byte
    header = data[:54]
    pixel_data = data[54:]
    return header, pixel_data

def write_image(file_path, header, pixel_data):
    """Ghi ảnh ra file BMP với header và dữ liệu pixel đã cho."""
    with open(file_path, "wb") as f:
        f.write(header)
        f.write(pixel_data)

def process_negative_pixel(pixel_data):
    """Xử lý ảnh âm cho dữ liệu pixel."""
    negative_data = bytearray()
    for i in range(len(pixel_data)):
        # Ảnh âm: giá trị mới = 255 - giá trị cũ
        negative_data.append(255 - pixel_data[i])
    return negative_data

def main():
    # Đường dẫn file ảnh BMP đầu vào và đầu ra
    input_image_path = "E:/Dowload/food.bmp"
    output_image_path = "negative_image.bmp"

    # Đọc ảnh BMP
    header, pixel_data = read_image(input_image_path)

    # Xử lý tạo ảnh âm
    negative_data = process_negative_pixel(pixel_data)

    # Ghi ảnh BMP đã xử lý ra file
    write_image(output_image_path, header, negative_data)

    print(f"Ảnh âm đã được lưu tại: {output_image_path}")

if __name__ == "__main__":
    main()
