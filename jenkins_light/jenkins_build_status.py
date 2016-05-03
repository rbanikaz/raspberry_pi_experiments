import base64
import json 
import sys
import os
import urllib2
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import time
from rgbmatrix import Adafruit_RGBmatrix



def get_build_status():
  with open('auth.json', 'r') as f:
    config = json.load(f)
  auth = '%s:%s' % (config["username"], config["password"])
  header = b'Basic ' + base64.b64encode(auth)

  jenkinsUrl = config["url"]
  jobName = config["job"]

  try:
    url = jenkinsUrl + "job/" + jobName + "/lastBuild/api/json"
    print header+" "+url
    req = urllib2.Request(url)
    req.add_header('Authorization', header)
    resp = urllib2.urlopen(req).read()
  except urllib2.HTTPError, e:
    print "URL Error: " + str(e.code) 
    return "ERROR"

  try:
    buildStatus = json.loads( resp )
  except ValueError as err:
    print "Failed to parse json"
    print err
    return "ERROR"

  if buildStatus["building"]:
    return "BUILD_INPROGRESS"
    
  
  if buildStatus["result"]:
    return buildStatus["result"]
  else:
    return "ERROR"


QM2="QM2"
CHECKMARK= u'\u2714'
CROSS= u'\u2716'
CIRCLE = u'\u2b55'

repo = QM2
build_status = "FAILURE"#get_build_status()
freesans = ImageFont.truetype("FreeSans.ttf")
symbola = ImageFont.truetype("Symbola.ttf", 16)

if build_status == "SUCCESS":
  symbol = CHECKMARK
  color = (0,255,0)
elif build_status == "BUILD_INPROGRESS":
  symbol = None
  color = (255,255,0)
else:
  symbol = CROSS
  color = (255,0,0)

width_repo = freesans.getsize(repo)[0]
width = width_repo

if symbol is not None:
  width += symbola.getsize(symbol)[0]


matrix = Adafruit_RGBmatrix(16, 1)


image = Image.new("RGB", (width, 16), "black")
draw = ImageDraw.Draw(image)

draw.text((0, 0), repo, color, font=freesans)

if symbol is not None:
  draw.text((width_repo, 0), symbol, color, font=symbola)

for n in range(32,0 , -1):
  matrix.Clear()
  matrix.SetImage(image.im.id, n, 0)
  time.sleep(0.05)

time.sleep(1)
matrix.Clear()
time.sleep(1)
matrix.SetImage(image.im.id, 0, 0)
time.sleep(1)
matrix.Clear()
time.sleep(1)
matrix.SetImage(image.im.id, 0, 0)
time.sleep(1)
matrix.Clear()
time.sleep(1)
matrix.SetImage(image.im.id, 0, 0)
time.sleep(1)
matrix.Clear()
time.sleep(1)
matrix.SetImage(image.im.id, 0, 0)
time.sleep(100)


