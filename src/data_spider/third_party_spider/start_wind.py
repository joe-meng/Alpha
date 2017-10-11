# -- coding: utf-8 --
import os
import wmi

if __name__ == '__main__':
    """
    该程序是监控wind程序是否开启的监视器
    """
    print("start")
    c = wmi.WMI()
    program_list = []
    program_path = "C:\\Wind\\Wind.NET.Client\\WindNET\\bin\\WindNET.exe"
    program_name = "wbrowser.exe"
    for process in c.Win32_Process():
        program_list.append(str(process.Name))
    if program_name not in program_list:
        print("not in ")
        try:
            os.system(program_path)
        except:
            print("start error")
    else:
        print("in")


