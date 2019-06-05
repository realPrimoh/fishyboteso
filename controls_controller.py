from pixel_loc import *


class Controller:

    @staticmethod
    def StartPause():
        G.pause = not G.pause
        print("PAUSED" if G.pause else "STARTED")

    @staticmethod
    def PixValConfig():
        if PixelLoc.config():
            print("Configured Successfully")
        else:
            print("Configuration failed")

    @staticmethod
    def StartMove():
        print("start moving" if FishyMove.fishy_move() else "Already Moving")

    @staticmethod
    def Debug():
        G.debug = not G.debug
        print("Debug ON" if G.debug else "Debug OFF")

    @staticmethod
    def Stop():
        G.stop = True
        print("stopping")

    @staticmethod
    def ClearPrint():
        Log.clearPrintIds()
        print("cleared only once print id")
