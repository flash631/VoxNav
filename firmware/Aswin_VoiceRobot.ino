#include <SoftwareSerial.h>
SoftwareSerial BT(0, 1);
String readvoice;
const byte MOTOR_A = 3;
const byte MOTOR_B = 2;
const int mspeed = 200;
const float stepcount = 20.00;
const float wheeldiameter = 66.10;
volatile int counter_A = 0;
volatile int counter_B = 0;
// Motor A
int enA = 10;
int in1 = 9;
int in2 = 8;
// Motor B
int enB = 5;
int in3 = 7;
int in4 = 6;
void ISR_countA()  
{
  counter_A++;
} 
void ISR_countB()  
{
  counter_B++;
}
int CMtoSteps(float cm) 
{
  int result;
  float circumference = (wheeldiameter * 3.14) / 10;
  float cm_step = circumference / stepcount;
  float f_result = cm / cm_step;
  result = (int) f_result;
  return result; 
}
void MoveForward(int steps) 
{
   counter_A = 0;
   counter_B = 0;
   digitalWrite(in1, HIGH);
   digitalWrite(in2, LOW);
   digitalWrite(in3, HIGH);
   digitalWrite(in4, LOW);
   while (steps > counter_A && steps > counter_B) 
   {
    if (steps > counter_A) 
    {
    analogWrite(enA,mspeed);
    }
    else 
    {
    analogWrite(enA,0);
    }
    if (steps > counter_B)
    {
    analogWrite(enB,mspeed);
    }
    else 
    {
    analogWrite(enB,0);
    }
   }
  analogWrite(enA,0);
  analogWrite(enB,0);
  counter_A = 0;
  counter_B = 0;
}
void MoveReverse(int steps) 
{
   counter_A = 0;
   counter_B = 0;
   digitalWrite(in1, LOW);
   digitalWrite(in2, HIGH);
   digitalWrite(in3, LOW);
   digitalWrite(in4, HIGH);
   while (steps > counter_A && steps > counter_B) 
   {
    if (steps > counter_A) 
    {
    analogWrite(enA,mspeed);
    }
    else 
    {
    analogWrite(enA,0);
    }
    if (steps > counter_B) 
    {
    analogWrite(enB,mspeed);
    }
    else 
    {
    analogWrite(enB,0);
    }
   }
   analogWrite(enA,0);
   analogWrite(enB,0);
   counter_A = 0;
   counter_B = 0;
}
void SpinRight(int steps) 
{
  counter_A = 0;
  counter_B = 0;
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  while (steps > counter_A && steps > counter_B) 
  {
   if (steps > counter_A) 
   {
   analogWrite(enA,mspeed);
   }
   else 
   {
    analogWrite(enA,0);
   }
   if (steps > counter_B) 
   {
    analogWrite(enB,mspeed);
   } 
   else 
   {
    analogWrite(enB,0);
   }
  }
  analogWrite(enA,0);
  analogWrite(enB,0);
  counter_A = 0; 
  counter_B = 0;  
}
void SpinLeft(int steps) 
{
  counter_A = 0;
  counter_B = 0;
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  while (steps > counter_A && steps > counter_B) 
  {
   if (steps > counter_A) 
   {
    analogWrite(enA,mspeed);
   }
   else 
   {
    analogWrite(enA,0);
   }
   if (steps > counter_B) 
   {
    analogWrite(enB,mspeed);
   }
   else 
   {
    analogWrite(enB,0);
   }
  }
  analogWrite(enA,0);
  analogWrite(enB,0);
  counter_A = 0;
  counter_B = 0;
}
void setup() 
{
  BT.begin(9600);
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt (MOTOR_A), ISR_countA, RISING);
  attachInterrupt(digitalPinToInterrupt (MOTOR_B), ISR_countB, RISING);
} 
void loop()
{ 
  while (BT.available())
  {  
  delay(10);
  String c = BT.read();
  char x = ' ';
  int b = c.indexOf(x);
  String cm1 = c.substring(0,b);
  String side = c.substring(b+1);
  float cm2 = cm1.atof;
  Serial.println(cm2);
  int y = CMtoSteps(cm2);
  Serial.println(side);
  readvoice += side;
  if (readvoice.length() > 0) 
  {
    Serial.println(readvoice);
  if(readvoice == "forward")
  {
    MoveForward(y);
    delay(100);
  }
  else if(readvoice == "back")
  {
    MoveReverse(y);
    delay(100);
  }
  else if (readvoice == "left")
  {
    SpinLeft(y);
    delay(100);
  }
 else if ( readvoice == "right")
 {
   SpinRight(y);
   delay(100);
 }
 }
}
