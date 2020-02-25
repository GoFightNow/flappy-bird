# Created by Go_Fight_Now on 2019/12/8 15:30. #
# -*- coding:utf-8 -*-
import pygame, random, pickle, os
from pygame.locals import *
from pygame import Surface

from SemesterProject.Bird import MyBird
from SemesterProject.Pipe import Pipe


def game_listener():
    """处理事务"""
    global is_pause
    global is_ranking
    global is_new_score
    global game_status
    global bird
    for event in pygame.event.get():
        if event.type == QUIT:
            print(ranking_dict)  # 打印排行榜到控制台
            save_ranking(ranking_dict)  # 储存排行榜
            print_log("游戏退出")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                """游戏在运行，且游戏没有暂停"""
                if game_status == GAME_RUN and not is_pause:
                    bird.move_up()  # 鸟上移
            elif event.key == K_p and game_status == GAME_RUN:
                # 更改游戏是否暂停
                if is_pause:
                    print_log("取消暂停")
                    is_pause = False
                else:
                    print_log("暂停")
                    is_pause = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                if game_status == GAME_GUIDE:
                    """引导界面"""
                    temp_mouse_rect = Rect(event.pos, (1, 1))  # 以鼠标点击坐标为点，创建矩形
                    if temp_mouse_rect.colliderect(guide_play_rect) and not is_ranking:
                        """在非排行榜界面，鼠标矩形与play按钮矩形相撞"""
                        game_status = GAME_MENU  # 进入到菜单界面
                    elif temp_mouse_rect.colliderect(guide_score_rect) and not is_ranking:
                        """在非排行榜界面，鼠标矩形与score按钮相撞"""
                        is_ranking = True  # 显示排行榜
                    elif not temp_mouse_rect.colliderect(ranking_bg_rect) and is_ranking:
                        """在排行榜界面，并且鼠标矩形不与排行榜界面相撞"""
                        is_ranking = False  # 取消排行榜显示
                elif game_status == GAME_MENU:
                    """菜单界面，全屏点击开始游戏"""
                    game_status = GAME_RUN
                elif game_status == GAME_RUN and not is_pause:
                    """在游戏界面，且没有暂停"""
                    bird.move_up()  # 鸟上移
                elif game_status == GAME_OVER:
                    """游戏结束界面"""
                    temp_mouse_rect = Rect(event.pos, (1, 1))
                    if temp_mouse_rect.colliderect(over_play_rect) and not is_ranking:
                        """在非排行榜界面，鼠标矩形与play按钮矩形相撞"""
                        is_new_score = False  # 将新分数标识去除
                        game_status = GAME_MENU  # 更改游戏状态，进入menu界面
                        bird = MyBird(window_screen)  # 重新实例化鸟
                        pipe_list.clear()  # 去除所有管子，重新生成
                        print_log("重新生成鸟，管子")
                    elif temp_mouse_rect.colliderect(over_score_rect) and not is_ranking:
                        """在非排行榜界面，鼠标矩形与score按钮相撞"""
                        is_ranking = True
                    elif not temp_mouse_rect.colliderect(ranking_bg_rect) and is_ranking:
                        """在排行榜界面，并且鼠标矩形不与排行榜界面相撞"""
                        is_ranking = False
        elif event.type == BirdDown:
            """自定义监听事件，鸟自动下降"""
            if game_status == GAME_RUN and not is_pause and not bird.isBottom:
                """下降需满足条件：游戏运行界面、没有暂停、鸟没有触底"""
                bird.move_down()
        elif event.type == getPipe:
            """自定义监听事件，自动出管子"""
            if game_status == GAME_RUN and not is_pause:
                """自动出管子需满足条件：游戏运行界面、没有暂停"""
                pipe_list.append(Pipe(window_screen, random.choice(pipe_color_list)))


def print_log(msg):
    print(msg)


def game_pause():
    """暂停"""
    while is_pause:
        window_screen.blit(resume_image, resume_image_rect)
        game_listener()
        pygame.display.update()
        clock.tick(15)


def game_ranking():
    """排行榜界面"""
    if is_ranking:
        window_screen.blit(ranking_title, ranking_title_rect)
        window_screen.blit(ranking_bg, ranking_bg_rect)
        names = list(ranking_dict.keys())
        scores = list(ranking_dict.values())
        temp_dict = {}
        for i in range(10) if len(names) > 10 else range(len(names)):
            max_index = scores.index(max(scores))
            temp_dict[names[max_index]] = max(scores)
            scores.remove(max(scores))
            names.remove(names[max_index])
        del names, scores
        font_begin_y = ranking_bg_rect.top + 10
        for k, v in temp_dict.items():
            r_name: Surface = rank_font.render(str(k), True, (0, 0, 0))
            r_score: Surface = rank_font.render(str(v), True, (0, 0, 0))
            r_score_rect: Rect = r_score.get_rect()
            r_score_rect.topright = (ranking_bg_rect.right - 10, font_begin_y)
            window_screen.blit(r_name, (ranking_bg_rect.left + 10, font_begin_y))
            window_screen.blit(r_score, r_score_rect)
            font_begin_y += r_name.get_height()


