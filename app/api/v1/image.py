from app.libs.redprint import Redprint
from app.validators.image import ImageForm
from app.internal.image import adjust_brightness_by_rate
from app.error.error_code import Success, ServerError
from app.config.settings import Config
from werkzeug.exceptions import HTTPException

api = Redprint('image')


@api.route('/adjust_brightness', methods=['POST'])
def adjust_brightness() -> HTTPException:
    """
    adjust brightness of an image by a rate set in configuration.
    :return: HTTPException
    """
    # 1. validate for parameters
    image_form = ImageForm().validate_for_api()
    # 2. adjust brightness of an image
    try:
        result = adjust_brightness_by_rate(image_form.image.data, Config.INCREASE_BRIGHTNESS_RATE,
                                           Config.DEFAULT_IMG_TYPE)
    except Exception as e:
        # 3. return a detail error when in debug mode
        if Config.DEBUG:
            return ServerError(msg={"error": str(e)})
        else:
            # 4. In dev mode, do not return details for security reasons
            return ServerError()
    # 5. return processed image
    return Success(msg={"image": result})
