import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

GEMINI_MODEL = "gemini-2.5-flash"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_OF_COSTFILES = os.path.join(BASE_DIR, "cost_files/")
DIRECTORY_OF_CALENDARWEEKS = os.path.join(BASE_DIR, "photos/")
PROMPT_TEXT = ("Es ist ein Kassenbon und Eurobeträge mit Komma"
                "Mache einen CSV Datensatz no header und ohne Erläuterung mit Semikolon als Trenner von Datum mit Punkt, Uhrzeit mit Doppelpunkt, Summe_Food, Summe_NonFood"
              )

# Set API Key
load_dotenv()
genai.configure(api_key = os.getenv('GEMINI_API_KEY'))

# Load Model
model = genai.GenerativeModel(GEMINI_MODEL)

def load_photos_of_one_week_and_AI_analyse_each_and_store_to_csv():
    """
    Load Photos of weekly receipts, analyse by AI, summarize their costs and store in one csv-file
    :parameter: none
    :return: dftotal
    """
    try:
        calendar_week_for_analysis = input("Enter in nine digits the subdirectory of the photos of weekly receipts like..e.g. 2025CW_30\n-->")
        dir_string_photo = os.path.join(DIRECTORY_OF_CALENDARWEEKS, calendar_week_for_analysis)
        csv_file = os.path.join(DIRECTORY_OF_COSTFILES, calendar_week_for_analysis + "_costs.csv")
        directory = Path(dir_string_photo)

        if not directory.exists():
            print(f"Error: Directory {dir_string_photo} does not exist!")
            return None

        # Ensure cost_files directory exists
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        for datei in directory.iterdir():
            if datei.is_file():
                try:
                    print("The analysis of receipt ", datei.name)
                    image_path = os.path.join(dir_string_photo, datei.name)
                    
                    with open(image_path, "rb") as img_file:
                        image_bytes = img_file.read()

                    # Prompt and Upload Foto
                    response = model.generate_content(
                        [
                            PROMPT_TEXT,
                            {"mime_type": "image/jpeg", "data": image_bytes}
                        ]
                    )
                    temp_answer = response.text
                    cw_dataset = temp_answer.replace(",", ".") + ";" + datei.name
                    
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
                    
                except Exception as e:
                    print(f"Error processing {datei.name}: {e}")
                    continue
        
        df_total = pd.read_csv(csv_file, sep=";")
        return df_total
    
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None

if __name__ == "__main__":
    dummy_temp = load_photos_of_one_week_and_AI_analyse_each_and_store_to_csv()

    if dummy_temp is not None:
        print("End of AI-Analysis !")
        try:
            dummy_temp["Summe_Food"] = dummy_temp["Summe_Food"].astype(float)
            dummy_temp["Summe_NonFood"] = dummy_temp["Summe_NonFood"].astype(float)
            sum_food = round(dummy_temp["Summe_Food"].sum(), 2)
            sum_nonfood = round(dummy_temp["Summe_NonFood"].sum(), 2)
            print("Die Wochendatei war \n", dummy_temp)
            print("Die Summe von Food war ", sum_food )
            print("Die Summe von NonFood war ",sum_nonfood)
        except Exception as e:
            print(f"Error processing results: {e}")
    else:
        print("Analysis failed or was cancelled.")