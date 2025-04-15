
from const.Const_Parameter import *


def startup():
    if os.path.exists(LOCK_FILE_PATH):
        print('The program is already running.')
        return
    else:
        with open(LOCK_FILE_PATH, 'w') as f:
            f.write('lock')
        python_file_path = os.path.join(APP_WORKSPACE_PATH, 'main_Client.py')
        os.system(f'python3 {python_file_path}')


if __name__ == '__main__':
    startup()
