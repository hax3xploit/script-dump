# Run with powershell/cmd as Admin.

import winreg


REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\RestrictRun"

file_path = input("Please Enter txt file location: ")


def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, 
                                       winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return False


with open(file_path, "r") as executable_list:
    lines = executable_list.readlines()
    #print(lines)

lines = [x.strip() for x in lines]
#print(lines)


for executable_files in lines:
    set_reg(str(executable_files), str(executable_files))
    print ("[+] "+get_reg(executable_files))  


