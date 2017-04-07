# -*- coding:utf-8 -*-
__author__ = 'dlmyb'

import json
from flask import Flask, request, Response, jsonify
import leancloud
import jwt

app = Flask("__name__", static_folder='static', static_path="")

JWT_KEY = "DLMYB"


@app.errorhandler(404)
def index(e):
    return app.send_static_file("index.html")


@app.route("/api/login", methods=['POST'])
def login():
    j = request.json
    username = j.get("username")
    password = j.get("password")
    u = leancloud.User()
    try:
        u.login(username, password)
    except leancloud.LeanCloudError as e:
        return Response(e.message, 401)

    resp = {
        "data": {
            "username": username,
            "name": u.get("name"),
            "jwt": jwt.encode({"username": username, "token": u.get_session_token()}, JWT_KEY)
        }
    }
    return jsonify(resp)


@app.route("/api/grades", methods=['POST'])
def grade():
    j = request.json
    try:
        jwtoken = j["jwt"]
        info = jwt.decode(jwtoken, JWT_KEY)
    except (jwt.InvalidTokenError, KeyError):
        return Response("Unexited User", 401)
    token = info['token']
    u = leancloud.User.become(token)
    result = {
        "data": json.loads(u.get("data")),
        "version": u.get("version")
    }
    return Response(json.dumps(result), 200)


@app.route("/api/check", methods=['POST'])
def check():
    j = request.json
    try:
        jwtoken = j['jwt']
        version = j['version']
    except KeyError:
        return Response("miss parms", 400)

    try:
        info = jwt.decode(jwtoken, JWT_KEY)
    except jwt.InvalidTokenError:
        return Response("Unexited User", 401)

    token = info['token']
    u = leancloud.User.become(token)
    if u.get("version") == version:
        return Response("", 200)
    else:
        return Response("", 410)
