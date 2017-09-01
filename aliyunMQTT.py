#coding:utf-8
#MQTT域名连接模式
import paho.mqtt.client as mqtt
from signUtil import SignUtil
import time
import json
import socket
import fcntl
import struct
import time
class AliyunMQTTDevice(object):
    def __init__(self,host="iot-as-mqtt.cn-shanghai.aliyuncs.com"
                  ,productKey="",deviceName="",deviceSecret=""):
        if not productKey or not deviceName or not deviceSecret:
            print('usage:connect([host],[url],productKey,deviceName,deviceSecret)')
            raise RuntimeError('请检查参数是否正确')          
        self.host=productKey+'.'+host
        self.deviceSecret=deviceSecret
        self.mqttClientId=None 
        self.deviceName=deviceName
        self.productKey=productKey
        self.mqttUsername=deviceName+"&"+productKey
        self.mqttPassword=None
        self.subTopic = "/"+productKey+"/"+deviceName+"/get"
        self.pubTopic = "/"+productKey+"/"+deviceName+"/update"
    def connect(self):
        self.__createMqtt()
        self.__connectMqtt(self.host,1883,self.mqttUsername,self.mqttPassword)
    def publish(self,message="",qos=0):
        if not self.mqttc or not self.pubTopic:
            raise RuntimeError("please connect first")
        self.mqttc.publish(self.pubTopic,message,qos)
    def disconnect(self):
        if self.mqttc:
            self.mqttc.disconnect()
    def __createMqtt(self):
        su=SignUtil()
        timestamp=str(time.time()).replace('.','')[:13]
        self.mqttClientId=self.__get_ip_address()+"|securemode=3,signmethod=hmacsha1,timestamp="+timestamp+"|"
        # mqttClientId: clientId+"|securemode=3,signmethod=hmacsha1,timestamp=132323232|" clientId自定义的建议mac或sn 64字符内
        d={}
        d['productKey']=self.productKey
        d['deviceName']=self.deviceName
        d['clientId']=self.__get_ip_address()
        d['timestamp']=timestamp  #可选 如果mqttClientId中有timestamp这个属性就必须要
        self.mqttPassword=su.sign(self.deviceSecret,d,'hmacSHA1')
    def __get_ip_address(self,ifname='wlan0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, 
           struct.pack('256s', ifname[:15])
        )[20:24])
    def __connectMqtt(self,host,port,mqttUsername,mqttPassword):
        self.mqttc=mqtt.Client(self.mqttClientId)
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
    deviceName = "XXXXXXX"
    deviceSecret = "XXXXXXXX"
    amd=AliyunMQTTDevice(productKey=productKey,deviceName=deviceName,deviceSecret=deviceSecret)
    amd.connect()