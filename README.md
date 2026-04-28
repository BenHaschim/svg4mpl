# svg4mpl

A lightweight, zero-dependency Python tool to arrange Matplotlib figures into SVG layouts. Perfect for **Typst** workflows.

## Features
- **Pure Python**: No dependencies beyond the standard library.
- **Functional**: No complex classes; just pass your figures and coordinates.
- **Typst Ready**: Optimized SVG output for seamless inclusion in Typst documents.

## Usage
```python
import matplotlib.pyplot as plt
import svg4mpl

fig, ax = plt.subplots()
ax.plot([1, 2], [1, 2])

# Minimalist functional approach
svg4mpl.compose(fig, x=0, y=0, output="final_figure.svg")
```

Do you have the **core function code** ready, or would you like me to help write the **SVG string-manipulation logic** to handle the merging?
