from __future__ import division

import serial

class Arduino(object):
  finger_thres = 0.6
  max_line_size = 100
  port = '/dev/tty.HC-06-DevB'
  max_val = 570
  min_val = 250
  
  def __init__(self, use_accel = False):
    self.use_accel = use_accel
    self.ser = serial.Serial(\
          port=self.port,\
          baudrate=9600,\
          parity=serial.PARITY_NONE,\
          timeout=10,\
          stopbits=serial.STOPBITS_ONE,\
          bytesize=serial.EIGHTBITS)
  
  def on_update(self):
    data_str = self.ser.readline()
    return self.parse_data(data_str)

  def parse_data(self, data_str):
    data = data_str.split()
    fingers_down = []
    for d in data[:4]:
      state = (int(d) - self.min_val)/(self.max_val - self.min_val)
      if state < self.finger_thres:
        fingers_down.append(True)
      else:
        fingers_down.append(False)
    return fingers_down

  def disable(self):
    self.ser.close()

  def enable(self):
    self.ser.open()
      
