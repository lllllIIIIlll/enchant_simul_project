import pygame
import rate

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

class IndexBox:
    def __init__(self, x, y, w, h, idx, s_rate, d_rate, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.idx = idx
        self.s_rate = s_rate
        self.d_rate = d_rate
        self.font = font

    def draw(self, screen):
        # Index, s_rate, d_rate 텍스트
        idx_txt = self.font.render(f"{self.idx+1}", True, (0,0,0))
        s_txt = self.font.render("s_rate", True, (0,0,0))
        d_txt = self.font.render("d_rate", True, (0,0,0))
        screen.blit(idx_txt, (self.rect.x+5, self.rect.y+5))
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
    clock = pygame.time.Clock()
    base_rate = rate.base_rate
    input_rate = rate.get_input_rate()
    rate_table = [list(t) for t in input_rate]  # 30개 [성공, 파괴] 리스트

    # 배치 설정
    box_w, box_h = 120, 100
    margin_x, margin_y = 10, 10
    start_x, start_y = 80, 120

    # 5x6 index_box + rate_box 생성
    index_boxes = []
    rate_boxes = []
    for i in range(5):
        for j in range(6):
            idx = i*6 + j
            x = start_x + j * (box_w + margin_x)
            y = start_y + i * (box_h + margin_y)
            # index_box
            index_boxes.append(IndexBox(x, y, box_w, box_h, idx, "성공률", "파괴율", font))
            # rate_box 2개 (성공, 파괴)
            s_box = RateBox(x+50, y+25, 60, 30, str(rate_table[idx][0]), font)
            d_box = RateBox(x+50, y+60, 60, 30, str(rate_table[idx][1]), font)
            rate_boxes.append((s_box, d_box))

    # 버튼
    save_btn = Button((screen.get_width()//2 - 75, 650, 150, 40), "저장하기", font)
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
                    # 모든 rate_box의 값을 input_rate로 저장
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
                    else:
                        prompt = "저장 실패: 값 개수 오류"
                elif restore_btn.is_clicked(event.pos):
                    # base_rate로 복구
                    for idx, (s_box, d_box) in enumerate(rate_boxes):
                        s_box.text = str(base_rate[idx][0])
                        s_box.txt_surface = font.render(s_box.text, True, (0, 0, 0))
                        d_box.text = str(base_rate[idx][1])
                        d_box.txt_surface = font.render(d_box.text, True, (0, 0, 0))
                    rate.set_input_rate(list(base_rate))  # base_rate가 30개인지 확인
                    prompt = "되돌리기 완료! base_rate로 복구되었습니다."
                elif back_btn.is_clicked(event.pos):
                    running = False

        screen.fill((240, 240, 240))
        title = font.render("확률표 조정", True, (0, 0, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))
        # index_box + rate_box 5x6 행렬로 그리기
        for idx, (ibox, (s_box, d_box)) in enumerate(zip(index_boxes, rate_boxes)):
            ibox.draw(screen)
            # s_rate, d_rate 라벨
            s_label = font.render("s_rate", True, (0,0,0))
            d_label = font.render("d_rate", True, (0,0,0))
            screen.blit(s_label, (s_box.rect.x, s_box.rect.y-18))
            screen.blit(d_label, (d_box.rect.x, d_box.rect.y-18))
            s_box.draw(screen)
            d_box.draw(screen)
        save_btn.draw(screen)
        restore_btn.draw(screen)
        back_btn.draw(screen)
        # 프롬프트
        if prompt:
            prompt_txt = font.render(prompt, True, (0, 100, 200))
            screen.blit(prompt_txt, (screen.get_width() // 2 - prompt_txt.get_width() // 2, 80))
        pygame.display.flip()
        clock.tick(30)

