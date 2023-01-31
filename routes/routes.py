#routes

import json
from config.config import app
from flask import render_template,request,jsonify
from flask_cors import cross_origin
from identitical.duplicacytool import get_similar
from model.model import get_questions

@app.route("/",methods=["GET"])
@cross_origin()
def documentation():
    return "API Documentation"

@app.route("/duplicate_page",methods=["POST","GET"])
@cross_origin()
def template():
    similar=None
    if request.method=="POST":
        file=request.files["file"]
        file.seek(0)
        data=json.loads(file.read())
        similar=get_similar(data)
    return render_template("duplicate.html",similar=similar)

@app.route("/duplicate_api",methods=["POST"])
@cross_origin()
def api():
    if request.method=="POST":
        file=request.files["file"]
        file.seek(0)
        data=json.loads(file.read())
        similar=get_similar(data)
        return jsonify(similar)

@app.route("/questions",methods=["POST"])
@cross_origin()
def questions():
    if request.method=="POST":
        data=request.json
        question=get_questions(data)
        return jsonify(question)
