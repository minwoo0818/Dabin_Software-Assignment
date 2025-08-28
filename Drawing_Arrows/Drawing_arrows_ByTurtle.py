import turtle
import math

#처음 클릭을 판정하는 변수
count = 0

def move_turtle(x, y):
    global count
    # 클릭된 좌표로 터틀을 이동시키는 함수
    if count == 0:
        t.penup()
        count += 1
        t.goto(x, y)
        t.pendown()
    t.goto(x, y)
    t.dot(10, "black") # 클릭한 지점에 점 찍기

t = turtle.Turtle()
screen = turtle.Screen()

screen.onclick(move_turtle) # 클릭시 함수 실행
screen.mainloop() # 이벤트 루프 시작