import sys
import os

pytest_plugins = [
    "tests.test_auth",
    "tests.test_reports",
    "tests.test_consent_gate",
]
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
