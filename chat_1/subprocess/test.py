# import sys
# import platform
# import subprocess
# from subprocess import Popen
#
# messages = ["This is Console1", "This is Console2"]
#
#
# def randomFunction():
#     return "import sys print(sys.argv[1] input('Press Enter...')"
#
#
# if platform.system() == "Windows":
#     new_window_command = "cmd.exe /c start".split()
# else:
#     new_window_command = "x-terminal-emulator -e".split()
#
# print(f"window: {new_window_command}")
# # echo = [sys.executable, "-c", randomFunction()]
# echo = [sys.executable, randomFunction()]
# print(f"echo: {echo}")
# process = [Popen(new_window_command + echo + [msg]) for msg in messages]
# print(f"process: {process}")
# for proc in process:
#     proc.wait()


# -----------------------------------------------

import subprocess

result = []
win_cmd = 'ipconfig'
# shell=True means do not show the command shell
# shell=False means show the command shell
process = subprocess.Popen(win_cmd,
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
for line in process.stdout:
    print(line)
    result.append(line)
errcode = process.returncode

print(result)
# for line in result:
#     print(line)
