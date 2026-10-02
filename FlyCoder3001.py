import time
import random
import sys
import math
import numpy as np
import pygame

# Инициализация графики
pygame.init()
WIDTH, HEIGHT = 700, 650 # Немного увеличили высоту для кнопки
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧬 КИБЕР-ЛАБОРАТОРИЯ: Нейроинтерфейс мухи (Python Edition v3.0)")
clock = pygame.time.Clock()

# Палитра киберпанка
BLACK  = (10, 10, 15)
GRID_C = (25, 25, 35)
WHITE  = (240, 240, 250)
NEON_BLUE  = (0, 229, 255)   # Зрение
NEON_GREEN = (0, 255, 136)   # Дофамин / Успех
NEON_RED   = (255, 7, 58)     # Боль / Ошибка
NEON_ORANGE = (255, 110, 0)   # Моторные нейроны
NEON_PURPLE = (188, 19, 254)  # Синапсы мозга
MENU_BG    = (255, 242, 204)  # Теплый желтый цвет для меню кормления

# Набор токенов теперь для языка Python!
TOKENS = ["print", "(", '"', "Hello", '"', ")", " ", "\n", "import", "def", "x"]

# --- КЛАСС 3D МОДЕЛИ МОЗГА ---
class FlyBrain3D:
    def __init__(self):
        self.nodes = []       
        self.connections = [] 
        self.angle_x = 0
        self.angle_y = 0.02   
        self.angle_z = 0.01
        self._generate_anatomy()

    def _generate_anatomy(self):
        for _ in range(35):
            self.nodes.append({"pos": [random.uniform(-140, -60), random.uniform(-60, 60), random.uniform(-60, 60)], "type": "optic", "activity": 0.1})
        for _ in range(35):
            self.nodes.append({"pos": [random.uniform(60, 140), random.uniform(-60, 60), random.uniform(-60, 60)], "type": "motor", "activity": 0.1})
        for _ in range(50):
            self.nodes.append({"pos": [random.uniform(-50, 50), random.uniform(-50, 50), random.uniform(-50, 50)], "type": "central", "activity": 0.1})
        
        for i in range(len(self.nodes)):
            for _ in range(2):
                j = random.randint(0, len(self.nodes) - 1)
                if i != j:
                    self.connections.append((i, j))

    def update_activity(self, active_zone, intensity=1.0):
        for node in self.nodes:
            node["activity"] *= 0.7  
            if node["type"] == active_zone:
                node["activity"] = intensity

    def rotate_point(self, x, y, z):
        rad = self.angle_x
        cos, sin = math.cos(rad), math.sin(rad)
        y, z = y * cos - z * sin, y * sin + z * cos
        
        rad = self.angle_y
        cos, sin = math.cos(rad), math.sin(rad)
        x, z = x * cos + z * sin, -x * sin + z * cos
        return x, y, z

    def draw(self, surface, center_x, center_y, pulse_color=None):
        for edge in self.connections:
            p1 = self.nodes[edge[0]]["pos"]
            p2 = self.nodes[edge[1]]["pos"]
            x1, y1, z1 = self.rotate_point(*p1)
            x2, y2, z2 = self.rotate_point(*p2)
            
            focal, dist = 300, 400
            pt1_x = int(x1 * focal / (z1 + dist)) + center_x
            pt1_y = int(y1 * focal / (z1 + dist)) + center_y
            pt2_x = int(x2 * focal / (z2 + dist)) + center_x
            pt2_y = int(y2 * focal / (z2 + dist)) + center_y
            
            line_color = pulse_color if pulse_color else GRID_C
            pygame.draw.line(surface, line_color, (pt1_x, pt1_y), (pt2_x, pt2_y), 1)

        for node in self.nodes:
            x, y, z = self.rotate_point(*node["pos"])
            focal, dist = 300, 400
            screen_x = int(x * focal / (z + dist)) + center_x
            screen_y = int(y * focal / (z + dist)) + center_y
            size = max(2, int(6 * focal / (z + dist)))
            
            if node["type"] == "optic":
                base_color = np.array(NEON_BLUE)
            elif node["type"] == "motor":
                base_color = np.array(NEON_ORANGE)
            else:
                base_color = np.array(NEON_PURPLE)
                
            if node["activity"] > 0.1:
                color = pulse_color if pulse_color else np.clip(base_color * (1 + node["activity"] * 2), 0, 255).astype(int)
                size += 2
            else:
                color = base_color
                
            pygame.draw.circle(surface, color, (screen_x, screen_y), size)

# --- ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ МУХИ ---
class FlyAI:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.3
        self.discount = 0.9
        self.epsilon = 1.0  

    def choose_action(self, current_code_state):
        if random.random() < self.epsilon:
            return random.choice(TOKENS)
        if current_code_state not in self.q_table:
            return random.choice(TOKENS)
        return max(self.q_table[current_code_state], key=self.q_table[current_code_state].get)

    def learn(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {t: 0.0 for t in TOKENS}
        if next_state not in self.q_table:
            self.q_table[next_state] = {t: 0.0 for t in TOKENS}
            
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())
        self.q_table[state][action] = old_value + self.learning_rate * (reward + self.discount * next_max - old_value)
