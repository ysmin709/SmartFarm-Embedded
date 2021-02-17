import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import time
import datetime
import pytz
import os

cred = credentials.Certificate('superfarmers-firebase-adminsdk-j56m6-37d22e20da.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'superfarmers'
})

db = firestore.client()

EXPORT204 = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"


class Data:
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"

    def __init__(self):
        self.uuid = "10000000716d0af6"
        self.local_time = None
        self.localMin = None
        self.localHour = None
        self.ph = 0.0
        self.ec = 0.0
        self.rtd = 0.0
        self.co2 = 0.0
        self.hum = 0.0
        self.errors = []
        self.uuid = os.system(EXPORT204)
        
    # ------------------- upload firebase def ------------------- #
    
    def getSerial(self):
        cpuSerial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpuSerial = line[10:26]
            f.close()
        
        except:
            cpuSerial = "ERROR"
        
        return cpuSerial
        
        
    # Set upload data
    def update(self, ph=0.0, ec=0.0, temp=0.0, co2=0.0, hum=0.0, error_type = 7000, error=False):
        if error:
            self.errors.append(error_type)
            self.local_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
            time = str(self.local_time)
            tmp1 = time.split(" ")
            tmp2 = tmp1[1].split(":")
            self.localMin = int(tmp2[1])
            self.localHour = int (tmp2[0])
        else:
            self.local_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
            time = str(self.local_time)
            tmp1 = time.split(" ")
            tmp2 = tmp1[1].split(":")
            self.localMin = int(tmp2[1])
            self.localHour = int(tmp2[0])
            self.ph = ph
            self.ec = ec
            self.liquid_temperature = temp
            self.co2 = co2
            self.hum = hum
        pass
    
    # Sensor Data upload to firestore
    def post(self):
        self.uuid = self.getSerial()  
        if self.localHour >= 0 and self.localHour <= 5:
            if self.localMin % 30 == 0:
                doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid)).collection(u'SensorData').document(u'{}'.format(self.local_time))
                doc_ref.set({
                    u'uuid': self.uuid,
                    u'local_time': self.local_time,
                    u'pH': float(self.ph),
                    u'ec': float(self.ec),
                    u'liquid_temperature': float(self.liquid_temperature),
                    u'co2': float(self.co2),
                    u'humidity': float(self.hum)
                })
                
                # Collection recognize flag
                try:
                    doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid))
                    doc_ref.update({
                        u'in_use': True,
                    })
                except:
                    doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid))
                    doc_ref.set({
                        u'in_use': True,
                    })
                
                pass
            
            else:
                pass
        else:
            if self.localMin % 5 == 0:
                doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid)).collection(u'SensorData').document(u'{}'.format(self.local_time))
                doc_ref.set({
                    u'uuid': self.uuid,
                    u'local_time': self.local_time,
                    u'pH': float(self.ph),
                    u'ec': float(self.ec),
                    u'liquid_temperature': float(self.liquid_temperature),
                    u'co2': float(self.co2),
                    u'humidity': float(self.hum)
                })
                
                # Collection recognize flag
                try:
                    doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid))
                    doc_ref.update({
                        u'in_use': True,
                    })
                except:
                    doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid))
                    doc_ref.set({
                        u'in_use': True,
                    })
                
                pass
            
            else:
                pass
    
    # error upload to firestore
    def errorPost(self):
        self.uuid = self.getSerial()
        doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid)).collection(u'error').document(u'{}'.format(self.local_time))
        doc_ref.set({
            u'uuid': self.uuid,
            u'time': self.local_time,
            u'errors': self.errors
        })
        pass
    
    
    def getRecipe(self):
        #doc_ref = db.collection(u'recipe').document(u'r3BaUsbRzZEVYWluEars')
        doc_ref = db.collection(u'recipe').document(u'test')
        try:
            doc = doc_ref.get()
            data = doc.to_dict()
        except google.cloud.exceptions.NotFound:
            print(u'No such document!')
            
        return data
    
    # --------------- use Sensor data -----------------#
    # Not use this code Error handling at Front
    def checkRecipe(self, ph = 0.0, ec = 0.0, rtd = 0.0, co2 = 0.0, hum = 0.0):
        data = self.getRecipe()
        
        check_ph = True if ph > data['phMin'] and ph < data['phMax'] else False
        check_ec = True if ec > data['ecMin'] and ec < data['ecMax'] else False
        check_rtd = True if rtd > data['tempMin'] and rtd < data['tempMax'] else False
        check_co2 = True if co2 > data['co2Min'] and co2 < data['co2Max'] else False
        check_hum = True if hum > data['humMin'] and hum < data['humMax'] else False
        
        if check_ph and check_ec and check_rtd and check_co2 and check_hum:
            self.update(ph=ph, ec=ec, temp=rtd, co2=co2, hum=hum)
            self.post()

        pass
    
    
    
    
    
    
