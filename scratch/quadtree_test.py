import numpy as np

def create_segmentation_mask(width, height, rect_width, rect_height):
    mask = np.zeros((height, width), dtype=np.uint8)
    start_x = (width - rect_width) // 2
    start_y = (height - rect_height) // 2
    mask[start_y:start_y+rect_height, start_x:start_x+rect_width] = 1
    return mask

def build_quadtree(mask):
    def split_quadtree(mask, level=0):
        height, width = mask.shape
        if np.all(mask == mask[0, 0]):
            return str(int(mask[0, 0]))
        
        mid_x, mid_y = width // 2, height // 2
        quadtree = {}
        quadtree['tl'] = split_quadtree(mask[:mid_y, :mid_x], level+1)
        quadtree['tr'] = split_quadtree(mask[:mid_y, mid_x:], level+1)
        quadtree['bl'] = split_quadtree(mask[mid_y:, :mid_x], level+1)
        quadtree['br'] = split_quadtree(mask[mid_y:, mid_x:], level+1)
        return quadtree
        # return f"({', '.join(quadtree)})"

    return split_quadtree(mask)

def print_quadtree(quadtree):
    stack = [(quadtree, 0, "root")]
    while stack:
        node, level, label = stack.pop()
        print(f"Level {level}")
        print(f"Node: {node}")
        print(f"Label: {label}")
        indent = '  ' * level
        if len(node) == 1:
            print(f"{indent}{label}: {node}")
        else:
            print(f"{indent}{label}: (")
            mid_x, mid_y = 128 // (2 ** level), 128 // (2 ** level)
            print(f"{indent}  Midpoint: ({mid_x}, {mid_y})")
            # subtrees = node[1:-1].split(', ')
            stack.append((node['br'], level+1, "Bottom-right"))
            stack.append((node['bl'], level+1, "Bottom-left"))
            stack.append((node['tr'], level+1, "Top-right"))
            stack.append((node['tl'], level+1, "Top-left"))
            print(f"{indent})")

# Create a segmentation mask
mask = create_segmentation_mask(128, 128, 50, 50)

# Build the quadtree representation
quadtree = build_quadtree(mask)

# visualize segmentation mask using matplotlib
import matplotlib.pyplot as plt
plt.imshow(mask, cmap='gray')
plt.show()

# Print the quadtree in a human-readable format
# print_quadtree(quadtree)
print(quadtree)