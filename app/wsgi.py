from waitress import serve
import sys
from main import app

if __name__ == "__main__":
    serve(app, listen=sys.argv[1])
