import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.db.session import engine, Base
from app.db.models import Document

Base.metadata.create_all(bind=engine)
print("Table created (or already existed).")