# 📄 Photo Analysis of Receipts

> AI-powered receipt analysis tool with REST API and Swagger documentation that extracts food and non-food costs from receipt photos using Google Gemini AI

## 🚀 TL;DR

This Flask application provides both a **REST API with Swagger documentation** and a web interface for AI-powered receipt analysis. Automatically categorize and sum up food vs non-food expenses by calendar week using Google Gemini AI.

**Quick Start:**
```bash
# Setup
cp .env_template .env  # Add your Gemini API key
pip install -r requirements.txt

# Run application
python run_app.py
# Visit Swagger API: http://localhost:8081/swagger/
# Visit Web App: http://localhost:8081/receipts/home

# Or run console analysis
python analyze_receipts.py
```

## 📋 What This Project Does

- **🔗 REST API**: Complete REST API with Swagger documentation for programmatic access
- **📸 Receipt Processing**: Upload receipt photos organized by calendar weeks
- **🤖 AI Analysis**: Uses Google Gemini AI to extract itemized costs 
- **📊 Categorization**: Automatically separates food from non-food expenses
- **📈 Weekly Reports**: Generates CSV summaries by calendar week
- **🌐 Web Interface**: Simple Flask web UI for manual analysis
- **💻 Console Mode**: Command-line batch processing

## 🔗 API Endpoints

### **Primary Interface: Swagger UI**
**Visit: http://localhost:8081/swagger/**

Interactive API documentation where you can:
- Test all endpoints directly in the browser
- View request/response schemas
- See example data formats

### **Available Endpoints:**

**Analysis Operations** (`/api/v1/analyze/`):
- `POST /` - Trigger AI analysis for a calendar week
- `GET /{calendar_week}` - Get detailed analysis results
- `GET /{calendar_week}/summary` - Get summary statistics
- `GET /weeks` - List all available calendar weeks

**System Operations** (`/api/v1/system/`):
- `GET /health` - API health check
- `GET /info` - System information 
- `GET /config` - Configuration details
- `GET /test` - Simple test endpoint

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Google Gemini AI API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation
1. **Clone and navigate:**
   ```bash
   cd Photo_Analysis_of_Receipts
   ```

2. **Install dependencies:**
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

### **Primary: Swagger API Interface**
```bash
python run_app.py
```
**Then visit: http://localhost:8081/swagger/**

This is the **main interface** for the application where you can:
1. **Explore all endpoints** with interactive documentation
2. **Test API calls** directly in the browser
3. **View response schemas** and example data
4. **Trigger analysis** for any calendar week
5. **Get results** in JSON format

### **Example API Usage:**

**1. List available weeks:**
```bash
curl http://localhost:8081/api/v1/analyze/weeks
```

**2. Trigger analysis:**
```bash
curl -X POST http://localhost:8081/api/v1/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"calendar_week": "2025CW_30"}'
```

**3. Get results:**
```bash
curl http://localhost:8081/api/v1/analyze/2025CW_30
```

### **Secondary: Web Interface**
Visit: http://localhost:8081/receipts/home

**Available routes:**
- `/receipts/home` - Project information and available weeks
- `/receipts/analyse` - Trigger analysis for a calendar week
- `/receipts/show` - View all analysis results
- `/receipts/about` - About page

### **Console Application (Alternative)**
```bash
python analyze_receipts.py
```

**How it works:**
1. Shows available calendar weeks
2. Enter calendar week (e.g., `2025CW_30`)
3. AI processes all photos in that folder
4. Shows summary and saves results to `src/server/api/cost_files/2025CW_30_costs.csv`

### **Output Format**
Both API and CSV files contain:
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
│       ├── 📁 api/
│       │   ├── 📄 __init__.py          # Flask app factory
│       │   ├── 📁 v1/                  # API version 1 endpoints
│       │   │   ├── 📄 analysis.py      # Analysis REST endpoints
│       │   │   └── 📄 system.py        # System & test endpoints
│       │   └── 📁 models/              # API data models
│       │       ├── 📄 analysis.py      # Analysis models
│       │       └── 📄 responses.py     # Response models
│       ├── 📁 web/                     # Web interface
│       │   ├── 📄 routes.py            # HTML routes
│       │   └── 📁 templates/           # HTML templates
│       ├── 📁 services/                # Business logic
│       │   └── 📄 receipt_analyzer.py  # AI analysis service
│       └── 📁 core/                    # Configuration
│           └── 📄 config.py            # App configuration
├── 📄 run_app.py                       # Main startup script
├── 📄 analyze_receipts.py              # Console interface
├── 📄 requirements.txt                 # Dependencies
├── 📄 .env_template                    # Environment template
└── 📄 README.md                        # This file
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
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python run_app.py
```

**Port 8081 in Use:**
```bash
# Edit run_app.py and change the port number
# Or kill the process using the port
lsof -ti:8081 | xargs kill -9
```

**Missing API Key:**
```bash
# Check your .env file exists and contains:
cat .env
# Should show: GEMINI_API_KEY=your_key...
```

**Swagger "Unable to render schema" Error:**
- This has been fixed in the current version
- Make sure you're using the latest code

**No Photos Found:**
```bash
# Create the directory structure:
mkdir -p src/server/api/photos/2025CW_30
# Add .jpeg files to the folder
```

## 📊 API Response Examples

**Analysis Result:**
```json
{
  "calendar_week": "2025CW_30",
  "status": "completed",
  "total_food": 45.67,
  "total_nonfood": 12.33,
  "total_receipts": 3,
  "receipts": [
    {
      "datum": "30.06.2025",
      "uhrzeit": "14:30",
      "summe_food": 23.45,
      "summe_nonfood": 5.67,
      "foto_datei": "receipt_01.jpeg"
    }
  ],
  "analysis_date": "2025-08-05T21:42:15.123456"
}
```

**Available Weeks:**
```json
{
  "weeks": [
    {
      "week": "2025CW_30",
      "year": 2025,
      "week_number": 30,
      "file_count": 5,
      "analysis_status": "analyzed",
      "last_analysis": "2025-08-05T21:42:15.123456"
    }
  ],
  "total": 1
}
```

## 🎯 Future Enhancements

- [ ] File upload endpoints in REST API
- [ ] User authentication for API access
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Support for PNG/PDF formats
- [ ] Advanced categorization beyond Food/NonFood
- [ ] Webhook notifications for analysis completion
- [ ] Batch processing multiple weeks via API

## 📝 Technical Notes

- **Framework**: Flask with Flask-RESTX for API and Swagger
- **AI Model**: Google Gemini 2.5 Flash
- **API Documentation**: Swagger UI with interactive testing
- **Data Processing**: Pandas for CSV handling
- **Image Processing**: Direct binary upload to Gemini
- **Language**: Mixed German/English (receipt text in German)
- **File Format**: JPEG images, JSON API responses, CSV output

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

**🔗 Start exploring: http://localhost:8081/swagger/**