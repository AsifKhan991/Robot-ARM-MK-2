from tkinter import *
import pickle
import time
import math
import serial

COM='COM7'
baud=57600
val=[]
pos_data=[]
port=1
Ardu_stat=1

step=5

if Ardu_stat==1:
    try:
        arduino = serial.Serial(COM, baud,timeout=5)
        print(' Port found! ')
    except serial.serialutil.SerialException:
        print(' Port not found! ')
        
        port=0

with open('pos.pkl','rb') as f:
    val = pickle.load(f)

for e in val:  #convert string values to integer
    pos=e[:-2].split(',')
    data=[]
    for n in pos:
        data.append(int(n))
    pos_data.append(data)
    
def i2s(x):
    s=''
    for e in x:
        s=s+str(e)+','
    return s+'\n'
time.sleep(2)

pre=pos_data[0]


run = Ardu_stat==1 and port == 1
time.sleep(2)

while run:
    #print(i2s(pos_data[0]))
    #arduino.write(i2s(pos_data[1]).encode())
    for i in range(len(pos_data)):
        pres=pos_data[i]
        print(i)
        while True:
                        
            if pre[0]!=pres[0] :
                diff=abs(pre[0]-pres[0])
                dr = 2500 
                if pres[0]<pre[0]:
                    dr = 500
                pre[0]=dr
                arduino.write(i2s(pre).encode())
                time.sleep(diff*0.00009*32)
                pre[0]=pres[0]
                arduino.write(i2s(pre).encode())
                time.sleep(2)
                
            elif pre[5]!=pres[5] :
                pre[5]=pres[5]
                arduino.write(i2s(pre).encode())
                time.sleep(4)
            else:
                arduino.write(i2s(pre).encode())
                
            arm_start=time.time()
            
            while(time.time()-arm_start<0.02):
                a=0
            for j in range(1,5):
                if (pres[j]-pre[j]<0):         
                    pre[j]=pre[j]-step
                elif (pres[j]-pre[j]>0):
                    pre[j]= pre[j]+step

                if abs(pre[j]-pres[j])<=step:
                    pre[j]=pres[j]
            
                
            if pre[1:5]==pres[1:5]: 
                break        
        














        
    
    
        
        
