import os, sys, time
from collections import namedtuple
from datetime import datetime
from datetime import timedelta
import requests


DRIVER_HOME="/home/pi/rpi-rgb-led-matrix/"
BINDING_DIR= DRIVER_HOME + "bindings/python/"
FONT_DIR= DRIVER_HOME + "fonts"

sys.path.append(BINDING_DIR)
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 4

matrix = RGBMatrix(options = options)

def get_font(fontName):
     font = graphics.Font()
     font.LoadFont(FONT_DIR + "/" + fontName + ".bdf")
     return font

def stream_messages(offscreen_canvas, messages):
    pos = offscreen_canvas.width
    while True:
        offscreen_canvas.Clear()

        len = 0
        for m in messages:
            len += graphics.DrawText(offscreen_canvas, m.font, pos + len, 12, m.color, m.message)

        pos -= 1
        if (pos + len < 0):
            break

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

Message = namedtuple('Message', ['message', 'font', 'color'])
RED = graphics.Color(255, 0, 0)
GREEN = graphics.Color(0, 255, 0)
WHITE = graphics.Color(255, 255, 255)
FONT = get_font("7x13")

def run():
    offscreen_canvas = matrix.CreateFrameCanvas()

    i = 0
    while True:
        if (i % 12 == 0):
            messages = list()
            current_time = time.strftime("%Y-%m-%d %I:%M %p")
            messages.append(Message(current_time + "    ", FONT, WHITE))
            messages.append(get_message(get_exchange_rate("BTC")))
            messages.append(get_message(get_exchange_rate("ETH")))
            messages.append(get_message(get_exchange_rate("LINK")))
            messages.append(get_message(get_exchange_rate("FIL")))
            messages.append(get_message(get_exchange_rate("SOL")))
            messages.append(get_message(get_exchange_rate("ICP")))
            messages.append(get_message(get_exchange_rate("DOGE")))
        else:
            current_time = time.strftime("%Y-%m-%d %I:%M %p")
            messages[0] = Message(current_time + "    ", FONT, WHITE)


        stream_messages(offscreen_canvas, messages)
        time.sleep(10)
        i = i + 1

def get_message(exch_rate):
    msg = "{} ${:,.2f}".format(exch_rate["symbol"], exch_rate["close_price"])
    diff = exch_rate["close_price"] - exch_rate["open_price"]
    color = RED if diff < 0 else GREEN
    percentage = diff / exch_rate["open_price"]
    msg += " ({:.1%})".format(percentage)
    return Message(msg + " ", FONT, color)


def get_exchange_rate(symbol):
    url = "https://rest.coinapi.io/v1/exchangerate/{symbol}/USD/history?period_id=12HRS&time_start={time_start}&time_end={time_end}&apikey={api_key}"
    api_key = os.environ.get("COINAPI_KEY")
    time_end = datetime.utcnow()
    time_start = (time_end - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    url = url.format(symbol=symbol, time_start=time_start, time_end=time_end.strftime("%Y-%m-%dT%H:%M:%S"))
    print(url)

    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    print(data)

    last_block = data.pop()

    return {
        "symbol": symbol,
        "close_price": last_block["rate_close"],
        "open_price": last_block["rate_open"]
    }


try:
    # Start loop
    print("Press CTRL-C to stop sample")
    run()
except KeyboardInterrupt:
    print("Exiting\n")
    sys.exit(0)
