import pygame
import enchant

pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("장비 강화 게임")

font = pygame.font.SysFont("malgungothic", 48)
small_font = pygame.font.SysFont("malgungothic", 32)

enchant_level = 1
button_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2, 120, 50)
result_text = ""

running = True
while running:
    screen.fill((240, 240, 255))

    # 현재 장비 레벨 표시
    level_surf = font.render(f"현재 장비 레벨 : {enchant_level}", True, (30, 30, 80))
    screen.blit(level_surf, (WIDTH//2 - level_surf.get_width()//2, 100))

    # 강화 버튼
    pygame.draw.rect(screen, (100, 180, 250), button_rect)
    btn_text = small_font.render("강화", True, (255, 255, 255))
    screen.blit(btn_text, (button_rect.x + (button_rect.width-btn_text.get_width())//2, button_rect.y + 10))

    # 결과 텍스트
    if result_text:
        result_surf = small_font.render(result_text, True, (200, 50, 50))
        screen.blit(result_surf, (WIDTH//2 - result_surf.get_width()//2, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # 강화 실행
                result = enchant.enchant(enchant_level, 1)  # mini_game=1(성공)로 고정, 필요시 수정
                if result == 1:
                    enchant_level += 1
                    result_text = "강화 성공! 레벨이 올랐습니다."
                elif result == 2:
                    result_text = "강화 실패! 레벨 유지."
                else:
                    enchant_level = 0
                    result_text = "장비 파괴! 레벨 0으로 초기화."

    pygame.display.flip()

pygame.quit()
