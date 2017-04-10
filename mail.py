# -*- coding:utf-8 -*-
__author__ = 'dlmyb'

from envelopes import Envelope
import os

MAILHOST = os.environ['MAILHOST']
MAILACCOUNT = os.environ['MAILACCOUNT']
MAILPASSWORD = os.environ['MAILPASSWORD']

def send(html):
    e = Envelope(
        from_addr=(unicode(MAILACCOUNT),u"Bug Report"),
        subject=u"Bug Report",
        html_body=html
    )
    e.add_to_addr(u"me@yinbin.ma")
    e.add_to_addr(u"me@zejun.li")
    e.send(host=MAILHOST,login=MAILACCOUNT,password=MAILPASSWORD,tls=True)