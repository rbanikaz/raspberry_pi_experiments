
import base64
import json
import sys
import urllib2
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

pac_size = 16

def get_pacman(mouth):
  image = Image.new("RGB", (pac_size , pac_size), "black")
  draw = ImageDraw.Draw(image)

  draw.ellipse((1, 1, pac_size , pac_size), fill = 'yellow', outline ='black')
  draw.ellipse((8,4,8,5), fill = 'black', outline = 'black')
  if mouth == "OPEN":
    draw.pieslice((1, 1, pac_size, pac_size ), 160, 220, fill="black", outline ='black')
  else:
    draw.pieslice((1, 1, pac_size, pac_size ), 178, 182, fill="black", outline ='black')
  return image

pacman_open = get_pacman("OPEN")
pacman_closed = get_pacman("CLOSED")

matrix = Adafruit_RGBmatrix(16, 1)

pellet = Image.new("RGB", (4, 4), "black")
draw = ImageDraw.Draw(pellet)
draw.ellipse((1,1,4,4), fill= 'blue', outline='blue')

section_width = 5

for n in range(32, -pac_size, -1):
  matrix.Clear()
  if n > 6:
    matrix.SetImage(pellet.im.id, 6, 5)
  if n > 12:
    matrix.SetImage(pellet.im.id, 12, 5)
  if n > 18:
    matrix.SetImage(pellet.im.id, 18, 5)
  if n > 24:
    matrix.SetImage(pellet.im.id, 24, 5)
  section = n / section_width
  if section % 2 == 0:
    matrix.SetImage(pacman_open.im.id, n, 0)
  else:
    matrix.SetImage(pacman_closed.im.id, n, 0)
  time.sleep(0.08)
