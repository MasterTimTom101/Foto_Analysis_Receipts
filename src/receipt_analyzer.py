import os
import google.generativeai as genai
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any

from .config import Config


class ReceiptAnalyzer:
    """Service class for AI-powered receipt analysis"""
    
    def __init__(self, config: Config):
        """Initialize the receipt analyzer with configuration"""
        self.config = config
        self._setup_gemini()
    
    def _setup_gemini(self):
        """Configure Gemini AI with API key"""
        if not self.config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required for receipt analysis")
        
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
    
    def analyze_calendar_week(self, calendar_week: str) -> Optional[pd.DataFrame]:
        """
        Analyze all receipt photos in a calendar week directory
        
        Args:
            calendar_week: Calendar week in format 2025CW_XX
            
        Returns:
            DataFrame with analysis results or None if failed
        """
        try:
            photos_dir = self.config.PHOTOS_DIR / calendar_week
            csv_file = self.config.COST_FILES_DIR / f"{calendar_week}_costs.csv"
            
            if not photos_dir.exists():
                print(f"Error: Directory {photos_dir} does not exist!")
                return None
            
            # Ensure cost_files directory exists
            self.config.COST_FILES_DIR.mkdir(parents=True, exist_ok=True)
            
            # Process each image file
            for image_file in photos_dir.iterdir():
                if self._is_supported_image(image_file):
                    self._process_single_receipt(image_file, csv_file)
            
            # Read and return final results
            if csv_file.exists():
                df_total = pd.read_csv(csv_file, sep=";")
                return self._process_results(df_total)
            
            return None
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            return None
    
    def _is_supported_image(self, file_path: Path) -> bool:
        """Check if file is a supported image format"""
        return file_path.is_file() and file_path.suffix.lower() in self.config.SUPPORTED_IMAGE_EXTENSIONS
    
    def _process_single_receipt(self, image_path: Path, csv_file: Path):
        """Process a single receipt image"""
        try:
            print(f"Analyzing receipt: {image_path.name}")
            
            # Read image file
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()
            
            # Analyze with Gemini AI
            response = self.model.generate_content([
                self.config.PROMPT_TEXT,
                {"mime_type": "image/jpeg", "data": image_bytes}
            ])
            
            # Process AI response
            temp_answer = response.text
            cw_dataset = temp_answer.replace(",", ".") + ";" + image_path.name
            
            # Save to CSV
            self._save_to_csv(cw_dataset, csv_file)
            
        except Exception as e:
            print(f"Error processing {image_path.name}: {e}")
    
    def _save_to_csv(self, cw_dataset: str, csv_file: Path):
        """Save analysis result to CSV file"""
        columns = ["Datum", "Uhrzeit", "Summe_Food", "Summe_NonFood", "Foto_Datei"]
        
        # Create new row DataFrame
        new_row_data = cw_dataset.split(";")
        df_new = pd.DataFrame([new_row_data], columns=columns)
        
        if csv_file.exists():
            # Append to existing file
            df_old = pd.read_csv(csv_file, sep=";")
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        else:
            # Create new file
            df_all = df_new
        
        # Save to CSV
        df_all.to_csv(csv_file, sep=";", index=False)
    
    def _process_results(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean the results DataFrame"""
        try:
            # Convert numeric columns
            df["Summe_Food"] = pd.to_numeric(df["Summe_Food"], errors='coerce').fillna(0.0)
            df["Summe_NonFood"] = pd.to_numeric(df["Summe_NonFood"], errors='coerce').fillna(0.0)
            
            return df
            
        except Exception as e:
            print(f"Error processing results: {e}")
            return df
    
    def get_week_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics for a week's analysis"""
        if df is None or df.empty:
            return {"total_food": 0.0, "total_nonfood": 0.0, "total_receipts": 0}
        
        return {
            "total_food": round(df["Summe_Food"].sum(), 2),
            "total_nonfood": round(df["Summe_NonFood"].sum(), 2),
            "total_receipts": len(df),
            "receipts": df.to_dict('records')
        }
    
    def get_available_weeks(self) -> List[str]:
        """Get list of available calendar weeks"""
        if not self.config.PHOTOS_DIR.exists():
            return []
        
        weeks = []
        for item in self.config.PHOTOS_DIR.iterdir():
            if item.is_dir() and item.name.startswith('2025CW_'):
                weeks.append(item.name)
        
        return sorted(weeks)