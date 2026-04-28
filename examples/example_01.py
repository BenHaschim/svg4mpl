import matplotlib.pyplot as plt
from svg4mpl import svgutil as S

# 1. Create a basic Matplotlib figure using physical units (10cm x 8cm)
# S.MplUnit converts these strings into the inch-based tuple Matplotlib expects
fig, ax = plt.subplots(figsize=S.MplUnit('10cm', '8cm'))
ax.plot([0, 1, 2], [10, 20, 15], marker='o', color='tab:blue')
ax.set_title("Matplotlib Plot")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Value (units)")
plt.close(fig) # We don't need to show it via plt.show()

# 2. Compose the SVG layout
# S.Figure(width, height, *children)
composition = S.Figure("10cm", "8cm",
    # A panel to group elements and apply transformations
    S.Panel(
        # Convert the Matplotlib figure to an SVG group
        S.MplFigure(fig),
        
        # Add a simple SVG shape on top (e.g., a highlight circle)
        S.Circle(cx=150, cy=100, r=20, stroke='red', style='stroke-width:2'),
        
        # Add a label
        S.Label("Important Point", pos=(175, 105), size=14, color='red'),
        
        # Shift everything in this panel
        kwargs={'transform': 'translate(10, -10)'}
    ),
    
    # Add a simple rectangle as a border or background element
    S.Rectangle(pos=(5, 5), size=(370, 290), stroke='black', style='fill:none; stroke-dasharray:5')
)

# 3. Save the final result to an SVG file
composition.write("simple_composition.svg")

print("SVG successfully saved to simple_composition.svg")
