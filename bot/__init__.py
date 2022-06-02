import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath('db/db.py')))
sys.path.append(os.path.dirname(os.path.realpath('settings.py')))
sys.path.append(os.path.dirname(os.path.realpath('barcode')))
sys.path.append(os.path.dirname(os.path.realpath('barcode.py')))
import bot


if __name__ == '__main__':
    bot.start()