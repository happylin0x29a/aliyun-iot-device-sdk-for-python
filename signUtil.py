#coding:utf-8
import hmac
import hashlib
import time
import urllib
from webUtil import getHttpsConnection
class SignUtil(object):
    def __init__(self):
        pass
    def sign(self,deviceSecret,params,signMethod):
        Keys=[]
        canonicalizedQueryString=[]
        if isinstance(params,dict):
            Keys=params.keys()
            Keys.sort()#按照字母顺序排序
        for sortedKey in Keys:
            canonicalizedQueryString.append(sortedKey)
            canonicalizedQueryString.append(params.get(sortedKey))
        canonicalizedQueryString=''.join(canonicalizedQueryString)
        # print('canonicalizedQueryString',canonicalizedQueryString)
        if 'hmacMD5'==signMethod:
            return hmac.new(deviceSecret,canonicalizedQueryString,hashlib.md5).hexdigest()
        elif 'hmacSHA1'==signMethod:
            return hmac.new(deviceSecret,canonicalizedQueryString,hashlib.sha1).hexdigest()
        else:
            raise ValueError('没有这种加密方法')
if __name__=='__main__':
    pass