import time
import base64
from config import setEnvironment
from google import genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage

setEnvironment()

# Image upload and having the llm analyze the image
client = genai.Client()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# Upload file to Google's servers; personal data is exposed
myfile = client.files.upload(file="/Users/holyboy/Projects/Langchain Book/No1/dsotm.jpg")
while myfile.state.name == "PROCESSING":
    time.sleep(2)
    myfile = client.files.get(name=myfile.name)
# Reference by file_id in FileContentBlock
message = HumanMessage(
    content=[
        {"type": "text", "text": "What is in the image?"},
        {
            "type": "file",
            "file_id": myfile.uri,  # or myfile.name
            "mime_type": "image/jpeg",
        },
    ]
)
response = llm.invoke([message])
print( response )

# Image generation (later test this; could not test it due to Resource Exhausted error)
'''
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-image")

response = llm.invoke("Generate a photorealistic image of a cuddly cat wearing a hat in png format.")

def _get_image_base64(response: AIMessage) -> None:
    image_block = next(
        block
        for block in response.content
        if isinstance(block, dict) and block.get("image_url")
    )
    return image_block["image_url"].get("url").split(",")[-1]

image_base64 = _get_image_base64(response)
with open("/Users/holyboy/Projects/Langchain Book/No1/output.png", "wb") as fh:
    fh.write(base64.b64decode(image_base64))

#from IPython.display import Image, display
#display(Image(data=base64.b64decode(image_base64), width=300))
'''
 
# Audio input (from langchain site)
'''
model = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview")

message = HumanMessage(
    content=[
        {"type": "text", "text": "Summarize this audio in a sentence."},
        {
            "type": "image_url",
            "image_url": "https://example.com/audio.mp3",
        },
    ]
)
response = model.invoke([message])
print( response )
'''

# Video input (from langchain site)
'''
model = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview")

video_bytes = open("path/to/your/video.mp4", "rb").read()
video_base64 = base64.b64encode(video_bytes).decode("utf-8")
mime_type = "video/mp4"

message = HumanMessage(
    content=[
        {"type": "text", "text": "Describe what's in this video in a sentence."},
        {
            "type": "video",
            "base64": video_base64,
            "mime_type": mime_type,
        },
    ]
)
response = model.invoke([message])
print( response )
'''