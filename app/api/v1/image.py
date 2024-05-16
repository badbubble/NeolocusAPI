from app.libs.redprint import Redprint

api = Redprint('image')


@api.route('/increase_brightness')
def increase_brightness():
    return "image"
