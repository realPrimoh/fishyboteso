from log import *


class Window:
    Screen = None
    windowOffset = None
    titleOffset = None
    hwnd = None
    showing = False

    def __init__(self, crop=None, color=None, scale=None):
        self.color = color
        self.crop = crop
        self.scale = scale

    @staticmethod
    def Init():
        try:
            Window.hwnd = win32gui.FindWindow(None, "Elder Scrolls Online")
            rect = win32gui.GetWindowRect(Window.hwnd)
            clientRect = win32gui.GetClientRect(Window.hwnd)
            Window.windowOffset = math.floor(((rect[2] - rect[0]) - clientRect[2]) / 2)
            Window.titleOffset = ((rect[3] - rect[1]) - clientRect[3]) - Window.windowOffset
            Window.Loop()
        except pywintypes.error:
            print("Game window not found")
            quit()

    @staticmethod
    def Loop():
        Window.showing = False

        bbox = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

        tempScreen = np.array(ImageGrab.grab(bbox=bbox))

        # tempScreen = cv2.cvtColor(tempScreen, cv2.COLOR_BGR2RGB)

        rect = win32gui.GetWindowRect(Window.hwnd)
        crop = (rect[0] + Window.windowOffset, rect[1] + Window.titleOffset, rect[2] - Window.windowOffset,
                           rect[3] - Window.windowOffset)

        Window.Screen = tempScreen[crop[1]:crop[3], crop[0]:crop[2]]

        if Window.Screen.size == 0:
            print("Don't drag game window outside the screen")
            quit(1)

    @staticmethod
    def LoopEnd():
        if not Window.showing:
            cv2.destroyAllWindows()
        else:
            cv2.waitKey(25)

    def getCapture(self):
        temp_img = Window.Screen

        if self.color is not None:
            temp_img = cv2.cvtColor(temp_img, self.color)

        if self.crop is not None:
            temp_img = temp_img[self.crop[1]:self.crop[3], self.crop[0]:self.crop[2]]

        if self.scale is not None:
            temp_img = cv2.resize(temp_img, (self.scale[0], self.scale[1]), interpolation=cv2.INTER_AREA)

        return temp_img

    def processedImage(self, func=None):
        if func is None:
            return self.getCapture()
        else:
            return func(self.getCapture())

    def show(self, name, resize=None, func=None):
        img = self.processedImage(func)

        if resize is not None:
            img = imutils.resize(img, width=resize)

        try:
            cv2.imshow(name, img)
        except:
            print("error showing img: {}".format(name))

        Window.showing = True


class PointerColor:
    win = None

    @staticmethod
    def Init():
        PointerColor.win = Window()

    @staticmethod
    def Loop():
        x, y = pyautogui.position()

        windowMinX = win32gui.GetWindowRect(Window.hwnd)[0] + Window.windowOffset
        windowMaxX = windowMinX + Window.Screen.shape[1]

        windowMinY = win32gui.GetWindowRect(Window.hwnd)[1] + Window.titleOffset
        windowMaxY = windowMinY + Window.Screen.shape[0]

        if windowMinX < x < windowMaxX and windowMinY < y < windowMaxY:
            PointerColor.win.crop = (x - windowMinX, y - windowMinY, x - windowMinX + 1, y - windowMinY + 1)

        PointerColor.win.show("mouse color", 200)

        Log.ou(PointerColor.win.processedImage(bgr2hsv)[0][0])


class WorldLoc:
    val = None
    win = None

    @staticmethod
    def Init():
        img = Window.Screen
        hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = (0, 0, 0)
        upper = (0, 0, 1)
        mask = cv2.inRange(hsvImg, lower, upper)
        contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, 2)
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        WorldLoc.win = Window(crop=(x, y, x + w, y + h), color=cv2.COLOR_BGR2GRAY)

    @staticmethod
    def GetVal():
        img = WorldLoc.win.getCapture()
        img = cv2.bitwise_not(img)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        # img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1]

        text = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=0123456789 -oem 0")

        try:
            nums = []
            for i in text.split(":"):
                nums.append(float(i))

            return nums
        except:
            time.sleep(2)
            return WorldLoc.GetVal()
