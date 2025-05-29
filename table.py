import pygame
import json
import subprocess

# list.py를 먼저 실행해서 최신 통계 갱신
subprocess.run(["python", "list.py"])

# 데이터 불러오기
with open("list_rate.json", encoding="utf-8") as f:
    rate_data = json.load(f)

level = rate_data["level"]
a_try = rate_data["a_try"]
a_s_rate = rate_data["a_s_rate"]
m_s_rate = rate_data["m_s_rate"]

# 4*31 배열 생성
table_data = []
table_data.append(["강화 단계", "평균 시도 횟수", "평균 성공률", "미니게임 성공 성공률"])
for i in range(30):
    table_data.append([
        str(level[i]),
        f"{a_try[i]:.2f}",
        f"{a_s_rate[i]*100:.2f}%",
        f"{m_s_rate[i]*100:.2f}%"
    ])

# Pygame 화면 설정
pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("강화 통계 테이블")
font = pygame.font.SysFont("malgun gothic", 18)
big_font = pygame.font.SysFont("malgun gothic", 24, bold=True)

ROW_HEIGHT = 32
HEADER_COLOR = (200, 220, 255)
ROW_COLOR = (240, 240, 240)
ALT_ROW_COLOR = (225, 225, 225)
TEXT_COLOR = (0, 0, 0)
SCROLLBAR_COLOR = (180, 180, 180)
SCROLLBAR_BG = (220, 220, 220)

table_x, table_y = 40, 20
table_w, table_h = 600, 620
visible_rows = table_h // ROW_HEIGHT

scroll_offset = 0
max_offset = max(0, len(table_data) - visible_rows)

# 버튼 클래스
class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        txt = self.font.render(self.text, True, (0, 0, 0))
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 초기화 함수
def reset_json():
    # list_rate.json 초기화
    with open("list_rate.json", encoding="utf-8") as f:
        rate_data = json.load(f)
    for key in rate_data:
        if key != "level":
            rate_data[key] = [0]*30
    with open("list_rate.json", "w", encoding="utf-8") as f:
        json.dump(rate_data, f, ensure_ascii=False, indent=2)
    # list_table.json 초기화
    with open("list_table.json", encoding="utf-8") as f:
        table_data = json.load(f)
    for key in table_data:
        if key != "level":
            table_data[key] = [0]*30
    with open("list_table.json", "w", encoding="utf-8") as f:
        json.dump(table_data, f, ensure_ascii=False, indent=2)

# 버튼 생성
reset_btn = Button((screen.get_width()-140, screen.get_height()-60, 110, 40), "초기화", font)
back_btn = Button((30, screen.get_height()-60, 110, 40), "뒤로가기", font)

running = True
while running:
    screen.fill((255, 255, 255))
    # 테이블 그리기
    for i in range(visible_rows):
        idx = i + scroll_offset
        if idx >= len(table_data):
            break
        row = table_data[idx]
        y = table_y + i * ROW_HEIGHT
        color = HEADER_COLOR if idx == 0 else (ROW_COLOR if idx % 2 == 1 else ALT_ROW_COLOR)
        pygame.draw.rect(screen, color, (table_x, y, table_w, ROW_HEIGHT))
        for j, cell in enumerate(row):
            txt = font.render(cell, True, TEXT_COLOR)
            screen.blit(txt, (table_x + 10 + j*140, y + 8))

    # 스크롤바 그리기
    if max_offset > 0:
        bar_h = int(table_h * visible_rows / len(table_data))
        bar_y = table_y + int(scroll_offset * (table_h - bar_h) / max_offset)
        pygame.draw.rect(screen, SCROLLBAR_BG, (table_x+table_w+8, table_y, 16, table_h))
        pygame.draw.rect(screen, SCROLLBAR_COLOR, (table_x+table_w+8, bar_y, 16, bar_h))

    reset_btn.draw(screen)
    back_btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_btn.is_clicked(event.pos):
                reset_json()
                # 리셋 후 화면 갱신
                with open("list_rate.json", encoding="utf-8") as f:
                    rate_data = json.load(f)
                a_try = rate_data["a_try"]
                a_s_rate = rate_data["a_s_rate"]
                m_s_rate = rate_data["m_s_rate"]
                for i in range(30):
                    table_data[i+1][1] = f"{a_try[i]:.2f}"
                    table_data[i+1][2] = f"{a_s_rate[i]*100:.2f}%"
                    table_data[i+1][3] = f"{m_s_rate[i]*100:.2f}%"
            elif back_btn.is_clicked(event.pos):
                running = False
        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset = min(max(scroll_offset - event.y, 0), max_offset)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scroll_offset = max(scroll_offset - 1, 0)
            elif event.key == pygame.K_DOWN:
                scroll_offset = min(scroll_offset + 1, max_offset)

    pygame.display.flip()

pygame.quit()