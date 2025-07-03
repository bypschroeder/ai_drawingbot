import requests
import os


def generate_line_art_image(first_word: str):
    """
    Generates a
    Generates a minimalistic line art image based on a given word using the LUIS model via its API.

    Args:
        first_word (str): The main subject or concept to be illustrated in the line art.

    Returns:
        str: A base64-encoded string representing the generated image.
    """
    api_url = os.getenv("API_URL")

    prompt = (
        f"{first_word}, single continuous black outline, line drawing, "
        "no fill, no shading, white background, minimalistic, vector style"
    )

    payload = {
        "prompt": prompt,
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

    response = requests.post(
        api_url, headers={"Content-Type": "application/json"}, json=payload
    )
    response.raise_for_status()

    return response.json()["images"][0]
