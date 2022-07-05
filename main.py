import asyncio
import time
from periodic import Periodic
import myserial


async def periodically(param):
    print(time.time(), param)
    #await asyncio.sleep(1)
    print(time.time(), param, 'Done!')
    
async def main():
    p1 = Periodic(1, myserial.getLoad(), 'Task1')
    p2 = Periodic(1, periodically, 'Task2')
    await p1.start()
    await p2.start()

nb_of_task = 2
data=[]
if __name__ == "__main__":
    myserial.checkForPorts()
    myserial.choosePort()
    myserial.chooseLogFile()
    
    
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()