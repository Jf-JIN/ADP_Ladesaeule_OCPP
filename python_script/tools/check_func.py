
import os


def isPidRunning(pid):
    try:
        return os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
