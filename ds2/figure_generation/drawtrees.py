from ds2.figure_generation.svghelper import SVGEngine
from ds2.orderedmapping.bstmapping import BSTMapping as Tree

from ds_viz.vizbst import drawtree as drawtocanvas
from ds_viz.gizehcanvas import Canvas

def drawtree(T, name, height = 200):
	canvas = Canvas(600, height)
	drawtocanvas(T, canvas)
	canvas.surface.write_to_png('figures/' + name + '.png')

def x(node, offset):
	nodewidth = 40
	lenleft = len(node.left) if node.left is not None else 0
	return nodewidth * (lenleft + 1) + offset

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
