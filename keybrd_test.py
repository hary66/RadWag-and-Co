import keyboard
import time
import sys
#keyboard.write("hello")
nb = 20

def running(nb = 10):
    n = 0
    while n < nb:
        stag = n * "0"
        print(stag, end='')
        print('|', end='\r')
        time.sleep(0.3)
        print('/', end='\r')
        time.sleep(0.3)
        print('-', end='\r')
        time.sleep(0.3)
        print('\\')
        time.sleep(0.3)
        print(n)
        n += 1
        #print("\033")
        #print("\033")
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[F")

        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                print('You Pressed A Key!')
                break  # finishing the loop
        except:
            #break  # if user pressed a key other than the given key the loop will break
            pass



running()