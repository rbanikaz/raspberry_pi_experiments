import os, sys, time, sqlite3
from collections import namedtuple
from datetime import datetime
from datetime import timedelta
import requests
from ticker_data import TickerData

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

    while True:
        messages = list()
        current_time = datetime.now()

        if current_time.hour >= 8 and current_time.hour <= 20:
            messages.append(Message(current_time.strftime("%Y-%m-%d %I:%M %p") + "    ", FONT, WHITE))
            for symbol in ["BTC", "ETH", "DOGE", "LINK", "ADA", "FIL", "SOL", "ICP"]:
                messages.append(get_message(get_exchange_rate(symbol)))

            stream_messages(offscreen_canvas, messages)

        time.sleep(10)


def get_message(exch_rate):
    msg = "{} ${:,.2f}".format(exch_rate["symbol"], exch_rate["close_price"])
    diff = exch_rate["close_price"] - exch_rate["open_price"]
    color = RED if diff < 0 else GREEN
    percentage = diff / exch_rate["open_price"]
    msg += " ({:.1%})".format(percentage)
    return Message(msg + " ", FONT, color)


def get_exchange_rate(symbol):
    con = sqlite3.connect("ticker.db")
    return TickerData(con).retrieve_rates(symbol)

if __name__ == "__main__":
    try:
        # Start loop
        print("Press CTRL-C to stop sample")
        run()
    except KeyboardInterrupt:
        print("Exiting\n")
        sys.exit(0)
