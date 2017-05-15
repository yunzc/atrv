#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/String.h>
#include <Arduino.h>
#include <math.h>

ros::NodeHandle nh;
std_msgs::String str_msg;
geometry_msgs::Twist cmd_vel_msg;

//Pin layout for each motor
//Motor 1 is the right motor!
int motor11 = 10;
int motor12 = 11;
int motor1activate = 8;
//activate pin needs to be HIGH to control motor
//Motor 2 is the left motor!
int motor21 = 5;
int motor22 = 6;
int motor2activate = 7;

// TODO - currently just an estimate
float ROBOT_WIDTH = 1.0; //exxagerate to get larger turning 
float WHEEL_RADIUS = 0.1525;
//in meters
float MAX_X_VELOCITY = 12.0; // [m/s]
float MAX_Z_OMEGA = 2.0; // [rad/s]


char hello[13] = "hello world!";

ros::Publisher chatter("chatter", &str_msg);

void cmd_vel_cb(const geometry_msgs::Twist& msg){

  /**
    * This is a message object. You stuff it with data, and then publish it.
    */
   std_msgs::String output_msg;
   output_msg.data = "got twist commands";
 chatter.publish( &output_msg);

  // Serial.print(String(msg.linear.x));
  // Serial.println(String(msg.angular.z));
  //send all zeros to ensure that robot stops moving
  if(msg.linear.x==0 && msg.angular.z==0){
    stopMotors();
  }
  // my attempts at converting Twist to Arduino motor commands
  // Might have left and right motors and fwd/bwd flipped
  else{
    float VEL_L = (msg.linear.x - msg.angular.z*ROBOT_WIDTH/2.0)/WHEEL_RADIUS;
    float VEL_R = (msg.linear.x + msg.angular.z*ROBOT_WIDTH/2.0)/WHEEL_RADIUS;
    drive(VEL_R, VEL_L);
  }
}

void activateMotors(){
  digitalWrite(motor1activate,HIGH);
  digitalWrite(motor2activate,HIGH);
}

void stopMotors(){
  analogWrite(motor11,0);
  analogWrite(motor12,0);
  analogWrite(motor21,0);
  analogWrite(motor22,0);
}

void killMotors(){
  Serial.println("** kill motors ** ");
  digitalWrite(motor1activate,LOW);
  digitalWrite(motor2activate,LOW);
  stopMotors();
}

// ros::Subscriber<geometry_msgs::Twist> cmd_vel_sub("aramis/cmd_vel", &cmd_vel_cb); //input needs to be in twists
ros::Subscriber<geometry_msgs::Twist> cmd_vel_sub("cmd_vel", &cmd_vel_cb); //input needs to be in twists

//ros::Subscriber<std_msgs::String> cmd_vel_str("aramis/cmd_str", &cmd_vel_string);

void drive(float vel_r, float vel_l){
  stopMotors();
  
 if (vel_r < 0){
   int skid = floor(-vel_r/MAX_X_VELOCITY*255);
   analogWrite(motor12, skid);
 }else{
   int skid = floor(vel_r/MAX_X_VELOCITY*255);
   analogWrite(motor11, skid);
 }
 if (vel_l < 0){
   int skid = floor(-vel_l/MAX_X_VELOCITY*255);
   analogWrite(motor22, skid);
 }else{
   int skid = floor(vel_l/MAX_X_VELOCITY*255);
   analogWrite(motor21, skid);
 }
}

void setup()
{

    Serial.begin(57600);

    pinMode(2, INPUT_PULLUP);
    pinMode(13, OUTPUT);

    pinMode(motor11, OUTPUT);
    pinMode(motor12, OUTPUT);
    pinMode(motor1activate, OUTPUT);
    pinMode(motor21, OUTPUT);
    pinMode(motor22, OUTPUT);
    pinMode(motor2activate, OUTPUT);

    activateMotors();

    // turnLeft();
    // delay(500);
    // turnRight();
    nh.initNode();
    nh.subscribe(cmd_vel_sub);
    // nh.subscribe(cmd_vel_str);
    nh.advertise(chatter);

}

void loop()
{

  //read the pushbutton value into a variable
 int sensorVal = digitalRead(2);
 //print out the value of the pushbutton
 Serial.println(sensorVal);
    // Serial.println(millis());

    if(sensorVal==1){
      killMotors();
      delay(4000);
    }

 // nh.spinOnce();

  nh.spinOnce();
  delay(10);

 }
