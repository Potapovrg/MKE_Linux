import spidev

#import OPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(10, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(1, 1)
spi.max_speed_hz = 187500
spi.cshigh=True
#spi.no_cs = True
spi.bits_per_word=8
spi.mode=0b00

#GPIO.output(10, GPIO.HIGH)
txData = [0b00001000,0x00,0,0,0,0b00000000,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,112]
rxData = spi.xfer(txData)
#GPIO.output(10, GPIO.LOW)

for i in range(len(rxData)):
    print (hex(rxData[i]))

spi.close()
