#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   基础模版
@Time    :   2024年4月2日15:29:02
@Author  :   cwz
'''

# here put the import lib
import re
import threading
import configparser
import win32api
import win32con
import win32gui
import win32ui
import time
# import threading
import numpy as np
import os
from PIL import Image
from PIL import ImageOps
import aircv as ac
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT
import string
import math
import datetime
from paddleocr import PaddleOCR

# import sys
import cv2

import requests

scale = 1.5  # 电脑的缩放比例
radius = 5  # 随机半径
x_coor = 10  # 窗口位置
y_coor = 10  # 窗口位置
pic_path = "maifeng_pic"  # 图片路径


class GameAutoBase:
    """
    @description  :自动点击类，包含后台截图、图像匹配
    ---------
    @param  :
    -------
    @Returns  :
    -------
    """

    def __init__(self, handle: HWND = None):
        '''
        初始化可以指定句柄  也可以不指定
        :param handle:
        '''
        if handle:
            self.__handle = handle
        else:
            self.__handle = self.find_win()
            print(self.__handle)
        self.__clickhandle = self.__handle
        self.__PostMessageW = windll.user32.PostMessageW
        self.__SendMessageW = windll.user32.SendMessageW
        self.__MapVirtualKeyW = windll.user32.MapVirtualKeyW
        self.__VkKeyScanA = windll.user32.VkKeyScanA
        self.__ClientToScreen = windll.user32.ClientToScreen
        self.__WM_KEYDOWN = 0x100
        self.__WM_KEYUP = 0x101
        self.__WM_MOUSEMOVE = 0x0200
        self.__WM_LBUTTONDOWN = 0x0201
        self.__WM_LBUTTONUP = 0x202
        self.__WM_MOUSEWHEEL = 0x020A
        self.__WHEEL_DELTA = 120
        self.__WM_SETCURSOR = 0x20
        self.__WM_MOUSEACTIVATE = 0x21
        self.__WM_MOUSELEAVE = 0x02A3
        self.__MK_CONTROL = 0x0008
        self.__HTCLIENT = 1
        self.__MA_ACTIVATE = 1
        self.__VkCode = {
            "back": 0x08,
            "tab": 0x09,
            "return": 0x0D,
            "shift": 0x10,
            "control": 0x11,
            "menu": 0x12,
            "pause": 0x13,
            "capital": 0x14,
            "escape": 0x1B,
            "space": 0x20,
            "end": 0x23,
            "home": 0x24,
            "left": 0x25,
            "up": 0x26,
            "right": 0x27,
            "down": 0x28,
            "print": 0x2A,
            "snapshot": 0x2C,
            "insert": 0x2D,
            "delete": 0x2E,
            "lwin": 0x5B,
            "rwin": 0x5C,
            "numpad0": 0x60,
            "numpad1": 0x61,
            "numpad2": 0x62,
            "numpad3": 0x63,
            "numpad4": 0x64,
            "numpad5": 0x65,
            "numpad6": 0x66,
            "numpad7": 0x67,
            "numpad8": 0x68,
            "numpad9": 0x69,
            "multiply": 0x6A,
            "add": 0x6B,
            "separator": 0x6C,
            "subtract": 0x6D,
            "decimal": 0x6E,
            "divide": 0x6F,
            "f1": 0x70,
            "f2": 0x71,
            "f3": 0x72,
            "f4": 0x73,
            "f5": 0x74,
            "f6": 0x75,
            "f7": 0x76,
            "f8": 0x77,
            "f9": 0x78,
            "f10": 0x79,
            "f11": 0x7A,
            "f12": 0x7B,
            "numlock": 0x90,
            "scroll": 0x91,
            "lshift": 0xA0,
            "rshift": 0xA1,
            "lcontrol": 0xA2,
            "rcontrol": 0xA3,
            "lmenu": 0xA4,
            "rmenu": 0XA5
        }

        # 推送平台配置
        self.s = requests.Session()
        self.push_plus_token = "" # pushPlus推送加
        self.server_push_token = "SCT129817T6chIXiMSf9xJPLA9a9vgEUYg" # 方糖（server酱）

        # 挂机设置
        self.tili_apple = False # 苹果兑换体力
        self.tili_buy = True # 钻石购买体力

    def find_win(self, cla="LDPlayerMainFrame", winname=None):
        hwndMain = win32gui.FindWindow(cla, winname)
        print("hwndMain=>{}".format(hwndMain))
        if win32gui.IsIconic(hwndMain):
            #     # 模拟将最小化窗口还原
            win32gui.SendMessage(hwndMain, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            win32gui.SetForegroundWindow(hwndMain)
        hwndChild = win32gui.FindWindowEx(hwndMain, None, "RenderWindow", None)
        return hwndChild

    def __get_virtual_keycode(self, key: str):
        """根据按键名获取虚拟按键码

        Args:
            key (str): 按键名

        Returns:
            int: 虚拟按键码
        """
        if len(key) == 1 and key in string.printable:
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
            return self.__VkKeyScanA(ord(key)) & 0xff
        else:
            return self.__VkCode[key]

    def __key_down(self, handle: HWND, key: str):
        """按下指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.__get_virtual_keycode(key)
        scan_code = self.__MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        wparam = vk_code
        lparam = (scan_code << 16) | 1
        self.__PostMessageW(handle, self.__WM_KEYDOWN, wparam, lparam)

    def __key_up(self, handle: HWND, key: str):
        """放开指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.__get_virtual_keycode(key)
        scan_code = self.__MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        self.__PostMessageW(handle, self.__WM_KEYUP, wparam, lparam)

    def __activate_mouse(self, handle: HWND):
        """
        @Description : 激活窗口接受鼠标消息
        ---------
        @Args : handle (HWND): 窗口句柄
        -------
        @Returns :
        -------
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mouseactivate
        lparam = (self.__WM_LBUTTONDOWN << 16) | self.__HTCLIENT
        self.__SendMessageW(handle, self.__WM_MOUSEACTIVATE, handle, lparam)

    def __set_cursor(self, handle: HWND, msg):
        """
        @Description : Sent to a window if the mouse causes the cursor to move within a window and mouse input is not captured
        ---------
        @Args : handle (HWND): 窗口句柄, msg : setcursor消息
        -------
        @Returns :
        -------
        """
        # https://docs.microsoft.com/en-us/windows/win32/menurc/wm-setcursor
        lparam = (msg << 16) | self.__HTCLIENT
        self.__SendMessageW(handle, self.__WM_SETCURSOR, handle, lparam)

    def __move_to(self, handle: HWND, x: int, y: int):
        """移动鼠标到坐标（x, y)

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
        wparam = 0
        lparam = y << 16 | x
        self.__PostMessageW(handle, self.__WM_MOUSEMOVE, wparam, lparam)

    def __left_down(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)按下鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
        wparam = 0x001  # MK_LBUTTON
        # wparam = 0  # MK_LBUTTON
        lparam = y << 16 | x
        self.__PostMessageW(handle, self.__WM_LBUTTONDOWN, wparam, lparam)

    def __left_up(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)放开鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
        wparam = 0x001  # MK_LBUTTON
        lparam = y << 16 | x
        self.__PostMessageW(handle, self.__WM_LBUTTONUP, wparam, lparam)

    def __scroll(self, handle: HWND, delta: int, x: int, y: int):
        """在坐标(x, y)滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            delta (int): 为正向上滚动，为负向下滚动
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.__activate_mouse(handle)
        self.__move_to(handle, x, y)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
        wparam = delta << 16
        p = POINT(x, x)
        self.__ClientToScreen(handle, byref(p))
        lparam = p.y << 16 | p.x
        self.__PostMessageW(handle, self.__WM_MOUSEWHEEL, wparam, lparam)

    def __scroll_up(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)向上滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.__scroll(handle, self.__WHEEL_DELTA, x, y)

    def __scroll_down(self, handle: HWND, x: int, y: int):
        """在坐标(x, y)向下滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.__scroll(handle, -self.__WHEEL_DELTA, x, y)

    def zoom_out(self, handle: HWND, x: int, y: int):
        """    捏合   Ctrl+鼠标轮滑

                Args:
                    handle (HWND): 窗口句柄
                    delta (int): 为正向上滚动，为负向下滚动
                    x (int): 横坐标
                    y (int): 纵坐标
                """
        self.__activate_mouse(handle)
        wParam = self.__MK_CONTROL | -self.__WHEEL_DELTA << 16
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
        p = POINT(x, y)
        self.__ClientToScreen(handle, byref(p))
        lparam = p.y << 16 | p.x
        self.__PostMessageW(handle, self.__WM_MOUSEWHEEL, wParam, lparam)

    def zoom_in(self, handle: HWND, x: int, y: int):
        """ 放大   Ctrl+鼠标轮滑

                Args:
                    handle (HWND): 窗口句柄
                    delta (int): 为正向上滚动，为负向下滚动
                    x (int): 横坐标
                    y (int): 纵坐标
        """
        self.__activate_mouse(handle)
        wParam = self.__MK_CONTROL | self.__WHEEL_DELTA << 16
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
        p = POINT(x, y)
        self.__ClientToScreen(handle, byref(p))
        lparam = p.y << 16 | p.x
        self.__PostMessageW(handle, self.__WM_MOUSEWHEEL, wParam, lparam)

    def get_winds(self, title: str):
        """
        @description : 获取游戏句柄 ,并把游戏窗口置顶并激活窗口
        ---------
        @param : 窗口名
        -------
        @Returns : 窗口句柄
        -------
        """
        self.__handle = windll.user32.FindWindowW(None, title)
        # self.__handle = 9636862
        self.__classname = win32gui.GetClassName(self.__handle)
        # print(self.__classname)
        self.__clickhandle = self.__handle
        # self.__subhandle = win32gui.FindWindowEx(self.__renderhandle, 0, "subWin", "sub")
        # print(self.__subhandle)
        # self.__subsubhandle = win32gui.FindWindowEx(self.__subhandle, 0, "subWin", "sub")
        # print(self.__subsubhandle)
        # win32gui.ShowWindow(hwnd1, win32con.SW_RESTORE)
        # print(win32gui.GetWindowRect(hwnd1))
        win32gui.SetWindowPos(self.__handle, win32con.HWND_TOP, x_coor, y_coor, 0, 0,
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
        print(self.__clickhandle)
        return self.__handle

    def get_src(self):
        """
        @description : 获得后台窗口截图
        ---------
        @param : None
        -------
        @Returns : None
        -------
        """

        left, top, right, bot = win32gui.GetWindowRect(self.__handle)
        # Remove border around window (8 pixels on each side)
        bl = 8
        # Remove border on top
        bt = 39

        width = int((right - left + 1) * scale) - 2 * bl
        height = int((bot - top + 1) * scale) - bt - bl
        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hWndDC = win32gui.GetWindowDC(self.__handle)
        # 创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        # 创建内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 为bitmap开辟存储空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        # 将截图保存到saveBitMap中
        saveDC.SelectObject(saveBitMap)
        # 保存bitmap到内存设备描述表
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (bl, bt), win32con.SRCCOPY)
        ###获取位图信息
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        ###生成图像
        im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        # 内存释放
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.__handle, hWndDC)
        ###PrintWindow成功,保存到文件,显示到屏幕
        im_PIL.save("src.jpg")  # 保存
        # im_PIL.show()  # 显示

    def find_pic(self, picname, ret=(0, 0, 540, 960), r=0.8):
        """
        @description : 图像识别之模板匹配
        ---------
        @param : 需要匹配的模板名
        -------
        @Returns : 将传进来的图片和全屏截图匹配如果找到就返回图像在屏幕的坐标 否则返回None
        -------
        """
        imsrc = self.window_capture(ret[0], ret[1], ret[2], ret[3])
        for pic in picname.split("|"):
            imobj = ac.imread('{}\\{}\\{}'.format(os.getcwd(), pic_path, pic))
            # imsrc = ac.imread('%s\\src.jpg' % os.getcwd())
            pos = ac.find_template(imsrc, imobj, r)
            if pos:
                print("识别到图像" + pic)
                return int(pos['result'][0]) + ret[0], int(pos['result'][1]) + ret[1]

        print("未识别到图像" + picname)
        return -1, -1

    def find_pic_all(self, picname, ret=(0, 0, 540, 960), r=0.7):
        """
        @description : 图像识别之模板匹配
        ---------
        @param : 需要匹配的模板名
        -------
        @Returns : 将传进来的图片和全屏截图匹配如果找到就返回图像在屏幕的坐标 否则返回None
        -------
        """
        imsrc = self.window_capture(ret[0], ret[1], ret[2], ret[3])
        imobj = ac.imread('{}\\{}\\{}'.format(os.getcwd(), pic_path, picname))
        result = ac.find_all_template(imsrc, imobj, r)
        # print("find_pic_all:{}".format(result))
        # find_pic_all:[{'result': (846.0, 466.0), 'rectangle': ((836, 457), (836, 475), (856, 457), (856, 475)), 'confidence': 0.8026019334793091},
        # {'result': (556.0, 193.0), 'rectangle': ((546, 184), (546, 202), (566, 184), (566, 202)), 'confidence': 0.7379016876220703},
        # {'result': (390.0, 151.0), 'rectangle': ((380, 142), (380, 160), (400, 142), (400, 160)), 'confidence': 0.6548370718955994}]
        return result
        # if pos:
        #     return int(pos['result'][0]) + ret[0], int(pos['result'][1]) + ret[1]

        # return -1, -1

    def find_pic_ex(self, path, ret=(0, 0, 540, 960), r=0.85):
        """
        @description : 图像识别之模板匹配
        ---------
        @param : 需要匹配的模板名
        -------
        @Returns : 将传进来的图片和全屏截图匹配如果找到就返回图像在屏幕的坐标 否则返回None
        -------
        """
        imsrc = self.window_capture(ret[0], ret[1], ret[2], ret[3])

        for file in os.listdir(path):
            imobj = ac.imread(os.path.join(path, file))
            pos = ac.find_template(imsrc, imobj, r)
            if pos:
                print("{} pos:{},{}".format(file, int(pos['result'][0]) + ret[0], int(pos['result'][1]) + ret[1]))
                return int(pos['result'][0]) + ret[0], int(pos['result'][1]) + ret[1]

        return -1, -1

    def mouse_click(self, x, y, times=0.5):
        """
        @description : 单击左键
        ---------
        @param : 位置坐标x,y 单击后延时times(s)
        -------
        @Returns :
        -------
        """
        self.__set_cursor(self.__handle, self.__WM_MOUSEACTIVATE)
        self.__move_to(self.__handle, int(x / scale), int(y / scale))
        self.__activate_mouse(self.__handle)
        self.__set_cursor(self.__handle, self.__WM_LBUTTONDOWN)
        self.__left_down(self.__handle, int(x / scale), int(y / scale))
        self.__move_to(self.__handle, int(x / scale), int(y / scale))
        self.__left_up(self.__handle, int(x / scale), int(y / scale))
        time.sleep(times)

    def 按下弹起(self, ret, times=1.5):
        self.__left_down(self.__handle, ret[0], ret[1])
        time.sleep(times)
        self.__left_up(self.__handle, ret[0], ret[1])

    def 点击(self, ret, times=0.5):
        self.mouse_click(ret[0], ret[1], times)

    def 双击(self, ret, times=0.2):
        self.mouse_click(ret[0], ret[1], times)
        self.mouse_click(ret[0], ret[1], times)

    def 点击图片(self, name, ret=(0, 0, 540, 960), times=2.5, r=0.8):
        pos = self.find_pic(name, ret, r)
        # print(pos)
        if pos[0] > 0:
            self.点击(pos, times)

    def 循环点击图片(self, name, ret=(0, 0, 540, 960), times=5.5, r=0.8):
        while True:
            pos = self.find_pic(name, ret, r)
            print(pos)
            if pos[0] > 0:
                self.点击(pos, times)
            else:
                break

    def mouse_click_image(self, name: str, region, times=0.5):
        """
        @Description : 鼠标左键点击识别到的图片位置
        ---------
        @Args : name:输入图片名; times:单击后延时
        -------
        @Returns : None
        -------
        """
        try:
            pos = self.find_pic(name, region)
            if pos[0] < 0:
                print("No results!")
            else:
                print(pos)
                self.mouse_click(pos[0], pos[1], times)
        except:
            raise Exception("error")

    def mouse_click_radius(self, x, y, times=0.5):
        """
        @description : 在范围内随机位置单击（防检测）
        ---------
        @param : 位置坐标x,y 单击后延时times(s)
        -------
        @Returns :
        -------
        """
        random_x = np.random.randint(-radius, radius)
        random_y = np.random.randint(-radius, radius)
        self.mouse_click(x + random_x, y + random_y, times)

    def mouse_scroll_up(self):
        self.__scroll_up(self.__handle, 471, 376)

    def mouse_scroll_down(self):
        self.__scroll_down(self.__handle, 471, 376)

    def push_key(self, key: str, times=1):
        """
        @Description : 按键
        ---------
        @Args : key:按键 times:按下改键后距松开的延时
        -------
        @Returns : None
        -------
        """
        self.__key_down(self.__clickhandle, key)
        time.sleep(times)
        self.__key_up(self.__clickhandle, key)
        time.sleep(times)

    def 拖动Ext(self, from_pos, to_pos):
        '''
        起始点 滑动到 目标点
        :param from_pos:  起始点
        :param to_pos:  目标点
        :return:
        '''
        print("拖动Ext=>{} to {}".format(from_pos, to_pos))
        self.__move_to(self.__handle, from_pos[0], from_pos[1])
        self.__left_down(self.__handle, from_pos[0], from_pos[1])
        time.sleep(0.5)
        self.__move_to(self.__handle, to_pos[0], to_pos[1])
        time.sleep(2)
        self.__left_up(self.__handle, to_pos[0], to_pos[1])
        time.sleep(0.5)
    def 滑动Ext(self, from_pos, to_pos, count: int = 1, step: int = 50):
        '''
        起始点 滑动到 目标点
        :param step:
        :param from_pos:  起始点
        :param to_pos:  目标点
        :param count:  滑动次数
        :return:
        '''
        # print("滑动Ext=>{} to {}".format(from_pos, to_pos))
        for j in range(count):
            self.__move_to(self.__handle, from_pos[0], from_pos[1])
            self.__left_down(self.__handle, from_pos[0], from_pos[1])
            time.sleep(0.5)
            for i in range(step):
                x_val = from_pos[0] + round((to_pos[0] - from_pos[0]) / step * i)
                if to_pos[0] < from_pos[0]:
                    x_val = from_pos[0] + round((to_pos[0] - from_pos[0]) / step * i)

                y_val = from_pos[1] + round((to_pos[1] - from_pos[1]) / step * i)
                if to_pos[1] < from_pos[1]:
                    y_val = from_pos[1] + round((from_pos[1] - to_pos[1]) / step * (step - i))

                # print("__move_to : {},{}".format(x_val, y_val))
                self.__move_to(self.__handle, x_val, y_val)
                time.sleep(0.05)
            self.__move_to(self.__handle, to_pos[0], to_pos[1])
            self.__left_up(self.__handle, to_pos[0], to_pos[1])

    def 缩小视图(self):
        for i in range(8):
            self.zoom_out(self.__handle, 500, 250)
            time.sleep(1)

    def 缩小视图f5(self):
        for i in range(5):
            self.push_key("f5", 1.5)

    def get_screenEx(self, stax: int, stay: int, endx: int, endy: int):
        hWnd = self.__handle
        width = endx - stax
        height = endy - stay
        # 创建设备描述表
        desktop_dc = win32gui.GetWindowDC(hWnd)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        # 创建一个内存设备描述表
        mem_dc = img_dc.CreateCompatibleDC()
        # 创建位图对象 screenshot = bmp
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)
        # 截图至内存设备描述表
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (stax, stay), win32con.SRCCOPY)
        signedIntsArray = screenshot.GetBitmapBits(True)
        # 内存释放
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (height, width, 4)
        im_opencv = im_opencv[..., :3]
        im_opencv = np.ascontiguousarray(im_opencv)
        return im_opencv

    def 截屏(self, ret=(0, 0, 540, 960)):
        return self.get_screenEx(ret[0], ret[1], ret[2], ret[3])

    def 截屏保存(self, ret=(0, 0, 540, 960)):
        # im = self.截屏((70, 2, 955, 35))
        im = self.截屏(ret)
        img_path = fr'./{pic_path}/capture/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).save(img_path)

    def window_capture(self, stax: int, stay: int, endx: int, endy: int):
        hwnd = self.__handle
        width = endx - stax
        height = endy - stay
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        # rctA = win32gui.GetWindowRect(hwnd)
        # w = rctA[2] - rctA[0]
        # h = rctA[3] - rctA[1]
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (stax, stay), win32con.SRCCOPY)
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        # path = './capture/{}.bmp'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"));
        # saveBitMap.SaveBitmapFile(saveDC, path)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (height, width, 4)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    def getOcr(self, stax: int, stay: int, endx: int, endy: int, flag=1):
        im = self.get_screenEx(stax, stay, endx, endy)
        # Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).save(fr'./ocr_image/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.png')
        result = PaddleOCR(use_angle_cls=True).ocr(im)
        print("{} {} 文字识别结果：{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       threading.current_thread().name, result))
        if flag == 2:
            return result
        if result:
            return result[0][1][0]
        else:
            return None

    def 文字识别(self, ret, flag=1):
        return self.getOcr(ret[0], ret[1], ret[2], ret[3], flag)

    def test_ocr(self, path):
        result = PaddleOCR(det=True, rec=True).ocr(path)
        print(result)