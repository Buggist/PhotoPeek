"""
加载图片途径（3种）：
    
    1 - 作为启动参数
    
    2 - 拖动进来
    
    3 - 方向键切换图片

操作：
    1 - 拖入更新图片
    
    2 - 左右键切换图片
    
    3 - A/D 键旋转图片
    
    4 - 滚轮缩放图片
    
    5 - 按住拖动图片

"""


import os, sys

import pygame

#----主配置--
window_size = (1280, 720)
caption     = '照片看看器'
icon_file   = r'data\Framed Picture.png'
# 设置窗口的背景颜色
background_color = (240, 240, 245)  # 偏蓝一点更符合视觉习惯，纯灰色看起来偏黄


#--

def main():
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = None
        
    global caption
    
    # 拖动中
    dragging = False
    
    file_path = ""
    
    # 创建窗口，设置窗口的大小和标题
    screen = pygame.display.set_mode(size=window_size, flags=pygame.RESIZABLE)
    pygame.display.set_caption(caption)
    screen.fill(background_color)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path_abs = script_dir + "\\" + icon_file
    # 设置 Logo
    icon = pygame.image.load(icon_path_abs)
    pygame.display.set_icon(icon)

    # 创建游标
    cursor_sys = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
    cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

    thickarrow_strings = (               #sized 16x16
      "    XXXXX       ",
      "   X..X..XXX    ",
      "   X..X..X..X   ",
      "   X..X..X..XXX ",
      "   X........X..X",
      "   X...........X",
      " XXX...........X",
      "X.XX...........X",
      "X..X...........X",
      "X..............X",
      " X.............X",
      " X.............X",
      "  X............X",
      "  X...........X ",
      "   X.........X  ",
      "    XXXXXXXXXX  ")

    a, b = pygame.cursors.compile(thickarrow_strings, black='X', white='.', xor='o')
    cursor_grab = pygame.cursors.Cursor([16, 16], [0, 0], a, b)
    
    # 当前图片
    if arg:
        # 图片加载
        scale_level = [1]   # 缩放级别
        
        file_path = arg
        
        image = pygame.image.load(file_path)
                
        image_show = scale_image_tofit_screen(screen, image)
        
        render_pos = get_renderpos(screen, image_show)
        
        screen.fill(background_color)
        screen.blit(image_show, render_pos)
        
        image_files = get_images_in_dir(file_path)
        
        caption_new = update_caption(caption, file_path)
        pygame.display.set_caption(caption_new)
    else:
        image = None

    # 主循环
    running = True
    while running:
        # 处理事件
        # queue = pygame.event.get()
        queue = [pygame.event.wait()]
        for event in queue:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEWHEEL:
                print("y:", event.y)
                if not image:
                    continue
                    
                image_show = scale_image(image, event.y, scale_level, screen)
                
                render_pos = get_renderpos(screen, image_show)

                # render_area = get_renderarea(screen, image_show, render_pos)

                # print("Area:", render_area)
                
                screen.fill(background_color)
                screen.blit(image_show, render_pos)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("左键按下")
                    dragging = True

                    # 变更游标
                    pygame.mouse.set_cursor(cursor_grab)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print("左键按下")
                    dragging = False

                    # 变更游标
                    pygame.mouse.set_cursor(cursor_sys)
                
            elif event.type == pygame.MOUSEMOTION:
                if dragging and image:
                    rel = event.rel
                    render_pos = (render_pos[0] + rel[0], render_pos[1] + rel[1])
                    
                    screen.fill(background_color)
                    screen.blit(image_show, render_pos)
                
            elif event.type == pygame.KEYDOWN:
                # 退出
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                elif event.key == pygame.K_RIGHT:
                    
                    index = image_files.index(file_path)
                    if index == len(image_files) - 1:
                         continue
                    else:
                        # 图片加载
                        scale_level = [1]   # 缩放级别
                        
                        file_path = image_files[index+1]
                        
                        image = pygame.image.load(file_path)
                        
                        image_show = scale_image_tofit_screen(screen, image)

                        render_pos = get_renderpos(screen, image_show)
                        
                        screen.fill(background_color)
                        screen.blit(image_show, render_pos)
                        
                        caption_new = update_caption(caption, file_path)
                        pygame.display.set_caption(caption_new)
                        
                        # image_files = get_images_in_dir(file_path)    # 此处不需要这一行
                        
                elif event.key == pygame.K_LEFT:
                    
                    index = image_files.index(file_path)
                    if index == 0:
                         continue
                    else:
                        # 图片加载
                        scale_level = [1]   # 缩放级别
                        
                        file_path = image_files[index-1]
                        
                        image = pygame.image.load(file_path)
                        
                        image_show = scale_image_tofit_screen(screen, image)

                        render_pos = get_renderpos(screen, image_show)
                        
                        screen.fill(background_color)
                        screen.blit(image_show, render_pos)
                        
                        caption_new = update_caption(caption, file_path)
                        pygame.display.set_caption(caption_new)
                        
                        # image_files = get_images_in_dir(file_path)    # 此处不需要这一行
                        
                elif event.key == pygame.K_a:
                    print("按下A")
                    
                    if image:
                        
                        image = rotate_image(image, -90)

                        image_show = scale_image_tofit_screen(screen, image)
                        render_pos = get_renderpos(screen, image_show)
                        
                        screen.fill(background_color)
                        screen.blit(image_show, render_pos)
                        
                elif event.key == pygame.K_d:
                    print("按下D")
                    
                    if image:

                        image = rotate_image(image, 90)

                        image_show = scale_image_tofit_screen(screen, image)
                        render_pos = get_renderpos(screen, image_show)
                        
                        screen.fill(background_color)
                        screen.blit(image_show, render_pos)
                    
            elif event.type == pygame.DROPFILE:
                print("开始拖拽！！")
                
                scale_level = [1]             # 重置缩放级别
                
                file_path = event.file
                
                # 图片加载
                scale_level = [1]   # 缩放级别
                
                image = pygame.image.load(file_path)
                
                print(image.get_size())
                
                image_show = scale_image_tofit_screen(screen, image)
                
                render_pos = get_renderpos(screen, image_show)
                
                screen.fill(background_color)
                screen.blit(image_show, render_pos)
                
                image_files = get_images_in_dir(file_path)
                
                caption_new = update_caption(caption, file_path)
                pygame.display.set_caption(caption_new)

            elif event.type == pygame.VIDEORESIZE:

                # 窗口尺寸变化时重新调整图片尺寸，重绘窗口
                image_show = scale_image_tofit_screen(screen, image)
                render_pos = get_renderpos(screen, image_show)
                
                screen.fill(background_color)
                screen.blit(image_show, render_pos)
                
                

        # 填充背景色
        

        # 更新屏幕显示
        pygame.display.flip()

    # 退出pygame
    pygame.quit()
    


