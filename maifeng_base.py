#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   基础模版
@Time    :   2024年4月2日15:29:02
@Author  :   cwz
'''
import time

from helper_functions import GameAutoBase

scale = 1  # 电脑的缩放比例
radius = 5  # 随机半径
x_coor = 10  # 窗口位置
y_coor = 10  # 窗口位置
pic_path = "maifeng_pic"  # 图片路径


class GameAuto(GameAutoBase):
    def 挂机(self):
        memu = [(119, 900), (195, 900), (269, 900), (346, 900), (421, 900)]
        n = 1
        while True:
            # 417, 803  进阶   68, 902  返回  497, 575 首领
            self.点击(memu[2], 5)
            if self.find_pic("shouling_01.png")[0] > 0:
                print("挑战首领")
                self.点击((497, 575), 5)
                t = time.time()
                while True:
                    if time.time() - t > 60 * 3:
                        print("超过3分钟，自动退出")
                        self.点击(memu[2], 5)
                        break
                    p = self.find_pic("tip_02.png")
                    if p[0] > 0:
                        print("挑战胜利，挑战下一关")
                        self.点击((356, 815), 5)
                        break
                    else:
                        print("休息5秒")
                        time.sleep(5)

            self.点击图片("next_01.png", (0, 0, 540, 960), 5, 0.9)
            self.点击图片("back_01.png", (0, 0, 540, 960), 5)

            # 行李
            self.点击(memu[1], 5)
            self.点击图片("yjqh_01.png", (0, 0, 540, 960), 5)
            p = self.find_pic("cuizi_01.png", (38, 42, 493, 428), 0.9)
            if p[0] > 0:
                self.点击(p, 5.5)
                self.点击((416, 802), 5.5)  # 进阶
                self.点击((271, 744), 5.5)  # 进阶
                self.点击图片("queding_02.png", (0, 0, 540, 960), 5)  # 确定
                self.点击((271, 744), 5.5)
                self.点击图片("back_01.png", (0, 0, 540, 960), 5)

            self.点击(memu[2], 5)

            # 旅人
            self.点击(memu[3], 5)
            while True:
                p = self.find_pic("gxjn_01.png")
                if p[0] > 0:
                    self.点击(p, 5)
                    self.点击((394, 698), 5)
                    self.点击((271, 735), 5)
                    self.点击图片("back_01.png", (0, 0, 540, 960), 5)
                else:
                    break

            self.点击(memu[2], 5)
            self.点击(memu[2], 5)

            # 新手试炼
            self.点击((441, 275), 5)
            self.循环点击图片("lingqu_01.png", (0, 0, 540, 960), 3.5, 0.9)
            self.点击图片("back_01.png", (0, 0, 540, 960), 5)

            # 冒险手册
            self.点击((502, 279), 5)
            self.循环点击图片("lingqu_01.png", (0, 0, 540, 960), 3.5, 0.9)
            self.点击图片("back_01.png", (0, 0, 540, 960), 5)

            print("休息1分钟")
            time.sleep(60)
            n += 1


if __name__ == '__main__':
    game = GameAuto()
    game.挂机()
    # print(game.find_pic("shouling_01.png"))
    # game.点击((269, 900), 5.5)
    # game.点击图片("yjqh_01.png", (0, 0, 960, 540), 5)
    # game.点击图片("red_01.png", (159, 864, 233, 923), 5)
    # game.截屏保存()
