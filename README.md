# 📄 Photo Analysis of Receipts

> AI-powered receipt analysis tool that extracts food and non-food costs from receipt photos using Google Gemini AI

## 🚀 TL;DR

This Flask web application with AI-powered backend analyzes receipt photos to automatically categorize and sum up food vs non-food expenses by calendar week. Perfect for expense tracking and budgeting.

**Quick Start:**
```bash
# Setup
cp .env_template .env  # Add your Gemini API key
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run web app
python run_app.py
# Visit: http://localhost:8080/receipts/home

# Run AI analysis (recommended)
python analyze_receipts.py

# Or alternative method
python src/server/api/tasks.py
```

## 📋 What This Project Does

- **📸 Receipt Processing**: Upload receipt photos organized by calendar weeks
- **🤖 AI Analysis**: Uses Google Gemini AI to extract itemized costs 
- **📊 Categorization**: Automatically separates food from non-food expenses
- **📈 Weekly Reports**: Generates CSV summaries by calendar week
- **🌐 Web Interface**: Simple Flask web UI for file management
- **💻 Console Mode**: Command-line batch processing

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Google Gemini AI API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation
1. **Clone and navigate:**
   ```bash
   cd Photo_Analysis_of_Receipts
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env_template .env
   # Edit .env and add your Gemini API key:
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Create photo directories:**
   ```bash
   mkdir -p src/server/api/photos/2025CW_30
   mkdir -p src/server/api/photos/2025CW_31
   # Add more calendar weeks as needed: 2025CW_32, 2025CW_33, etc.
   ```

5. **Add receipt photos:**
   - Place JPEG images in the calendar week folders
   - Supported formats: `.jpeg`, `.jpg` 
   - Recommended resolution: VGA (640x480)
   - Example structure:
     ```
     src/server/api/photos/
     ├── 2025CW_30/
     │   ├── receipt_01.jpeg
     │   └── receipt_02.jpeg
     └── 2025CW_31/
         ├── grocery_receipt.jpeg
         └── restaurant_bill.jpeg
     ```

## 🎯 Usage

### Web Application
```bash
python run_app.py
```
Then visit: http://localhost:8080/receipts/home

**Available routes:**
- `/receipts/home` - Project information
- `/receipts/upload` - Upload interface  
- `/receipts/analyse` - Analysis tools
- `/receipts/show` - View results
- `/receipts/about` - About page

### Console Application (AI Analysis)

**Recommended method:**
```bash
python analyze_receipts.py
```

**Alternative method:**
```bash
python src/server/api/tasks.py
```

**How it works:**
1. Shows available calendar weeks
2. Enter calendar week (e.g., `2025CW_30`)
3. AI processes all photos in that folder
4. Shows summary and saves results to `src/server/api/cost_files/2025CW_30_costs.csv`

### Output Format
CSV files contain:
- `Datum` - Date from receipt
- `Uhrzeit` - Time from receipt  
- `Summe_Food` - Food costs (€)
- `Summe_NonFood` - Non-food costs (€)
- `Foto_Datei` - Source image filename

## 🏗️ Project Structure

```
📦 Photo_Analysis_of_Receipts/
├── 📁 src/
│   └── 📁 server/
│       └── 📁 api/
│           ├── 📄 app.py              # Flask app entry point
│           ├── 📄 routes.py           # Web routes
│           ├── 📄 tasks.py            # AI analysis logic
│           ├── 📄 prompts.py          # AI prompts
│           ├── 📁 templates/          # HTML templates
│           ├── 📁 photos/             # Receipt images by week
│           └── 📁 cost_files/         # Generated CSV reports
├── 📄 run_app.py                      # Easy startup script
├── 📄 requirements.txt                # Dependencies
├── 📄 .env_template                   # Environment template
└── 📄 README.md                       # This file
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
```

### Calendar Week Format
- Use 9-digit format: `2025CW_XX`
- Examples: `2025CW_30`, `2025CW_31`, `2025CW_52`

## 🚨 Troubleshooting

**Import Errors:**
```bash
# Make sure you're in the project root and virtual environment is activated
pwd  # Should show .../Photo_Analysis_of_Receipts
source .venv/bin/activate
python run_app.py
```

**Port 8080 in Use:**
```bash
# If port 8080 is busy, edit run_app.py and change the port number
# Or kill the process using the port
lsof -ti:8080 | xargs kill -9
```

**Missing API Key:**
```bash
# Check your .env file exists and contains:
cat .env
# Should show: GEMINI_API_KEY=your_key...
```


**No Photos Found:**
```bash
# Create the directory structure:
mkdir -p src/server/api/photos/2025CW_30
# Add .jpeg files to the folder
```

## 🎯 Future Enhancements

- [ ] File upload functionality in web interface
- [ ] User authentication system
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Support for PNG/PDF formats
- [ ] Advanced categorization beyond Food/NonFood
- [ ] Export to Excel/PDF reports
- [ ] Batch processing multiple weeks at once

## 📝 Technical Notes

- **Framework**: Flask (Python web framework)
- **AI Model**: Google Gemini 2.5 Flash
- **Data Processing**: Pandas for CSV handling
- **Image Processing**: Direct binary upload to Gemini
- **Language**: Mixed German/English (receipt text in German)
- **File Format**: JPEG images, CSV output

## 🤝 Contributing

This is a bootcamp project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes  
4. Submit a pull request

## 📄 License

Educational project - see course materials for usage rights.

---

*Built with ❤️ as part of a coding bootcamp project*