# --- ГЛАВНЫЙ СКРИПТ ---
# --- ГЛАВНЫЙ СКРИПТ ---
def main():
    brain = FlyBrain3D()
    fly = FlyAI()
    
    health = 100
    dopamine = 0
    generation = 1
    step = 1
    
    # Идеальный паттерн для Python: print("Hello")
    target_syntax = ['print', '(', '"', 'Hello', '"', ')']
    current_chain = []
    
    font = pygame.font.SysFont("Consolas", 14)
    font_bold = pygame.font.SysFont("Consolas", 18, bold=True)
    font_menu = pygame.font.SysFont("Arial", 22, bold=True)
    
    running = True
    pulse_color = None
    pulse_timer = 0

    # Переменные для меню кормления
    show_feed_menu = False
    feed_menu_start_time = 0

    # Размеры и позиция кнопки "ПОКОРМИТЬ" в самом нижнем углу
    btn_w, btn_h = 140, 40
    btn_x = WIDTH - btn_w - 15
    btn_y = HEIGHT - btn_h - 15

    while running:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()
        
        # Рисуем фоновую сетку лаборатории
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, GRID_C, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, GRID_C, (0, y), (WIDTH, y))

        # Обработка событий кликов
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                # ИСПРАВЛЕНО: Правильная проверка клика по координатам X и Y
                if not show_feed_menu:
                    if btn_x <= mouse_pos[0] <= btn_x + btn_w and btn_y <= mouse_pos[1] <= btn_y + btn_h:
                        show_feed_menu = True
                        feed_menu_start_time = current_time

        # --- ЛОГИКА МЕНЮ КОРМЛЕНИЯ (ЗАМОРАЖИВАЕТ ИГРУ НА 3 СЕКУНДЫ) ---
        if show_feed_menu:
            # Если прошло 3 секунды (3000 миллисекунд)
            if current_time - feed_menu_start_time >= 3000:
                show_feed_menu = False
                dopamine += 100  # Добавляем +100 дофамина!
                health = min(100, health + 20) # Немного подлечим муху за еду
                pulse_color = NEON_GREEN
                pulse_timer = 5
            else:
                # Отрисовка 3D мозга на заднем плане, чтобы картинка не ломалась
                brain.draw(screen, center_x=480, center_y=300, pulse_color=pulse_color)
                
                # Рисуем всплывающее меню по центру экрана
                menu_w, menu_h = 320, 220
                menu_x = (WIDTH - menu_w) // 2
                menu_y = (HEIGHT - menu_h) // 2
                
                # Фон меню
                pygame.draw.rect(screen, MENU_BG, (menu_x, menu_y, menu_w, menu_h))
                pygame.draw.rect(screen, NEON_ORANGE, (menu_x, menu_y, menu_w, menu_h), 3) # Рамка
                
                # Текст "ням-ням-ням"
                yummy_text = font_menu.render("ням-ням-ням... 🍰🍯", True, (39, 174, 96))
                screen.blit(yummy_text, (menu_x + 50, menu_y + 30))
                
                # Рисуем Радостную Муху (ASCII Арт в окне)
                fly_lines = [
                    "    \\  /  ",
                    "  🪰( 🧠 )🪰",
                    "   / | \\  ",
                    "*Радостно кушает*"
                ]
                for idx, line in enumerate(fly_lines):
                    fly_render = font_bold.render(line, True, (211, 84, 0))
                    screen.blit(fly_render, (menu_x + 80, menu_y + 80 + (idx * 20)))
                
                pygame.display.flip()
                clock.tick(15)
                continue # Пропускаем остальную симуляцию, пока муха ест

        # --- ОБЫЧНАЯ ЛОГИКА СИМУЛЯЦИИ КОДА ---
        state_str = "".join(current_chain[-3:]) 
        phase = (pygame.time.get_ticks() // 600) % 3
        
        if phase == 0:  
            brain.update_activity("optic", intensity=1.5)
            status_text = "👁️ Python IDE: Рецепторы мухи сканируют синтаксис..."
        elif phase == 1: 
            brain.update_activity("motor", intensity=1.5)
            status_text = "🪰 ДВИГАТЕЛЬНЫЙ ИМПУЛЬС: Муха печатает код на Python."
        else: 
            brain.update_activity("central", intensity=1.5)
            status_text = "🧠 ИНТЕРПРЕТАТОР PYTHON: Проверка инструкций в памяти..."
            
            action = fly.choose_action(state_str)
            current_chain.append(action)
            if len(current_chain) > 6:
                current_chain.pop(0)
                
            # ПРОВЕРКА СИНТАКСИСА PYTHON
            is_valid_progress = False
            for i in range(1, len(current_chain) + 1):
                if current_chain[:i] == target_syntax[:i]:
                    is_valid_progress = True
            if current_chain == target_syntax: 
                reward = 200
                dopamine += 150
                pulse_color = NEON_GREEN
                pulse_timer = 10
                current_chain = [] 
                fly.epsilon = max(0.01, fly.epsilon - 0.15) 
                print(f"🎉 Муха написала: print(\"Hello\") на Python! Дофамин взлетел!")
            elif is_valid_progress and len(current_chain) > 0: 
                reward = 25
                dopamine += 10
                pulse_color = NEON_GREEN
                pulse_timer = 3
            else: 
                reward = -10
                health -= 5  
                dopamine = max(0, dopamine - 2)
                pulse_color = NEON_RED
                pulse_timer = 3
                if len(current_chain) > 3: current_chain.pop(0) 
                
            next_state_str = "".join(current_chain[-3:])
            fly.learn(state_str, action, reward, next_state_str)
            step += 1

        if pulse_timer > 0:
            pulse_timer -= 1
        else:
            pulse_color = None

        # Отрисовка 3D-мозга
        brain.draw(screen, center_x=480, center_y=300, pulse_color=pulse_color)

        if health <= 0:
            generation += 1
            health = 100
            current_chain = []
            fly.epsilon = min(1.0, fly.epsilon + 0.1) 

        # --- ОТРЕСОВКА ИНТЕРФЕЙСА ---
        # Левая верхняя плашка (Статистика)
        pygame.draw.rect(screen, (20, 20, 30), (15, 15, 270, 110))
        pygame.draw.rect(screen, GRID_C, (15, 15, 270, 110), 1)
        
        screen.blit(font_bold.render(f"ПОПУЛЯЦИЯ МУХ: Поколение #{generation}", True, WHITE), (25, 25))
        screen.blit(font.render(f"Жизненная сила: {health}%", True, WHITE), (25, 55))
        pygame.draw.rect(screen, (100, 0, 0), (25, 75, 200, 8))
        pygame.draw.rect(screen, NEON_RED, (25, 75, int(health * 2), 8))
        screen.blit(font.render(f"Нейро-дофамин: {dopamine} ед.", True, NEON_GREEN), (25, 95))

        # Окно вывода PYTHON IDE
        pygame.draw.rect(screen, (5, 5, 10), (15, 140, 270, 250))
        pygame.draw.rect(screen, NEON_PURPLE, (15, 140, 270, 250), 1)
        screen.blit(font_bold.render("ВИРТУАЛЬНЫЙ ТЕРМИНАЛ PYTHON:", True, NEON_PURPLE), (25, 150))
        
        raw_code = "".join(current_chain) if current_chain else "[ Сборка кода... ]"
        code_lines = [
            "# -= Мой Скрипт Python =-",
            "import sys",
            "if __name__ == '__main__':",
            f"    {raw_code}",
            "    sys.exit()"
        ]
        for idx, line in enumerate(code_lines):
            color = NEON_GREEN if idx == 3 and pulse_color == NEON_GREEN else WHITE
            if idx == 3 and pulse_color == NEON_RED: color = NEON_RED
            screen.blit(font.render(line, True, color), (30, 190 + (idx * 22)))

        # Нижняя панель логов
        pygame.draw.rect(screen, (15, 15, 25), (15, 410, 670, 170))
        pygame.draw.rect(screen, GRID_C, (15, 410, 670, 170), 1)
        screen.blit(font_bold.render("ИНДИКАТОРЫ НЕЙРОИНТЕРФЕЙСА:", True, NEON_BLUE), (25, 420))
        screen.blit(font.render(status_text, True, WHITE), (25, 455))
        
        intellect = int((1.0 - fly.epsilon) * 100)
        screen.blit(font.render(f"Адаптация ИИ (Уровень интеллекта): {intellect}%", True, NEON_BLUE), (25, 490))
        screen.blit(font.render(f"Всего итераций обучения: {step}", True, WHITE), (25, 520))
        screen.blit(font.render("Кликни на кнопку справа внизу, чтобы покормить муху", True, NEON_ORANGE), (25, 550))

        # --- КНОПКА ПОКОРМИТЬ ---
        # ИСПРАВЛЕНО: Правильная проверка наведения мыши по координатам X и Y
        mouse_pos = pygame.mouse.get_pos()
        if btn_x <= mouse_pos[0] <= btn_x + btn_w and btn_y <= mouse_pos[1] <= btn_y + btn_h:
            btn_color = (46, 204, 113) # Ярко-зеленый при наведении
        else:
            btn_color = (39, 174, 96)  # Обычный зеленый
            
        pygame.draw.rect(screen, btn_color, (btn_x, btn_y, btn_w, btn_h), border_radius=5)
        btn_text = font_bold.render("ПОКОРМИТЬ 🍰", True, WHITE)
        screen.blit(btn_text, (btn_x + 13, btn_y + 10))

        pygame.display.flip()
        clock.tick(15) 

    pygame.quit()

if __name__ == "__main__":
    main()
