"""A program that encodes and decodes hidden
messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the
    provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    pixels_red = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            LSB = bin(pixels_red[i, j])[-1]
            if LSB == '1':
                pixels[i, j] = (255, 255, 255)  # sets to black if LSB is 1
            else:
                pixels[i, j] = (0, 0, 0)

    decoded_image.save("images/decoded_image1.png")


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is
    provided by default.
    """
    original_image = Image.open(template_image)
    x_size = original_image.size[0]
    y_size = original_image.size[1]

    image_size = original_image.size
    image_to_encode = write_text(text_to_encode, image_size)
    hidden_pixels = image_to_encode.load()
    original_pixels = original_image.load()

    encoded_image = Image.new("RGB", image_size)
    encoded_pixels = encoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            red = original_pixels[i, j][0]
            blue = original_pixels[i, j][1]
            green = original_pixels[i, j][2]

            LSB = bin(red)[-1]  # convert red value to binary

            if hidden_pixels[i, j] == (255, 255, 255):
                if LSB == '1':
                    encoded_pixels[i, j] = (red, blue, green)  # keep same
                elif LSB == '0':  # need to change LSB to 1
                    encoded_pixels[i, j] = (red + 1, blue, green)
            else:
                if LSB == '1':  # need to change LSB from 1 to 0
                    encoded_pixels[i, j] = (red - 1, blue, green)
                else:
                    encoded_pixels[i, j] = (red, blue, green)  # keep same

    encoded_image.save("images/encoded_image1.png")

    pass  # TODO: Fill out this function


if __name__ == '__main__':
    print("Encoding the image...")
    encode_image('Christian is not a Meme Lord')

    print("Decoding the image...")
    decode_image('images/encoded_image1.png')