def show_score():
    """显示分数"""
    # 将分数转换为图片
    score_list = [number_list[int(each_str)] for each_str in str(bird.score)]
    # 计算分数图片总宽度
    score_img_width_sum = 0
    score_item: Surface
    for score_item in score_list:
        score_img_width_sum += score_item.get_width()
    # 计算起始位置的x坐标
    score_x = (window_screen.get_width() - score_img_width_sum) // 2
    score_img: Surface
    for score_img in score_list:
        window_screen.blit(score_img, (score_x, window_screen.get_height() // 10))
        score_x += score_img.get_width()


def show_business_pipe():
    global game_status
    """加载管子，计算管子碰撞，小鸟过了管子计分，删除管子"""
    for pipe in pipe_list:
        pipe.display()
        pipe.move()
        # 计算碰撞
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            print_log("鸟碰撞到了管子")
            game_status = GAME_OVER
        # 计算分数
        if bird.rect.left > pipe.top_rect.right and bird.rect.left > pipe.bottom_rect.right:
            if pipe.isCrash:
                pipe.isCrash = False
                bird.score += 1
        # 删除多余的管子
        if pipe.top_x < -pipe.top_pipe.get_width() - 100 and len(pipe_list) >= 10:
            pipe_list.remove(pipe)


def show_end_best_score():
    # 计算本次游戏得分
    end_score_list = [score_number_list[int(each_str)] for each_str in str(bird.score)]
    end_score_width = 0
    end_score_height = end_score_list[0].get_height()
    each_score_width: Surface
    for each_score_width in end_score_list:
        end_score_width += each_score_width.get_width()
    end_score_rect = Rect(0, over_panel_rect.top + 35, end_score_width, end_score_height)
    end_score_rect.right = over_panel_rect.right - 28
    score_img_x = end_score_rect.left
    each_score: Surface
    for each_score in end_score_list:
        window_screen.blit(each_score, (score_img_x, end_score_rect.top))
        score_img_x += each_score.get_width()

    # 计算排行榜中最高分
    end_best_list = [score_number_list[int(each_str)] for each_str in str(max(ranking_dict.values()))]
    end_best_width = 0
    end_best_height = end_best_list[0].get_height()
    each_best_width: Surface
    for each_best_width in end_best_list:
        end_best_width += each_best_width.get_width()
    end_best_rect = Rect(0, over_panel_rect.top + 75, end_best_width, end_best_height)
    end_best_rect.right = over_panel_rect.right - 28
    best_img_x = end_best_rect.left
    each_best: Surface
    for each_best in end_best_list:
        window_screen.blit(each_best, (best_img_x, end_best_rect.top))
        best_img_x += each_best.get_width()


def save_ranking(ranking):
    with open('排行榜.pkl', 'wb') as pickle_file:
        # 使用pickle将变量压缩存入文件
        pickle.dump(ranking, pickle_file)


def get_ranking():
    with open('排行榜.pkl', 'rb') as pickle_file:
        return pickle.load(pickle_file)


def show_medal():
    """显示奖牌"""
    global medals_index
    if bird.score > 200:
        medals_index = 3
    elif bird.score > 150:
        medals_index = 2
    elif bird.score > 100:
        medals_index = 1
    elif bird.score > 50:
        medals_index = 0
    medals_rect: Rect = medals_list[medals_index].get_rect()
    medals_rect.center = (over_panel_rect.left + 55, over_panel_rect.top + 65)
    if bird.score > 50:
        window_screen.blit(medals_list[medals_index], medals_rect)


if __name__ == '__main__':
    # 在控制台打印出游戏说明
    print(f"\t\033[35m游戏操作说明")
    print(f"P/p 在挑战时暂停游戏")
    print(f"左键/空格 使小鸟跳跃\033[0m")
    # 输入玩家名字
    player_name = input("\033[1;4;36m ---> 请输入游戏名字(输入英文): \033[0m")
    if player_name is None or player_name == "":
        player_name = "def_player"
    print_log("您的名字是:" + player_name)
    # 游戏窗口设置
    pygame.init()
    window_screen: Surface = pygame.display.set_mode((288 * 2, 512), 0, 32)
    pygame.display.set_caption("flappy bird")
    pygame.display.set_icon(pygame.image.load("./img/bird1_1.png"))
    clock = pygame.time.Clock()
    pause_font = pygame.font.Font("./font/DejaVu Sans Mono Bold for Powerline.ttf", 18)
    name_font = pygame.font.Font("./font/BRADHITC.TTF", 18)
    rank_font = pygame.font.Font("./font/BRADHITC.TTF", 20)
    rank_font.set_bold(True)

    # 参数储存
    is_pause = False
    is_ranking = False
    is_new_score = False
    GAME_GUIDE = 0
    GAME_MENU = 1
    GAME_RUN = 2
    GAME_OVER = -1
    game_status = GAME_GUIDE
    # 创建排行榜文件或读取
    ranking_file_path = "./排行榜.pkl"
    ranking_dict = {}
    if not os.path.exists(ranking_file_path):
        ranking_dict = {'Go': 11, 'Sen': 12, 'Wang': 61, 'ZZW': 76, 'china': 9,
                        'usa': 13, 'uk': 45, 'nice': 6, 'bad': 9, 'amazing': 6, }
        save_ranking(ranking_dict)
    ranking_dict: dict = get_ranking()
    print(ranking_dict)

    medals_list = [pygame.image.load("./img/medals_0.png"), pygame.image.load("./img/medals_1.png"),
                   pygame.image.load("./img/medals_2.png"), pygame.image.load("./img/medals_3.png")]
    medals_index = 0
    pipe_list = []
    pipe_color_list = ["pipe", "pipe2"]
    number_list = [pygame.image.load("./img/font_0" + str(i) + ".png") for i in range(10)]
    score_number_list = [pygame.image.load("./img/number_score_0" + str(i) + ".png") for i in range(10)]

    # 游戏主体设置
    background: Surface = pygame.image.load("./img/bg_day.png")
    # 0.积分榜
    ranking_title: Surface = pygame.image.load("./img/button_score.png")
    ranking_title_rect: Rect = ranking_title.get_rect()
    ranking_title_rect.center = (window_screen.get_width() // 2, window_screen.get_height() // 5)

    ranking_bg: Surface = pygame.image.load("./img/ranking_background.png")
    ranking_bg_rect: Rect = ranking_bg.get_rect()
    ranking_bg_rect.center = (window_screen.get_width() // 2, window_screen.get_height() // 5 + 180)
    # 1.开始界面
    guide_title: Surface = pygame.image.load("./img/title.png")
    guide_title_rect: Rect = guide_title.get_rect()
    guide_title_rect.center = (window_screen.get_width() // 2, window_screen.get_height() // 3)

    guide_bird: Surface = pygame.image.load("./img/bird0_0.png")
    guide_bird: Surface = pygame.transform.smoothscale(guide_bird, (
        guide_bird.get_width() // 5 * 6, guide_bird.get_height() // 5 * 6))
    guide_bird_rect: Rect = guide_bird.get_rect()
    guide_bird_rect.center = (window_screen.get_width() // 2, (window_screen.get_height() // 3) + 60)

    guide_rate: Surface = pygame.image.load("./img/button_rate.png")
    guide_rate_rect: Rect = guide_rate.get_rect()
    guide_rate_rect.center = (window_screen.get_width() // 2, (window_screen.get_height() // 3) + 120)

    guide_play: Surface = pygame.image.load("./img/button_play.png")
    guide_play_rect: Rect = guide_play.get_rect()
    guide_play_rect.center = (
        window_screen.get_width() // 2 - guide_play.get_width() // 2, (window_screen.get_height() // 3) + 180)

    guide_score: Surface = pygame.image.load("./img/button_score.png")
    guide_score_rect: Rect = guide_score.get_rect()
    guide_score_rect.center = (
        window_screen.get_width() // 2 + guide_play.get_width() // 2, (window_screen.get_height() // 3) + 180)

    guide_copyright: Surface = pygame.image.load("./img/brand_copyright.png")
    guide_copyright_rect: Rect = guide_copyright.get_rect()
    guide_copyright_rect.center = (window_screen.get_width() // 2, (window_screen.get_height() // 3) + 220)
    # 2.引导界面
    menu_score: Surface = pygame.image.load("./img/font_00.png")
    menu_score_rect: Rect = menu_score.get_rect()
    menu_score_rect.center = (window_screen.get_width() // 2, window_screen.get_height() // 10)

    menu_ready: Surface = pygame.image.load("./img/text_ready.png")
    menu_ready_rect: Rect = menu_ready.get_rect()
    menu_ready_rect.center = (window_screen.get_width() // 2, window_screen.get_height() // 3)

    menu_tutorial: Surface = pygame.image.load("./img/tutorial.png")
    menu_tutorial: Surface = pygame.transform.smoothscale(menu_tutorial, (
        menu_tutorial.get_width() // 5 * 6, menu_tutorial.get_height() // 5 * 6))
    menu_tutorial_rect: Rect = menu_tutorial.get_rect()
    menu_tutorial_rect.center = (window_screen.get_width() // 2, (window_screen.get_height() // 3) + 100)
    # 3.开始游戏
    pause_image: Surface = pygame.image.load("./img/button_pause.png")
    pause_image_rect: Rect = pause_image.get_rect()
    pause_image_rect.center = (pause_image.get_width() // 2 + 20, pause_image.get_height() // 2 + 20)

    resume_image: Surface = pygame.image.load("./img/button_resume.png")
    resume_image_rect: Rect = resume_image.get_rect()
    resume_image_rect.center = (resume_image.get_width() // 2 + 20, resume_image.get_height() // 2 + 20)
    bird = MyBird(window_screen)
    # 4.游戏结束
    over_text: Surface = pygame.image.load("./img/text_game_over.png")
    over_text_rect: Rect = over_text.get_rect()
    over_text_rect.center = (window_screen.get_width() // 2, window_screen.get_height() // 3)

    over_panel: Surface = pygame.image.load("./img/score_panel.png")
    over_panel_rect: Rect = over_panel.get_rect()
    over_panel_rect.center = (window_screen.get_width() // 2, (window_screen.get_height() // 3) + 100)

    over_new: Surface = pygame.image.load("./img/new.png")
    over_new_rect: Rect = over_new.get_rect()
    over_new_rect.topright = (over_panel_rect.right - 65, over_panel_rect.top + 60)

    over_play: Surface = pygame.image.load("./img/button_play.png")
    over_play_rect: Rect = over_play.get_rect()
    over_play_rect.center = (
        window_screen.get_width() // 2 - guide_play.get_width() // 2, (window_screen.get_height() // 3) + 220)

    over_score: Surface = pygame.image.load("./img/button_score.png")
    over_score_rect: Rect = over_score.get_rect()
    over_score_rect.center = (
        window_screen.get_width() // 2 + guide_play.get_width() // 2, (window_screen.get_height() // 3) + 220)

    # 设置定时器执行任务
    BirdDown = USEREVENT + 1
    pygame.time.set_timer(BirdDown, 20)
    getPipe = USEREVENT + 2
    pygame.time.set_timer(getPipe, random.choice(range(1500, 2000 + 1, 100)))
    # 游戏开始
    while True:
        # 填充背景色
        window_screen.fill((255, 255, 255))
        # 设置背景图
        window_screen.blit(background, (0, 0))
        window_screen.blit(background, (288, 0))
        # 确定显示内容
        name: Surface = name_font.render(player_name, True, (0, 0, 0))

        if game_status == GAME_GUIDE:
            """开始界面"""
            window_screen.blit(guide_title, guide_title_rect)
            window_screen.blit(guide_bird, guide_bird_rect)
            window_screen.blit(guide_rate, guide_rate_rect)
            window_screen.blit(guide_play, guide_play_rect)
            window_screen.blit(guide_score, guide_score_rect)
            window_screen.blit(guide_copyright, guide_copyright_rect)
            game_ranking()
        elif game_status == GAME_MENU:
            """游戏开始提示"""
            window_screen.blit(menu_score, menu_score_rect)
            window_screen.blit(menu_ready, menu_ready_rect)
            bird.display()
            window_screen.blit(menu_tutorial, menu_tutorial_rect)
        elif game_status == GAME_RUN:
            """开始游戏"""
            # 操作鸟类
            bird.update()
            if bird.scope() == -1:
                game_status = GAME_OVER
            bird.display()
            # 管道滑出
            show_business_pipe()
            # 显示界面 UI
            window_screen.blit(pause_image, pause_image_rect)
            pause_text: Surface = pause_font.render("P/p", True, (255, 255, 255))
            window_screen.blit(pause_text, (pause_image_rect.right + 2, pause_image_rect.bottom + 2))
            # 显示分数
            show_score()
            # 暂停
            game_pause()
        elif game_status == GAME_OVER:
            """游戏结束"""
            bird.display()
            for pipe in pipe_list:
                pipe.display()
            window_screen.blit(over_text, over_text_rect)
            window_screen.blit(over_panel, over_panel_rect)
            if len(ranking_dict) == 0 or bird.score > max(ranking_dict.values()):
                is_new_score = True
                if len(ranking_dict) == 0:
                    ranking_dict[player_name] = bird.score
            if is_new_score:
                window_screen.blit(over_new, over_new_rect)
            if bird.score > ranking_dict.get(player_name, 0):
                ranking_dict[player_name] = bird.score
            show_end_best_score()
            show_medal()
            window_screen.blit(over_play, over_play_rect)
            window_screen.blit(over_score, over_score_rect)
            game_ranking()
        # 事件响应
        game_listener()
        # 显示名字
        window_screen.blit(name, (window_screen.get_width() - name.get_width() - 5, 5))
        pygame.display.update()
        clock.tick(20)
