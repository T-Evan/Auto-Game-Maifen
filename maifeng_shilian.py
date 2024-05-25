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
    # 匹配超时重新匹配
    def 超时重试(self):
        p = self.find_pic("new_chaoshi_01.png")
        if p[0] > 0:
            p = self.find_pic("queding_03.png")
            if p[0] > 0:
                # 点击 ”确定“ 重新匹配
                print("重新匹配")
                self.点击(p, 3.5)
                return 1
        return 0

    def 试炼主页(self):
        while True:
            pos = self.find_pic("mjzj_01.png")
            if pos[0] > 0:
                print("当前是试炼首页")
                break
            self.点击图片("back_01.png|back_02.png", (0, 0, 540, 960), 5)
            pos = self.find_pic("shilian_01.png|new_shilian_01.png", (466, 308, 537, 475), 0.9)
            if pos[0] > 0:
                self.点击(pos, 5)
            else:
                if self.find_pic("maoxian_01.png|new_maoxian_01.png", (0, 0, 540, 960), 0.95)[0] > 0:
                    self.点击((500, 440), 3.5)
                    self.点击图片("lkdw_01.png", (0, 0, 540, 960), 5)
                    self.点击图片("queding_01.png", (0, 0, 540, 960), 5)
            # self.点击图片("shilian_01.png", (0, 0, 540, 960), 5)

    def 绝境(self, lv=1, jj=1):
        list = [(265, 220), (265, 375), (272, 530), (268, 682)]
        self.试炼主页()
        # 绝境
        self.notice_push("绝境挑战")
        self.点击(list[1], 5.5)
        # 黑海渊兽剿灭战
        # self.点击(list3[jj], 5.5)
        p = self.find_pic("jjgw_04.png")
        if p[0] > 0:
            self.点击(p, 3.5)
        self.点击图片("cjdw_01.png", (0, 0, 540, 960), 5)
        self.点击图片("cjdw_02.png", (0, 0, 540, 960), 5)
        # 点击开始匹配
        self.点击((270, 743), 2.5)

        retry_ct = 0
        juejing_flag = False
        while True:
            p = self.find_pic("new_zhunbei_01.png")
            if p[0] > 0:
                self.点击(p, 3.5)
                juejing_flag = True
                break
            retry_ct += self.超时重试()
            if retry_ct > 3:
                self.notice_push("绝境挑战匹配超时，跳过")
                break
            print("绝境挑战匹配中，等待3秒")
            time.sleep(3)
        if juejing_flag:
            st = time.time()
            time.sleep(60)
            while True:
                if time.time() - st > 10 * 60:
                    self.notice_push("绝境挑战，超过10分钟，自动退出")
                    break
                p = self.find_pic("lkdw_01.png|fangqi_01.png")
                if p[0] > 0:
                    self.点击(p, 3.5)
                    self.点击图片("queding_01.png", (0, 0, 540, 960), 5)
                    break
                self.点击图片("queding_02.png", (0, 0, 540, 960), 5)
                self.点击图片("kaiqi_01.png|kaiqi_02.png", (0, 0, 540, 960), 5)
                if self.find_pic("hdjl_01.png")[0] > 0:
                    self.点击(list[2], 5.5)
                print("绝境挑战中，等待10秒")
                time.sleep(10)

    def 恶龙(self):
        list = [(265, 220), (265, 375), (272, 530), (268, 682)]
        self.试炼主页()
        # 恶龙
        self.notice_push("恶龙大通缉")
        self.点击(list[2], 5.5)
        self.点击图片("cjdw_01.png", (0, 0, 540, 960), 5)
        self.点击图片("cjdw_02.png", (0, 0, 540, 960), 5)
        self.点击((270, 743), 2.5)

        retry_ct = 0
        elong_flag = False
        while True:
            p = self.find_pic("zhunbei_02.png|zhunbei_01.png", (258, 456, 472, 546))
            if p[0] > 0:
                self.点击(p, 5.5)
                elong_flag = True
                break
            retry_ct += self.超时重试()
            if retry_ct > 3:
                self.notice_push("恶龙挑战匹配超时，跳过")
                break
            print("恶龙挑战匹配中，等待3秒")
            time.sleep(3)
        if elong_flag:
            self.notice_push("恶龙挑战开始")
            st = time.time()
            self.notice_push("恶龙挑战中，等待2分钟")
            time.sleep(2 * 60)
            while True:
                if time.time() - st > 5 * 60:
                    self.notice_push("恶龙挑战，超过5分钟，自动退出")
                    break
                p = self.find_pic("lkdw_01.png")
                if p[0] > 0:
                    self.点击(p, 3.5)
                    self.点击图片("queding_01.png", (0, 0, 540, 960), 5)
                    break
                self.点击图片("queding_02.png", (0, 0, 540, 960), 5)
                self.点击图片("kaiqi_01.png|kaiqi_02.png", (0, 0, 540, 960), 5)
                if self.find_pic("hdjl_01.png")[0] > 0:
                    self.点击(list[2], 5.5)
                    self.notice_push("恶龙挑战完成，领取奖励")
                print("恶龙挑战中，等待10秒")
                time.sleep(10)
        # self.点击图片("back_01.png|back_02.png", (0, 0, 540, 960), 5)

    def 秘境(self):
        list = [(265, 220), (265, 375), (272, 530), (268, 682)]
        self.试炼主页()
        # self.点击((501, 384), 3.5)
        self.notice_push("秘境之间，开始执行")
        self.点击(list[0], 5.5)
        # 体力
        self.点击((516, 68), 2.5)  # 点击右上角体力补充+号
        p = self.find_pic("tlbc_01.png")  # 匹配进入体力补充页
        tili_flag = False
        if p[0] > 0:
            # 体力购买
            # 苹果兑换体力开关
            if self.tili_apple:
                self.点击((185, 667), 3.5)
            # 钻石购买体力开关
            if self.tili_buy:
                self.点击((361, 671), 3.5)  # 钻石购买体力

            # 识别当前体力是否满足20
            txt = self.文字识别((246, 356, 289, 375))
            if txt and "/60" in txt:
                num = int(txt.replace("/60", ""))
                if num > 20:
                    tzcs = int(num / 20)
                    tili_flag = True
            self.点击图片("back_01.png", (0, 0, 540, 960), 5)  # 返回秘境地图选择页
        if tili_flag:  # 体力满足20，执行匹配
            # self.点击图片("men_01.png", (0, 0, 540, 960), 5)
            # self.点击(list2[lv - 1], 3.5)
            # if lv == 1:
            #     self.点击图片("yuanye_01.png", (0, 0, 540, 960), 5)
            # if lv == 2:
            #     self.点击图片("senlin_01.png", (0, 0, 540, 960), 5)
            # if lv == 3:
            #     self.点击图片("shamo_01.png", (0, 0, 540, 960), 5)

            self.点击图片("cjdw_01.png", (0, 0, 540, 960), 5)
            self.点击图片("cjdw_02.png", (0, 0, 540, 960), 5)
            # self.点击图片("queding_01.png", (0, 0, 540, 960), 5)
            self.点击((270, 743), 2.5)  # 开始匹配
            msg = "秘境挑战开始匹配，体力剩余" + str(num)
            self.notice_push(msg)

            # 等待匹配中
            retry_ct = 0
            mijing_flag = False
            while True:
                # p = self.find_pic("start_01.png")
                p = self.find_pic("new_zhunbei_01.png")
                if p[0] > 0:
                    self.点击(p, 3.5)
                    # 检查是否有队友未确认，进入重新匹配状态
                    time.sleep(10)
                    print("秘境挑战匹配确认，等待10秒")
                    p = self.find_pic("new_pipeiwait_01.png")
                    if p[0] > 0:
                        print("秘境挑战匹配中，等待")
                        continue
                    # 确认已进入挑战
                    mijing_flag = True
                    break
                # 匹配超时重新匹配
                retry_ct += self.超时重试()
                if retry_ct > 3:
                    self.notice_push("秘境挑战匹配超时，跳过")
                    break
                print("秘境挑战匹配中，等待3秒")
                time.sleep(3)
            if mijing_flag:
                # 进入挑战，重新计时
                self.notice_push("秘境挑战开始")
                st = time.time()
                while True:
                    print("秘境挑战中，等待3秒")
                    if time.time() - st > 10 * 60:
                        print("秘境挑战，超过10分钟，自动退出")
                        break
                    p = self.find_pic("kaiqi_02.png|kaiqi_01.png|new_fangqi_01.png")
                    if p[0] > 0:
                        self.notice_push("秘境挑战结束，开宝箱/放弃")
                        self.点击(p, 3.5)
                        break
                    time.sleep(3)
                self.notice_push("秘境挑战结束，退出")
                self.点击图片("back_01.png", (0, 0, 540, 960), 5)
                self.点击图片("back_02.png", (0, 0, 540, 960), 5)
        else:
            self.点击图片("back_02.png", (0, 0, 540, 960), 5)

    def 梦魇(self):
        list = [(265, 220), (265, 375), (272, 530), (268, 682)]
        self.试炼主页()
        # 梦魇
        self.notice_push("梦魇狂潮，开始执行")
        self.点击(list[2], 5.5)
        self.点击图片("cjdw_01.png", (0, 0, 540, 960), 5)
        self.点击图片("cjdw_02.png", (0, 0, 540, 960), 5)
        self.点击((270, 743), 2.5)

        retry_ct = 0
        mengyan_flag = False
        while True:
            p = self.find_pic("zhunbei_02.png|zhunbei_01.png")
            if p[0] > 0:
                self.点击(p, 3.5)
                mengyan_flag = True
                break
            # 匹配超时重新匹配
            retry_ct += self.超时重试()
            if retry_ct > 3:
                self.notice_push("梦魇挑战匹配超时，跳过")
                break
            print("等待3秒")
            time.sleep(3)
        if mengyan_flag:
            self.notice_push("梦魇挑战开始")
            time.sleep(2 * 60)
            st = time.time()
            while True:
                if time.time() - st > 5 * 60:
                    self.notice_push("梦魇狂潮，挑战超过5分钟，自动退出")
                    break
                p = self.find_pic("lkdw_01.png")
                if p[0] > 0:
                    self.点击(p, 3.5)
                    self.点击图片("queding_01.png", (0, 0, 540, 960), 5)
                    break
                self.点击图片("queding_02.png", (0, 0, 540, 960), 5)
                self.点击图片("kaiqi_01.png", (0, 0, 540, 960), 5)
                if self.find_pic("hdjl_01.png")[0] > 0:
                    self.点击(list[2], 5.5)
                    self.notice_push("梦魇挑战结束，领取奖励")
                print("梦魇狂潮挑战中，等待10秒")
                time.sleep(10)
            self.点击图片("back_01.png|back_02.png", (0, 0, 540, 960), 5)

    def 试炼(self, lv=1, jj=1):
        list = [(265, 220), (265, 375), (272, 530), (268, 682)]
        list2 = [(105, 202), (105, 276), (105, 347), (105, 424)]  # 秘境
        list3 = [(334, 470), (167, 379), (131, 560), (449, 687)]  # 绝境
        flag = False
        tzcs = 0

        self.notice_push("试炼开始")
        # self.秘境()
        self.绝境()
        # self.恶龙()
        # self.梦魇()

    def notice_push(self, msg=""):
        print(msg)
        server_push_link = "http://sctapi.ftqq.com/" + self.server_push_token + ".send?title=麦芬！" + msg
        r = self.s.get(server_push_link)


if __name__ == '__main__':
    game = GameAuto()
    while True:
        game.试炼()
        print("休息2分钟")
        time.sleep(2 * 60)
        # game.截屏保存()
