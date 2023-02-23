from base64 import b64decode
import json
import os

from slack import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dalle_service import get_image_from_dalle

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token = SLACK_BOT_TOKEN) 
client = WebClient(SLACK_BOT_TOKEN)

def write_image_to_file(json_response, description):
    for _, image_dict in enumerate(json_response["data"]):  
        image_file = "./images/" + description + ".png"
        with open(image_file, mode="wb") as png:
            png.write(b64decode(image_dict["b64_json"]))
        return image_file

def construct_attachments(image_url):
    return  [
      {
        "image_url": image_url
      },
    ]
    
@app.event("app_mention")
def generate_image(body, logger):
    
    image_description = str(body["event"]["text"]).split(">")[1]

    print("Description provided: " + image_description)
    
    response = get_image_from_dalle(image_description)
    image_file = write_image_to_file(response, image_description)
    
    print("Wowzaa! generated image")
    result = client.files_upload(
        channels=body["event"]["channel"],
        file=image_file,
    )

    response = client.chat_postMessage(channel = body["event"]["channel"], 
                                       thread_ts = body["event"]["event_ts"],
                                       attachments=construct_attachments(result['file']['permalink']))
    os.remove(image_file)


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
    