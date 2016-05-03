import base64
import json
import sys
import os
import urllib2
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import Adafruit_RGBmatrix

CHECKMARK= u'\u2714'
CROSS= u'\u2716'
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

def get_build_status(user, pw, url, job):
  auth = '%s:%s' % (user, pw)
  header = b'Basic ' + base64.b64encode(auth)

  try:
    url = url + "job/" + job + "/lastBuild/api/json"
    print header+" "+url
    req = urllib2.Request(url)
    req.add_header('Authorization', header)
    resp = urllib2.urlopen(req).read()
    buildStatus = json.loads( resp)
  except urllib2.HTTPError, e:
    print "URL Error: " + str(e.code)
    return "ERROR"
  except ValueError as err:
    print "JSON ERROR " + err
    return "ERROR"

  if buildStatus["building"]:
    return "BUILD_INPROGRESS"

  if buildStatus["result"]:
    return buildStatus["result"]

  return "ERROR"


def draw_image(job, build_status):
  freesans = ImageFont.truetype("FreeSans.ttf")
  symbola = ImageFont.truetype("Symbola.ttf", 16)

  if build_status == "SUCCESS":
    symbol = CHECKMARK
    color = GREEN
  elif build_status == "BUILD_INPROGRESS":
    symbol = None
    color = YELLOW
  else:
    symbol = CROSS
    color = RED

  width_text = freesans.getsize(job)[0]
  width = width_text

  if symbol is not None:
    width += symbola.getsize(symbol)[0]

  image = Image.new("RGB", (width, 16), "black")
  draw = ImageDraw.Draw(image)

  draw.text((0, 0), job, color, font=freesans)

  if symbol is not None:
    draw.text((width_text, 0), symbol, color, font=symbola)

  return image


def main():
  with open('auth.json', 'r') as f:
    config = json.load(f)
  un  = config["username"]
  pw  = config["password"]
  url = config["url"]
  job = config["job"]

  matrix = Adafruit_RGBmatrix(16, 1)
  images = {};

  while 1:
    build_status = get_build_status(un, pw, url, job)

    if build_status not in images:
       images[build_status] = draw_image(job, build_status)

    image = images[build_status]

    #Scroll in from right
    for n in range(32, 0, -1):
      matrix.Clear()
      matrix.SetImage(image.im.id, n, 0)
      time.sleep(0.05)

    # Flash 3 times
    for n in range(0, 2):
      matrix.Clear()
      time.sleep(1)
      matrix.SetImage(image.im.id, 0, 0)
      time.sleep(1)

    # Stand for 1 min
    time.sleep(60)

main()
