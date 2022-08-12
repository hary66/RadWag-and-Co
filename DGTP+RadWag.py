import serial
import time
import logging
import serial.tools.list_ports as port_list
import os

logging_file = 'log_DGTP+RAdWag.csv'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger = logging.basicConfig(format='%(asctime)s : %(created)f : %(message)s')
formatter = logging.Formatter('%(asctime)s * %(created)f * %(message)s')

stream_handler = logging.StreamHandler()
#stream_handler.setLevel(logging.WARNING)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(logging_file, 'a')
file_handler.setFormatter(formatter)
#file_handler.setLevel(logging.CRITICAL)
file_handler.setLevel(logging.DEBUG)

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


def getLoad_all():
    getLoad_RadWag()
    getLoad_DGTP()

def getLoad_RadWag():
    message = 'SI\r\n'
    logger.info("get_load-routine" + message)
    ser_RadWag.write(message.encode('Ascii'))
    logger.debug('4')

    

def getLoad_DGTP():
    message = 'GR10\r\n'
    logger.info("get_load-routine" + message)
    ser_DGTP.write(message.encode('Ascii'))
    logger.debug('5')


period = 5    
last = time.time()



#___________MAIN___________________

ser_RadWag = serial.Serial(choosePort(), choosePortBaudRate())
ser_DGTP = serial.Serial(choosePort(), choosePortBaudRate())
logger.critical('\n\n' + head_of_file())

msg = [0, 0]
RadWag_flag = 0
DGTP_flag = 0
while True:
    current_timestamp = time.time()
    if (current_timestamp - last > period):
        last = current_timestamp
        getLoad_all()
        logger.debug(str(period) + ' second has elapsed')


    if (ser_RadWag.inWaiting()!=0):
        try:
            datapacket = ser_RadWag.readline()
            datapacket = str(datapacket, 'utf-8')
            datapacket = datapacket.strip('\r\n')
            #datapacket =datapacket.strip('?')
            # #datapacket =datapacket.strip('SI')
            msg[0] = datapacket
            RadWag_flag = 1
            logger.debug('1')
        except OSError:
            logger.critical("Data not received. Skipping..")

    if (ser_DGTP.inWaiting()!=0):
        try:
            datapacket = ser_DGTP.readline()
            datapacket = str(datapacket, 'utf-8')
            datapacket = datapacket.strip('\r\n')
            #datapacket =datapacket.strip('?')
            # #datapacket =datapacket.strip('SI')
            msg[1] = datapacket
            DGTP_flag = 1
            logger.debug('2')

        except OSError:
            logger.critical("Data not received. Skipping..")
            
    if (RadWag_flag & DGTP_flag):
        message = msg[0] + "* " + msg[1]
        #message = msg[0]

        RadWag_flag = 0
        DGTP_flag = 0
        logger.critical(message)
        logger.debug('3')

