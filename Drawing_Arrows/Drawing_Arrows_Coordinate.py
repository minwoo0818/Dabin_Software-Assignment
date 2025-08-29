import turtle
import math

count = 0
points = []

def move_turtle(x, y):
    global count, points
    points.append((x, y))

    if count == 0:
        count = 1
        return
    else:
        x1, y1 = points[0]
        x2, y2 = points[1]

        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(dy, dx))

        t.penup()
        t.goto(x1, y1)
        t.setheading(angle)   # 화살표 방향 맞추기
        t.pendown()

        t.begin_fill()  # ------------------- 채우기 시작

        # 1번: 왼쪽으로 90도 꺾어 dist/5 전진
        t.left(90)
        t.forward(dist/5)

        # 2번: 다시 오른쪽 90도 → 3/5 거리 전진
        t.right(90)
        t.forward(dist*3/5)

        # 3번: 왼쪽 90도 → dist/5 전진
        t.left(90)
        t.forward(dist/5)

        # 4번: 오른쪽 135도 → 화살촉 왼쪽 그리기
        t.right(135)
        t.forward(math.sqrt(2) * (dist*2/5))

        # 5번: 반대쪽 화살촉 (왼쪽 90도)
        t.left(90)
        t.forward(math.sqrt(2) * (dist*2/5))

        # 6번: 오른쪽 135도 → dist/5 전진 (위쪽 테두리)
        t.right(135)
        t.forward(dist/5)

        # 7번: 오른쪽 90도 → dist*3/5 후진해서 시작점 복귀
        t.right(90)
        t.forward(dist*3/5)

        # 8번: 왼쪽 90도 → dist/5 후진해서 원래 위치
        t.left(90)
        t.forward(dist/5)

        t.end_fill()   # ------------------- 채우기 끝

        # 초기화
        points = []
        count = 0


t = turtle.Turtle()
t.fillcolor("black")
t.pencolor("black")
t.speed(0)

screen = turtle.Screen()
screen.onclick(move_turtle)
screen.mainloop()
