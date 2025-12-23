import os
import shutil
from app import app, db

print("--- REMOVING OLD DATA ---")
# データベースファイルを直接削除
if os.path.exists("instance"):
    shutil.rmtree("instance")
    print("Deleted instance folder")
if os.path.exists("database.db"):
    os.remove("database.db") 
    print("Deleted database.db")

print("--- CREATING NEW DB ---")
with app.app_context():
    db.create_all()
    print("✅ SUCCESS! Database created.")
