import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

Cond = input("請輸入您要查詢的課程關鍵字:")

collection_ref = db.collection("111")
docs = collection_ref.get()

for doc in docs:
    result = doc.to_dict()
    if Cond in result["Course"]:
        print(result["Leacture"] + "老師開的" + result["Course"] + "課程，每週" + result["Time"] + "於" + result["Room"] + "上課")
