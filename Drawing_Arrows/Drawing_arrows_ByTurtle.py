# import turtle
# import math

# count = 0    #처음 클릭을 판정하는 변수
# points = []  # 클릭 좌표 저장

# def move_turtle(x, y):
#     global count, points
#     points.append((x, y))
#     # 클릭된 좌표로 터틀을 이동시키는 함수
#     if count == 0:
#         t.penup()
#         count += 1
#         t.goto(x, y)
#         t.pendown()
#     else:
#         #이동
#         t.goto(x, y)

#         #값 저장
#         x1, y1 = points[0]
#         x2, y2 = points[1]

#         #거리 기울기 계산
#         dx = x2 - x1
#         dy = y2 - y1
#         dist = math.sqrt(dx**2 + dy**2)
#         angle = math.degrees(math.atan2(dy, dx))
        
#         # 다시 처음으로 이동
#         t.penup()
#         t.goto(x1, y1)

#         #1번 수행 
#         t.pendown()
#         t.setheading(angle)
#         t.left(90)
#         t.forward(dist/5)

#         #2번 수행
#         t.right(90)
#         t.forward(dist/5*3)

#         #3번 수행
#         t.left(90)
#         t.forward(dist/5)

#         #4번 수행
#         t.right(135)
#         t.forward(math.sqrt(((dist * 2 / 5)**2)*2))
#         t.end_fill()

#         # 다시 새 화살표 그릴 수 있도록 초기화
#         points = []
#         count = 0


        
#     #t.dot(10, "black") # 클릭한 지점에 점 찍기

# t = turtle.Turtle()
# t.fillcolor("black")
# screen = turtle.Screen()

# screen.onclick(move_turtle) # 클릭시 함수 실행
# screen.mainloop() # 이벤트 루프 시작
import turtle
import math

points = []  # 클릭 좌표 저장

def draw_arrow(x, y):
    global points
    points.append((x, y))

    if len(points) == 2:
        x1, y1 = points[0]
        x2, y2 = points[1]

        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(dy, dx))

        # 화살대
        t.penup()
        t.goto(x1, y1)
        t.pendown()
        t.goto(x2, y2)

        # 화살촉
        t.penup()
        t.goto(x2, y2)
        t.setheading(angle)

        t.begin_fill()
        t.left(135)
        t.forward(dist * (2**0.5) / 5)

        t.back(dist * (2**0.5) / 5)
        t.right(270)
        t.forward(dist * (2**0.5) / 5)

        t.goto(x2, y2)
        t.end_fill()

        # 다시 새 화살표 그릴 수 있도록 초기화
        points = []

t = turtle.Turtle()
t.shape("turtle")
t.fillcolor("black")
t.pencolor("black")

screen = turtle.Screen()
screen.onclick(draw_arrow)
screen.mainloop()
