from machine import I2C
import time

class WIFI(object):
    AT = b'AT\r\n'
    ATCWMODE = b'AT+CWMODE=1\r\n'
    ATCIPMODE = b'AT+CIPMODE=0\r\n'
    ATCIPMUX = b'AT+CIPMUX=1\r\n'
    ATCWLAP = b'AT+CWLAP\r\n'
    ATJAP = b'AT+CWJAP=\"Salon_24G\",\"marek204811\"\r\n'
    ATQAP = b'AT+CWQAP\r\n'
    ATCIPSERVER = b'AT+CIPSERVER=1,80\r\n'
    ATCIPSERVERCLOSE = b'AT+CIPSERVER=0\r\n'
    ATCIFSR = b'AT+CIFSR\r\n'
    ATCIPSTO = b'AT+CIPSTO=5\r\n'
    ATEOFF = b'ATE0\r\n'
    ATRFPOWER = b'AT+RFPOWER=20\r\n'
    ATSNTP = b'AT+CIPSNTPCFG=1,8,\"0.pool.ntp.org\",\"1.pool.ntp.org\",\"2.pool.ntp.org\"\r\n'
    ATDNS = b'AT+CIPDNS_DEF=1,\"91.212.2.19\"\r\n'
    ATTIME = b'AT+CIPSNTPTIME?\r\n'
    ATCIPSEND = b'AT+CIPSEND='
    ATCIPCLOSE = b'AT+CIPCLOSE='
    ATCIPSTA = b'AT+CIPSTA?\r\n'
    ATCIPSTAMAC = b'AT+CIPSTAMAC?'

    connections = []
    
    def __init__(self, uart):
        self.uart = uart
        self.send_cmd(self.AT)
        self.send_cmd(self.ATEOFF)
        self.send_cmd(self.ATCWMODE)
        self.send_cmd(self.ATCIPMODE)
        self.send_cmd(self.ATCIPMUX)
        self.send_cmd(self.ATRFPOWER)
        self.send_cmd(self.ATJAP)
        time.sleep_ms(1500)
        self.send_cmd(self.ATCIPSERVERCLOSE)
        time.sleep_ms(1500)
        self.send_cmd(self.ATCIPSERVER)
        time.sleep_ms(200)
        self.send_cmd(self.ATCIPSTA)
        time.sleep_ms(200)
        
    def read(self):
        char = self.uart.read(1)
        buf = char if char != None else None
        lastChar = b''
        while char != None and char != b'\n' and lastChar != b'\r':
            time.sleep_ms(10)
            lastChar = char
            char = self.uart.read(1)
            if char != None:
                buf += char
        return buf
        
         
    def send_cmd(self, cmd):
        print(cmd)
        self.uart.write(cmd)
        time.sleep_ms(150)
        response = self.read()
        print(response)
        while not response is None or (not response is None and response.contains("busy")):
            time.sleep_ms(250)
            response = self.read()
            print(response)
            
    def send_data(self, connection, data):
        command = str(self.ATCIPSEND, 'utf-8') + str(connection) + "," + str(len(data)) + "\r\n"
        print(command)
        self.uart.write(command)
        time.sleep_ms(200)
        #print(self.read())
        self.uart.write(data)
    
    def close_connection(self, connection):
        self.uart.write(self.ATCIPCLOSE)
        self.uart.write(str(connection))
        self.uart.write(b'\r\n')
    
    def receive(self):
        buf = "OK"
        buf = self.uart.readline()
        if not buf is None:
            print(buf)
            if buf.find(b'CONNECT') != -1:
                con = int(str(buf[0])) - 48
                self.connections.append((con,"START"))
                print(self.connections)
               # self.close_connection(con)
            if buf.find(b'CLOSED') != -1:
                con = int(str(buf[0])) - 48
                self.connections.append((con,"END"))
                print(self.connections)
            if buf.find(b'+IPD') != -1 and buf.find(b'GET') != -1 and buf.find(b'HTTP') != -1 and buf.find(b'favicon.ico') != -1:
                connection = int(str(buf[5])) - 48
                count = int(buf[7:buf.find(b':GET')])
                count -= (len(buf) - buf.find(b':GET'))
                print("html " + str(count))
                while count > 0:
                    count -= 1
                    self.uart.read()
                print("all")
                self.close_connection(connection)
            if buf.find(b'+IPD') != -1 and buf.find(b'GET') != -1 and buf.find(b'HTTP') != -1 and buf.find(b'favicon.ico') == -1:
                count = int(buf[7:buf.find(b':GET')])
                count -= (len(buf) - buf.find(b':GET'))
                print("html " + str(count))
                while count > 0:
                    count -= 1
                    self.uart.read()
                print("all")
                time.sleep_ms(100)
                connection = int(str(buf[5])) - 48
                with open('html.txt') as f:
                    lines = f.readlines()
                    data = ""
                    for line in lines:
                        data += line
                    f.close()
                self.send_data(connection, data)
                time.sleep_ms(150)
                self.close_connection(connection)
            
         

