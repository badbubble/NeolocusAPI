from PIL import Image
import requests
import io
import base64
import argparse
import os


def encode_image_to_base64(image_path: str) -> str:
    print(f"[*] Encoding {image_path}...")
    with Image.open(image_path) as img:
        original_format = img.format
        if original_format is None:
            raise ValueError("[E] Failed to detect the image format")
        if img.mode not in ['RGB', 'RGBA']:
            img = img.convert('RGB')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=original_format)
        img_byte_arr.seek(0)
    print("[+] Encoding done.")
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')


def decode_image_from_base64(base64_img: str) -> Image:
    print("[*] Decoding image...")
    base64_img = base64.b64decode(base64_img)
    print("[+] Decoding done.")
    return Image.open(io.BytesIO(base64_img))


def main() -> None:
    parser = argparse.ArgumentParser(description="Process some parameters.")

    parser.add_argument('--ip', type=str, required=True, help='The IP address to connect to.')
    parser.add_argument('--port', type=int, required=True, help='The port number to connect on.')
    parser.add_argument('--img_path', type=str, required=True, help='The path to the image file.')
    parser.add_argument('--save_path', type=str, required=True, help='The path where the bright image should be saved.')
    args = parser.parse_args()
    if os.path.exists(args.img_path):
        base64_img = encode_image_to_base64(args.img_path)
    else:
        print("[E] The image file does not exist.")
        return

    try:
        print("[*] Sending request...")
        response = requests.post(f"http://{args.ip}:{args.port}/v1/image/adjust_brightness",
                                 json={"image": base64_img}).json()
        print("[+] Sending done.")
    except Exception as e:
        print(e)
        return

    # check error code
    error_code = response['error_code']
    # success
    if error_code == 0:
        image_data = response['msg']['image']
        image = decode_image_from_base64(image_data)

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        _, file_extension = os.path.splitext(args.save_path)
        if file_extension not in image_extensions:
            print("[E] The save file should have an image extension.")
            return
        directory_path = os.path.dirname(args.save_path)
        if os.path.exists(directory_path) or len(directory_path) == 0:
            print(f"[*] Saving image...")
            image.save(args.save_path)
            print(f"[+] Saved successfully to {args.save_path}.")
        else:
            print("[E] The save path does not exist.")
            return
    # invalid parameters
    elif error_code == 101:
        print(response)
        print(f"[E] You sent invalid parameters: {response["msg"]["image"]}")
    elif error_code == 1000:
        print(response)
        print(f"[E] Internal Server Error: {response['msg']['error']}")


if __name__ == "__main__":
    main()
