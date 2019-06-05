from window import *

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()

speedPerSec = 0.00026260921537524186


class Position:

    def __init__(self, x=0.0, y=0.0, angle=0.0):
        self.x = x
        self.y = y
        self.angle = angle

    @staticmethod
    def Input():
        x = float(input("x?"))
        y = float(input("y?"))

        return Position(x, y)

    @staticmethod
    def Get():
        vals = WorldLoc.GetVal()
        return Position(vals[0], vals[1], vals[2])

    @staticmethod
    def dist(tar, cur):
        return math.sqrt(math.pow(tar.x - cur.x, 2) + math.pow(tar.y - cur.y, 2))

    def __str__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.angle)


class Record:
    vals = []
    onHalt = False

    class MoveType(Enum):
        MOVE_TO = "move to"
        LOOK_AT = "look at"
        HALT = "halt"

    def __init__(self, moveType, data=None):
        if data is None:
            data = []
        self.moveType = moveType
        self.data = data

    @staticmethod
    def Load():
        try:
            Record.vals = pickle.load(open("MoveRecords.pickle", "rb"))
        except (OSError, IOError):
            Record.vals = []

    @staticmethod
    def Clear():
        Record.vals = []
        print("cleared")

    @staticmethod
    def Save():
        pickle.dump(Record.vals, open("MoveRecords.pickle", "wb"))
        print("saved")

    @staticmethod
    def MoveToHere():
        pos = Position.Get()
        Record.vals.append(Record(Record.MoveType.MOVE_TO, [pos.x, pos.y]))
        print("recorded move here")

    @staticmethod
    def LookAtHere():
        Record.vals.append(Record(Record.MoveType.LOOK_AT, [Position.Get().angle]))
        print("recorded look here")

    @staticmethod
    def HaltHere():
        Record.vals.append(Record(Record.MoveType.HALT))
        print("recorded halt here")

    @staticmethod
    def Execute():
        vals = Record.vals
        while True:
            for v in vals:
                while Record.onHalt:
                    time.sleep(1)

                if G.stop:
                    return

                if v.moveType == Record.MoveType.MOVE_TO:
                    FishyMove.moveTo(v.data[0], v.data[1])
                elif v.moveType == Record.MoveType.LOOK_AT:
                    FishyMove.lookAt(v.data[0])
                elif v.moveType == Record.MoveType.HALT:
                    Record.HaltExe()
            vals.reverse()


    @staticmethod
    def UnHaltExe():
        Record.onHalt = False

    @staticmethod
    def HaltExe():
        Record.onHalt = True


class FishyMove:
    thread = None

    @staticmethod
    def calcMoveSpeed():
        cur = Position.Get()

        print("running in 2 secs")
        time.sleep(3)
        keyboard.press('w')
        time.sleep(5)
        keyboard.release('w')

        final = Position.Get()

        distance = Position.dist(final, cur)
        print(distance / 5)

    @staticmethod
    def lookAt(tarAngle):
        curAngle = Position.Get().angle

        while curAngle != tarAngle:
            diff = tarAngle - curAngle
            lr = Key.left if diff > 0 else Key.right
            for i in range(int(math.fabs(diff))):
                keyboard.press(lr)

            time.sleep(2)
            curAngle = Position.Get().angle

    @staticmethod
    def moveTo(x, y):
        target = Position(x, y)
        cur = Position.Get()
        tarAngle = int(math.degrees(math.atan2(target.x - cur.x, target.y - cur.y)) % 360)

        FishyMove.lookAt(tarAngle)

        distance = Position.dist(target, cur)
        t = distance / speedPerSec
        keyboard.press('w')
        time.sleep(t)
        keyboard.release('w')

        cur = Position.Get()

        newDist = Position.dist(cur, target)
        if newDist >= 0.0003:#0.00026
            print(newDist)
            FishyMove.moveTo(x, y)

    @staticmethod
    def fishy_move():
        if FishyMove.thread is not None and FishyMove.thread.is_alive():
            return False

        FishyMove.thread = Thread(target=Record.Execute, args=())
        FishyMove.thread.start()
        return True

    @staticmethod
    def join():
        if FishyMove.thread is None:
            return

        FishyMove.thread.join()
