import base64
import openai
import os
from dotenv import load_dotenv

OPENAI_MODEL = "gpt-4o-mini"

# Foto coding into base64
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

# Load API-Key
load_dotenv()
client1 = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Foto File and coding base64
calendar_week = input("Enter the calendar week of the analysis..eg. 30\n")
image_path = f"Fotos/CW_{calendar_week}/Bon_01.jpeg"                      
base64_image = encode_image(image_path)

# Prompt to OpenAI
response = client1.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text":
                    "Es ist ein Kassenbon"
                    "Gib aus Datum"
                    "Gib aus Uhrzeit"
                    "Gib aus Summe Nonfood"
                    "Gib aus Summe Food"
                 },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=1000,
)

# Print the Response of OpenAI
print(response.choices[0].message.content)
