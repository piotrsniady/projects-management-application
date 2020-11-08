from functions import *
import sys


if __name__ == '__main__':
    argv_list = []
    if len(sys.argv) != 1:
        for i in sys.argv:
            argv_list.append(i)
        print(f'[WARNING] There should be only file name argument!. EXTRA arguments are:{argv_list[1:]}.')
        quit()
    else:
        show_menu()
