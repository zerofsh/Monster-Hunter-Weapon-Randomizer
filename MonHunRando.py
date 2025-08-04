import tkinter as tk
import random
import math
from typing import Dict, List, Tuple

class SpinningWheel:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MONSTER HUNTER WEAPON WHEEL")
        self.root.resizable(False, False)
        
        # Set dark grey background for main window
        self.root.configure(bg='#333333')
        
        # Configuration constants
        self.CANVAS_SIZE = (1000, 700)
        self.WHEEL_RADIUS = 200
        self.COLORS = ["#e460ff", "#ffdc3f", "#85ff4c", "#603cff",
                      "#fc528a", "#6bd0ff", "#ffaa49", "#b44252",
                      "#41f586", "#9c61fc", "#609efa", "#dd3939", "#73b185", "#ff7c10"]
        self.OPTIONS = ["SnS", "GS", "LS", "DB", "HH", 
                       "GL", "SA", "IG", "CB", "LBG", "HBG","LNC","BOW","HMR"]
        
        # Custom messages for each weapon
        self.WEAPON_MESSAGES = {
            "SnS": "Hyaaaaa!",
            "GS": "I charged and I missed ... So I charged again ... and then I missed again ...",
            "LS": "So cool so weeb so master of I-Frames!",
            "DB": "Spin to win babyyy!!!",
            "HH": "Tooting your flute has never been more helpful!",
            "GL": "Explosive poking & slashing",
            "SA": "It do be switching",
            "IG": "Je suis monté - Pardon",
            "CB": "Too many braincells required gl",
            "LBG": "...pew pew?!",
            "HBG": "... explosive pew pew!",
            "LNC": "Go get em with your tickles!",
            "BOW": "And we say bye bye stamina",
            "HMR": "Bonk!"
        }
        
        self.current_rotation = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize all UI components with dark theme"""
        # Create canvas with dark grey background
        self.canvas = tk.Canvas(self.root, width=self.CANVAS_SIZE[0], 
                              height=self.CANVAS_SIZE[1], bg='#333333',
                              highlightthickness=0)
        self.canvas.pack()
        
        self.wheel_center = (self.CANVAS_SIZE[0]//2, self.CANVAS_SIZE[1]//2 - 50)
        self.setup_wheel()
        self.setup_labels()
        self.setup_pointer()
        self.setup_controls()
    
    def setup_wheel(self):
        """Create the wheel with colored segments"""
        coord = (self.wheel_center[0]-self.WHEEL_RADIUS, 
                self.wheel_center[1]-self.WHEEL_RADIUS,
                self.wheel_center[0]+self.WHEEL_RADIUS, 
                self.wheel_center[1]+self.WHEEL_RADIUS)
        
        segment_angle = 360 / len(self.OPTIONS)
        
        # Changed outline to light grey (#eeeeee)
        self.segments = [
            self.canvas.create_arc(coord, start=i*segment_angle, extent=segment_angle, 
                                  fill=self.COLORS[i], outline='#eeeeee', width=2)  # Light grey outline
            for i in range(len(self.OPTIONS))
        ]
        
        # Center circle with light grey outline
        self.canvas.create_oval(
            self.wheel_center[0]-25, self.wheel_center[1]-25,
            self.wheel_center[0]+25, self.wheel_center[1]+25,
            fill='#222222', outline='#eeeeee', width=2
        )
    
    def setup_labels(self):
        """Create labels with color blocks outside the wheel"""
        block_size = 25
        weapons_per_side = (len(self.OPTIONS) // 2)
        weapons_per_side += 1 if len(self.OPTIONS) % 2 != 0 else 0
        
        for i, (text, color) in enumerate(zip(self.OPTIONS, self.COLORS)):
            # Position calculation
            side = 'left' if i < weapons_per_side else 'right'
            x_pos = 0.15 if side == 'left' else 0.85
            y_pos = 0.3 + (i % weapons_per_side) * (0.6/weapons_per_side)
            
            # Color block with light grey outline
            block_x = self.CANVAS_SIZE[0] * x_pos
            block_y = self.CANVAS_SIZE[1] * y_pos
            offset = block_size + 5
            
            if side == 'right':
                self.canvas.create_rectangle(
                    block_x - offset, block_y - block_size//2,
                    block_x - 5, block_y + block_size//2,
                    fill=color, outline='#eeeeee', width=2  # Light grey outline
                )
                anchor, x_offset = 'e', -offset-10
            else:
                self.canvas.create_rectangle(
                    block_x + 5, block_y - block_size//2,
                    block_x + offset, block_y + block_size//2,
                    fill=color, outline='#eeeeee', width=2  # Light grey outline
                )
                anchor, x_offset = 'w', offset+10
            
            # Text label with dark background
            label = tk.Label(self.canvas, text=text, bg='#333333', 
                           fg='white', font=("Arial", 10, "bold"))
            label.place(relx=x_pos, rely=y_pos, anchor=anchor, x=x_offset)
    
    def setup_pointer(self):
        """Create the pointer at the top of the wheel"""
        pointer_pos = (self.wheel_center[0], 
                      self.wheel_center[1] - self.WHEEL_RADIUS - 20)
        self.canvas.create_polygon(
            pointer_pos[0]-20, pointer_pos[1]+40,
            pointer_pos[0]+20, pointer_pos[1]+40,
            pointer_pos[0], pointer_pos[1],
            fill='#222222', outline="#eeeeee", width=2  # Light grey outline
        )
    
    def setup_controls(self):
        """Create spin button and winner display with dark theme"""
        self.spin_btn = tk.Button(
            self.root, text="SPIN!", command=self.spin,
            bg='#444444', fg='white', font=("Arial", 16, "bold"),
            padx=40, pady=15, bd=0, highlightbackground='#333333',
            activebackground='#555555', activeforeground='white'
        )
        self.spin_btn.place(relx=0.5, rely=0.85, anchor="center")
        
        # Create two labels - one for the weapon, one for the message
        self.weapon_text = tk.Label(
            self.root, text="", bg='#333333', fg='white',
            font=("Arial", 14, "bold")
        )
        self.weapon_text.place(relx=0.5, rely=0.9, anchor="center")
        
        self.message_text = tk.Label(
            self.root, text="", bg='#333333', fg='#aaaaaa',  # Lighter grey for message
            font=("Arial", 12)
        )
        self.message_text.place(relx=0.5, rely=0.94, anchor="center")
    
    def get_winner_index(self) -> int:
        """Calculate which segment is under the pointer"""
        segment_angle = 360 / len(self.OPTIONS)
        pointer_angle = (360 - self.current_rotation + 90) % 360
        return int(pointer_angle // segment_angle) % len(self.OPTIONS)
    
    def rotate(self, speed: float = 15):
        """Rotate the wheel by specified speed"""
        self.current_rotation = (self.current_rotation + speed) % 360
        segment_angle = 360 / len(self.OPTIONS)
        for i, segment in enumerate(self.segments):
            self.canvas.itemconfig(segment, start=(i * segment_angle + self.current_rotation) % 360)
        self.root.update()
    
    def spin(self):
        """Handle the spinning animation"""
        self.current_rotation = random.randint(0, 360)
        self.weapon_text.config(text="Spinning...")
        self.message_text.config(text="")
        self.spin_btn.config(state=tk.DISABLED)
        
        # Fast spin
        for _ in range(20):
            self.rotate(speed=15)
            self.root.after(30)
        
        # Slow down
        for i in range(30):
            self.rotate(speed=15 - i*0.4)
            self.root.after(50 + i*5)
        
        # Show winner
        self.root.after(500, self.show_winner)
    
    def show_winner(self):
        """Display the winning weapon and its custom message"""
        winner_index = self.get_winner_index()
        weapon = self.OPTIONS[winner_index]
        message = self.WEAPON_MESSAGES.get(weapon, "")
        
        self.weapon_text.config(text=f"Your Weapon: {weapon}")
        self.message_text.config(text=message)
        self.spin_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpinningWheel(root)
    root.mainloop()
