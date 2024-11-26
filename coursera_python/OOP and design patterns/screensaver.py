import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, pair, y=None):
        if y is None:
            self.x = pair[0]
            self.y = pair[1]
        else:
            self.x = pair
            self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2d(self.x * other, self.y * other)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def int_pair(self):
        return (int(self.x), int(self.y))


class Polyline:

    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point_speed(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p in points:
            pygame.draw.circle(gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):
    def __init__(self, count):
        super(Knot, self).__init__()
        self.count = count
        self.curve_index = 0

    def add_point_speed(self, point, speed):
        super(Knot, self).add_point_speed(point, speed)
        self.get_knot()

    def set_points(self):
        super(Knot, self).set_points()
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res

    def remove_point(self, index):
        del self.points[index]
        del self.speeds[index]


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    data.append(["", ""])
    data.append(["N", "New curve"])
    data.append(["F", "Faster"])
    data.append(["S", "Slower"])
    data.append(["D", "Delete curve"])


    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    polyline = Polyline()
    knots = [Knot(steps)]
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)

    clock = pygame.time.Clock()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.add_point_speed(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
                for knot in knots:
                    knot.add_point_speed(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    polyline = Polyline()
                    knots = [Knot(steps)]
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_n:
                    knots.append(Knot(steps))
                if event.key == pygame.K_d:
                    if knots:
                        current_knot = knots[knots.index(knots[-1])]
                        current_knot.remove_point(current_knot.points.index(current_knot.points[-1]))
                if event.key == pygame.K_f:
                    if knots:
                        current_knot = knots[knots.index(knots[-1])]
                        for speed_index in range(len(current_knot.speeds)):
                            current_knot.speeds[speed_index] = Vec2d(current_knot.speeds[speed_index].x * 2,
                                                                     current_knot.speeds[speed_index].y * 2)
                if event.key == pygame.K_s:
                    for knot in knots:
                        for speed_index in range(len(knot.speeds)):
                            knot.speeds[speed_index] = Vec2d(knot.speeds[speed_index].x * 0.8,
                                                             knot.speeds[speed_index].y * 0.8)

        gameDisplay.fill((0, 0, 0))

        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        polyline.draw_points(polyline.points)

        for knot in knots:
            knot.draw_points(knot.get_knot(), 3, color)

            if not pause:
                knot.set_points()


        if show_help:
            draw_help()

        pygame.display.flip()
        clock.tick(60)

    pygame.display.quit()
    pygame.quit()
    exit(0)
