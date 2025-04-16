
from const.Const_Parameter import *
from tools.check_func import *
import subprocess


def startup():
    if os.path.exists(LOCK_FILE_PATH):
        with open(LOCK_FILE_PATH, 'r') as f:
            pid = f.read()
            if pid:
                try:
                    pid = int(pid)
                    if isPidRunning(pid):
                        return
                except:
                    pass
    python_file_path = os.path.join(APP_WORKSPACE_PATH, 'main_Client.py')
    subprocess.Popen(['python3', python_file_path],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL,
                     start_new_session=True)


if __name__ == '__main__':
    startup()
