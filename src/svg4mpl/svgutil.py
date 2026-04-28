
import xml.etree.ElementTree as ET

#__all__ = []



def MplUnit(*args):
    inch_convert = {
        'cm': 1/254*100,
        'mm': 1/254*1000,
    }
    rv = []
    for s in args:
        s = str(s)
        unit = ''.join(filter(str.isalpha, s)).strip()
        number = s.replace(unit, '')
        rv+= [eval(number)*inch_convert.get(unit,1)*(96 / 72)]

    return tuple(rv)

def get_dict(style, separator=';'):
    style = {v[0].strip():v[1].strip() for v in [w.split(':') for w in style.split(separator) if ':' in w]}
    return style

def get_color(color):
    COLORS = {
        "tab:blue": "#1f77b4",
        "tab:orange": "#ff7f0e",
        "tab:green": "#2ca02c",
        "tab:red": "#d62728",
        "tab:purple": "#9467bd",
        "tab:lightblue": "#aec7e8",
        "tab:lightorange": "#ffbb78",
        "tab:lightgreen": "#98df8a",
        "tab:lightred": "#ff9896",
        "tab:lightpurple": "#c5b0d5",
        }
    if color in COLORS:
        color = COLORS[color]
    if isinstance(color, tuple):
        if len(color)==3 or color[3]==1:
            color = f"rgb({','.join([str(round(v*255)) for v in color[:3]])})"
        else:
            color = f"rgba({','.join([str(round(v*255)) for v in color[:3]])},{color[3]})"

    return color

def Figure(width, height, *args, kwargs=None):

    if kwargs is None:
        kwargs = {}

    attrib = {
        #"xmlns": "http://www.w3.org/2000/svg",
        #"xmlns:xlink": "http://www.w3.org/2000/svg",
        "width": f"{width}",
        "height": f"{height}",
    }

    # Merge default attributes with any extra keyword attributes
    root = ET.Element("svg", {**attrib, **kwargs})
    #root.append(ET.Element("def", {}))
    # Append any provided child elements
    for child in args:
        root.append(child)

    # Return an ElementTree rooted at <svg>...</svg>

    from IPython.display import SVG as svg_display, display
    display(svg_display(data=ET.tostring(root, encoding="unicode")))
    return ET.ElementTree(root)

def Panel(*args, style="", kwargs=None):
    if kwargs is None:
        kwargs = {}

    attrib = {}
    # Build style with optional translation
    
    if style:
        attrib["style"] = style

    # Create <g> element with merged attributes
    g = ET.Element("g", {**attrib, **kwargs})

    # Append children
    for child in args:
        g.append(child)

    return g

def MplFigure(fig, style="", kwargs=None):
    import io
    style = {        
        } | get_dict(style)
    style = "; ".join([f"{k}: {v}" for k, v in style.items()])
    if kwargs is None:
        kwargs = {}
        if style:
            kwargs = {'style':style} | kwargs
    buf = io.BytesIO()
    fig.savefig(buf, format="svg", transparent=True)
    svg_string = buf.getvalue().decode('utf-8')
    element = ET.fromstring(svg_string)
    buf.close()
    for child in element:
        if any([
            child.tag == "{http://www.w3.org/2000/svg}metadata",
            child.tag == "{http://www.w3.org/2000/svg}defs" and child[0].text == """*{stroke-linejoin: round; stroke-linecap: butt}"""            
            ]):
            element.remove(child)
    for text_elem_sel in ['text','tspan']:
        for text_elem in element.findall(f'.//svg:{text_elem_sel}', {'svg': 'http://www.w3.org/2000/svg'}):
            new_style_str = get_dict(text_elem.get('style', ''))
            if 'font-family' in new_style_str:
                del new_style_str['font-family']
                new_style_str = "; ".join([f"{k}: {v}" for k, v in new_style_str.items()])
                text_elem.set('style', new_style_str)



    element.tag = 'g'
    #element.attrib = {'transform':'scale(1.3333333333)'}|kwargs
    element.attrib = kwargs
    return element

def SVGFigure(filename,style="",kwargs=None):
    if kwargs is None:
        kwargs = {}
    #rv = ET.Element('g', kwargs)
    #rv.append(ET.parse(filename).getroot())
    rv = ET.parse(filename).getroot()
    rv.tag = 'g'
    rv.attrib = kwargs
    return rv

