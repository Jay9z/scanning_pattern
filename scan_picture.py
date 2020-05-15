import numpy as np
import sys
import cv2

class ScanPattern:
    Width = 1000.0   # mm
    Length = 1000.0  # mm
    Interval = 0.1  # mm
    Speed = 0.0 #mm/s
    def __init__(self):
        self.ImageWidth = int(self.Width/self.Interval)  # mm
        self.ImageLength = int(self.Length/self.Interval)  # mm
        self.WidthFrequency = 29.75  # Hz
        self.LengthFrequency = 30.0  # Hz
        self.Time = 10.0  # second
        self.Image = np.zeros((self.ImageLength+1,self.ImageWidth+1+int(self.Speed*self.Time/self.Interval)))
        self.Phase = np.pi/4

    def image_fill(self, pos):
        x, y = pos
        ##print(*pos,":",self.Image[x,y])
        self.Image[pos] = min(self.Image[pos] + 128, 255)

    def x(self, t):
        phase = self.Phase
        fre = self.WidthFrequency
        return np.sin(2*np.pi*fre*t+phase)*self.ImageWidth/2 + self.ImageWidth/2 + t*self.Speed/self.Interval

    def y(self, t):
        fre = self.LengthFrequency
        return np.sin(2*np.pi*fre*t)*self.ImageLength/2 + self.ImageLength/2

    def scan(self):
        dt1 = np.arcsin(min(1 / self.ImageWidth/self.WidthFrequency,1))
        dt2 = np.arcsin(min(1 / self.ImageLength/self.LengthFrequency,1))
        dt = min(dt1, dt2)/10
        print(dt)
        for t in np.arange(0, self.Time, dt):
            pos = (int(self.y(t)), int(self.x(t)))
            self.image_fill(pos)

    def save(self):
        path = "x{}y{}f{}f{}p{}s{}.jpg".format(self.Width,
                                          self.Length,
                                          self.WidthFrequency,
                                          self.LengthFrequency,
                                          self.Phase,
                                          self.Speed )
        cv2.imwrite(path, self.Image)

if __name__ == "__main__":
    laserScanner = ScanPattern()
    laserScanner.scan()
    laserScanner.save()
    print("DONE!")
