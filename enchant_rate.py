import pygame
import rate
import time

class RateBox:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 8 and (event.unicode.isdigit() or event.unicode in "."):
                    self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 230, 255), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

        if self.active:
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                cursor_x = self.rect.x + 5 + self.txt_surface.get_width()
                cursor_y = self.rect.y + 7
                cursor_h = self.txt_surface.get_height()
                pygame.draw.line(screen, (0,0,0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_h), 2)

class IndexBox:
    def __init__(self, x, y, w, h, idx, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.idx = idx
        self.font = font
        
    def draw(self, screen):
        bold_font = pygame.font.SysFont("malgun gothic", 14, bold=True)
        idx_txt = bold_font.render(f"{self.idx+1}단계", True, (0,0,0))
        s_txt = self.font.render(str("성공"), True, (0,0,0))
        d_txt = self.font.render(str("파괴"), True, (0,0,0))
        idx_rect = idx_txt.get_rect(center=(self.rect.x + self.rect.w // 2, self.rect.y + 15))
        
        screen.blit(idx_txt, idx_rect)
        screen.blit(s_txt, (self.rect.x+5, self.rect.y+30))
        screen.blit(d_txt, (self.rect.x+5, self.rect.y+60))

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

def show_rate_table_popup(screen):
    font = pygame.font.SysFont("malgun gothic", 16)
    big_font = pygame.font.SysFont("malgun gothic", 24, bold=True)
    clock = pygame.time.Clock()
    base_rate = rate.base_rate
    input_rate = rate.get_input_rate()
    rate_table = [list(t) for t in input_rate]

    box_w, box_h = 120, 100
    margin_x, margin_y = 10, 10
    cols, rows = 6, 5

    total_w = cols * box_w + (cols - 1) * margin_x
    total_h = rows * box_h + (rows - 1) * margin_y

    start_x = (screen.get_width() - total_w) // 2
    start_y = (screen.get_height() - total_h) // 2

    index_boxes = []
    rate_boxes = []
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            x = start_x + j * (box_w + margin_x)
            y = start_y + i * (box_h + margin_y)
            index_boxes.append(IndexBox(x, y, box_w, box_h, idx, font))
            s_box = RateBox(x+50, y+25, 60, 30, str(rate_table[idx][0]), font)
            d_box = RateBox(x+50, y+60, 60, 30, str(rate_table[idx][1]), font)
            rate_boxes.append((s_box, d_box))

    save_btn = Button((screen.get_width()//2 - 75, screen.get_height() - 70, 100, 40), "저장하기", font)
    restore_btn = Button((screen.get_width() - 180, screen.get_height() - 70, 150, 40), "되돌리기", font)
    back_btn = Button((30, screen.get_height() - 70, 100, 40), "뒤로가기", font)

    prompt = ""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            for s_box, d_box in rate_boxes:
                s_box.handle_event(event)
                d_box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_btn.is_clicked(event.pos):
                    new_rate = []
                    for s_box, d_box in rate_boxes:
                        try:
                            s = float(s_box.text)
                        except:
                            s = 0.0
                        try:
                            d = float(d_box.text)
                        except:
                            d = 0.0
                        new_rate.append((s, d))
                    if len(new_rate) == 30:
                        rate.set_input_rate(new_rate)
                        prompt = "저장 완료!"
                    else:
                        prompt = "저장 실패: 값 개수 오류"
                elif restore_btn.is_clicked(event.pos):
                    for idx, (s_box, d_box) in enumerate(rate_boxes):
                        s_box.text = str(base_rate[idx][0])
                        s_box.txt_surface = font.render(s_box.text, True, (0, 0, 0))
                        d_box.text = str(base_rate[idx][1])
                        d_box.txt_surface = font.render(d_box.text, True, (0, 0, 0))
                    rate.set_input_rate(list(base_rate))
                    prompt = "되돌리기 완료!"
                elif back_btn.is_clicked(event.pos):
                    running = False

        screen.fill((240, 240, 240))
        title = big_font.render("확률표 조정", True, (0, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))
        for idx, (ibox, (s_box, d_box)) in enumerate(zip(index_boxes, rate_boxes)):
            ibox.draw(screen, s_box.text, d_box.text)
            s_box.draw(screen)
            d_box.draw(screen)
        save_btn.draw(screen)
        restore_btn.draw(screen)
        back_btn.draw(screen)
        if prompt:
            prompt_txt = font.render(prompt, True, (0, 100, 200))
            screen.blit(prompt_txt, (screen.get_width() // 2 - prompt_txt.get_width() // 2, 80))
        pygame.display.flip()
        clock.tick(30)

