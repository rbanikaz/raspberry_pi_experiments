import base64
import json 
import sys
import urllib2
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def get_build_status():
  with open('auth.json', 'r') as f:
    config = json.load(f)
  auth = '%s:%s' % (config["username"], config["password"])
  header = b'Basic ' + base64.b64encode(auth)

  jenkinsUrl = config["url"]
  jobName = config["job"]

  try:
    url = jenkinsUrl + jobName + "/lastBuild/api/json"
    req = urllib2.Request(url)
    req.add_header('Authorization', header)
    resp = urllib2.urlopen(req)
  except urllib2.HTTPError, e:
    print "URL Error: " + str(e.code) 
    print "      (job name [" + jobName + "] probably wrong)"
    return "ERROR"

  try:
    buildStatus = json.load( resp )
  except:
    print "Failed to parse json"
    return "ERROR"

  if buildStatus["building"]:
    return "BUILD_INPROGRESS"
    
  
  if buildStatus["result"]:
    return buildStatus["result"]
  else:
    return "ERROR"


QM2="QM2 "
CHECKMARK= u'\u2714'
CROSS= u'\u2716'
CIRCLE = u'\u2b55'

repo = QM2
build_status = "FAILUR"#get_build_status()
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


im = Image.new("RGB", (width, 16), "black")
draw = ImageDraw.Draw(im)

draw.text((0, 0), repo, color, font=freesans)

if symbol is not None:
  draw.text((width_repo, 0), symbol, color, font=symbola)

im.save("blah.png", "PNG")



