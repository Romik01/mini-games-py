import pygame
import sys
import math
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
WIDTH, HEIGHT = 400, 400
SCREEN_SIZE = (WIDTH, HEIGHT)

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Определение точек (9 точек для головоломки)
points = []

# Генерация случайных координат для 9 точек
for _ in range(9):
    x = random.randint(10, WIDTH - 10)
    y = random.randint(10, HEIGHT - 10)
    points.append((x, y))

# Определение углов (3 угла для головоломки)
angles = []

# Определение текущей выбранной точки
selected_points = []

# Флаги для отслеживания состояния игры
game_started = False
game_over = False

# Основной игровой цикл
def main():
    global game_started, selected_points, angles, game_over

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Головоломка")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_started and not game_over:
                    x, y = pygame.mouse.get_pos()
                    clicked_point = find_closest_point(x, y)
                    if selected_points and clicked_point not in selected_points:
                        if len(selected_points) == 2:
                            angle = selected_points + [clicked_point]
                            if can_create_angle(angle):
                                angles.append(angle)
                                selected_points = []
                            else:
                                show_message(screen, "Неправильно")
                        elif len(selected_points) == 1:
                            selected_points.append(clicked_point)
                    elif clicked_point not in selected_points:
                        selected_points.append(clicked_point)
                elif game_over:
                    if restart_button.collidepoint(event.pos):
                        game_over = False
                        initialize_game()
                else:
                    game_started = True
                    initialize_game()

        if not game_started:
            screen.fill(WHITE)
            if game_over:
                draw_game_over_screen(screen)
            else:
                draw_start_screen(screen)
            pygame.display.flip()
            continue

        screen.fill(WHITE)

        # Отрисовка точек
        for point in points:
            pygame.draw.circle(screen, BLACK, point, 5)

        # Отрисовка углов
        for angle in angles:
            pygame.draw.line(screen, RED, angle[0], angle[1], 2)
            pygame.draw.line(screen, RED, angle[0], angle[2], 2)

        # Отрисовка выбранных точек
        for point in selected_points:
            pygame.draw.circle(screen, BLACK, point, 8)

        pygame.display.flip()

# Функция для отображения всплывающего сообщения
def show_message(screen, message):
    global game_over
    game_over = True
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)  # Отображение сообщения на 1 секунду

# Функция для поиска ближайшей точки к заданным координатам
def find_closest_point(x, y):
    min_distance = float('inf')
    closest_point = None
    for point in points:
        if point not in selected_points:
            distance = math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_point = point
    return closest_point

# Функция для проверки, можно ли создать угол с заданными точками
def can_create_angle(angle):
    if len(angle) != 3:
        return False
    a, b, c = angle

    # Проверка, что угол не является 180 градусов
    if math.isclose(math.dist(a, b), math.dist(b, c)):
        return False

    # Проверка, что угол не пересекает другие углы
    for existing_angle in angles:
        if do_angles_intersect(angle, existing_angle):
            return False

    # Проверка, что стороны прилегающие к углу равны
    if not math.isclose(math.dist(a, b), math.dist(a, c)):
        return False

    return True

# Проверка, пересекаются ли два угла
def do_angles_intersect(angle1, angle2):
    # Получаем координаты точек для каждого угла
    a1, b1, c1 = angle1
    a2, b2, c2 = angle2

    # Проверяем, пересекаются ли отрезки ab1 и ab2
    if do_segments_intersect(a1, b1, a2, b2):
        return True

    # Проверяем, пересекаются ли отрезки ab1 и ac2
    if do_segments_intersect(a1, b1, a2, c2):
        return True

    # Проверяем, пересекаются ли отрезки ac1 и ab2
    if do_segments_intersect(a1, c1, a2, b2):
        return True

    # Проверяем, пересекаются ли отрезки ac1 и ac2
    if do_segments_intersect(a1, c1, a2, c2):
        return True

    return False

# Проверка, пересекаются ли два отрезка
def do_segments_intersect(p1, p2, q1, q2):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0: return 0
        return 1 if val > 0 else 2

    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and is_on_segment(p1, q1, p2): return True
    if o2 == 0 and is_on_segment(p1, q2, p2): return True
    if o3 == 0 and is_on_segment(q1, p1, q2): return True
    if o4 == 0 and is_on_segment(q1, p2, q2): return True

    return False

# Проверка, лежит ли точка q на отрезке pr
def is_on_segment(p, q, r):
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
        (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False

# Инициализация игры
def initialize_game():
    global angles, game_started, game_over, selected_points
    angles = []
    selected_points = []
    game_over = False

# Отрисовка начального экрана
def draw_start_screen(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Нажмите для начала игры", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Отрисовка экрана завершения игры
def draw_game_over_screen(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Игра завершена!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

if __name__ == "__main__":
    initialize_game()
    main()
