from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

confessions = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form.get("confession")
        emotion = request.form.get("emotion")

        if text:
            confessions.insert(0, {
                "text": text,
                "emotion": emotion,
                "time": datetime.now().strftime("%H:%M"),
                "reactions": {"❤️": 0, "😢": 0, "😮": 0}
            })
        return redirect("/")

    return render_template("index.html", confessions=confessions)

@app.route("/react/<int:i>/<emoji>")
def react(i, emoji):
    confessions[i]["reactions"][emoji] += 1
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


