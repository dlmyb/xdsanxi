# -*- coding:utf-8 -*-
__author__ = 'dlmyb'

from flask import Flask,request,Response,render_template
import leancloud
import json
import jwt

app = Flask("__name__")

JWT_KEY = "DLMYB"

# templates 里面扔网页,static 放css,js
@app.route("/",methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/api/login",methods=['POST'])
def login():
    j = request.json
    username = j.get("username")
    password = j.get("password")
    u = leancloud.User()
    try:
        u.login(username,password)
    except leancloud.LeanCloudError as e:
        return Response(e.message,401)
    req = Response({
        "data":{
            "username":username,
            "name":u.get("name"),
            "jwt":jwt.encode({"username":username,"token":u.get_session_token()},JWT_KEY)
        }
    })
    req.headers["Content-Type"] = "application/json"
    return req

@app.route("/api/grades",methods=['POST'])
def grade():
    j = request.json
    jwtoken = j['jwt']
    try:
        info = jwt.decode(jwtoken,JWT_KEY)
    except jwt.InvalidTokenError:
        return Response("Unexited User",401)
    token = info['token']
    u = leancloud.User.become(token)
    result = {
        "data":json.loads(u.get("data")),
        "version":u.get("version")
    }
    return Response(json.dumps(result),200)

@app.route("/api/check",methods=['POST'])
def check():
    j = request.json
    jwtoken = j['jwt']
    version = j['version']
    try:
        info = jwt.decode(jwtoken,JWT_KEY)
    except jwt.InvalidTokenError:
        return Response("Unexited User",401)
    token = info['token']
    u = leancloud.User.become(token)
    if u.get("version") == version:
        return Response("",200)
    else:
        return Response("",301)



