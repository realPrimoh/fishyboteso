from controls import *


def startFishing(init, run, end):
    """
    Starts the fishing codde
    :return: void
    """

    sleepFor = (1 / float(arguments["--check-frequency"]))
    G.getControlHelp = Control.getControlHelp

    Log.ctrl()
    Window.Init()
    init()

    with Listener(on_release=Control.on_release, on_press=arrow.on_press):
        while not G.stop:
            current_time = time.time()
            Window.Loop()
            Log.Loop()
            # note custom cod start

            run()

            Log.LoopEnd()
            Window.LoopEnd()
            frameTime = time.time() - current_time
            if frameTime < sleepFor:
                time.sleep(sleepFor - frameTime)
            else:
                Log.po(231, "Program taking more time than expected {:0.2f}s, "
                            "this might slow your computer try increasing --check-frequency\".".format(frameTime))
    end()
