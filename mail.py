# -*- coding:utf-8 -*-
__author__ = 'dlmyb'

from envelopes import Envelope
import os

MAILHOST = os.environ['MAILHOST']
MAILACCOUNT = os.environ['MAILACCOUNT']
MAILPASSWORD = os.environ['MAILPASSWORD']

def send(html):
    e = Envelope(
        from_addr=(u"noreply@xdmsc.club",u"Bug Report"),
        subject=u"Bug Report",
        html_body=html
    )
    e.send(host=MAILHOST,login=MAILACCOUNT,password=MAILPASSWORD,tls=True)