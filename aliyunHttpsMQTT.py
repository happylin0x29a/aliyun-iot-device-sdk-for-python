#coding:utf-8
#使用https认证再连接模式
import paho.mqtt.client as mqtt
from signUtil import SignUtil
from webUtil import doPost
import json
class AliyunHttpsMQTTDevice(object):
    def __init__(self,host="iot-auth.cn-shanghai.aliyuncs.com",url="/auth/devicename"
                  ,productKey="",deviceName="",deviceSecret=""):
        if not productKey or not deviceName or not deviceSecret:
            print('usage:connect([host],[url],productKey,deviceName,deviceSecret)')
            raise RuntimeError('请检查参数是否正确')          
        self.host=host
        self.url=url
        self.productKey=productKey
        self.deviceName=deviceName
        self.deviceSecret=deviceSecret
        self.clientId=productKey+'&'+deviceName
        self.subTopic = "/"+productKey+"/"+deviceName+"/get"
        self.pubTopic = "/"+productKey+"/"+deviceName+"/update"
        self.mqttc=mqtt.Client(self.clientId)
    def __doPost(self):
        su=SignUtil()
        d={}
        d['productKey']=self.productKey
        d['deviceName']=self.deviceName
        d['clientId']=self.clientId
        sign=su.sign(self.deviceSecret,d,"hmacMD5") 
        #d=将所有提交给服务器的参数（version,sign,resources,signmethod除外）, 按照字母顺序排序, 然后将参数值依次拼接，无拼接符号
        d['sign']=sign
        # d['signmethod']='hmacmd5'#可选 算法类型，hmacmd5或hmacsha1
        # d['timestamp']=str(time.time()).replace('.','')[:13] #可选 	时间戳，目前时间戳并不做窗口校验，只起到加盐的作用
        d['resources']='mqtt'
        #可选 希望获取的资源描述，如mqtt。 多个资源名称用逗号隔开 不选择 服务器不回复mqtt服务器host
        result=doPost(self.host,self.url,d) #请求资源
        if result:
            mapresult=json.loads(result)
            code=mapresult['code']
            if code==200:
                print('认证成功')
            else:
                raise RuntimeError('认证失败')
            mqttHost=mapresult['data']["resources"]["mqtt"]["host"]
            port=mapresult['data']["resources"]["mqtt"]["port"]
            iotId=mapresult['data']["iotId"]
            iotToken=mapresult['data']["iotToken"]
            self.__connectMqtt(mqttHost,port,iotId,iotToken)
        else:
            raise RuntimeError("HTTPS请求失败 无返回数据")   
    def connect(self):
        self.__doPost()
    def disconnect(self):
        if self.mqttc:
            self.mqttc.disconnect()
    def publish(self,message="",qos=0):
        if not self.mqttc or not self.pubTopic:
            raise RuntimeError("please connect first")
        self.mqttc.publish(self.pubTopic,message,qos)
    def __connectMqtt(self,host,port,mqttUsername,mqttPassword):
        self.mqttc.username_pw_set(mqttUsername,mqttPassword)
        self.mqttc.subscribe(self.subTopic,1)
        self.mqttc.on_connect=self.__on_connect
        self.mqttc.on_message=self.__on_message
        self.mqttc.on_publish=self.__on_publish
        self.mqttc.on_disconnect=self.__on_disconnect
        self.mqttc.connect(host,port)
        self.publish(message="hello aliyun")
        self.mqttc.loop_forever()
    def __on_connect(self,client, userdata, flags, rc):
        if rc==0:
            print("Connect successful")
        else:
            print("Connect failed")
    def __on_message(self,client, userdata, message):
        message=message.payload.decode('utf8')
        print('receive message:%s'%(message)) 
    def __on_publish(self,client, userdata, mid):
        print('publish message success mid:%s'%(mid))
    def __on_disconnect(self,client,userdata,rc):
        if rc==0:
            print('disconnect success')
        else:
            print('disconnect fail')

if __name__=='__main__':
    productKey = "XXXXXXX"
    deviceName = "XXXXXX"
    deviceSecret = "XXXXXXXX"
    amt=AliyunHttpsMQTTDevice(productKey=productKey,deviceName=deviceName,deviceSecret=deviceSecret)
    amt.connect()