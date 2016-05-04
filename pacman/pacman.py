
import base64
import json
import sys
import urllib2
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

radius = 16

def get_pacman(mouth):
  image = Image.new("RGB", (radius , radius), "black")
  draw = ImageDraw.Draw(image)

  draw.ellipse((1, 1, radius , radius), fill = 'yellow', outline ='black')
  if mouth == "OPEN":
    draw.pieslice((1, 1, radius, radius ), 160, 220, fill="black", outline ='black')
  else:
    draw.pieslice((1, 1, radius, radius ), 175, 185, fill="black", outline ='black')
  return image

pacman_open = get_pacman("OPEN")
pacman_closed = get_pacman("CLOSED")

matrix = Adafruit_RGBmatrix(16, 1)

span = (32,31,30,29, 24,23,22,21, 16,15,14,13, 8,7,6,5, 1,-1,-2,-3, -8,-9,-10,-11)

for n in range(32, -radius, -1):
  matrix.Clear()
  if n in span:
    matrix.SetImage(pacman_open.im.id, n, 0)
  else:
    matrix.SetImage(pacman_closed.im.id, n, 0)
  time.sleep(0.05)
