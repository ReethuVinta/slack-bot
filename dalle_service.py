import os
import openai

def get_image_from_dalle(description):
    
    file_descriptor = os.open("./openai_key.txt", os.O_RDONLY)
    key = os.read(file_descriptor, 51)

    openai.api_key = key.decode()

    response = openai.Image.create(
        prompt=description,
        n=1,
        size="256x256",
    )

    return response["data"][0]["url"]