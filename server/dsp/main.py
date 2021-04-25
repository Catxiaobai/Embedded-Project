import psutil
import os
import win32api
import win32con
import time

deactivate_time = 10
exe_path1 = r'C:\Program Files\Notepad++\notepad++.exe'
process_name1 = "notepad++.exe"
exe_path = r'E:/大学/研一/301项目-测试生成/开发板/5--开发工具/串口调试助手/sscom32.exe'
process_name = "sscom32.exe"
path = "E:/大学/研一/301项目-测试生成/开发板/5--开发工具/串口调试助手/"
main = "sscom32.exe"

def exe_is_active():
    """
    判断"notepad++.exe"进程是否存在
    :return: 进程存在，返回False，否则为True
    """
    processes_name = []
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        processes_name.append(p.name())

    if process_name in processes_name:
        print('{} is active.'.format(process_name))
        return True
    else:
        print('{} is not active.'.format(process_name))
        return False


def start():
    if exe_is_active():
        # 终止进程
        os.system(r'taskkill /F /IM {}'.format(process_name))
        time.sleep(2)
    else:

        # 打开软件
        print('Open {}'.format(process_name))
        os.startfile(exe_path)
        time.sleep(5)

        print('Start:')
        # 模拟键盘输入ctrl+r
        # ctrl键位码是17
        win32api.keybd_event(17, 0, 0, 0)
        time.sleep(1)
        # r键位码是86
        win32api.keybd_event(86, 0, 0, 0)
        time.sleep(1)

        # 释放按键
        win32api.keybd_event(82, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(1)
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 等待执行结束
        print('Wait {}s'.format(deactivate_time))
        time.sleep(deactivate_time)

        # 终止进程
        print('Kill {}'.format(process_name))
        os.system(r'taskkill /F /IM {}'.format(process_name))