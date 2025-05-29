import pygame
import json
import os
from enchant import enchant 
from mini_game import mini_game_popup
from enchant_rate import show_rate_table_popup
import subprocess
import requests

pygame.init()
screen = pygame.display.set_mode((1000, 820))
pygame.display.set_caption("장비강화")
font = pygame.font.SysFont("malgun gothic", 20, bold=True)
big_font = pygame.font.SysFont("malgun gothic", 24, bold=True)

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        bold_font = pygame.font.SysFont("malgun gothic", 20, bold=True)
        txt = bold_font.render(self.text, True, (0, 0, 0))
        txt_rect = txt.get_rect(center=self.rect.center)  
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def load_equipment():
    with open("equipment.json", encoding="utf-8") as f:
        return json.load(f)

def load_stats():
    path = "list_table.json"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            stats = json.load(f)
            # enchant_count가 없으면 0으로 추가
            if "enchant_count" not in stats:
                stats["enchant_count"] = 0
            return stats
    # 없으면 0으로 초기화
    return {
        "level": [0]*30,
        "level_try": [0]*30,
        "m_s": [0]*30,
        "success": [0]*30,
        "enchant_count": 0
    }

def save_stats(stats):
    with open("list_table.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

stats = load_stats()
enchant_count = stats.get("enchant_count", 0)

def draw_type_buttons(buttons, screen_width, screen_height):
    btn_width, btn_height = 150, 50
    btn_gap = 40
    total_width = len(buttons) * btn_width + (len(buttons) - 1) * btn_gap
    start_x = (screen_width - total_width) // 2
    y = screen_height - 120
    for i, btn in enumerate(buttons):
        btn.rect = pygame.Rect(start_x + i * (btn_width + btn_gap), y, btn_width, btn_height)
        btn.draw(screen)

def draw_stars(enchant_level, screen_width):
    max_per_row = 15
    img_size = 30
    gap = 15
    stars_width = min(enchant_level, max_per_row) * img_size + max(0, min(enchant_level, max_per_row) - 1) * gap
    start_x = (screen_width - stars_width) // 2
    y = 40
    last_star_bottom = y
    img_star = pygame.image.load("picture/star2.png")
    img_star = pygame.transform.scale(img_star, (img_size, img_size))
    for i in range(enchant_level):
        row = i // max_per_row
        col = i % max_per_row
        x = start_x + col * (img_size + gap)
        star_y = y + row * (img_size + gap)
        screen.blit(img_star, (x, star_y))
        last_star_bottom = max(last_star_bottom, star_y + img_size + gap)
    return last_star_bottom

def draw_equipment_image(equip, enchant_level, screen_width, screen_height):
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
    img = pygame.transform.scale(img, (160, 420))
    img_rect = img.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(img, img_rect)

equipment_data = load_equipment()
type_select = []
for e in equipment_data:
    if e["type"] not in type_select:
        type_select.append(e["type"])
type_buttons = [Button((0, 0, 150, 50), t) for t in type_select]

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
                if rate_btn.is_clicked(event.pos):
                    show_rate_table_popup(screen)
                elif quit_btn.is_clicked(event.pos):
                    # table.py의 reset_btn 기능을 실행 (reset_json 함수 호출)
                    # 방법1: table.py에 reset_json만 실행하는 엔드포인트를 만들어두고, 여기서 호출
                    # 방법2: reset_json만 실행하는 별도 스크립트 생성 후 여기서 실행
                    # 여기서는 방법2 예시 (reset_table.py를 만들어서 실행)
                    subprocess.run(["python", "table.py", "--reset"])
                    running = False
                elif table_btn.is_clicked(event.pos):
                    subprocess.Popen(["python", "table.py"])
                for btn in type_buttons:
                    if btn.is_clicked(event.pos):
                        selected_type = btn.text
                        enchant_level = 0
                        result_msg = ""
            else:
                if enhance_btn.is_clicked(event.pos):
                    equip = next((e for e in equipment_data if e["type"] == selected_type), None)
                    if equip:
                        mini_result = mini_game_popup(screen)
                        # 강화 시도 기록
                        stats["level_try"][enchant_level] += 1
                        prev_level = enchant_level
                        enchant_level, result_msg = enchant(equip, enchant_level, mini_result)
                        # 성공 기록
                        if result_msg == "강화 성공":
                            stats["success"][prev_level] += 1
                            # mini_game이 1이고, 강화가 '성공'일 때만 m_s 증가
                            if mini_result == 1 and (result_msg == "강화 성공" or result_msg == "성공"):
                                stats["m_s"][prev_level] += 1
                        enchant_count += 1
                        stats["enchant_count"] = enchant_count  # json에 저장
                        save_stats(stats)
                        popup_timer = pygame.time.get_ticks()
                elif back_btn.is_clicked(event.pos):
                    selected_type = None
                    enchant_level = 0
                    result_msg = ""

    if selected_type is None:   # 초기 화면
        title = big_font.render("장비강화", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen_width // 2, 100))
        screen.blit(title, title_rect)

        rate_btn_y = title_rect.bottom + 30 
        rate_btn = Button((screen_width // 2 - 75, rate_btn_y, 150, 40), "확률표")
        rate_btn.draw(screen)

        # table_btn(통계표) 버튼 추가
        table_btn = Button((screen_width // 2 + 85, rate_btn_y, 150, 40), "통계표")
        table_btn.draw(screen)

        quit_btn = Button((screen_width - 150, screen_height - 70, 100, 40), "종료")
        quit_btn.draw(screen)

        draw_type_buttons(type_buttons, screen_width, screen_height)

        img_enchant = pygame.image.load("picture/Anvil 2.png")
        img_enchant = pygame.transform.scale(img_enchant, (500, 500))
        img_rect = img_enchant.get_rect(center=(screen_width // 2, screen_height // 2 ))
        screen.blit(img_enchant, img_rect)
        
    else: # 선택 장비 강화
        last_star_bottom = draw_stars(enchant_level, screen_width)

        level_txt = font.render(f"강화 레벨: {enchant_level}", True, (0, 0, 0))
        level_rect = level_txt.get_rect(center=(screen_width // 2, last_star_bottom))
        screen.blit(level_txt, level_rect)

        equip = next((e for e in equipment_data if e["type"] == selected_type), None)
        if equip:
            draw_equipment_image(equip, enchant_level, screen_width, screen_height)

        enhance_btn = Button(((screen_width - 150) // 2, screen_height - 100, 150, 50), "강화")
        enhance_btn.draw(screen)

        back_btn = Button((30, screen_height - 70, 100, 40), "뒤로가기")
        back_btn.draw(screen)

        count_txt = font.render(f"누적 강화 횟수: {enchant_count}", True, (0, 0, 0))
        count_rect = count_txt.get_rect(bottomright=(screen_width - 30, screen_height - 30))
        screen.blit(count_txt, count_rect)

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