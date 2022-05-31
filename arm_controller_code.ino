#include <Servo.h>
Servo servo[6]; 

String val = "";    
int s=0,e=0,i=0,grip=0;

int angle[6]={1500,1100,800,1650,1500,1700}; 

void setup() {
  servo[0].attach(11);//base rotation
  servo[1].attach(10);//vertical arm
  servo[2].attach(9); //horizontal arm
  servo[3].attach(6); //end effector angle
  servo[4].attach(5); //end effector rotation
  servo[5].attach(3); //gripper control
  //delay(1000); 
  for(i=0;i<=5;i++){       
     servo[i].writeMicroseconds(angle[i]);    
  }
  delay(1000); 
  Serial.begin(57600);
  delay(1000);
  pinMode(13,OUTPUT);
  
}
void grab(int pressure){
  if(pressure==0){
    for(i=angle[5];i<=1700;i++){
      servo[5].writeMicroseconds(i);
      angle[5]=i;
      delay(3);
    }
    grip=0;
    digitalWrite(13,LOW);
  }else{
    while(grip==0){
      angle[5]=angle[5]-1;
      servo[5].writeMicroseconds(angle[5]);
      delay(3);
      if(angle[5]==0 || analogRead(A2)>pressure){
        grip=1;
        digitalWrite(13,HIGH);
        break;
      }
    }   
  }
}
void loop() { 
  while (Serial.available() > 0) {  
    int inChar = Serial.read();
    val += (char)inChar;
   
    if (inChar == '\n') {
      for(i=0;i<=5;i++){      
        e=val.indexOf(",",s);
        if(i==5){
          grab((val.substring(s,e)).toInt());
        }else{
          servo[i].writeMicroseconds((val.substring(s,e)).toInt());
        }
        s=e+1;      
      }
      val = "";
      s=0;
      e=0;
    }
  }
}
