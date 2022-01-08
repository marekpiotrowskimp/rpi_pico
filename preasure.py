import time

class Preasure:
    address = 0x5d
    def __init__(self, ssd, i2c):
        self.ssd = ssd
        self.i2c = i2c      
        self.start_preasure()
        
    def start_preasure(self):
        msg = bytearray()
        msg.append(0x90)    
        self.i2c.writeto_mem(self.address, 0x20, msg)
        msg = bytearray()
        msg.append(0x01)    
        self.i2c.writeto_mem(self.address, 0x21, msg)
        self.start = time.ticks_ms()
        
    def update(self, x, y, color, background):
        now = time.ticks_ms()
        if now - self.start > 3000:
            self.start = time.ticks_ms()
            #self.start_preasure()
            self.ssd.fill_rect(x, y - 5, 70, 25, background)
            Pressure_LSB = int.from_bytes(self.i2c.readfrom_mem(self.address, 0x29, 1), "big") 
            Pressure_MSB = int.from_bytes(self.i2c.readfrom_mem(self.address, 0x2A, 1), "big") 
            Pressure_XLB = int.from_bytes(self.i2c.readfrom_mem(self.address, 0x28, 1), "big") 
            count = (Pressure_MSB) << 16 | ( Pressure_LSB << 8 ) | Pressure_XLB
            Pressure = count/4096.0
            self.ssd.text(str(Pressure), x, y, color)

            #Temp_LSB = int.from_bytes(self.i2c.readfrom_mem(self.address, 0x2B, 1), "big") 
            #Temp_MSB = int.from_bytes(self.i2c.readfrom_mem(self.address, 0x2C, 1), "big") 
            #count = (Temp_MSB << 8) | Temp_LSB
            #comp = count - (1 << 16)
            #Temp = 42.5 + (comp/480.0)
            #self.ssd.text(str(Temp), x, y + 10, color)
 