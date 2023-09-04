import spidev

spi = spidev.SpiDev()
spi.open(1, 1)
spi.max_speed_hz = 187500
spi.cshigh=True
#spi.no_cs = True
spi.bits_per_word=8
spi.mode=0b00

txData = [0b00010000,0x00,0,0,0,0b00000000,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,224]
rxData = spi.xfer(txData)


for i in range(len(rxData)):
    print (hex(rxData[i]))

spi.close()
