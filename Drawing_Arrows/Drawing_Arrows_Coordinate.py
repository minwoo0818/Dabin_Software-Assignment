import turtle
import math

count = 0
points = []

def move_turtle(x, y):
    global count, points
    points.append((x, y))

    if count == 0:
        count = 1  # 첫 번째 클릭이면 그냥 저장만
        return
    else:
        x1, y1 = points[0]
        x2, y2 = points[1]

        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:  # 두 점이 같으면 무시
            points, count = [], 0
            return

        # 방향 단위벡터 & 수직 단위벡터
        ux, uy = dx/dist, dy/dist
        px, py = -uy, ux

        half_w = dist/5
        shaft_len = dist*3/5

        # 꼭짓점 좌표 계산
        tail_top    = (x1 + px*half_w, y1 + py*half_w)
        tail_bottom = (x1 - px*half_w, y1 - py*half_w)

        shaft_top    = (x1 + ux*shaft_len + px*half_w, y1 + uy*shaft_len + py*half_w)
        shaft_bottom = (x1 + ux*shaft_len - px*half_w, y1 + uy*shaft_len - py*half_w)

        head_top    = (x1 + ux*shaft_len + px*2*half_w, y1 + uy*shaft_len + py*2*half_w)
        head_bottom = (x1 + ux*shaft_len - px*2*half_w, y1 + uy*shaft_len - py*2*half_w)

        tip = (x2, y2)

        polygon = [tail_bottom, shaft_bottom, head_bottom, tip, head_top, shaft_top, tail_top, tail_bottom]

        # 그리기
        t.penup()
        t.goto(polygon[0])
        t.pendown()
        t.begin_fill()
        for px, py in polygon[1:]:
            t.goto(px, py)
        t.end_fill()

        # 초기화
        points, count = [], 0


t = turtle.Turtle()
t.fillcolor("black")
t.pencolor("black")
t.speed(0)

screen = turtle.Screen()
screen.onclick(move_turtle)
screen.mainloop()
