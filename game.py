import pygame
import json
from enchant import enchant 
from mini_game import mini_game_popup

pygame.init()
screen = pygame.display.set_mode((800, 640))
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

type_select = []
for e in equipment_data:
    if e["type"] not in type_select:
        type_select.append(e["type"])
        
type_buttons = [Button((50 + i*180, 200, 150, 50), t) for i, t in enumerate(type_select)]

selected_type = None
enchant_level = 0
result_msg = ""
popup_timer = 0
enchant_count = 0  

running = True
while running:
    screen.fill((255, 255, 255))
    screen_width, screen_height = screen.get_size()

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
                # 강화 버튼: 중 하단
                enhance_btn = Button(
                    ((screen_width - 150) // 2, screen_height - 100, 150, 50), "강화"
                )
                # 뒤로가기 버튼: 좌 하단
                back_btn = Button(
                    (30, screen_height - 70, 100, 40), "뒤로가기"
                )
                if enhance_btn.is_clicked(event.pos):
                    equip = next((e for e in equipment_data if e["type"] == selected_type), None)
                    if equip:
                        mini_result = mini_game_popup(screen)
                        enchant_level, result_msg = enchant(equip, enchant_level, mini_result)
                        enchant_count += 1
                        popup_timer = pygame.time.get_ticks()
                elif back_btn.is_clicked(event.pos):
                    selected_type = None
                    enchant_level = 0
                    result_msg = ""

    if selected_type is None:
        title = font.render("장비강화", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen_width // 2, 100))
        screen.blit(title, title_rect)
        # type 버튼: 중 하단 정렬
        btn_width, btn_height = 150, 50
        btn_gap = 40
        total_width = len(type_buttons) * btn_width + (len(type_buttons) - 1) * btn_gap
        start_x = (screen_width - total_width) // 2
        y = screen_height - 120
        for i, btn in enumerate(type_buttons):
            btn.rect = pygame.Rect(start_x + i * (btn_width + btn_gap), y, btn_width, btn_height)
            btn.draw(screen)

        img_enchant = pygame.image.load("picture/star.png")
        img_enchant = pygame.transform.scale(img_enchant, (200, 200))
        img_rect = img_enchant.get_rect(center=(screen_width // 2, screen_height // 2 ))
        screen.blit(img_enchant, img_rect)
        
    else:
        # img_star: 중 상단 정렬
        try:
            max_per_row = 15
            img_size = 30
            gap = 15
            stars_width = min(enchant_level, max_per_row) * img_size + max(0, min(enchant_level, max_per_row) - 1) * gap
            start_x = (screen_width - stars_width) // 2
            y = 40  # 상단 여백
            last_star_bottom = y
            for i in range(enchant_level):
                row = i // max_per_row
                col = i % max_per_row
                x = start_x + col * (img_size + gap)
                star_y = y + row * (img_size + gap)
                img_star = pygame.image.load("picture/star.png")
                img_star = pygame.transform.scale(img_star, (img_size, img_size))
                screen.blit(img_star, (x, star_y))
                last_star_bottom = max(last_star_bottom, star_y + img_size + gap)
        except Exception:
            last_star_bottom = 70

        # 강화 레벨: img_star 바로 아래 중앙
        level_txt = font.render(f"강화 레벨: {enchant_level}", True, (0, 0, 0))
        level_rect = level_txt.get_rect(center=(screen_width // 2, last_star_bottom + 0))
        screen.blit(level_txt, level_rect)

        # 장비 이미지: 화면 정 중앙에 배치
        equip = next((e for e in equipment_data if e["type"] == selected_type), None)
        if equip:
            try:
                if 0 <= enchant_level < 15:
                    img_key = "image1"
                elif 15 <= enchant_level < 20:
                    img_key = "image2"
                elif 20 <= enchant_level < 26:
                    img_key = "image3"
                elif 26 <= enchant_level <= 30:
                    img_key = "image4"
                else:
                    img_key = "image1"
                img = pygame.image.load(equip.get(img_key, equip["image1"]))
                img = pygame.transform.scale(img, (120, 420))
                img_rect = img.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(img, img_rect)
            except Exception:
                pass

        # 강화 버튼: 중 하단
        enhance_btn = Button(
            ((screen_width - 150) // 2, screen_height - 100, 150, 50), "강화"
        )
        enhance_btn.draw(screen)

        # 뒤로가기 버튼: 좌 하단
        back_btn = Button(
            (30, screen_height - 70, 100, 40), "뒤로가기"
        )
        back_btn.draw(screen)

        # 누적 강화 횟수: 우 하단
        count_txt = font.render(f"누적 강화 횟수: {enchant_count}", True, (0, 0, 0))
        count_rect = count_txt.get_rect(bottomright=(screen_width - 30, screen_height - 30))
        screen.blit(count_txt, count_rect)

        # result_msg 팝업: 중 중단 정렬(팝업)
        if result_msg:
            now = pygame.time.get_ticks()
            if now - popup_timer < 1000:
                popup_rect = pygame.Rect(0, 0, 300, 60)
                popup_rect.center = (screen_width // 2, screen_height // 2)
                pygame.draw.rect(screen, (220, 220, 220), popup_rect)
                pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)
                msg_txt = font.render(result_msg, True, (255, 0, 0))
                msg_rect = msg_txt.get_rect(center=popup_rect.center)
                screen.blit(msg_txt, msg_rect)
            else:
                result_msg = ""

    pygame.display.flip()

pygame.quit()
