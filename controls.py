from controls_controller import *
from functools import partial as p


def NextControlState():
    Control.current += 1

    if Control.current >= len(Control.controls):
        Control.current = 0

    print(Control.getControlHelp())


class Control:
    current = 1 if arguments["--debug"] else 0

    class Keywords(Enum):
        SwitchMode = p(NextControlState)
        StartPause = p(Controller.StartPause)
        Debug = p(Controller.Debug)
        Stop = p(Controller.Stop)
        ClearPrintOnce = p(Controller.ClearPrint)

        FishingConfig = p(Controller.PixValConfig)

        MoveClear = p(Record.Clear)
        MoveSave = p(Record.Save)
        MoveTo = p(Record.MoveToHere)
        MoveLookAt = p(Record.LookAtHere)
        MoveHalt = p(Record.HaltHere)
        MoveExecute = p(Controller.StartMove)

    controls = [
        {
            "name": "SYSTEM",
            "controls": [
                [Keywords.SwitchMode, Key.f7],
                [Keywords.MoveExecute, Key.f9],
                [Keywords.FishingConfig, Key.f10],
                [Keywords.StartPause, Key.f11],
                [Keywords.Stop, Key.f12]
            ]
        },
        {
            "name": "DEBUG",
            "controls": [
                [Keywords.SwitchMode, Key.f7],
                [Keywords.ClearPrintOnce, Key.f11],
                [Keywords.Debug, Key.f12],
            ]
        },
        {
            "name": "MOVE CP 1",
            "controls": [
                [Keywords.SwitchMode, Key.f7],
                [Keywords.MoveClear, Key.f10],
                [Keywords.MoveSave, Key.f11]
            ]
        },
        {
            "name": "MOVE CP 2",
            "controls": [
                [Keywords.SwitchMode, Key.f7],
                [Keywords.MoveTo, Key.f10],
                [Keywords.MoveLookAt, Key.f11],
                [Keywords.MoveHalt, Key.f12]
            ]
        }
    ]

    @staticmethod
    def getControlHelp():
        s = "\n\nCurrent Mode: " + Control.get()["name"] + "\n"
        for c in Control.controls[Control.current]["controls"]:
            s += c[0].name + ": " + c[1].name + "\n"

        return s

    @staticmethod
    def get():
        return Control.controls[Control.current]

    @staticmethod
    def find(key):
        for c in Control.get()["controls"]:
            if key == c[1]:
                return c

        return None

    @staticmethod
    def on_release(key):
        c = Control.find(key)
        if c is None:
            return

        c[0].value()
