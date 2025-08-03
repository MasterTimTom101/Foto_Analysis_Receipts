import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

GEMINI_MODEL = "gemini-2.5-flash"
DIRECTORY_OF_COSTFILES = "cost_files/"
DIRECTORY_OF_CALEDARWEEKS = "photos/"
PROMPT_TEXT = ("Es ist ein Kassenbon und Eurobeträge mit Komma"
                "Mache einen CSV Datensatz no header und ohne Erläuterung mit Semikolon als Trenner von Datum mit Punkt, Uhrzeit mit Doppelpunkt, Summe_Food, Summe_NonFood"
              )

# Set API Key
load_dotenv()
genai.configure(api_key = os.getenv('GEMINI_API_KEY'))

# Load Model
model = genai.GenerativeModel(GEMINI_MODEL)

def load_photos_of_one_week_and_AI_analyse_each_and_store_to_csv():
    # Load Photos of weekly receipts, analyse by AI, summarize their costs and store in one csv-file
    cw_sum_food = 0.00
    cw_sum_nonfood = 0.00

    calendar_week_for_analysis = input("Enter in nine digits the subdirectory of the photos of weekly receipts like..e.g. 2025CW_30\n-->")
    dir_string_photo = DIRECTORY_OF_CALEDARWEEKS + calendar_week_for_analysis
    dir_string_cost = DIRECTORY_OF_COSTFILES + calendar_week_for_analysis
    directory = Path(dir_string_photo)
    csv_file = DIRECTORY_OF_COSTFILES + calendar_week_for_analysis + "_costs.csv"

    # Demo of new row
    demo_row = {
        "Datum": datetime.today().strftime("%d.%m.%Y"),
        "Uhrzeit": datetime.now().strftime("%H:%M:%S"),
        "Summe_Food": 00.00,
        "Summe_NonFood": 00.00,
        "Foto_Datei": "no_file.jpeg"
    }

    for datei in directory.iterdir():
        if datei.is_file():
            print("The analysis of receipt ", datei.name)
            image_path = dir_string_photo + "/" + datei.name
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()

            # Prompt and Upload Foto
            response = model.generate_content(
                [
                    PROMPT_TEXT,
                    {"mime_type": "image/jpeg", "data": image_bytes}
                ]
            )

            # Printing the response of AI plus the file name of the receipt photo
            temp_answer = response.text
            cw_dataset = temp_answer.replace(",", ".") + ";" + datei.name
            #print("Der Datensatz war ", cw_dataset)

            # check if existing file for costs-files
            if os.path.exists(csv_file):
                # read existing file
                df_old = pd.read_csv(csv_file, sep=";")
                # New row as new DataFrame
                new_row = cw_dataset
                df_new = pd.DataFrame([new_row.split(";")], columns= ["Datum","Uhrzeit","Summe_Food","Summe_NonFood","Foto_Datei"])
                # Appending new row
                df_all = pd.concat([df_old, df_new], ignore_index=True)
            else:
                # if not existing then take the new row as a start of Dataframe
                new_row = cw_dataset
                df_all = pd.DataFrame([new_row.split(";")], columns= ["Datum","Uhrzeit","Summe_Food","Summe_NonFood","Foto_Datei"])

            # Overwrite the file by the df_all
            df_all.to_csv(csv_file, sep=";", index=False)

    print("End of AI-Analysis !")
    df_total = pd.read_csv(csv_file, sep=";")
    df_total["Summe_Food"] = df_total["Summe_Food"].astype(float)
    df_total["Summe_NonFood"] = df_total["Summe_NonFood"].astype(float)
    sum_food = round(df_total["Summe_Food"].sum(), 2)
    sum_nonfood = round(df_total["Summe_NonFood"].sum(), 2)
    print("Die Summe von Food war ", sum_food )
    print("Die Summe von NonFood war ",sum_nonfood)
    return

load_photos_of_one_week_and_AI_analyse_each_and_store_to_csv()
