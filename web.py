from flask import Flask, render_template, request
from datetime import datetime, timezone, timedelta


app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>王櫻樺Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=櫻樺>傳送使用者暱稱</a><br>"
    homepage += "<a href=/account>網頁表單輸入實例</a><br>"
    homepage += "<a href=/I>櫻樺簡介網頁</a><br>"

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

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/I")
def aboutme():
    return render_template("aboutme.html")

if __name__ == "__main__":
    app.run()
