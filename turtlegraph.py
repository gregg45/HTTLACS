import turtle
def draw_bar(t, height):
	"""Get turtle t to draw one bar, of height. """
	if height >= 200:
		tess.color("blue","red")
	elif 100 < height < 200:
		tess.color("blue","yellow")
	else:
		tess.color("blue","green")

	t.forward(40)
	t.forward(-40)
	t.begin_fill()
	t.left(90)
	t.forward(height)
	if height < 0:
		t.penup()
		t.forward(-20)
		t.write("   " + str(height))
		t.forward(20)
		t.pendown()
	else:
		t.write("   " + str(height))
	t.right(90)
	t.forward(40)
	t.right(90)
	t.forward(height)
	t.left(90)
	t.end_fill()
	t.forward(10)

wn = turtle.Screen()
tess = turtle.Turtle()


tess.pensize(3)
wn.bgcolor("lightgreen")

xs = [50, -100, 150, -200, 250]

for b in xs:
	draw_bar(tess,b)