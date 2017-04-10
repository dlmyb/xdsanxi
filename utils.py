# -*- coding:utf-8 -*-
__author__ = 'dlmyb'

from envelopes import Envelope
import os

MAILHOST = os.environ['MAILHOST']
MAILACCOUNT = os.environ['MAILACCOUNT']
MAILPASSWORD = os.environ['MAILPASSWORD']

def send(html,*attachment):
    e = Envelope(
        from_addr=(unicode(MAILACCOUNT),u"Bug Report"),
        subject=u"Bug Report",
        html_body=html
    )
    e.add_to_addr(u"me@yinbin.ma")
    e.add_to_addr(u"me@zejun.li")
    for attach in attachment:
        e.add_attachment(attach,mimetype="Application/jpg")
    e.send(host=MAILHOST,login=MAILACCOUNT,password=MAILPASSWORD,tls=True)

import struct
import imghdr

def get_image_size(fhandle,fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    # with open(fname, 'rb') as fhandle:
    head = fhandle.read(24)
    fname = fname.split(".")[-1]
    if len(head) != 24:
        return
    # if imghdr.what(fname) == 'png':
    if fname == 'png':
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            return
        width, height = struct.unpack('>ii', head[16:24])
    # elif imghdr.what(fname) == 'gif':
    elif fname =='gif':
        width, height = struct.unpack('<HH', head[6:10])
    # elif imghdr.what(fname) == 'jpeg':
    elif fname == 'jpeg' or fname == 'jpg':
        try:
            fhandle.seek(0) # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                fhandle.seek(size, 1)
                byte = fhandle.read(1)
                while ord(byte) == 0xff:
                    byte = fhandle.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', fhandle.read(2))[0] - 2
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
            height, width = struct.unpack('>HH', fhandle.read(4))
        except Exception: #IGNORE:W0703
            return
    else:
        return
    return (width, height)