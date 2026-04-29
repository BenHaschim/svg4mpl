# svg4mpl

A lightweight, functional Python utility to compose and arrange Matplotlib figures alongside standard SVG elements (shapes, text, paths) into a single, cohesive SVG layout.

Perfect for creating complex figure panels for academic papers, specifically optimized for seamless inclusion in **Typst** documents.

### Features
* **Pure Python:** Minimal overhead using Python's built-in `xml.etree.ElementTree`.
* **Functional API:** No complex classes or object-oriented boilerplate; just pass your figures and coordinates into intuitive functions.
* **Typst Ready:** Automatically strips problematic `<metadata>` and redundant style tags from Matplotlib SVGs, ensuring clean output for Typst and other modern typesetting systems.
* **Jupyter Integration:** Automatically renders previews of your SVG compositions directly within Jupyter Notebooks.

### Installation
Install directly via pip:

    pip install svg4mpl
  
Alternatively, you can install the latest development version directly from git:

    pip install git+https://github.com/BenHaschim/svg4mpl.git

*Note: While `svg4mpl` aims for minimal dependencies, it is designed to be used alongside `matplotlib` in an `IPython`/Jupyter environment.*

### Quick Start
Instead of wrestling with Matplotlib's complex layout engines (like `GridSpec`) to mix shapes, annotations, and plots, you can generate your plots individually and compose them using `svg4mpl`.
```python
import matplotlib.pyplot as plt
from svg4mpl import svgutil as S

# 1. Create a basic Matplotlib figure using physical units
# S.MplUnit converts human-readable strings into Matplotlib's expected inch tuple
fig, ax = plt.subplots(figsize=S.MplUnit('10cm', '8cm'))
ax.plot([0, 1, 2], [10, 20, 15], marker='o', color='tab:blue')
ax.set_title("Matplotlib Plot")
plt.close(fig) # Prevent duplicate display in Jupyter

# 2. Compose the SVG layout
composition = S.Figure(
    "10cm", "8cm",
    # Group elements into a Panel to apply collective transformations
    S.Panel(
        # Inject the Matplotlib figure
        S.MplFigure(fig),
        
        # Overlay standard SVG shapes and text
        S.Circle(cx=150, cy=100, r=20, stroke='red', style='stroke-width:2'),
        S.Label("Important Point", pos=(175, 105), size=14, color='red'),
        
        # Translate the entire panel
        kwargs={'transform': 'translate(10, -10)'}
    ),
    
    # Add a border or background element
    S.Rectangle(pos=(5, 5), size=(370, 290), stroke='black', style='fill:none; stroke-dasharray:5')
)

# 3. Save the final result to an SVG file
composition.write("simple_composition.svg")
```
### Core API
All layout functions are located in `svg4mpl.svgutil`. They return standard `xml.etree.ElementTree` elements, making them highly hackable.

### Containers
* `Figure(width, height, *children, kwargs)`: The root `<svg>` container. Returns an `ElementTree` object which can be saved via `.write(filename)`.
* `Panel(*children, style="", kwargs)`: Creates an SVG group (`<g>`), perfect for grouping plots and annotations so they can be translated or scaled together.

### Imports
* `MplFigure(fig, style="", kwargs)`: Takes a Matplotlib `Figure` object, renders it to SVG in memory, cleans up the XML, and returns it as a group element.
* `SVGFigure(filename, style="", kwargs)`: Loads an external SVG file and prepares it for inclusion in the layout.

### Primitives
Draw standard vector graphics right on top of your plots.
* `Line(pos1, pos2, stroke, width, ...)`
* `Rectangle(pos, size, fill, stroke, ...)`
* `Circle(cx, cy, r, fill, stroke, ...)`
* `Label(text, pos, r, size, color, ...)`
* `Path(d, filename, fill, stroke, ...)`

### Utilities
* `MplUnit(*args)`: Pass in `'10cm'` or `'5mm'` to convert physical dimensions into the inch-based numbers expected by Matplotlib's figsize.
* `get_color(color)`: Supports `rgb()`, standard named colors, and Matplotlib's tab: color palette (e.g., `tab:blue`).
* `save_pdf(svg_filename, pdf_filename, font_name="Aptos", font_path=None)`:

    *Note: You can take outputted SVG file and pipe it through the `typst compile` CLI tool to generate a PDF. (Requires Typst to be installed on your system). If you prefer to do this directly from your command line or within a Jupyter Notebook cell using shell commands, you can use the following syntax:*

    ```
    ! echo '#set page(height:auto,width:auto,margin:0cm);#set text(font: "Aptos");#image("simple_composition.svg")' | typst compile --font-path "M:/My Fonts/" - "simple_composition.pdf"
    ```

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