def scale_image_tofit_screen(screen, image):
    image_rect = image.get_rect()
    screen_rect = screen.get_rect()

    if image_rect.height > screen_rect.height or (
        image_rect.width > screen_rect.width
    ):
        # 计算缩放比例
        scale_height = screen_rect.height / image_rect.height
        scale_width = screen_rect.width / image_rect.width
        scale = min(scale_height, scale_width)  # 确保图片不会超出窗口宽度

        # 等比缩放图片
        scaled_image = pygame.transform.scale(image, (int(image_rect.width * scale), int(image_rect.height * scale)))

    else:
        scaled_image = image
    
    return scaled_image
    
    
def get_renderpos(screen, image):
    screen_rect = screen.get_rect()
    image_rect = image.get_rect()
    
    x = (screen_rect.width - image_rect.width) / 2
    y = (screen_rect.height - image_rect.height) / 2
    
    return (x, y)


# def get_renderarea(screen, image, render_pos):
    # screen_rect = screen.get_rect()
    # image_rect = image.get_rect()

    # if image_rect.width > screen_rect.width:
        # x_start = -render_pos[0]
        # x_end = x_start + screen_rect.width
    # else:
        # x_start = 0
        # x_end = image_rect.width
        
    # if image_rect.height > screen_rect.height:
        # y_start = -render_pos[1]
        # y_end = y_start + screen_rect.height
    # else:
        # y_start = 0
        # y_end = image_rect.height

    # print((x_start, x_end, y_start, y_end))

    # area = pygame.Rect(x_start, y_start, x_end, y_end)

    # return area
    
    
def scale_image(image, step, scale_level, screen):
    image_rect = image.get_rect()

    # 这里的【scale_level[0] <= 1.1】是为了避免缩放出 0.9xx 之类的预期之外的倍数。
    if step < 0 and scale_level[0] <= 1.1 and (
        scale_level[0] * image_rect.width <= screen.get_size()[0] ) and (
        scale_level[0] * image_rect.height <= screen.get_size()[1]
    ):
        if scale_level[0] <= 9:
            scale_level[0] = scale_level[0]
        else:
            scale_level[0] = 1
    # 这里的【scale_level[0] >= 18】是为了避免缩放出 20.xx 之类的预期之外的倍数。
    elif step > 0 and scale_level[0] >= 18:
        scale_level[0] = 20
    else:
        scale_level[0] = (step * 0.1 + 1) * scale_level[0]

    print("倍数:", scale_level[0])

    scaled_image = pygame.transform.scale(image, (int(image_rect.width * scale_level[0]), int(image_rect.height * scale_level[0])))
        
    return scaled_image
    
    
def get_images_in_dir(file_path):
    # 获取PNG文件所在的目录
    directory = os.path.dirname(file_path)
    
    # 定义图片格式列表
    image_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.lbm', '.pcx', '.pnm', '.tga', '.TIFF', '.webp']
    
    # 获取目录中所有文件的列表
    all_files = os.listdir(directory)
    
    # 过滤出图片格式的文件
    image_files = [os.path.join(directory, file) for file in all_files if os.path.splitext(file)[1].lower() in image_formats]
    
    image_files = sorted(image_files)
    
    return image_files
    

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)
    
    
def update_caption(caption, file_path):
    file_name = os.path.basename(file_path)
    new_caption = file_name + ' - ' + caption
    
    return new_caption


if __name__ == "__main__":
    pygame.display.init()
    main()









    
