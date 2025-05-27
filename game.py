import pygame
import json
from enchant import enchant 
from mini_game import mini_game

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("장비강화")
font = pygame.font.SysFont("malgun gothic", 20)

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        txt = font.render(self.text, True, (0, 0, 0))
        txt_rect = txt.get_rect(center=self.rect.center)  
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

with open("equipment.json", encoding="utf-8") as f:
    equipment_data = json.load(f)

type_select = list({e["type"] for e in equipment_data})
type_buttons = [Button((50 + i*180, 200, 150, 50), t) for i, t in enumerate(type_select)]

selected_type = None
enchant_level = 0
result_msg = ""
popup_timer = 0
enchant_count = 0  

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if selected_type is None:
                for btn in type_buttons:
                    if btn.is_clicked(event.pos):
                        selected_type = btn.text
                        enchant_level = 0
                        result_msg = ""
                    
            else:
                enhance_btn = Button((225, 300, 150, 50), "강화")
                back_btn = Button((30, 340, 100, 40), "뒤로가기")
                if enhance_btn.is_clicked(event.pos):
                    equip = next((e for e in equipment_data if e["type"] == selected_type), None)
                    if equip:
                        mini_result = mini_game()  # 미니게임 실행 (1 또는 0 반환)
                        enchant_level, result_msg = enchant(equip, enchant_level, mini_result)
                        enchant_count += 1
                        popup_timer = pygame.time.get_ticks() 
                elif back_btn.is_clicked(event.pos):
                    selected_type = None
                    enchant_level = 0
                    result_msg = ""

    if selected_type is None:
        title = font.render("장비강화", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect)
        for btn in type_buttons:
            btn.draw(screen)
    else:
        try:
            max_per_row = 15
            img_size = 30
            margin_x = 50
            margin_y = 30
            gap = 30
            for i in range(enchant_level):
                row = i // max_per_row
                col = i % max_per_row
                x = margin_x + col * gap
                y = margin_y + row * gap
                img_star = pygame.image.load("picture/sword1.jpg") # 별 이미지 삽입 필요
                img_star = pygame.transform.scale(img_star, (img_size, img_size))
                screen.blit(img_star, (x, y))
        except Exception:
            pass
        # 강화 레벨 표기
        level_txt = font.render(f"강화 레벨: {enchant_level}", True, (0, 0, 0))
        level_rect = level_txt.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(level_txt, level_rect)
        # 선택된 타입의 장비 이미지 표기
        equip = next((e for e in equipment_data if e["type"] == selected_type), None)
        if equip:
            try:
                img = pygame.image.load(equip["image1"])
                img = pygame.transform.scale(img, (100, 100))
                screen.blit(img, (250, 150))
            except Exception:
                pass
        # 강화 버튼
        enhance_btn = Button((225, 300, 150, 50), "강화")
        enhance_btn.draw(screen)
        # 뒤로가기 버튼
        back_btn = Button((30, 340, 100, 40), "뒤로가기")
        back_btn.draw(screen)
        # 누적 강화 횟수 우하단 중앙정렬
        count_txt = font.render(f"누적 강화 횟수: {enchant_count}", True, (0, 0, 0))
        text_rect = count_txt.get_rect()
        screen_width, screen_height = screen.get_size()
        count_rect = count_txt.get_rect(
            center=(screen_width - text_rect.width // 2 - 20, screen_height - text_rect.height // 2 - 20)
        )
        screen.blit(count_txt, count_rect)
        # result_msg 팝업 출력 (1초간)
        if result_msg:
            now = pygame.time.get_ticks()
            if now - popup_timer < 400:
                popup_rect = pygame.Rect(150, 250, 300, 60)
                pygame.draw.rect(screen, (220, 220, 220), popup_rect)
                pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)
                msg_txt = font.render(result_msg, True, (255, 0, 0))
                msg_rect = msg_txt.get_rect(center=popup_rect.center)
                screen.blit(msg_txt, msg_rect)
            else:
                result_msg = ""  # 1초 후 팝업 메시지 제거

    pygame.display.flip()

pygame.quit()
