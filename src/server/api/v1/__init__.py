"""
API version 1 endpoints
"""

from .simple_test import api as test_api
from .system import api as system_api
from .analysis import api as analysis_api

__all__ = ['test_api', 'system_api', 'analysis_api']