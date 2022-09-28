from waitress import serve
import sys
from main import app
from db import init_database

if __name__ == "__main__":
    init_database()
    serve(app, listen=sys.argv[1])
