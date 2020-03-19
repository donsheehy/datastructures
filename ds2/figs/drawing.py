from ds_viz.canvas import svg_plus_pdf
from ds_viz.datastructures import VizList, VizBST

def figpath(name):
    return '../figures/' + name

def drawbst(T, name):
    vizT = VizBST(T._root, (5,5))
    with svg_plus_pdf(600, vizT.height + 10, figpath(name)) as canvas:
        vizT.draw(canvas)

def drawlist(L, name):
    with svg_plus_pdf(600, 60, figpath(name)) as canvas:
        vizL = VizList(L)
        vizL.position = (5,5)
        vizL.draw(canvas)
