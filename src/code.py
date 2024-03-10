from fltk import *
from random import *
import time
import sys

class Drawing(Fl_Widget):
	def draw(self):
		global x, y, count, particles
		fl_rectf(self.x(), self.y(), self.w(), self.h(), FL_WHITE)
		if count < 5:
			fl_rectf(x, y, 10, 10, FL_BLACK)
		for cor in particles:
			fl_rectf(cor[0], cor[1], 10, 10, FL_BLACK)
	
		
def func_button(widget):
	global x, y, drawing
	x += 1
	y += 1
	drawing.redraw()
	
window = Fl_Window(800, 600)
drawing = Drawing(20, 70, 280, 280)
box = Fl_Box(1, 1, 150, 30, "Hello, World!")
box.box(FL_UP_BOX)
box.labelsize(18)
box.labelfont(FL_BOLD+FL_ITALIC)
box.labeltype(FL_SHADOW_LABEL)
lbutton = Fl_Light_Button(152, 1, 80, 30, "Light")
button = Fl_Button(233, 1, 80, 30, "Button")
button.callback(func_button)
rbutton = Fl_Round_Button(314, 1, 80, 30, "Round")

particles = []
count = 0

p_u = 0.05
p_d = 0.5
p_l = 0.22
p_r = 0.23

def main():
	global x, y, drawing, count
	if count == 0:
		flag = True
		count = 1
	if flag == True:
		x = randint(20, 250)
		y = 90
		flag = False
	else:
		r = random()
		if r < p_l:
			x -= 1
		elif r < p_l + p_r:
			x += 1
		elif r < p_l + p_r + p_d:
			y += 1
		else:
			y -= 1
		
	drawing.redraw()
	Fl.repeat_timeout(0.015, main)

main()

window.end()
window.show()

Fl.run()
		
