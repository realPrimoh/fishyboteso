"""
fishing_event.py
Defines different fishing modes (states) which acts as state for state machine
also implements callbacks which is called when states are changed
"""
import logging
import time
from abc import abstractmethod, ABC
import random

import pyautogui

from fishy import web

_fishCaught = 0
_totalFishCaught = 0
_stickInitTime = 0
_fish_times = []
_hole_start_time = 0
_FishingStarted = False


class FishEvent(ABC):
    @abstractmethod
    def on_enter_callback(self, previous_mode):
        pass

    @abstractmethod
    def on_exit_callback(self, current_mode):
        pass


class HookEvent(FishEvent):
    def __init__(self, action_key: str, collect_r: bool):
        self.action_key = action_key
        self.collect_r = collect_r

    def on_enter_callback(self, previous_mode):
        """
        called when the fish hook is detected
        increases the `fishCaught`  and `totalFishCaught`, calculates the time it took to catch
        presses e to catch the fish

        :param previous_mode: previous mode in the state machine
        """
        global _fishCaught, _totalFishCaught

        _fishCaught += 1
        _totalFishCaught += 1
        time_to_hook = time.time() - _stickInitTime
        _fish_times.append(time_to_hook)
        logging.info("HOOOOOOOOOOOOOOOOOOOOOOOK....... " + str(_fishCaught) + " caught " + "in " + str(
            round(time_to_hook, 2)) + " secs.  " + "Total: " + str(_totalFishCaught))
        random_sleep = random.randrange(0.1, 1.3, 0.05)
        logging.info("Sleeping for " + str(random_sleep) + " seconds")
        time.sleep(random_sleep)
        pyautogui.press(self.action_key)

        if self.collect_r:
            time.sleep(0.1)
            pyautogui.press('r')
            time.sleep(0.1)

    def on_exit_callback(self, current_mode):
        pass


class LookEvent(FishEvent):
    """
    state when looking on a fishing hole
    """

    def __init__(self, action_key: str):
        self.action_key = action_key

    def on_enter_callback(self, previous_mode):
        """
        presses e to throw the fishing rod
        :param previous_mode: previous mode in the state machine
        """
        pyautogui.press(self.action_key)

    def on_exit_callback(self, current_mode):
        pass


class IdleEvent(FishEvent):
    """
    State when the fishing hole is depleted or the bot is doing nothing
    """

    def __init__(self, uid):
        """
        sets the flag to send notification on phone
        """
        self.uid = uid

    def on_enter_callback(self, previous_mode):
        """
        Resets the fishCaught counter and logs a message depending on the previous state
        :param previous_mode: previous mode in the state machine
        """
        global _fishCaught

        if _fishCaught > 0:
            web.send_hole_deplete(self.uid, _fishCaught, time.time() - _hole_start_time, _fish_times)
            _fishCaught = 0

        if previous_mode.name == "hook":
            logging.info("HOLE DEPLETED")
        else:
            logging.info("FISHING INTERRUPTED")

    def on_exit_callback(self, current_mode):
        pass


class StickEvent(FishEvent):
    """
    State when fishing is going on
    """

    def on_enter_callback(self, previous_mode):
        """
        resets the fishing timer
        :param previous_mode: previous mode in the state machine
        """
        global _stickInitTime, _hole_start_time, _fish_times, _FishingStarted

        _stickInitTime = time.time()
        _FishingStarted = True

        if _fishCaught == 0:
            _hole_start_time = time.time()
            _fish_times = []

    def on_exit_callback(self, current_mode):
        pass
