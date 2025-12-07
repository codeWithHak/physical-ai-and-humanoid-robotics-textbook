import os
import sys

# Get the directory of this file (api)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
parent_dir = os.path.dirname(current_dir)
# Get the src directory
src_dir = os.path.join(parent_dir, 'src')
# Add src to sys.path
sys.path.append(src_dir)

# Import the app
from src.main import app