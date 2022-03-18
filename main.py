import os
import time
import numpy as np


class Keysight(object):
    """Initializes a connection to the device port (presumably USB)"""

    def __init__(self, location):
        self.connect = os.open(location, os.O_RDWR)
        print(self.getID())

    def write(self, command):
        os.write(self.connect, str.encode(command))

    def read(self, length=4000):
        return os.read(self.connect, length).decode("utf-8")

    def getID(self):
        self.write("*IDN?")
        return self.read(100)

    def invert(self):
        self.write("SOUR:TRACk INVerted")

    def outp_high_imp(self):
        self.write("OUTPut:LOAD INFinity")

    def sine(self, freq, vpp, offset):
        self.write("SOURCe1:APPLy:SINusoid {} HZ, {} VPP, {} V".format(freq, vpp, offset))
        self.write("SOURCe2:APPLy:SINusoid {} HZ, {} VPP, {} V".format(freq, vpp, offset))

    def white_noise(self, bandwidth, vpp, offset):
        self.write("FUNCtion:NOISe:BANDwidth {}".format(bandwidth))
        self.write("SOURCe1:APPLy:NOISe 1HZ, {}V, {} V".format(vpp, offset))  # 1Hz is just a placeholder
        self.write("SOURCe2:APPLy:NOISe 1HZ, {}V, {} V".format(vpp, offset))

    def ramp(self, freq, vpp, offset):
        self.write("SOURCe1:APPLy:RAMP {} HZ, {} VPP, {} V".format(freq, vpp, offset))
        self.write("SOURCe2:APPLy:RAMP {} HZ, {} VPP, {} V".format(freq, vpp, offset))

    def sweep(self, freq_i, freq_f, Nf, vpp, offset):
        freqs = np.linspace(freq_i, freq_f, num=Nf)
        for freq in freqs:
            self.sine(freq, vpp, offset)


    def outp_off(self):
        self.write("OUTP1 OFF")
        self.write("OUTP2 OFF")
        time.sleep(2)


if __name__ == '__main__':
    keysight = Keysight("/dev/usbtmc0")
    keysight.write("*CLS")

    time.sleep(1)

    keysight.invert()
    keysight.outp_high_imp()

    keysight.sine(freq=1e3, vpp=0.5, offset=-0.5)
    time.sleep(5)
    keysight.outp_off()

    keysight.white_noise(bandwidth=2e6, vpp=0.8, offset=0.3)
    time.sleep(5)
    keysight.outp_off()

    keysight.ramp(freq=1e3, vpp=0.5, offset=-0.5)
    time.sleep(5)
    keysight.outp_off()

    keysight.sweep(freq_i=1e5, freq_f=1e6, Nf=100, vpp=0.5, offset=-0.5)
    time.sleep(5)
    keysight.outp_off()
