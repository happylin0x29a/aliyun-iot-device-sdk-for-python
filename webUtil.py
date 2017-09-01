#coding:utf-8
import httplib,urllib
import socket
import ssl
def getHttpsConnection(host):
    httpsConn = None
    try:    
        httpsConn = httplib.HTTPSConnection(host)
    except BaseException as e:
        print('httpsConn Error',e)
    return httpsConn
def doPost(host,url,data):
    data=urllib.urlencode(data).encode('utf8')
    conn=getHttpsConnection(host)
    headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
              "Accept":"text/xml,text/javascript,text/html,application/json"
    }
    conn.request("POST",url,data,headers)
    print('发送给服务器参数:%s'%(data))
    response=conn.getresponse()
    return response.read()
if __name__ == "__main__":
    pass