import serial
import time
import logging
import serial.tools.list_ports as port_list
import os

logging_file = 'log_DGTP.csv'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger = logging.basicConfig(format='%(asctime)s : %(created)f : %(message)s')
formatter = logging.Formatter('%(asctime)s * %(created)f * %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(logging_file, 'a')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.CRITICAL)
logger.addHandler(file_handler)

def head_of_file():
    head = input("Enter a remarque to the head of logging file : ")
    return head

def checkForPorts():
    logger.debug('checkForPorts routine')
    print("\nChoice | Available ports")
    ports = (port_list.comports())
    portsDictionnary={}

    for i in range(0, len(ports)):  
        portsDictionnary[str(i+1)] = ports[i].device
        print( str(i+1) + "         " + portsDictionnary[str(i+1)])
     
    print("")
    return portsDictionnary

def choosePortBaudRate():
    logger.debug('choosePortBaudRate routine')
    Baud = input("\nEnter Baud Rate (default to 9600) : ")
    if Baud == "":
        Baud = 9600
    return Baud
    
def choosePort():
    portsDictionnary = checkForPorts()
    if len(portsDictionnary) == 1:
        port = portsDictionnary["1"]
        print(port + " is the only port available and in use !")
    elif len(portsDictionnary) == 0:
        print("No serial/RS232 converter found !\nCheck for connection or add converter.\n")
    else:
        choosePort = str(input("Confirm the chosen port : "))
        type (choosePort)
        port=portsDictionnary[choosePort]
        print ("You have choosen " + port + " as port to use !")
    return port

def getLoad():
    #print(ser.write(b"SI\r\n"))
    #message = 'READ\r\n'
    message = 'GR10\r\n'
    logger.info("get_load-routine" + message)
    ser.write(message.encode('Ascii'))
    #time.sleep(0.5)
    #return ser.readline().decode()

period = 5    
last = time.time()



#___________MAIN___________________

ser = serial.Serial(choosePort(), choosePortBaudRate())
logger.critical('\n\n' + head_of_file())

while True:
    current_timestamp = time.time()
    if (current_timestamp - last > period):
        last = current_timestamp
        getLoad()
        logger.debug(str(period) + ' second has elapsed')


    if (ser.inWaiting()!=0):
        try:
            datapacket = ser.readline()
            datapacket = str(datapacket, 'utf-8')
            datapacket = datapacket.strip('\r\n')
            #datapacket =datapacket.strip('?')
            # #datapacket =datapacket.strip('SI')
            logger.critical(datapacket)
        except OSError:
            logger.critical("Data not received. Skipping..")
