from flet import (Container, Column, Button, Control, Offset,Row, Card, Duration,AnimationCurve, Text, Colors, Page, Animation, alignment, border, padding)
import flet as ft
from typing import cast
CORRECT_COLOR = "#6AAA64"  # Green
PRESENT_COLOR = "#C9B458"  # Yellow
ABSENT_COLOR = "#787C7E"   # Dark Gray
DEFAULT_COLOR = "#D3D6DA"  # Light Gray (for light theme)

# Global dictionary to map character to its Flet control instance
KEY_CONTROLS = {}

class Keyboard(Container):
    def __init__(self, key_press_handler=None):
        super().__init__()
        
        self.key_states = {} 
        self.key_press_handler = key_press_handler

        # Key layout definition
        self.keyboard_layout = [
            ["Q","W","E","R","T","Y","U","I","O","P"],
            ["A","S","D","F","G","H","J","K","L"], 
            ["ENTER","Z","X","C","V","B","N","M","DEL"]
        ]

        # Function to create a single key Container
        def create_key_button(text, key_width=52):
            # Define width based on key type
            if len(text) > 1: # 'ENTER' or 'DEL'
                key_width = 75 
            
            button = Container(
                data=text,
                width=key_width,
                height=58,
                bgcolor=ABSENT_COLOR, # Initial color
                border_radius=ft.border_radius.all(4),
                alignment=alignment.center,
                on_click=self._handle_key_click,
                content=Text(
                    text,
                    color=Colors.WHITE,
                    size=20,
                    weight=ft.FontWeight.BOLD
                )
            )
            KEY_CONTROLS[text.lower()] = button
            return button

        row_controls = []
        row_controls.append(
            Row(
                controls=[create_key_button(c) for c in self.keyboard_layout[0]],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6
            )
        )
        row_controls.append(
            Row(
                controls=[create_key_button(c) for c in self.keyboard_layout[1]],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6
            )
        )
        row_controls.append(
            Row(
                controls=[create_key_button(c) for c in self.keyboard_layout[2]],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6
            )
        )

        # Set the content of the main Keyboard container
        self.content = Column(
            controls=row_controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6, # Spacing between keyboard rows
        )

    def _handle_key_click(self, e):
            if self.key_press_handler:
                self.key_press_handler(e.control.data)
    def setAnswerState(self,lst):
        for (boxColor, char) in lst:
            t = cast(Button,KEY_CONTROLS.get(char.lower()))
            t.bgcolor = boxColor
            t.update()


