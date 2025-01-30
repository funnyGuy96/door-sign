import pygame
import socketio
import sys
from datetime import datetime
import requests

# Initialize Pygame and screen
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Digital Door Sign')

# Colors and Fonts - Make sure WHITE is pure white
BG_COLOR = (26, 26, 26)
WHITE = (255, 255, 255)  # Pure white for maximum visibility
time_font = pygame.font.Font(None, 48)
date_font = pygame.font.Font(None, 48)
status_font = pygame.font.Font(None, 120)
description_font = pygame.font.Font(None, 40)

# Global variables
current_status = None
current_description = None

# Initialize SocketIO
sio = socketio.Client()
SERVER_URL = 'http://localhost:5000'

def create_rounded_surface(width, height, radius, color):
    """Create a surface with rounded corners"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, width, height)
    
    # Main rectangle
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    return surface

def draw_display():
    global screen, current_status, current_description
    
    # Clear screen
    screen.fill(BG_COLOR)
    
    # Draw time and date in pure white
    now = datetime.now()
    time_text = time_font.render(now.strftime("%H:%M:%S"), True, WHITE)
    date_text = date_font.render(now.strftime("%d.%m.%Y"), True, WHITE)
    
    screen.blit(time_text, (20, 20))
    screen.blit(date_text, (580, 20))
    
    # Only draw status if it exists
    if current_status:
        # Convert color
        color = current_status['color']
        if isinstance(color, str) and color.startswith('#'):
            color = color.lstrip('#')
            color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
        # Create status text in pure white
        status_text = status_font.render(current_status['name'], True, WHITE)
        
        # Create background with padding
        padding = 60
        bg_width = status_text.get_width() + padding * 2
        bg_height = status_text.get_height() + padding * 2
        
        # Create rounded background
        status_bg = create_rounded_surface(bg_width, bg_height, 30, color)  # Increased radius to 30
        
        # Add white text to background
        text_rect = status_text.get_rect(center=(bg_width/2, bg_height/2))
        status_bg.blit(status_text, text_rect)
        
        # Position on screen
        bg_rect = status_bg.get_rect(center=(400, 240))
        screen.blit(status_bg, bg_rect)
        
        # Draw description in pure white
        if current_description:
            desc_text = description_font.render(current_description, True, WHITE)
            desc_rect = desc_text.get_rect(center=(400, bg_rect.bottom + 40))
            screen.blit(desc_text, desc_rect)
    else:
        # Draw "No Status" message in pure white
        no_status_text = description_font.render("No Status Set", True, WHITE)
        no_status_rect = no_status_text.get_rect(center=(400, 240))
        screen.blit(no_status_text, no_status_rect)
    
    pygame.display.flip()

@sio.event
def connect():
    print('Connected to server')
    # Get initial status
    try:
        response = requests.get(f'{SERVER_URL}/api/current_status')
        if response.status_code == 200:
            data = response.json()
            global current_status, current_description
            current_status = data['status']
            current_description = data['description']
            draw_display()
    except Exception as e:
        print(f"Error getting initial status: {e}")

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('status_update')
def on_status_update(data):
    global current_status, current_description
    current_status = data['status']
    current_description = data['description']
    draw_display()

def main():
    try:
        # Connect to server
        print("Connecting to server...")
        sio.connect(SERVER_URL)
        print("Connected!")

        # Main loop
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            draw_display()
            clock.tick(1)  # Update every second
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if sio.connected:
            sio.disconnect()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main() 