import globalPluginHandler
import tones
import speech
import winUser
import winKernel
from ctypes import *


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_doBeep(self, gesture):
        processInfo = self.__getProcessInfo()
        speech.speakMessage(processInfo)


    def __getProcessInfo(self):
        info = ""
        hWnd = winUser.user32.GetForegroundWindow()
        if winUser.user32.IsWindow(hWnd) == False:
            return info
        pid = wintypes.DWORD()
        winUser.user32.GetWindowThreadProcessId(hWnd, byref(pid))
        if pid.value == 0:
            return info
        PROCESS_QUERY_INFORMATION = 0x0400
        hProcess = winKernel.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
        if hProcess == 0:
            return info
        max_length = wintypes.DWORD(256)
        imageName = create_string_buffer(max_length.value)
        winKernel.kernel32.QueryFullProcessImageNameA(hProcess, 0, imageName, byref(max_length))
        info = imageName.value
        info = info.decode('gbk')
        if info != "":
            info = "进程名：%s\n进程ID：%d\n进程路径：%s" % (info.split('\\')[-1], pid.value, info)

        return info


    __gestures = {
        "kb:NVDA+SHIFT+P": "doBeep"
    }
