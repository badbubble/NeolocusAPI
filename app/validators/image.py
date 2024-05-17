from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from .base import BaseForm
from app.config.settings import Config


def validate_image_size(form, field):
    """
    Validates that the size of the image is within the set limits.
    """
    data = field.data
    max_length = Config.MAX_IMG_SIZE
    max_base64_length = int(max_length * 4 / 3)  # Adjust for Base64 inflation

    min_length = Config.MIN_IMG_SIZE
    min_base64_length = int(min_length * 4 / 3)

    if len(data) > max_base64_length:
        raise ValidationError("image size is too big.")
    elif len(data) < min_base64_length:
        raise ValidationError("image size is too small.")


class ImageForm(BaseForm):
    # 1. 'image' should contain data
    image = StringField('image', [
        DataRequired("image data is required"),
        validate_image_size,
    ])
