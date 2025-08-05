import sys
import os

# Handle direct execution
if __name__ == "__main__":
    # Add the project root to Python path for direct execution
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    sys.path.insert(0, project_root)
    from src.server.core.config import DevelopmentConfig
    from src.server.services.receipt_analyzer import ReceiptAnalyzer
else:
    # Handle module import
    from ..core.config import DevelopmentConfig
    from ..services.receipt_analyzer import ReceiptAnalyzer

def load_photos_of_one_week_and_AI_analyse_each_and_store_to_csv():
    """
    Load Photos of weekly receipts, analyse by AI, summarize their costs and store in one csv-file
    :parameter: none
    :return: dftotal
    """
    # Initialize configuration and service
    config = DevelopmentConfig()
    analyzer = ReceiptAnalyzer(config)
    
    # Get calendar week from user
    calendar_week_for_analysis = input("Enter in nine digits the subdirectory of the photos of weekly receipts like..e.g. 2025CW_30\n-->")
    
    # Analyze the calendar week
    df_total = analyzer.analyze_calendar_week(calendar_week_for_analysis)
    
    return df_total

if __name__ == "__main__":
    dummy_temp = load_photos_of_one_week_and_AI_analyse_each_and_store_to_csv()

    if dummy_temp is not None:
        print("End of AI-Analysis!")
        
        # Initialize analyzer for summary
        config = DevelopmentConfig()
        analyzer = ReceiptAnalyzer(config)
        
        # Get summary statistics
        summary = analyzer.get_week_summary(dummy_temp)
        
        print("Weekly Analysis Summary:")
        print(f"Total Food Costs: €{summary['total_food']}")
        print(f"Total Non-Food Costs: €{summary['total_nonfood']}")
        print(f"Total Receipts Processed: {summary['total_receipts']}")
        print("\nDetailed Results:")
        print(dummy_temp)
    else:
        print("Analysis failed or was cancelled.")