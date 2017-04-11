# -*- coding:utf-8 -*-
__author__ = 'dlmyb'

import json
from flask import Flask, request, Response, jsonify
from utils import send, get_image_size
import leancloud
import jwt
from StringIO import StringIO

app = Flask("__name__", static_folder='static', static_path="")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

JWT_KEY = "DLMYB"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    try:
        u = leancloud.User.become(token)
    except leancloud.LeanCloudError as e:
        return Response(e.message, 401)
    u.fetch()
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
    u.fetch()
    if u.get("version") == version:
        return Response("", 200)
    else:
        return Response("", 410)


@app.route("/api/feedback", methods=['POST'])
def feedback():
    file = request.files
    form = request.form
    try:
        jwtoken = form.get("jwt")
        email = form.get("email")
    except KeyError:
        return Response("", 400)
    try:
        info = jwt.decode(jwtoken, JWT_KEY)
    except jwt.InvalidTokenError:
        return Response("Unexited User", 401)
    imgs = file.getlist("imgs")
    fileList = list()
    for img in imgs:
        if allowed_file(img.filename) and img:
            s = StringIO(img.read())
            fileObject = leancloud.File(img.filename, s)
            width, height = get_image_size(s, img.filename)
            fileObject.metadata['width'] = width
            fileObject.metadata['height'] = height
            fileObject.save()
            fileList.append(fileObject)
        else:
            return Response("", 400)

    # fileObject = leancloud.File(imgs.filename,StringIO(imgs.read()))
    # fileObject.save()
    # fileList.append(fileObject)

    description = form.get("description")
    u = leancloud.User.become(info["token"])
    Obj = leancloud.Object.create("bugList")
    Obj.set("description", description)
    Obj.set("imgs", fileList)
    Obj.set("upload", u)
    Obj.save()
    html = \
        u"""<!doctype html>
    <head>
    <meta charset="utf-8">
    </head>
    <html lang="zh-hans">
    <body>
    <p>存在一个 Bug,由 <b><a href="mailto:{email}">{name}</a></b> 用户提出,说明如下:</p>
    <p>{description}</p>
    </br>
    {img}
    </body></html>""".format(
        name=u.get("name"),
        description=description,
        email=email,
        img="\n".join([u"<img src=\"{}\" alt=\"img\" width=\"{}\" height=\"{}\">".format(
            img.url,
            img.metadata['width'],
            img.metadata['height']
        )
                       for img in fileList])
        )
    send(html)
    return Response("Upload success!", 200)
