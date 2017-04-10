# coding: utf-8

from leancloud import Engine,HttpsRedirectMiddleware
from app import app

engine = Engine(HttpsRedirectMiddleware(app))
# @engine.define
# def hello(**params):
#     if 'name' in params:
#         return 'Hello, {}!'.format(params['name'])
#     else:
#         return 'Hello, LeanCloud!'

#
# @engine.after_save("bugList")
# def bugreport(item):
#     imgList = item.get("imgs")
#     map(lambda x:x.fetch(),imgList)
#     u = item.get("upload").fetch()
#     html = \
#     """<!doctype html>
#     <html lang="zh-hans">
#     <body>
#     <p>存在一个 Bug,由 <b>{name}</b> 用户提出,说明如下:</p>
#     <p>{description}</p>
#     {img}
#     </body></html>""".format(
#         name=u.get("name"),
#         description=item.get("description"),
#         img="\n".join(["<img src=\"{}\" alt=\"img\">".format(img.url) for img in imgList])
#     )
#     print "sending emails!"
#     send(html)
