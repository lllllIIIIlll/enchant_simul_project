import pygame
import random

def run_mini_game_popup(screen, WIDTH, HEIGHT):
    popup_width, popup_height = 120, 80
    popup = pygame.Surface((popup_width, popup_height))
    popup_rect = popup.get_rect(center=(WIDTH//2, HEIGHT//2))
    whole_bar = 1024
    success_bar = random.randint(128, 312)
    player_pos = popup_width // 2
    player_speed = 3
    running = True
    result = 2

    bar_scale = popup_width / whole_bar
    center = popup_width // 2
    success_start = int(center - (success_bar // 2) * bar_scale)
    success_end = int(center + (success_bar // 2) * bar_scale)

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 메인 루프 종료 신호만 보내고 함수는 실패로 반환
                running = False
                result = 2
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if success_start <= int(player_pos) <= success_end:
                    result = 1
                else:
                    result = 2
                running = False

        player_pos += player_speed
        if player_pos < 0:
            player_pos = 0
            player_speed *= -1
        elif player_pos > popup_width:
            player_pos = popup_width
            player_speed *= -1

        # 메인 화면 반투명 처리
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # 미니게임 팝업 그리기
        popup.fill((230, 230, 230))
        pygame.draw.rect(popup, (180, 180, 180), (0, popup_height//2 - 10, popup_width, 20))
        pygame.draw.rect(popup, (100, 220, 100), (success_start, popup_height//2 - 10, success_end - success_start, 20))
        pygame.draw.rect(popup, (220, 50, 50), (int(player_pos)-5, popup_height//2 - 20, 10, 40))
        screen.blit(popup, popup_rect.topleft)

        pygame.display.flip()
        clock.tick(60)
    return result