def Line(pos1,pos2,stroke="black",width=1,style="",kwargs=None):
    attrib = {"x1": f"{pos1[0]}","y1": f"{pos1[1]}", "x2":f"{pos2[0]}", "y2":f"{pos2[1]}",
        "stroke":get_color(stroke),}
    if style:
        attrib["style"] = style
    if kwargs is None:
        kwargs = {}    
    rv = ET.Element('line', attrib|kwargs)
    return rv

def Rectangle(pos,size,fill="none",stroke="none",style="",kwargs=None):
    if kwargs is None:
        kwargs = {}
    style = {        
        'fill': get_color(fill),
        'stroke': get_color(stroke),
        } | get_dict(style)
    style = "; ".join([f"{k}: {v}" for k, v in style.items()])
    return ET.Element('rect', {"x": f"{pos[0]}","y": f"{pos[1]}", "width":f"{size[0]}", "height":f"{size[1]}", "style": style}|kwargs )

def Circle(cx,cy,r,fill="none",stroke="none",style="",kwargs=None):
    if kwargs is None:
        kwargs = {}
    style = {        
        'fill': get_color(fill),
        'stroke': get_color(stroke),
        } | get_dict(style)
    style = "; ".join([f"{k}: {v}" for k, v in style.items()])
    return ET.Element('circle', {"cx": f"{cx}","cy": f"{cy}","r": f"{r}", "style": style})

def Label(text,pos=None,r=0,size=12,color="black",style="",kwargs=None):
    if pos is None:
        pos = (0,0)
    if kwargs is None:
        kwargs = {}
    attrib = {"transform": f"translate({pos[0]}, {pos[1]}) rotate({r})"}
    style = {        
        'font-size': f"{size}",
        'fill': get_color(color),
        } | get_dict(style)
    style = "; ".join([f"{k}: {v}" for k, v in style.items()])
    attrib|= attrib|{"style":style}
    rv = ET.Element('text', attrib|kwargs)
    if isinstance(text, list):
        for sub_text in text:
            if isinstance(sub_text, tuple):
                sub_text, kwargs = sub_text
                tspan = ET.Element('tspan', kwargs)
            else:
                tspan = ET.Element('tspan')
            tspan.text = (sub_text)
            rv.append(tspan)
    else:
        rv.text = text
    return rv

def Path(d="",filename=None,fill="none",stroke="none",style="",kwargs=None):
    if kwargs is None:
        kwargs = {}
    #attrib = {"style": f"transform:scale({s[0]},{s[1]}) translate({pos1[0]}pt, {pos1[1]}pt); fill:none;stroke:{get_color(color)};stroke-width:{3}pt;"}
    style = {
        'fill': get_color(fill),
        'stroke': get_color(stroke),
        } | get_dict(style)
    style = "; ".join([f"{k}: {v}" for k, v in style.items()])
    attrib = {}
    attrib["style"] = style
    if filename != None:
        with open(f'{filename}','r') as f:
            attrib|= {"d":f.read()}
    else:
        attrib|= {"d":d}
    return ET.Element('{http://www.w3.org/2000/svg}path', attrib|kwargs)


def Defination(*args):
    rv = ET.Element("defs")
    for child in args:
        rv.append(child)
    return rv

def Marker(id,*args,kwargs):
    attrib = {}
    attrib['id'] = id
    rv = ET.Element("marker", attrib|kwargs)
    for child in args:
        rv.append(child)
    return rv



def ClipPath(id, *args, kwargs=None):
    if kwargs is None:
        kwargs = {}

    attrib = {}
    attrib['id'] = id
    rv = ET.Element("clipPath", attrib|kwargs)
    for child in args:
        rv.append(child)
    return rv


def Clip(*args, rect=None, style="", kwargs=None):
    if kwargs is None:
        kwargs = {}

    attrib = {}
    # Build style with optional translation
    
    if style:
        attrib["style"] = style

    # Create <g> element with merged attributes
    rv = ET.Element("g", {**attrib, **kwargs})
    kwargs2={}

    if rect is not None:
        rv.append(Defination( ClipPath(rect[0], Rectangle(rect[1],rect[2]), ), ),)
        kwargs2={'clip-path':f"url(#{rect[0]})",'transform':f"translate({-rect[1][0]}, {-rect[1][1]})"}
    g = ET.Element("g", kwargs2)

    # Append children
    for child in args:
        g.append(child)
    
    rv.append(g)

    return rv



ET.register_namespace("", "http://www.w3.org/2000/svg")       # default namespace
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")  # explicit prefix
