"""
API version 1 endpoints
"""

from .system import api as system_api
from .analysis import api as analysis_api

__all__ = ['system_api', 'analysis_api']