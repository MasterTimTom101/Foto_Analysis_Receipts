"""
Server package for the receipt analysis application
"""

from .api import create_app
from .core.config import config
from .services.receipt_analyzer import ReceiptAnalyzer

__all__ = ['create_app', 'config', 'ReceiptAnalyzer']