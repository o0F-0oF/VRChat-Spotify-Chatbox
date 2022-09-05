from pythonosc.udp_client import SimpleUDPClient
import win32gui
import win32process
import psutil
import ctypes
import time

spotifyName = ""
b = [f"{spotifyName}", True]
ip = "127.0.0.1"
port = 9000
client = SimpleUDPClient(ip, port)
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
def getProcessIDByName():
    spotify_pids = []
    process_name = "Spotify.exe"

    for proc in psutil.process_iter():
        if process_name in proc.name():
            spotify_pids.append(proc.pid)

    return spotify_pids

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

def getWindowTitleByHandle(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def getspotifyHandle():
    pids = getProcessIDByName()

    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return hwnd


spotify_handle = getspotifyHandle()

while(True):
    if(getWindowTitleByHandle(spotify_handle) != spotifyName):
        spotifyName = getWindowTitleByHandle(spotify_handle)
        b[0] = f"{spotifyName}"
        time.sleep(2)
        client.send_message("/chatbox/input", b)
        print("sent!")
    else:
        print("we already had it but sending it again :D")
        time.sleep(2)
        client.send_message("/chatbox/input", b)
        print("sent!")
    time.sleep(5)