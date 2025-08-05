#!/usr/bin/env python3
"""
Entry point for the receipt analysis console application
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server.core.config import DevelopmentConfig
from server.services.receipt_analyzer import ReceiptAnalyzer

def main():
    """Main function for receipt analysis"""
    print("🤖 Receipt Analysis Console Application")
    print("=" * 50)
    
    try:
        # Initialize configuration and service
        config = DevelopmentConfig()
        analyzer = ReceiptAnalyzer(config)
        
        # Show available weeks
        available_weeks = analyzer.get_available_weeks()
        if available_weeks:
            print(f"Available calendar weeks: {', '.join(available_weeks)}")
        else:
            print("No calendar weeks found. Make sure you have photos in src/server/api/photos/2025CW_XX/ directories")
        
        # Get calendar week from user
        calendar_week = input("\nEnter calendar week (e.g., 2025CW_30): ").strip()
        
        if not calendar_week:
            print("No calendar week entered. Exiting.")
            return
        
        print(f"\n🔍 Analyzing receipts for {calendar_week}...")
        
        # Analyze the calendar week
        df_total = analyzer.analyze_calendar_week(calendar_week)
        
        if df_total is not None:
            print("\n✅ Analysis Complete!")
            
            # Get summary statistics
            summary = analyzer.get_week_summary(df_total)
            
            print("\n📊 Weekly Analysis Summary:")
            print(f"   Total Food Costs: €{summary['total_food']}")
            print(f"   Total Non-Food Costs: €{summary['total_nonfood']}")
            print(f"   Total Receipts Processed: {summary['total_receipts']}")
            
            print(f"\n💾 Results saved to: src/server/api/cost_files/{calendar_week}_costs.csv")
            
            if input("\nShow detailed results? (y/N): ").lower().startswith('y'):
                print("\n📋 Detailed Results:")
                print(df_total.to_string(index=False))
        else:
            print("\n❌ Analysis failed or was cancelled.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Analysis cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have:")
        print("1. Set GEMINI_API_KEY in your .env file")
        print("2. Created photo directories: src/server/api/photos/2025CW_XX/")
        print("3. Added .jpeg images to the directories")

if __name__ == "__main__":
    main()