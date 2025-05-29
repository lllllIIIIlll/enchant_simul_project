import pygame
import subprocess
import sys
from fnc import list  

subprocess.run(["python", "list.py"])

if "--reset" in sys.argv:
    list.reset_json()
    sys.exit()

pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("강화 통계 테이블")
font = pygame.font.SysFont("malgun gothic", 18)
big_font = pygame.font.SysFont("malgun gothic", 24, bold=True)

ROW_H = 32 # H = height, C = color
HEADER_C = (200, 220, 255)
ROW_C = (240, 240, 240)
ALT_ROW_C = (225, 225, 225)
TEXT_C = (0, 0, 0)
SCROLLBAR_C = (180, 180, 180)
SCROLLBAR_BG = (220, 220, 220)

table_x, table_y = 40, 20  
table_w, table_h = 600, 620
visible_rows = table_h // ROW_H

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

reset_btn = Button((screen.get_width()-140, screen.get_height()-60, 110, 40), "초기화", big_font)
back_btn = Button((30, screen.get_height()-60, 110, 40), "뒤로가기", big_font)

table_data = list.load_table_data()
scroll_offset = 0
max_offset = max(0, len(table_data) - visible_rows)

running = True
while running:
    screen.fill((255, 255, 255))
    for i in range(visible_rows):
        idx = i + scroll_offset
        if idx >= len(table_data):
            break
        row = table_data[idx]
        y = table_y + i * ROW_H
        color = HEADER_C if idx == 0 else (ROW_C if idx % 2 == 1 else ALT_ROW_C )
        pygame.draw.rect(screen, color, (table_x, y, table_w, ROW_H))
        for j, cell in enumerate(row):
            txt = font.render(cell, True, TEXT_C)
            screen.blit(txt, (table_x + 10 + j*140, y + 8))

    if max_offset > 0:
        bar_h = int(table_h * visible_rows / len(table_data))
        bar_y = table_y + int(scroll_offset * (table_h - bar_h) / max_offset)
        pygame.draw.rect(screen, SCROLLBAR_BG, (table_x+table_w+8, table_y, 16, table_h))
        pygame.draw.rect(screen, SCROLLBAR_C, (table_x+table_w+8, bar_y, 16, bar_h))

    reset_btn.draw(screen)
    back_btn.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_btn.is_clicked(event.pos):
                list.reset_json()
                table_data = list.load_table_data()  # 리셋 후 테이블 갱신
            elif back_btn.is_clicked(event.pos):
                running = False
        elif event.type == pygame.MOUSEWHEEL:
            scroll_offset = min(max(scroll_offset - event.y, 0), max_offset)
    
    pygame.display.flip()

pygame.quit()