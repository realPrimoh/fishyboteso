from fishing_mode import *

"""
Defines different fishing modes (states) which acts as state for state machine
also implements callbacks which is called when states are changed
"""

class FishEvent(ABC):
    @abstractmethod
    def onEnterCallback(self, previousMode):
        pass

    @abstractmethod
    def onExitCallback(self, currentMode):
        pass

class HookEvent(FishEvent):
    def onEnterCallback(self, previousMode):
        """
        called when the fish hook is detected
        increases the `fishCaught`  and `totalFishCaught`, calculates the time it took to catch
        presses e to catch the fish

        :param previousMode: previous mode in the state machine
        """
        G.fishCaught += 1
        G.totalFishCaught += 1
        timeToHook = time.time() - G.stickInitTime
        print("HOOOOOOOOOOOOOOOOOOOOOOOK....... " + str(G.fishCaught) + " caught " + "in " + str(
            round_float(timeToHook)) + " secs.  " + "Total: " + str(G.totalFishCaught))
        pyautogui.press('e')

        if arguments["--collect-r"]:
            time.sleep(0.1)
            pyautogui.press('r')
            time.sleep(0.1)

    def onExitCallback(self, currentMode):
        pass


class LookEvent(FishEvent):
    """
    state when looking on a fishing hole
    """
    def onEnterCallback(self, previousMode):
        """
        presses e to throw the fishing rod
        :param previousMode: previous mode in the state machine
        """
        pyautogui.press('e')

    def onExitCallback(self, currentMode):
        pass


class IdleEvent(FishEvent):
    """
    State when the fishing hole is depleted or the bot is doing nothing
    """

    def __init__(self, use_net):
        """
        sets the flag to send notification on phone
        :param use_net: true if user wants to send notification on phone
        """
        self.use_net = use_net

    def onEnterCallback(self, previousMode):
        """
        Resets the fishCaught counter and logs a message depending on the previous state
        :param previousMode: previous mode in the state machine
        """

        G.fishCaught = 0
        if self.use_net:
            net.sendHoleDeplete(G.fishCaught)

        if previousMode.name == "hook":
            print("HOLE DEPLETED")
        elif previousMode.name == "stick":
            print("FISHING INTERRUPTED")

    def onExitCallback(self, currentMode):
        pass


class StickEvent(FishEvent):
    """
    State when fishing is going on
    """

    def onEnterCallback(self, previousMode):
        """
        resets the fishing timer
        :param previousMode: previous mode in the state machine
        """
        G.stickInitTime = time.time()

    def onExitCallback(self, currentMode):
        pass
