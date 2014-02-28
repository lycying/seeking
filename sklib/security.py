# coding:utf-8
#
# Copyright (c) 2010, guo.li <lycying@gmail.com>
# Site < http://code.google.com/p/seeking/ >
# All rights reserved.
# vim: set ft=python sw=2 ts=2 et:
#

from pyDes import triple_des,PAD_PKCS5
from hashlib import md5
import base64

def sk_encode(request,password):
    iv =  md5(password.encode('utf-8')).hexdigest()
    if len(iv) >=24:
        iv = iv[0:24]
    else:
        iv = iv+"0"*(24-len(iv))
        
    k = triple_des(iv,padmode=PAD_PKCS5)
                    
    result = base64.b64encode(k.encrypt(request.encode("utf8")))
    return result;
def sk_decode(request,password):
    iv =  md5(password.encode('utf-8')).hexdigest()
    if len(iv) >=24:
        iv = iv[0:24]
    else:
        iv = iv+"0"*(24-len(iv))
                    
    k = triple_des(iv,padmode=PAD_PKCS5)
    result = k.decrypt(base64.b64decode(request)).decode("utf8")
    return result;

