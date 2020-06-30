"""
版本信息：
.1 测试完成蛇的运动，碰撞检测以及食物的定位
。2 主功能进入类中，完成类的定义以及功能优化
。3 添加分数，速度，以及其他相关文字信息的显示，缩小实际蛇运动轨迹范围，添加直线作为墙壁
。4 添加开始界面，显示游戏名称，版本号以及作者信息，代码上部添加版本更迭信息
.45 加入童心派的模块，可以利用童心派来控制
"""

import sys
import pygame
from pygame.locals import *
import random
import cyberpi  #童心派模块

font_path = 'C:/windows/Fonts/msyh.ttc'
color_White = (255, 255, 255)
color_Black = (0, 0, 0)
color_Green = (0, 255, 0)

direction = ['RIGHT', 'LEFT', 'UP', 'DOWN']

rect_size_turple = rect_width, rect_height = 10, 10

winSize = width, height = 800, 600


class GameSnake:
    def __init__(self, winwidth, winheight, rect_num):
        pygame.init()  # pygame init
        self.gameversion = '.4'
        self.winSize = [winwidth, winheight]  # 窗口的宽和高，形成列表
        self.startclock = 5  # 开始的刷新频率
        self.clock = pygame.time.Clock()  # 初始化pygame的时钟
        self.screen = pygame.display.set_mode(self.winSize)  # 设施游戏窗口大小，并赋值给screen变量
        self.score = 0  # 初始化分数
        self.speed_rate = 0.2  # 难度改变系数
        pygame.display.set_caption('snake_v0' + self.gameversion)  # 设置标题
        self.snake_moving_direction = random.choice(direction[1:])  # 设置开局方向随机
        self.snakepos = [(int(winSize[0] / 2), int(winSize[1] / 2))]  # 定义蛇的坐标列表，初始在在屏幕中央
        for x in range(rect_num - 1):
            self.snakepos.append((int(winSize[0] / 2 + 10 * (x + 1)), int(winSize[1] / 2)))  # 根据方块数量添加蛇的身体位置坐标
        self.foodpos = self.foodx, self.foody = self._setFoodxy()  # 初始化食物坐标
        # print(self.foodpos)
        # print(self.rectpos)
        self._gameStart()  # 显示开始界面，部分游戏信息
        self._gameloop()  # 游戏主循环函数开始

    def _gameStart(self):  # 开始界面
        text = pygame.font.Font(font_path, 15)
        # 要显示的开始界面的信息，放在列表中，方便遍历以及定位
        gamestart_text = ['贪吃蛇', 'Version 0' + self.gameversion, '制作人：[86]沪-陈奕玮', '按任意键开始']
        while True:
            for gt in gamestart_text:
                g_text = text.render(gt, 1, color_White)
                self.screen.blit(g_text, (int(winSize[0] / 4), int(winSize[0] / 4) + gamestart_text.index(gt) * 40))
            for pos in self.snakepos:  # 重画下一个状态的蛇的位置
                pygame.draw.rect(self.screen, color_Green, pos + rect_size_turple, 1)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

            if cyberpi.controller.is_press("any"):
                return

    def _setGameinfo(self):  # 显示基本信息，顺便填充左右两个空白，以免不要太难看
        # 为了能仍多个字符在一起，又可以进行遍历，于是变成列表形式，用字符串遍历的话会把某些字符进行拆分
        first_left_text = ['制', '作', '人', '：', '86', '沪', '|', '陈', '奕', '玮', '#', '#', '#']
        second_left_text = ['游', '戏', '版', '本', '：']
        first_right_text = ['控', '制', '：', '方', '向', '键', '#', '#', '#']
        second_right_text = ['速', '度', '随', '分', '数', '增', '加']
        # left_text = [first_left_text, second_left_text]
        # right_text = [first_right_text, second_right_text]
        second_left_text.append(self.gameversion)  # 把游戏版本设置成初始化信息中的常量，方便更改
        left_text = first_left_text + second_left_text
        right_text = first_right_text + second_right_text
        text = pygame.font.Font(font_path, 15)
        # for lt in left_text:
        #     for x in lt:
        #         l_text = text.render(x, 1, color_Green)
        #         self.screen.blit(l_text, (left_text.index(lt)*10, lt.index(x)*10))
        #
        # for rt in right_text:
        #     for x in rt:
        #         r_text = text.render(x, 1, color_Green)
        #         self.screen.blit(r_text, (winSize[0]-20+right_text.index(rt)*10, rt.index(x)*10))
        for lt in left_text:  # 遍历列表，方便输出成竖排文字的形式
            if lt == '|' or lt == ':':  # 遇到标点符号，尽量居中，显得好看点
                l_text = text.render(lt, 1, color_Green)
                self.screen.blit(l_text, (10, left_text.index(lt) * 15))  # 利用index来控制每个元素的y轴位置
            else:
                l_text = text.render(lt, 1, color_Green)
                self.screen.blit(l_text, (2, left_text.index(lt) * 15))

        for rt in right_text:
            r_text = text.render(rt, 1, color_Green)
            self.screen.blit(r_text, (winSize[0] - 18, right_text.index(rt) * 15))
        # 把不经常刷新的信息放在一起，提升代码的可读性
        pygame.draw.aaline(self.screen, color_Green, (20, 0), (20, self.winSize[1] - 20))  # 显示左边绿色边框
        pygame.draw.aaline(self.screen, color_Green, (self.winSize[0] - 20, 0),
                           (self.winSize[0] - 20, self.winSize[1] - 20))  # 显示右边绿色边框
        pygame.draw.aaline(self.screen, color_Green, (0, self.winSize[1] - 20),
                           (self.winSize[0], self.winSize[1] - 20))  # 显示下方边框

        # score_text = text.render(str(self.score), 1, color_Green)
        # speed_text = text.render('速度：{:.2f}'.format(self.startclock), 1, color_Green)
        # self.screen.blit(score_text, (int(winSize[0] - 20), int(winSize[1] - 20)))
        # self.screen.blit(speed_text, (0, int(winSize[1] - 20)))  # 实例化字体对象并显示部分文本 第一种分开显示，在左右两边

        info_text = text.render('速度：{:.2f} 分数：{}'.format(self.startclock, self.score), 1, color_Green)
        self.screen.blit(info_text, (0, int(winSize[1] - 20)))  # 实例化字体对象并显示部分文本 第二种统一在左边

    def _setFoodxy(self):  # 设置食物坐标的方法
        foodx = random.randint(20, self.winSize[0] - 30)
        if foodx % 10 != 0:  # 强制食物的坐标为10的整数倍，保证食物坐标能与蛇头坐标能够重合
            foodx -= foodx % 10
        foody = random.randint(0, self.winSize[1] - 30)
        if foody % 10 != 0:
            foody -= foody % 10
        return foodx, foody

    def _isEatFood(self):  # 判断是否吃到食物
        if self.snakepos[0][0] == self.foodx and self.snakepos[0][1] == self.foody:  # 判断蛇头位置是否与食物的位置重合
            return True
        return False

    def _isKillSelf(self):  # 判断是否碰到自身的身体
        for pos in self.snakepos:  # 遍历蛇的所有身体
            if pos is not self.snakepos[0]:  # 如果身体不是舌头的话
                # if pos[0] == self.snakepos[0][0] and pos[1] == self.snakepos[0][1]:  # 如果身体的某一部分的坐标跟舌头的坐标一致
                if pos == self.snakepos[0]:
                    return True
        return False

    def _isHiltWall(self):  # 判断是否撞墙
        #  判断是否撞墙的唯一标准就是x或者y坐标的其中一个是否超出了边界，及最大边框位置
        if self.snakepos[0][0] < 20 or self.snakepos[0][0] >= self.winSize[0] - 20 or \
                self.snakepos[0][1] < 0 or self.snakepos[0][1] >= self.winSize[1] - 20:
            return True
        return False

    def _input(self):  # 接受键盘输入，上下左右及退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if self.snake_moving_direction != 'RIGHT':
                        self.snake_moving_direction = direction[1]
                if event.key == K_RIGHT:
                    if self.snake_moving_direction != 'LEFT':
                        self.snake_moving_direction = direction[0]
                if event.key == K_UP:
                    if self.snake_moving_direction != 'DOWN':
                        self.snake_moving_direction = direction[2]
                if event.key == K_DOWN:
                    if self.snake_moving_direction != 'UP':
                        self.snake_moving_direction = direction[3]

        # 童心派控制
        if cyberpi.controller.is_press("up"):
            if self.snake_moving_direction != 'DOWN':
                self.snake_moving_direction = direction[2]
        if cyberpi.controller.is_press("down"):
            if self.snake_moving_direction != 'UP':
                self.snake_moving_direction = direction[3]
        if cyberpi.controller.is_press("left"):
            if self.snake_moving_direction != 'RIGHT':
                self.snake_moving_direction = direction[1]
        if cyberpi.controller.is_press("right"):
            if self.snake_moving_direction != 'LEFT':
                self.snake_moving_direction = direction[0]

    def _snake_moving(self):  # 蛇的移动，核心思想是蛇列表insert下一个坐标位置，然后pop出队尾坐标
        if self.snake_moving_direction == 'UP':
            self.snakepos.insert(0, (self.snakepos[0][0], self.snakepos[0][1] - 10))
        elif self.snake_moving_direction == 'DOWN':
            self.snakepos.insert(0, (self.snakepos[0][0], self.snakepos[0][1] + 10))
        elif self.snake_moving_direction == 'RIGHT':
            self.snakepos.insert(0, (self.snakepos[0][0] + 10, self.snakepos[0][1]))
        elif self.snake_moving_direction == 'LEFT':
            self.snakepos.insert(0, (self.snakepos[0][0] - 10, self.snakepos[0][1]))
        self.snakepos.pop()

    def _updating(self):  # 主刷新程序，每次刷新需更新蛇的状态
        self.screen.fill(color_Black)

        if self._isKillSelf() or self._isHiltWall():  # 每次刷新必须判断是否是死亡状态
            self._gameOver()
        elif self._isEatFood():  # 然后判断是否下一个位置是食物状态
            self.snakepos.insert(0, self.foodpos)  # 如果是就把食物位置添加到蛇头位置，蛇尾不变
            self.foodpos = self.foodx, self.foody = self._setFoodxy()  # 然后更新食物位置
            self.score += 1
            self.startclock += self.speed_rate  # 改变刷新帧率，间接改变了游戏速度
        for pos in self.snakepos:  # 重画下一个状态的蛇的位置
            pygame.draw.rect(self.screen, color_Green, pos + rect_size_turple, 1)
        pygame.draw.rect(self.screen, color_Green, self.foodpos + rect_size_turple, 1)  # 重画下一个食物的位置
        self._snake_moving()  # 蛇再次移动一次

        self._setGameinfo()
        pygame.display.flip()  # 将内存中的下一帧显示在界面上

    def _gameOver(self):
        # cyberpi.display.show_label('Game Over', size, 'center')
        while True:  # 游戏一旦结束便重画整个画面，只显示游戏结束四个大字
            self.screen.fill(color_Black)
            text = pygame.font.Font(font_path, 50)  # 设置字体对象
            gomeover_text = text.render('游戏结束', 1, color_White)  # 设置文字内容
            self.screen.blit(gomeover_text, (int(winSize[0] / 2) - 120, int(winSize[1] / 2)))  # 固定位置
            pygame.display.flip()  # 显示内存中的下一帧
            for event in pygame.event.get():  # 等待结束推出的指令
                if event.type == pygame.QUIT:
                    sys.exit()

    def _gameloop(self):  # 游戏主循环
        while True:
            self._input()
            self._updating()
            self.clock.tick(self.startclock)


if __name__ == '__main__':
    try:
        snake = GameSnake(winSize[0], winSize[1], 3)  # 实例化对象
    except Exception as e:
        print(e)