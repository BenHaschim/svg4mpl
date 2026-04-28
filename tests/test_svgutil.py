import xml.etree.ElementTree as ET
from unittest.mock import patch
import pytest
import matplotlib.pyplot as plt

# Assuming the package is installed or the source is in the PYTHONPATH
from svg4mpl import svgutil as S

class TestUtilities:
    def test_mplunit(self):
        """Test physical unit to Matplotlib scale conversion."""
        # 1 cm = 10 mm, so they should evaluate to the exact same conversion
        cm_val = S.MplUnit('1cm')[0]
        mm_val = S.MplUnit('10mm')[0]
        assert pytest.approx(cm_val) == mm_val
        
        # Test multiple arguments
        tuple_val = S.MplUnit('10cm', '50mm')
        assert len(tuple_val) == 2
        assert tuple_val[0] == pytest.approx(tuple_val[1] * 2)

    def test_get_dict(self):
        """Test CSS style string parsing into dictionary."""
        style_str = "fill: red; stroke: black; stroke-width: 2"
        style_dict = S.get_dict(style_str)
        assert style_dict == {'fill': 'red', 'stroke': 'black', 'stroke-width': '2'}

    def test_get_color(self):
        """Test color format conversion."""
        # Tab colors
        assert S.get_color("tab:blue") == "#1f77b4"
        assert S.get_color("tab:red") == "#d62728"
        
        # RGB / RGBA Tuples
        assert S.get_color((1, 0, 0)) == "rgb(255,0,0)"
        assert S.get_color((0.5, 0.5, 0.5)) == "rgb(128,128,128)"
        assert S.get_color((1, 0, 0, 0.5)) == "rgba(255,0,0,0.5)"
        
        # Standard names should pass through unchanged
        assert S.get_color("black") == "black"


class TestPrimitives:
    def test_line(self):
        line = S.Line((0, 0), (10, 20), stroke="tab:blue")
        assert line.tag == "line"
        assert line.attrib["x1"] == "0"
        assert line.attrib["y2"] == "20"
        assert line.attrib["stroke"] == "#1f77b4"

    def test_rectangle(self):
        rect = S.Rectangle(pos=(5, 5), size=(20, 10))
        assert rect.tag == "rect"
        assert rect.attrib["x"] == "5"
        assert rect.attrib["width"] == "20"
        # Should contain default styles injected by get_color("none")
        assert "fill: none" in rect.attrib["style"]

    def test_circle(self):
        circle = S.Circle(cx=150, cy=100, r=20, fill="tab:green")
        assert circle.tag == "circle"
        assert circle.attrib["cx"] == "150"
        assert circle.attrib["r"] == "20"
        assert "fill: #2ca02c" in circle.attrib["style"]

    def test_label(self):
        label = S.Label("Important Point", pos=(50, 50), r=45, size=14)
        assert label.tag == "text"
        assert label.text == "Important Point"
        assert "translate(50, 50)" in label.attrib["transform"]
        assert "rotate(45)" in label.attrib["transform"]
        assert "font-size: 14" in label.attrib["style"]

    def test_path(self):
        path = S.Path(d="M 10 10 L 20 20", fill="black")
        assert path.tag == "{http://www.w3.org/2000/svg}path"
        assert path.attrib["d"] == "M 10 10 L 20 20"
        assert "fill: black" in path.attrib["style"]


class TestContainers:
    def test_panel(self):
        """Test the Panel function creates a proper <g> group."""
        circle = S.Circle(10, 10, 5)
        line = S.Line((0,0), (10,10))
        panel = S.Panel(circle, line, kwargs={'transform': 'translate(10, 10)'})
        
        assert panel.tag == "g"
        assert len(panel) == 2
        assert panel.attrib["transform"] == "translate(10, 10)"

    # We patch IPython.display because tests might run outside a Jupyter notebook
    @patch('IPython.display.display')
    @patch('IPython.display.SVG')
    def test_figure(self, mock_svg, mock_display):
        """Test the root Figure composition."""
        rect = S.Rectangle((0,0), (10,10))
        fig = S.Figure("10cm", "8cm", rect)
        
        # Figure returns an ElementTree, so get the root
        root = fig.getroot()
        assert root.tag == "svg"
        assert root.attrib["width"] == "10cm"
        assert root.attrib["height"] == "8cm"
        assert len(root) == 1
        assert root[0].tag == "rect"
        
        # Verify IPython's SVG preview was called
        mock_display.assert_called_once()
        mock_svg.assert_called_once()


class TestMplIntegration:
    def test_mplfigure(self):
        """Test that Matplotlib figures are successfully serialized into cleaned SVG groups."""
        # 1. Create a dummy matplotlib figure
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.plot([0, 1, 2], [10, 20, 15])
        ax.set_title("Test Plot")
        
        # 2. Pass to svg4mpl
        svg_group = S.MplFigure(fig)
        
        # Close the plot to avoid memory leaks during tests
        plt.close(fig)
        
        # 3. Assertions
        assert svg_group.tag == "g"
        
        # Ensure that problematic metadata tags were stripped
        for child in svg_group:
            assert child.tag != "{http://www.w3.org/2000/svg}metadata"
