from fltk import *
from random import *
import time
import sys

fid_xy = [280, 280]
tfid_xy = [20, 70]
p_s = 10

class Drawing(Fl_Widget):
	def draw(self):
		global x, y, count, particles, c_max, part
		fl_rectf(self.x(), self.y(), self.w(), self.h(), FL_WHITE)
		if count <= c_max:
			fl_rectf(part.x, part.y, p_s, p_s, FL_BLACK)
		for cor in particles:
			fl_rectf(cor[0], cor[1], p_s, p_s, FL_BLACK)
	
class Particle():
	def __init__(self):
		self.x = choice([30, 40, 50, 80, 120])
		self.y = 90
		self.p = [0.05, 0.22, 0.23, 0.5]
		self.t = False
	def move(self):
		global particles, p_s, fid_xy, tfid_xy
		for i in particles:
			if (self.x == i[0] and self.y == i[1] - p_s) or (self.x == i[0] - p_s and self.y == i[1]) or (self.x == i[0] + p_s and self.y == i[1]):
				self.t = True
				break
		if self.y < fid_xy[1] + tfid_xy[1] - p_s and self.t == False:
			r = random()
			if r < self.p[0]:
				self.y -= p_s
			elif r < self.p[0]+self.p[1]:
				self.x -= p_s
			elif r < self.p[0]+self.p[1]+self.p[2]:
				self.x += p_s
			else:
				self.y += p_s 
			if self.x < tfid_xy[0]:
				self.x = tfid_xy[0]+fid_xy[0]-p_s
			if self.x > tfid_xy[0]+fid_xy[0]:
				self.x = tfid_xy[0]+p_s 
		else:
			self.t = True
		 	


window = Fl_Window(800, 600)
drawing = Drawing(20, 70, fid_xy[0], fid_xy[1])
box = Fl_Box(1, 1, 150, 30, "Hello, World!")
box.box(FL_UP_BOX)
box.labelsize(18)
box.labelfont(FL_BOLD+FL_ITALIC)
box.labeltype(FL_SHADOW_LABEL)
lbutton = Fl_Light_Button(152, 1, 80, 30, "Light")
button = Fl_Button(233, 1, 80, 30, "Button")
rbutton = Fl_Round_Button(314, 1, 80, 30, "Round")

particles = []
count = 0
c_max = 100
flag = False
end = False
x = 0
y = 0
part = Particle()

p_u = 0.05
p_d = 0.5
p_l = 0.22
p_r = 0.23

'''def main():
	global x, y, drawing, count, fid_xy, tfid_xy, particles, flag, p_s, end
	
	if count == 0:
		flag = True
	if flag == True and count <= c_max:
		x = choice([30, 40, 50, 80, 120])
		y = 90
		flag = False
		count += 1
	if y < fid_xy[1] + tfid_xy[1] - p_s and flag == False:
		r = random()
		if r < p_l:
			x -= p_s
		elif r < p_l + p_r:
			x += p_s
		elif r < p_l + p_r + p_d:
			y += p_s
		else:
			y -= p_s
		for p in particles:
			if (x == p[0] and y == p[1] - p_s) or (x == p[0] - p_s and y == p[1]) or (x == p[0] + p_s and y == p[1]):
				flag = True
				
	if y >= fid_xy[1] + tfid_xy[1] - p_s or flag == True:
		particles += [[x, y]]
		print(particles)
		flag = True
		
	drawing.redraw()
	Fl.repeat_timeout(0.015, main)'''
	
def main():
	global drawing, count, fid_xy, tfid_xy, particles, p_s, flag, part
	
	if (count == 0 or part.t == True) and count <= c_max:
		part = Particle()
		count += 1
	if part.t == False:
		part.move()
	if part.t == True:
		particles += [[part.x, part.y]]
	
	drawing.redraw()
	Fl.repeat_timeout(0.005, main)

main()

window.end()
window.show()

Fl.run()
		
