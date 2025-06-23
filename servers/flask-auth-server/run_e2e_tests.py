import sys
import os
import pytest

def run_e2e_tests():
    # Add the directory containing app.py to the Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    pytest.main(['tests/test_e2e_auth.py', '-v'])

if __name__ == '__main__':
    run_e2e_tests()