import os
import openai

openai.api_key = os.environ["OPENAI_KEY"]

def get_image_from_dalle(description):
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="256x256",
        response_format="b64_json",
    )

    return response