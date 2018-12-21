import canvas
from bstpq import BSTPQ as Tree

def draw_line(x1, y1, x2, y2):
	canvas.set_line_width(3)
	canvas.draw_line(x1, y1, x2, y2)
		
def draw_circle(x, y, r):
	canvas.set_line_width(3)
	canvas.set_stroke_color(0, 0, 0)
	canvas.set_fill_color(255,255,255)
	canvas.fill_ellipse(x - r, y - r, 2 * r, 2 * r)
	canvas.draw_ellipse(x - r, y - r, 2 * r, 2 * r)
	
def x(node, offset):
	nodewidth = 40
	return nodewidth * (len(node.left) + 1) + offset

def draw_label(s, x, y):
	fs = 30
	fnt = 'Helvetica-Bold'
	w, h = canvas.get_text_size(str(s), fnt, fs)
	canvas.set_fill_color(0,0,0)
	canvas.draw_text(str(s), x - w / 2, y - h / 2, fnt, fs)

def draw(T, xoffset = 0, yoffset = 500):
	if isinstance(T, Tree):
		return draw(T._root)
	radius = 30
	levelheight = 80
	a,b = x(T, xoffset), yoffset
	c = yoffset - levelheight	
	if len(T.left) > 0:
		draw_line(a, b, x(T.left, xoffset), c)	
		draw(T.left, xoffset, c)
	if len(T.right) > 0:
		draw_line(a, b, x(T.right, a), c)
		draw(T.right, a, c)
	draw_circle(a, b, radius)
	draw_label(T.key, a, b)

if __name__ == '__main__':
	canvas.set_size(600, 600)
	T = Tree(range(15))
	draw(T)

