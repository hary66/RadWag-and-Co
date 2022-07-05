from asyncio.log import logger
import serial
import serial.tools.list_ports as port_list
import logging
import os
import time

 
logging.basicConfig(level=60, format='%(asctime)s : %(created)f : %(message)s')

datalogger = logging.getLogger()
datalogger.setLevel(logging.DEBUG)
#file_handler = logging.FileHandler('activity.log')





def checkForPorts():
    datalogger.error('checkForPorts routine')
    print("\nChoice | Available ports")
    ports = (port_list.comports())
    portsDictionnary={}

    for i in range(0, len(ports)):  
        portsDictionnary[str(i+1)] = ports[i].device
        print( str(i+1) + "         " + portsDictionnary[str(i+1)])
     
    print("")
    return portsDictionnary
    
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

def init_scale():
    ser.write("I\r\n".encode())
    datalogger.info("init_scale-routine")
    ser.write("Z\r\n".encode())


def getLoad():
    #print(ser.write(b"SI\r\n"))
    datalogger.info("get_load-routine")
    ser.write("SI\r\n".encode())
    time.sleep(0.5)
    return ser.readline().decode()
    
   # if return1 == 'S A\r\n':
   #     print("Commande reçue : ", end='')
   #     print (return1)
   # return2 =ser.readline().decode()
   # print (return2)
   # return2=return2.strip('S ')
   # print (return2)
   # return2=return2.split()
   # print (return2[0])
   # logging.debug(return2[0])
   # return return2[0]

def chooseLogFile():
    #print("chooseLogFile routine")
    Data_log_file_full_path = os.getcwd()
    Data_log_file_folder = Data_log_file_full_path + "/" + (input("Enter the folder you want the file to be stored to.\n" + Data_log_file_full_path + "/"))
    #os.chdir(Data_log_file_full_path)
    Data_log_file_name = input("Enter the file you want to log the data to :")
    Data_log_file_full_path = Data_log_file_full_path + "/" + Data_log_file_name
    datalogger.debug(Data_log_file_full_path)
   # logging.basicConfig(filenanme=Data_log_file_full_path, level=logging.CRITICAL, format='%(created)f:%(message)s', filemode='a')

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    #stream_handler(message = ("choosen LogFile" + Data_log_file_full_path))
    datalogger.addHandler(stream_handler)
    file_handler = logging.FileHandler(Data_log_file_full_path, 'a')
    file_handler.setLevel(logging.DEBUG)
    datalogger.addHandler(file_handler)

######_____________main________________#####################
ser = serial.Serial(
    port= choosePort(),
    baudrate = 115200,
    timeout= 5,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    rtscts=0)

chooseLogFile()

init_scale()

logging.debug (ser.is_open)
logging.debug(ser.name)
#print (ser5.is_open)
#print(ser5.name)
data = getLoad()
logging.critical(data)
''' while 1:
    if ser.in_waiting:
        print("Serial data coming in")
        if ser.read != :
            data += ser.read()
        else:
            print(data.decode('utf8')) '''
logging.debug (ser.is_open)
ser.close()
logging.debug (ser.is_open)