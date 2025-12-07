# wsgi.py
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import and run the Flask app
from poverty_backend.api.index import app as application

if __name__ == "__main__":
    application.run()