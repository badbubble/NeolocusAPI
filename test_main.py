import json
import pytest
from app import create_app
from PIL import Image
import io
import base64


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def encode_image_to_base64(image_path: str) -> str:
    with Image.open(image_path) as img:
        original_format = img.format
        if original_format is None:
            raise ValueError("Failed to detect the image format")
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGB')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=original_format)
        img_byte_arr.seek(0)
    print("[+] Encoding done.")
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')


def test_invalid_param_big_img(client):
    response = client.post('/v1/image/adjust_brightness',
                           json={"image": encode_image_to_base64("test_images/cat.png") * 100})
    json_data = json.loads(response.data)
    assert json_data["error_code"] == 101
    assert json_data["msg"] == {"image":  ["image size is too big."]}
    assert response.status_code == 200


def test_invalid_param_small_img(client):
    response = client.post('/v1/image/adjust_brightness',
                           json={"image": "123"})
    json_data = json.loads(response.data)
    assert json_data["error_code"] == 101
    assert json_data["msg"] == {"image":  ["image size is too small."]}
    assert response.status_code == 200


def test_invalid_param_empty_img(client):
    response = client.post('/v1/image/adjust_brightness',
                           json={"image": ""})
    json_data = json.loads(response.data)
    assert json_data["error_code"] == 101
    assert json_data["msg"] == {"image":  ["image data is required"]}
    assert response.status_code == 200


def test_png_img(client):
    response = client.post('/v1/image/adjust_brightness',
                           json={"image": encode_image_to_base64("test_images/cat.png")})
    json_data = json.loads(response.data)
    assert json_data["error_code"] == 0
    assert len(json_data["msg"]) > 0
    assert response.status_code == 200


def test_jpg_img(client):
    response = client.post('/v1/image/adjust_brightness',
                           json={"image": encode_image_to_base64("test_images/dog.jpg")})
    json_data = json.loads(response.data)
    assert json_data["error_code"] == 0
    assert len(json_data["msg"]) > 0
    assert response.status_code == 200


def test_abnormal_img(client):
    response = client.post('/v1/image/adjust_brightness',
                           json={"image": encode_image_to_base64("test_images/dog.jpg")[1:]})
    json_data = json.loads(response.data)
    assert json_data["error_code"] == 1000
    assert json_data["msg"] == "server is busy!"
    assert response.status_code == 500
