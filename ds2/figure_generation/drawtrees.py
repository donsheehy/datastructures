from svghelper import SVGEngine
from bstmapping import BSTMapping as Tree

# def draw_line(x1, y1, x2, y2):
# 	canvas.set_line_width(3)
# 	canvas.draw_line(x1, y1, x2, y2)
#
# def draw_circle(x, y, r):
# 	canvas.set_line_width(3)
# 	canvas.set_stroke_color(0, 0, 0)
# 	canvas.set_fill_color(255,255,255)
# 	canvas.fill_ellipse(x - r, y - r, 2 * r, 2 * r)
# 	canvas.draw_ellipse(x - r, y - r, 2 * r, 2 * r)

def x(node, offset):
	nodewidth = 40
	lenleft = len(node.left) if node.left is not None else 0
	return nodewidth * (lenleft + 1) + offset

# def draw_label(s, x, y):
# 	fs = 30
# 	fnt = 'Helvetica-Bold'
# 	w, h = canvas.get_text_size(str(s), fnt, fs)
# 	canvas.set_fill_color(0,0,0)
# 	canvas.draw_text(str(s), x - w / 2, y - h / 2, fnt, fs)

textstyle = {"stroke_width" : "0", "stroke" : "black",
            "fill" : "black", "fill_opacity" : "1",
            "font_size" : "20pt"}

def draw(T, height=200):
	canvas = SVGEngine(500, height)
	if isinstance(T, Tree): T = T._root
	drawsubtree(canvas, T, 0, 20)
	print(canvas)

def drawsubtree(engine, T, xoffset, yoffset):
	if T is None: return
	radius = 18
	levelheight = 50
	a,b = x(T, xoffset), yoffset
	c = yoffset + levelheight
	if T.left is not None and len(T.left) > 0:
		engine.draw_line((a, b), (x(T.left, xoffset), c))
		drawsubtree(engine, T.left, xoffset, c)
	if T.right is not None and len(T.right) > 0:
		engine.draw_line((a, b), (x(T.right, a), c))
		drawsubtree(engine, T.right, a, c)
	engine.draw_circle((a, b), radius)
	engine.draw_text_center(T.key, (a, b), **textstyle)


if __name__ == '__main__':
	T = Tree()
	for i in range(15):
		T[i] = None
	draw(T)
