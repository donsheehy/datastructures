import svgwrite

DEFAULTS = {"stroke_width" : "3", "stroke" : "black",
            "fill" : "white", "fill_opacity" : "1",
            "font_size" : "36pt"}

class SVGEngine():
    def __init__(self, width, height):
        self.size = (width,height)
        self.svg_doc = svgwrite.Drawing(None,self.size)

    def __str__(self):
        return self.svg_doc.tostring()

    def save(self, filename):
        self.svg_doc.save()

    def getSVG(self):
        return self.svg_doc

    #SHAPE CONSTRUCTION
    def _add_defaults(self, **kwargs):
        #adds design defaults to kwargs of draw methods when not specified
        for kwarg, default in DEFAULTS.items():
            if kwarg not in kwargs:
                kwargs[kwarg] = default
        return kwargs

    def draw_circle(self, center, radius = 50, **kwargs):
        kwargs = self._add_defaults(**kwargs)
        circle = self.svg_doc.circle(center, r = radius, **kwargs)
        self.svg_doc.add(circle)

    def draw_line(self, start, end, **kwargs):
        kwargs = self._add_defaults(**kwargs)
        line = self.svg_doc.line(start, end, **kwargs)
        self.svg_doc.add(line)

    def draw_rect(self, left_upper_corner, width=50, height=50, **kwargs):
        kwargs = self._add_defaults(**kwargs)
        rect = self.svg_doc.rect(insert=left_upper_corner, size=(width,height), **kwargs)
        self.svg_doc.add(rect)

    def draw_rect_center(self, center, width=50, height=50, **kwargs):
        left_upper_x = center[0] - width/2
        left_upper_y = center[1] - height/2
        corner = (left_upper_x, left_upper_y)
        rect = self.draw_rect(self, corner, width, height, **kwargs)
        self.svg_doc.add(rect)

    def draw_rounded_rect(self, left_upper_corner, width=50, height=50, rx=5, ry=5, **kwargs):
        kwargs = self._add_defaults(**kwargs)
        rect = self.svg_doc.rect(insert=left_upper_corner,
                                 size=(width,height),
                                 rx=rx,
                                 ry=ry,
                                 **kwargs)
        self.svg_doc.add(rect)

    def draw_ellipse(self, center, rx=75, ry=50, **kwargs):
        kwargs = self._add_defaults(**kwargs)
        ellipse = self.svg_doc.ellipse(center, r=(rx,ry), **kwargs)
        self.svg_doc.add(ellipse)

    def draw_text_default(self, text, left_lower_corner, **kwargs):
        """text defined by upper left corner point"""

        kwargs = self._add_defaults(**kwargs)
        text = self.svg_doc.text(text, left_lower_corner, **kwargs)
        self.svg_doc.add(text)

    def draw_text_center(self, text, center, **kwargs):
        """text defined by center point"""

        kwargs = self._add_defaults(**kwargs)
        text = self.svg_doc.text(text, center, text_anchor="middle", dominant_baseline="central", **kwargs)
        #note: some image viewers don't recognize the dominant_baseline attribute  dominant_baseline="central",
        self.svg_doc.add(text)

    def draw_arrow(self, start, end, **kwargs):
        """ See http://vanseodesign.com/web-design/svg-markers/ for more info on drawing arrowheads"""

        kwargs = self._add_defaults(**kwargs)
        arrow_marker = self.svg_doc.marker(id="arrow", insert=(1,3), size=(9,6),
                                           orient="auto", markerUnits="strokeWidth", viewBox="0 0 10 10")
        arrow_marker.add(self.svg_doc.path(d="M0,0 L0,6 L9,3 z", fill=kwargs["stroke"]))
        self.svg_doc.add(arrow_marker)
        arrow = self.svg_doc.line(start, end, marker_end=arrow_marker.get_funciri(), **kwargs)
        self.svg_doc.add(arrow)

    def draw_pointer(self, start, end, **kwargs):
        #TODO: implement pointer drawing
        self.draw_arrow(start, end, **kwargs)
#TODO: pointer start dots, regular polygons, text along a line

if __name__ == '__main__':
    textstyle = {'fill': 'black', 'stroke_width': 0, 'font_size': '24pt'}
    s = SVGEngine(300, 300)
    s.draw_line((10,10), (200,250), **{'class':'theline'})
    s.draw_circle((160, 118), 70)
    s.draw_text_center("It's text!", (160,125), **textstyle)
    print(s)
