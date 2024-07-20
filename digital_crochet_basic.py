import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Crochet parameters
num_layers = 1
layer_index = 0
layer_stitches = [8]  # Default number of stitches per layer
stitch_type = ['dc']  # Default stitch type ('dc': double crochet)

# Calculate dimensions for drawing
radius = 20  # Radius of each stitch circle
circle_distance = 40  # Distance between circles
start_x = SCREEN_WIDTH // 2
start_y = SCREEN_HEIGHT // 2

# Initialize Pygame font and load JetBrains Mono font
pygame.font.init()
font_path = "JetBrainsMono-Light.ttf"  # Replace with your actual path to the font file
font = pygame.font.Font(font_path, 18)  # Use size 18 for lighter weight

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Crochet Doily Simulator')

# Function to draw crochet pattern and text
def draw_crochet_pattern():
    screen.fill(WHITE)
    for layer_idx in range(num_layers):
        for stitch_idx in range(layer_stitches[layer_idx]):
            angle = (2 * stitch_idx * math.pi / layer_stitches[layer_idx]) + (layer_idx * math.pi / num_layers)
            x = start_x + layer_idx * circle_distance * math.cos(angle)
            y = start_y + layer_idx * circle_distance * math.sin(angle)
            if stitch_type[layer_idx] == 'dc':
                rect = pygame.Rect(int(x) - radius // 2, int(y) - radius // 2, radius, radius)
                pygame.draw.rect(screen, BLACK, rect, 1)  # Outline only
            elif stitch_type[layer_idx] == 'ch':
                pygame.draw.circle(screen, BLACK, (int(x), int(y)), radius // 2, 1)  # Outline only
            elif stitch_type[layer_idx] == 'sc':
                pygame.draw.circle(screen, BLACK, (int(x), int(y)), radius // 2)  # Full black circle
            elif stitch_type[layer_idx] == 'hdc':
                rect = pygame.Rect(int(x) - radius // 2, int(y) - radius // 2, radius, radius)
                pygame.draw.rect(screen, BLACK, rect)  # Full black rectangle
    
    # Display text
    text_layers = font.render(f'Layers: {num_layers}', True, BLACK)
    text_stitches = font.render(f'Stitches: {layer_stitches[layer_index]}', True, BLACK)
    text_stitch_type = font.render(f'Stitch Type: {stitch_type[layer_index]}', True, BLACK)
    screen.blit(text_layers, (10, 10))
    screen.blit(text_stitches, (10, 30))
    screen.blit(text_stitch_type, (10, 50))
    
    pygame.display.flip()

# Initial draw
draw_crochet_pattern()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move to the next layer or create a new layer if at the last layer
                if layer_index >= num_layers - 1:
                    num_layers += 1
                    layer_stitches.append(8)  # Default number of stitches for new layer
                    stitch_type.append('dc')  # Default stitch type for new layer
                layer_index = min(layer_index + 1, num_layers - 1)
            elif event.key == pygame.K_DOWN:
                # Remove the current layer if it's not the last layer
                if num_layers > 1:
                    num_layers -= 1
                    layer_stitches.pop(layer_index)
                    stitch_type.pop(layer_index)
                    layer_index = min(layer_index, num_layers - 1)
            elif event.key == pygame.K_RIGHT:
                # Increase number of stitches in the current layer
                if layer_index < num_layers:
                    layer_stitches[layer_index] = min(layer_stitches[layer_index] + 1, 20)  # Limit max stitches
            elif event.key == pygame.K_LEFT:
                # Decrease number of stitches in the current layer
                if layer_index < num_layers:
                    layer_stitches[layer_index] = max(layer_stitches[layer_index] - 1, 1)  # Ensure min one stitch
            elif event.key == pygame.K_SPACE:
                # Change stitch type for the current layer
                if layer_index < num_layers:
                    if stitch_type[layer_index] == 'dc':
                        stitch_type[layer_index] = 'ch'  # Change to chain stitch (ch)
                    elif stitch_type[layer_index] == 'ch':
                        stitch_type[layer_index] = 'sc'  # Change to single crochet (sc)
                    elif stitch_type[layer_index] == 'sc':
                        stitch_type[layer_index] = 'hdc'  # Change to half double crochet (hdc)
                    elif stitch_type[layer_index] == 'hdc':
                        stitch_type[layer_index] = 'dc'  # Change back to double crochet (dc)
    
    # Redraw the crochet pattern and text based on updated parameters
    draw_crochet_pattern()
