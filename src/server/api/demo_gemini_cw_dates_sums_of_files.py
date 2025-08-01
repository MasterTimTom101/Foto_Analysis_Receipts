import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

GEMINI_MODEL = "gemini-2.5-flash"

# Set API Key
load_dotenv()
genai.configure(api_key = os.getenv('GEMINI_API_KEY'))

# Load Model
model = genai.GenerativeModel(GEMINI_MODEL)

# Load Fotos
calendar_week = input("Enter the calendar week of the analysis..eg. 01-09 or 10-52 or e.g. 30\n")
dir_string = "Fotos/CW_" + calendar_week
directory = Path(dir_string)
for datei in directory.iterdir():
    if datei.is_file():
        print("die datei war", datei.name)
        image_path = dir_string + "/" + datei.name
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()

        # Prompt and Upload Foto
        response = model.generate_content(
            [
                "Es ist ein Kassenbon"
                "Gib aus Datum"
                "Gib aus Uhrzeit"
                "Gib aus Summe Nonfood"
                "Gib aus Summe Food",
                {"mime_type": "image/jpeg", "data": image_bytes}
            ]
        )

        # Printing the Response of Gemini
        print(response.text)
