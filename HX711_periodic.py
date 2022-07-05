#Created by h.thibault
#Created date : 01/07/2022


from curses import baudrate
import serial
import time
import logging
import serial.tools.list_ports as port_list
import os

######__Scale_config__############
logging_file = 'logHX711_50kg.csv'
baud_rate = 115200
period = 5 
scale_parameter = 1
#####__ lobal variable__#########
continuousReadings = -1

##################################

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger = logging.basicConfig(format='%(asctime)s : %(created)f : %(message)s')
formatter = logging.Formatter('%(asctime)s : %(created)f : %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(logging_file, 'a')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.CRITICAL)
logger.addHandler(file_handler)

def head_of_file():
    head = input("Enter a remarque to the head of the logging file : ")
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

def choosePortBaudRate(Baud = baud_rate):
    logger.warning('choosePortBaudRate routine : ')
    Baud = input("\nEnter Baud Rate (default to " + str(baud_rate) + " baud)")
    if Baud == "":
        Baud = baud_rate
    logger.info("BaudRate set to " + str(Baud))
    print("BaudRate set to " + str(Baud) + "\n")
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
    message = 'SI\r\n'
    logger.info("get_load-routine : " + message)
    ser.write(message.encode('Ascii'))
    
def init_scale():
    message = 'I\r\n'   #ESP32 is programmed to initialize the scale when it receives the "I" command
    logger.info("init_scale-routine : " + message)
    ser.write(message.encode('Ascii'))

def zero_scale():
    message = 'Z\r\n'   #ESP32 is programmed to zero the scale when it receives the "Z" command
    logger.warning("zero_scale-routine : " + message)
    ser.write(message.encode('Ascii'))
    
def param_scale(scale = scale_parameter):
    masse_etalon = input("Enter parametric load weight\n(Don't forget to put the weight on the scale !) : ")
    if masse_etalon =="":
        masse_etalon == scale
    message = 'ICG ' + masse_etalon + '\r\n'    #ESP32 is programmed to send weight in readable units using the given parameter "ICG xxxx" command, "xxx" representing the parametric weight applied on the scale.
    logger.warning("param_scale-routine : " + message)
    ser.write(message.encode('Ascii'))
    scale_parameter = masse_etalon
    
def save_parameter_to_EEPROM():
    MdP = input('Give password to save parameter to ESP32 :')
    if MdP == '1234':
        message = 'S\r\n'
        logger.info("save_parameter_to_EEPROM-routine : " + message)
        logger.warning("parameters saved to EEPROM")
        ser.write(message.encode('Ascii'))
    else:
        logger.info("Sorry. Wrong password.")

def set_continuousReadings(cr = 0):
    continuousReadings = cr

def check_for_command():
    if continuousReadings == 0:
        command = input ('\nEnter a command : ')
        if command == "I":
            init_scale()
        elif command =="Z":
            zero_scale()
        elif command == "ICG":
            print('\nCommand : ' + command)
            param_scale()
        elif command == "SI":
            print('\nCommand : ' + command)
            print('continuousReadings : ' + str(continuousReadings))
            set_continuousReadings(-1)
            print('continuousReadings : ' + str(continuousReadings))
        elif command == "C1":
            print('\nCommand : ' + command)
            print('continuousReadings : ' + str(continuousReadings))
            continuousReadings = 5
            set_continuousReadings(input("Enter a number of seconds between each of the consecutive weighting :\nBe aware that it is to be driven by the non real time OS and thus not so accurate ! "))
            print('continuousReadings : ' + str(continuousReadings))
        elif command == "C0":
            print('\nCommand : ' + command)
            set_continuousReadings(0)
            print('continuousReadings : ' + str(continuousReadings))
        elif command == "PC":
            print(command + " command not implemented yet")
            logger.info(command + " command not implemented yet")
        elif command == "S":
            save_parameter_to_EEPROM()
        else:
            command = input('Command not recognized.\nPlease choose one of the following command :I, Z, ICG, SI, C0, C1, PC : ')
            #print('\nChoose one of the following command :I, Z, ICG, SI, C0, C1, PC : ')
    
    

#___________MAIN___________________

ser = serial.Serial(choosePort(), choosePortBaudRate())
logger.critical('\n\n' + head_of_file())
last = 0
   

while True:
    check_for_command()

    if continuousReadings != 0:
        current_timestamp = time.time()
        if  current_timestamp - last > continuousReadings:
            last = current_timestamp
            getLoad()
            logger.debug(str(period) + ' second has elapsed')
            if continuousReadings == -1:
                continuousReadings = 0

    time.sleep(0.5)
    while (ser.inWaiting()!=0):
        datapacket = ser.readline()
        datapacket = str(datapacket, 'utf-8')
        datapacket = datapacket.strip('\r\n')
        #datapacket =datapacket.strip('?')
        # #datapacket =datapacket.strip('SI')
        logger.critical(datapacket)
