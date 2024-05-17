from PIL import Image, ImageEnhance
import base64
import io


def adjust_brightness_by_rate(
        base64_string: str,
        brightness_rate: float,
        default_return_image_type: str = "PNG"
) -> str | None:
    """
    Decodes a Base64 encoded image, increases its brightness by brightness_rate,
    and returns the new image encoded as a Base64 string.

    :param default_return_image_type: when Pillow cannot determine the image type, defaults to PNG
    :param base64_string: The Base64 encoded string of the image.
    :param brightness_rate: The float brightness value.
    :return: The Base64 encoded string of the adjusted image.
    """

    try:
        # 1. Decode the Base64 image data
        decoded_image = base64.b64decode(base64_string)
        # 2. Load the image from the decoded bytes
        img = Image.open(io.BytesIO(decoded_image))
        # 3. Increase brightness by brightness_rate
        enhancer = ImageEnhance.Brightness(img)
        img_enhanced = enhancer.enhance(brightness_rate)

        # 4. Save the enhanced image to a bytes buffer
        buffer = io.BytesIO()
        img_enhanced.save(buffer, format=img.format if img.format else default_return_image_type)
        buffer.seek(0)

        # 5. Re-encode the enhanced image to Base64
        enhanced_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return enhanced_base64
    except Exception as e:
        raise e
