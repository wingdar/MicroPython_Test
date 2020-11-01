#main.py
import ssd1306
from machine import Pin, I2C
import time
import font

#====================================================================
def Draw_chinese(ch_str, x_axis, y_axis): 
   offset_ = 0 
   y_axis = y_axis*8  # 中文寬度佔 8個點  
   x_axis = (x_axis*16)  # 中文高度佔 16個點 
   for k in ch_str: 
       code = 0x00  # 將中文轉成16進制編碼 
       data_code = k.encode("utf-8") 
       code |= data_code[0] << 16 
       code |= data_code[1] << 8
       code |= data_code[2]
       byte_data = font.fonts[code]
       for y in range(0, 16):
           a_ = bin(byte_data[y]).replace('0b', '')
           while len(a_) < 8:
               a_ = '0'+a_
           b_ = bin(byte_data[y+16]).replace('0b', '')
           while len(b_) < 8:
               b_ = '0'+b_
           for x in range(0, 8):
               oled.pixel(x_axis+offset_+x, y+y_axis, int(a_[x]))   
               oled.pixel(x_axis+offset_+x+8, y+y_axis, int(b_[x]))   
       offset_ += 16
#====================================================================
i2c = I2C(-1, scl=Pin(5), sda=Pin(4), freq=400000)                

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))

oled=ssd1306.SSD1306_I2C(128, 64, i2c)


while True:
    oled.fill(1)        
    oled.show()  
    time.sleep(2)
    oled.fill(0)      
    oled.show()
    time.sleep(2)
    oled.text("Temp. ", 0, 0)
    oled.text("This is DAR ", 0, 10)
    oled.text("TEST OLED. ", 0, 20)
    oled.show()
    time.sleep(5)
    
    oled.fill(0)
    Draw_chinese('永達愛怡芳',0,0) 
    oled.show()
    time.sleep(5)