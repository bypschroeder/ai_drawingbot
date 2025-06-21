import requests
import base64

API_URL = "https://stable-diffusion-rproxy.ki-awz.iisys.de/sdapi/v1/txt2img"
HEADERS = {"Content-Type": "application/json"}

payload = {
    "prompt": "house, single continuous black outline, line drawing, no fill, no shading, white background, minimalistic, vector style",
    "negative_prompt": "color, filled, shading, shadow, 3D, photo, texture, solid areas, background, blur, sketch, crosshatch, grayscale, painting",
    "styles": ["sketch"],
    "seed": -1,
    "sampler_name": "Euler",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 40,
    "cfg_scale": 9,
    "width": 512,
    "height": 512,
    "restore_faces": False,
    "tiling": False,
    "send_images": True,
    "save_images": False,
}


response = requests.post(API_URL, headers=HEADERS, json=payload)
response.raise_for_status()
data = response.json()

image_base64 = data["images"][0]

image_bytes = base64.b64decode(image_base64)

with open("output_image.png", "wb") as f:
    f.write(image_bytes)

print("Image saved as output_image.png")
