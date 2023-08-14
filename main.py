try:
  import urequests as requests
except:
  import requests
import machine
import utime
import network
import gc
gc.collect()
#WIFI CREDENTIALS 
ssid = 'm'
password = '12345678'

#TWILLIO ACCOUNT CREDENTIALS 
account_sid = ''
auth_token = ''
# YOUR PHONE NUMBER GIVEN IN TWILLIO ACCOUNT
recipient_num = '+91'
#TWILLIO NUMBER 
sender_num = '+1'

#INITIALIZED PIN IN PICO W 
pir = machine.Pin(2, machine.Pin.IN)
redled = machine.Pin(5, machine.Pin.OUT)
buzzer_pin = machine.Pin(4, machine.Pin.OUT)
ir = machine.Pin(3, machine.Pin.IN)
yeled = machine.Pin(6, machine.Pin.OUT)
greled=machine.Pin(7, machine.Pin.OUT)

#SMS FUNCTION
def send_sms(recipient, sender,
             message, auth_token, account_sid):
      
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "To={}&From={}&Body={}".format(recipient,sender,message)
    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(account_sid)
    
    print("Trying to send SMS with Twilio")
    
    response = requests.post(url,
                             data=data,
                             auth=(account_sid,auth_token),
                             headers=headers)
    
    if response.status_code == 201:
        print("SMS sent!")
    else:
        print("Error sending SMS: {}".format(response.text))
    
    response.close()
#WIFI CONNECTION FUNCTION
def connect_wifi(ssid, password):
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())

connect_wifi(ssid, password)

#MAIN FUNCTION 
while True:

#GREEN LED IS ALWAYS ON YELLOW WILL TURN ON ONLY IF IT IS DETECTED 
    if pir.value()==1:
        greled.value(0)
        redled.value(1)
        buzzer_pin.on()
        utime.sleep(3)
        buzzer_pin.off()
        # YOU CAN CUSTOMIZE  THE MESSAGE
        message = "Some movement detected inside home lock the door call 100 immedietly"
        send_sms(recipient_num, sender_num, message, auth_token, account_sid)
        
        
    else:
        greled.value(1)
        redled.value(0)
         
#CODE FOR PIR IT WILL TURN ON 2 TIMES FOR 15 SEC WITH RED LED AND BUZZER     
    if ir.value()==1:
        greled.value(1)
        utime.sleep(1)
        yeled.value(0)
        greled.value(0)
        
    else:
        greled.value(0)
        yeled.value(1)
        message = "Some movement detected outside check survailance"
        send_sms(recipient_num, sender_num, message, auth_token, account_sid)