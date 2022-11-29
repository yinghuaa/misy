import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>王櫻樺Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=櫻樺>傳送使用者暱稱</a><br>"
    homepage += "<a href=/I>櫻樺的個人網頁</a><br>"
    homepage += "<a href=/account>表單</a><br><br>"
    homepage += "<br><a href=/movie>讀取開眼電影即將上映影片，寫入Firestore</a><br>"

    homepage += "<a href=/search>選修課程查詢</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/I")
def about():
    return render_template("aboutme.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cond = request.form["course"]
        comd = request.form["Leacture"]
        db = firestore.client()
        collection_ref = db.collection("111")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["Course"] and comd in dict["Leacture"]:
                result += dict["Leacture"] + "老師開的" + dict["Course"] + "課程,每週"
                result += dict["Time"] + "於" + dict["Room"] + "上課<br>"
        if result == "":
            result = "抱歉，查無相關條件的選修課程。"
        return result
    else:
        return render_template("search.html")

@app.route("/movie", methods=["GET", "POST"])
def movie():
    if request.method == "POST":
        Cond = request.form["keyword"]
        result = "您輸入的電影關鍵字是：" + Cond

        db = firestore.client()
        collection_ref = db.collection("王櫻樺電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if Cond in dict["title"]:
                result += "片名:<a href="+ dict["hyperlink"] + ">" + dict["title"] + "</a><br>"
                result += "電影分級:"+ dict["rate"] + "<br><br>"
                #result += "電影介紹:"+ dict["hyperlink"] + "<br>"
        if result =="":
            result = "抱歉,查無相關條件的電影資訊。"
        return result
    else:
        return render_template("movie.html")

@app.route("/webhook3", methods=["POST"])
def webhook3():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        if (rate == "輔12級"):
            rate = "輔導級(未滿十二歲之兒童不得觀賞)"
        elif (rate == "輔15級"):
            rate = "輔導級(未滿十五歲之人不得觀賞)"
        info = "您選擇的電影分級是：" + rate + "，相關電影：\n"

        collection_ref = db.collection("王櫻樺電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["title"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()