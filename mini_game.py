import pygame
import random
import time

def mini_game_popup(screen):
    popup_width, popup_height = 240, 160
    popup = pygame.Surface((popup_width, popup_height))
    popup_rect = popup.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    font = pygame.font.SysFont("malgun gothic", 18)
    clock = pygame.time.Clock()

    bar_x = 20
    bar_y = 100
    bar_width = popup_width - 2 * bar_x
    bar_height = 10

    center = bar_x + bar_width // 2
    success_width = 40 + random.randint(-15, 15)
    success_left = center - success_width // 2
    success_right = center + success_width // 2

    player_img = pygame.image.load("picture/star.png")
    player_img = pygame.transform.scale(player_img, (20, 20))
    player_x = bar_x
    player_y = bar_y - 15
    player_speed = 3
    accel = 0.15
    direction = 1

    start_time = time.time()
    result = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if success_left <= player_x <= success_right:
                    return 1
                return 0
            elif event.type == pygame.QUIT:
                return 0

        player_x += player_speed * direction
        player_speed += accel * direction
        if player_x <= bar_x:
            player_x = bar_x
            direction = 1
            player_speed = abs(player_speed)
        elif player_x >= bar_x + bar_width - 20:
            player_x = bar_x + bar_width - 20
            direction = -1
            player_speed = abs(player_speed)

        # 팝업 그리기
        popup.fill((240, 240, 240))
        txt = font.render("중앙을 맞추세요", True, (0, 0, 0))
        txt_rect = txt.get_rect(center=(popup_width // 2, 30))
        popup.blit(txt, txt_rect)
        pygame.draw.rect(popup, (180, 180, 180), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(popup, (100, 200, 100), (success_left, bar_y, success_width, bar_height))
        popup.blit(player_img, (int(player_x), player_y))

        # 메인 화면에 팝업 표시
        screen.blit(popup, popup_rect)
        pygame.display.flip()
        clock.tick(60)

        if time.time() - start_time > 5:
            return 0
    return 0