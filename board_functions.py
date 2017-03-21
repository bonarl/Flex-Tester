import sys
import glob
import serial
import string

class Del:
  def __init__(self, keep=string.digits):
    self.comp = dict((ord(c),c) for c in keep)
  def __getitem__(self, k):
    return self.comp.get(k)
DD = Del()

def listSerialPorts():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
        
def enc(string):
    return(string.encode())

print(listSerialPorts())
coms = listSerialPorts()
class expander():
    def __init__(self, port= "/dev/ttyUSB0", baudrate = 9600):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.ser.write(enc('INIT\n'))
        self.ser.write(enc('*CLS\n'))
        self.ser.flush()
    def clear(self): 
        self.ser.write(enc('*CLS\n'))  
        return(self.ser.readline())
        #clears error register on board
    def i_d(self):
        self.ser.write(enc('*IDN?\n'))
        return(self.ser.readline())
        #returns ID of board      
    def errors(self):
        self.ser.write(enc('SYST:ERR?\n'))
        return(self.ser.readline())
        #returns any errors on board, returning 0 if none       
    def set_connectors(self, cons):
        self.ser.write(enc('CAB:CONS %s \n' % (cons)))
        return(self.ser.readline())
        #specify number of connections on board     
    def ask_connectors(self):
        self.ser.write(enc('CAB:CONS?\n'))
        return(self.ser.readline())
        #ask how many connectors on board
    def set_pins(self, pins):
        self.ser.flush()
        self.ser.write(enc('CAB:CONS?\n'))
        cons_string = str(self.ser.readline())
        cons = int(cons_string.translate(DD))
        for j in range(cons):
            self.ser.write(enc('CAB:PINS:J%s %s \n' % (j+1, pins)))
        return(self.ser.readline())          
        #set number of pins on board
    def ask_pins(self):
        self.ser.write(enc('CAB:PINS?\n'))
        return(self.ser.readline())
        #ask number of pins on board, returns list of connectors with pin numbers
    def scan(self):
        self.ser.write(enc('CAB:SCAN\n'))    
        return(self.ser.readline())
        #scan cable connections   
    def scan_length(self):
        self.ser.write(enc('CAB:SCAN\n'))
        print(self.ser.readline())
        self.ser.write(enc('CAB:UPLOAD:LEN?\n'))
        return(self.ser.readline())
        #scans connections and returns length of scan of connections table        
    def scan_results(self):
        self.ser.write(enc('CAB:SCAN\n'))
        print(self.ser.readline())
        self.ser.write(enc('CAB:UPLOAD\n'))
        results = []
        working = True
        while working == True:
            result = self.ser.readline().decode('utf-8').strip()
            if result != '<END>':
                results.append(result)
            else:
                working = False
        return(results)
        #scans and returns connections table        
    def test(self):
        self.ser.write(enc('CAB:TEST:RUN\n')) 
        while True:
            print(self.ser.readline())
        #test cable       
    def report_all(self):
        self.ser.write(enc('CAB:TEST:RUN\n'))
        print(self.ser.readline())
        self.ser.write(enc('CAB:TEST:REPORT[ALL]\n'))
        return(self.ser.readline())
        #test and report all connections from test        
    def report_fails(self):
        self.ser.write(enc('CAB:TEST:RUN\n'))
        print(self.ser.readline())
        self.ser.write(enc('CAB:TEST:REPORT[FAILS]\n'))
        while True:
            print(self.ser.readline())
        #test and report fails only        
    def save_network(self):
        self.ser.write(enc('CAB:FILE:SAVE\n'))
        return(self.ser.readline())
        #saves network profile to board     
    def load_network(self):
        self.ser.write(enc('CAB:FILE:LOAD\n'))
        return(self.ser.readline())
        #load saved profile from board
        
