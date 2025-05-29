import pygame
import random
import time

def mini_game_popup(screen):
    popup_w, popup_h = 240, 160
    popup = pygame.Surface((popup_w, popup_h))
    popup_rect = popup.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    font = pygame.font.SysFont("malgun gothic", 18)
    bold_font = pygame.font.SysFont("malgun gothic", 18, bold=True)
    clock = pygame.time.Clock()

    bar_x, bar_y = 20, 100
    bar_w, bar_h = popup_w - 2 * bar_x, 20
    center = bar_x + bar_w // 2
    success_w = 40 + random.randint(-15, 15)
    success_left = center - success_w // 2
    success_right = center + success_w // 2

    player_img = pygame.transform.scale(pygame.image.load("picture/star2.png"), (20, 20)) #플레이어
    player_x = bar_x
    player_y = bar_y 
    speed = 3
    accel = 0.15
    direction = 1

    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return int(success_left <= player_x <= success_right)
            if event.type == pygame.QUIT:
                return 0

        # 별 이동
        player_x += speed * direction
        speed += accel * direction
        if player_x <= bar_x:
            player_x, direction, speed = bar_x, 1, abs(speed)
        elif player_x >= bar_x + bar_w - 20:
            player_x, direction, speed = bar_x + bar_w - 20, -1, abs(speed)

        # 화면 그리기
        popup.fill((240, 240, 240))
        txt = font.render("중앙을 맞추세요", True, (0, 0, 0))
        popup.blit(txt, txt.get_rect(center=(popup_w // 2, 30)))
        pygame.draw.rect(popup, (180, 180, 180), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(popup, (100, 200, 100), (success_left, bar_y, success_w, bar_h))
        popup.blit(player_img, (int(player_x), player_y))

        remain = max(0, 5 - int(time.time() - start_time))
        if remain > 0:
            time_txt = bold_font.render(str(remain), True, (0, 0, 0))
            popup.blit(time_txt, time_txt.get_rect(center=(popup_w // 2, popup_h // 2)))

        screen.blit(popup, popup_rect)
        pygame.display.flip()
        clock.tick(60)

        if time.time() - start_time > 5:
            return 0