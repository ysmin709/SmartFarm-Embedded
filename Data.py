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
        self.pH = 0.0
        self.ec = 0.0
        self.rtd = 0.0
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
        
        
    def update(self, pH=0.0, ec=0.0, temp=0.0, error_type = 7000, error=False):
        if error:
            self.errors.append(error_type)
            self.local_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        else:
            self.local_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
            self.pH = pH
            self.ec = ec
            self.liquid_temperature = temp
            
        pass
    
    def post(self):
        self.uuid = self.getSerial()
        doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid)).collection(u'Sensor Data').document(u'{}'.format(self.local_time))
        doc_ref.set({
            u'uuid': self.uuid,
            u'local_time': self.local_time,
            u'pH': float(self.pH),
            u'ec': float(self.ec),
            u'liquid_temperature': float(self.liquid_temperature) 
        })
        doc_ref = db.collection(u'device').document(u'{}'.format(self.uuid))
        doc_ref.update({
            u'in_use': True,
        })
        
        pass
    
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
    
    def checkRecipe(self, ph = 0.0, ec = 0.0, rtd = 0.0):
        data = self.getRecipe()
        
        check_ph = True if ph > data['phMin'] and ph < data['phMax'] else False
        check_ec = True if ec > data['ecMin'] and ec < data['ecMax'] else False
        check_rtd = True if rtd > data['tempMin'] and rtd < data['tempMax'] else False
        
        if check_ph and check_ec and check_rtd:
            self.update(pH=ph, ec=ec, temp=rtd)
            print(ph, ec, rtd)
            self.post()
        else:
            if ph < data['phMin']: # under_ph
                self.update(error_type=5001, error=True)
                self.errorPost()
            elif ph > data['phMax']: # over ph
                self.update(error_type=5000, error=True)
                self.errorPost()
            elif ec < data['ecMin']: # under ec
                self.update(error_type=5011, error=True)
                self.errorPost()
            elif ec > data['ecMax']: # over ec
                self.update(error_type=5010, error=True)
                self.errorPost()
            elif rtd < data['tempMin']: # under temperature
                self.update(error_type=5021, error=True)
                self.errorPost()
            elif rtd > data['tempMax']: # over temperature
                self.update(error_type=5020, error=True)
                self.errorPost()
        pass
    
    
    
    
    
    