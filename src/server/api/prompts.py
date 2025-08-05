"""
AI Prompts for receipt analysis
"""

# Main prompt for receipt analysis
RECEIPT_ANALYSIS_PROMPT = (
    "Es ist ein Kassenbon und Eurobeträge mit Komma. "
    "Mache einen CSV Datensatz no header und ohne Erläuterung mit Semikolon als Trenner von "
    "Datum mit Punkt, Uhrzeit mit Doppelpunkt, Summe_Food, Summe_NonFood"
)

# Alternative prompts for future use
DETAILED_RECEIPT_PROMPT = (
    "Analysiere diesen Kassenbon und extrahiere folgende Informationen: "
    "Datum, Uhrzeit, Einzelpositionen mit Preisen, Kategorisierung in Food/NonFood, Gesamtsumme"
)

# Prompt for categorization
CATEGORIZATION_PROMPT = (
    "Kategorisiere die folgenden Artikel als 'Food' oder 'NonFood': "
)

# Export the main prompt for backward compatibility
PROMPT_TEXT = RECEIPT_ANALYSIS_PROMPT