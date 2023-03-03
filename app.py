from flask import Flask, redirect,url_for, request, render_template, jsonify

app=Flask(__name__)

@app.route('/')
def home():
    name=""
    return render_template("home.html", transcription=name)

if __name__=="__main__":
    app.run(debug=True)