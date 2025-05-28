import pygame
import random

base_rate = [
    (0.95, 0.0), (0.90, 0.0), (0.85, 0.0), (0.85, 0.0), (0.80, 0.0),
    (0.75, 0.0), (0.70, 0.0), (0.65, 0.0), (0.60, 0.0), (0.55, 0.0),
    (0.50, 0.0), (0.45, 0.0), (0.40, 0.0), (0.35, 0.0), (0.30, 0.021),
    (0.30, 0.021), (0.30, 0.068), (0.15, 0.068), (0.15, 0.085), (0.15, 0.105),
    (0.30, 0.1275), (0.15, 0.17), (0.15, 0.18), (0.10, 0.18), (0.10, 0.18),
    (0.07, 0.186), (0.05, 0.19), (0.03, 0.194), (0.10, 0.198), (0.10, 0.198)
]
input_rate = base_rate.copy()

def show_rate_table_popup(screen):
    font = pygame.font.SysFont("malgun gothic", 18)
    clock = pygame.time.Clock()
    input_boxes = []
    box_w, box_h = 80, 30
    for i in range(5):
        for j in range(6):
            idx = i*6 + j
            x = 100 + j * (box_w + 10)
            y = 150 + i * (box_h + 10)
            text = str(input_rate[idx][0])
            input_boxes.append(InputBox(x, y, box_w, box_h, text))

    save_btn = Button((screen.get_width() // 2 - 75, 400, 150, 40), "저장하기")
    # 복구 버튼: 우측 하단
    restore_btn = Button((screen.get_width() - 180, screen.get_height() - 70, 150, 40), "복구")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_btn.is_clicked(event.pos):
                    for idx, box in enumerate(input_boxes):
                        try:
                            val = float(box.text)
                        except:
                            val = 0.0
                        input_rate[idx] = (val, input_rate[idx][1])
                    running = False
                elif restore_btn.is_clicked(event.pos):
                    # base_rate 값으로 덮어쓰기
                    for idx in range(30):
                        input_boxes[idx].text = str(base_rate[idx][0])
                        input_boxes[idx].txt_surface = font.render(input_boxes[idx].text, True, (0, 0, 0))
                        input_rate[idx] = (base_rate[idx][0], base_rate[idx][1])
                    # 복구 즉시 저장 효과
                    running = False

        screen.fill((240, 240, 240))
        title = font.render("확률표 조정", True, (0, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 80))
        for box in input_boxes:
            box.draw(screen)
        save_btn.draw(screen)
        restore_btn.draw(screen)
        pygame.display.flip()
        clock.tick(30)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200, 200, 255)
        self.text = text
        self.txt_surface = pygame.font.SysFont("malgun gothic", 18).render(text, True, (0, 0, 0))
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
                self.text += event.unicode
            self.txt_surface = pygame.font.SysFont("malgun gothic", 18).render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        txt = pygame.font.SysFont("malgun gothic", 18).render(self.text, True, (0, 0, 0))
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def enchant_rate(enchant_level, mini_game):
    if enchant_level < 0 or enchant_level > 29:
        return 3
    base_success, destroy_rate = input_rate[enchant_level]
    success_rate = base_success * (1 + mini_enchant(mini_game))
    rand = random.random()
    if rand < success_rate:
        return 1
    elif rand < destroy_rate:
        return 0
    else:
        return 2

def mini_enchant(mini_game):
    if mini_game == 1:
        return 0.05
    elif mini_game == 0:
        return 0