import pygame
import json
from enchant import enchant  # 주석 해제

# 초기화
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("장비강화")
font = pygame.font.SysFont("malgun gothic", 20)

# 버튼 클래스
class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        txt = font.render(self.text, True, (0, 0, 0))
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 장비 데이터 로드
with open("equipment.json", encoding="utf-8") as f:
    equipment_data = json.load(f)

type_select = ["무기", "방어구", "악세서리"]
type_buttons = [Button((50 + i*180, 200, 150, 50), t) for i, t in enumerate(type_select)]

selected_type = None
enchant_level = 0
result_msg = ""
popup_timer = 0

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
            else:
                # 강화 버튼 클릭 처리
                enhance_btn = Button((225, 300, 150, 50), "강화")
                if enhance_btn.is_clicked(event.pos):
                    equip = next((e for e in equipment_data if e["type"] == selected_type), None)
                    if equip:
                        enchant_level, result_msg = enchant(equip, enchant_level)
                        
                        popup_timer = pygame.time.get_ticks()  # 팝업 시작 시간

    if selected_type is None:
        # 첫 화면: 장비강화 + 타입 선택 버튼
        title = font.render("장비강화", True, (0, 0, 0))
        screen.blit(title, (230, 100))
        for btn in type_buttons:
            btn.draw(screen)
    else:
        # 강화 화면
        # 상단: 강화 레벨에 따라 이미지 추가 (예시: sword1.png)
        try:
            for i in range(enchant_level):
                img_star = pygame.image.load("picture/sword1.png")
                img_star = pygame.transform.scale(img_star, (30, 30))
                screen.blit(img_star, (50 + i*35, 30))
        except Exception:
            pass
        # 강화 레벨 표기
        level_txt = font.render(f"강화 레벨: {enchant_level}", True, (0, 0, 0))
        screen.blit(level_txt, (200, 100))
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

        # result_msg 팝업 출력 (1초간)
        if result_msg:
            now = pygame.time.get_ticks()
            if now - popup_timer < 1000:
                popup_rect = pygame.Rect(150, 250, 300, 60)
                pygame.draw.rect(screen, (220, 220, 220), popup_rect)
                pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)
                msg_txt = font.render(result_msg, True, (255, 0, 0))
                screen.blit(msg_txt, (popup_rect.x + 30, popup_rect.y + 15))
            else:
                result_msg = ""  # 1초 후 팝업 메시지 제거

    pygame.display.flip()

pygame.quit()
