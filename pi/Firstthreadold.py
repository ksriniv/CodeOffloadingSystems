from threading import Thread
from time import sleep
import Sendcode
import ReceiveCode

def Main():

    t1 = Thread(target= Sendcode.Send, args=())
    t2 = Thread(target= ReceiveCode.Receive, args=())
    t1.start()
    t2.start()

    
if __name__ == '__main__':
    ReceiveCode.Connect()
    Sendcode.Connect()
    Main()
