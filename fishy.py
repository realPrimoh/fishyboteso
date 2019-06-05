from loop import *


class Fishy:
    fishPixWindow = None

    @staticmethod
    def init():
        Fishy.fishPixWindow = Window(color=cv2.COLOR_BGR2HSV)
        # coodsWindow = Window()
        # mouseColor = Window()
        # PointerColor.Init()

        use_net = arguments["--ip"] is not None
        if use_net:
            net.initialize(arguments["--ip"])

        FishingMode("hook", 0, HookEvent())
        FishingMode("stick", 1, StickEvent())
        FishingMode("look", 2, LookEvent())
        FishingMode("idle", 3, IdleEvent(use_net))

        WorldLoc.Init()
        Record.Load()

    @staticmethod
    def run():
        Fishy.fishPixWindow.crop = PixelLoc.val
        FishingMode.Loop(Fishy.fishPixWindow)

        if G.debug:
            # PointerColor.Loop()
            print(WorldLoc.GetVal())
            WorldLoc.win.show("world loc")

    @staticmethod
    def end():
        # isOn[0] = False
        FishyMove.join()


if __name__ == "__main__":
    startFishing(Fishy.init, Fishy.run, Fishy.end)
