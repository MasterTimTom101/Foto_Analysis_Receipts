#!/usr/bin/env python3
"""
Simple startup script for the Receipt Analysis application
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.server.api.app import app

if __name__ == '__main__':
    print("Starting Receipt Analysis Web Application...")
    print("Application will be available at: http://localhost:8080")
    print("Available routes:")
    print("  - http://localhost:8080/receipts/home")
    print("  - http://localhost:8080/receipts/upload") 
    print("  - http://localhost:8080/receipts/analyse")
    print("  - http://localhost:8080/receipts/show")
    print("  - http://localhost:8080/receipts/about")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=8080)