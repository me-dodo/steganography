from PIL import Image

def encode_text_into_image(image_path, text) -> Image.Image:
    image = Image.open(image_path)
    encoded_image = image.copy()

    # Convert text to binary
    binary_text = ''.join([format(ord(char), '08b') for char in text])
    binary_text += '00000000'  # End of text marker

    data_idx = 0
    width, height = image.size
    for y in range(height):
        for x in range(width):
            if data_idx >= len(binary_text):
                return encoded_image

            pixel = list(encoded_image.getpixel((x, y)))
            for n in range(3):  # R, G, B channels
                if data_idx < len(binary_text):
                    pixel[n] = int(pixel[n] & ~1) | int(binary_text[data_idx])
                    data_idx += 1
            encoded_image.putpixel((x, y), tuple(pixel))

    return encoded_image


def decode_text_from_image(image: Image.Image) -> str:
    binary_text = ''
    decoded_text = ''

    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            for n in range(3):  # R, G, B channels
                binary_text += str(pixel[n] & 1)

    # Convert binary to ASCII 8-bit characters
    chars = [chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)]
    
    # Combine characters and stop at null character (`\x00`)
    decoded_text = ''.join(chars).split('\x00', 1)[0]
    return decoded_text
