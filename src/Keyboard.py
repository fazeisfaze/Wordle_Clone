from flet import (Container, Column, Button, Control, Offset,Row, Card, Duration,AnimationCurve, Text, Colors, Page, Animation, alignment, border, padding)
import flet as ft
from typing import cast
CORRECT_COLOR = "#6AAA64" 
PRESENT_COLOR = "#C9B458"  
DEFAULT_COLOR = "#787C7E"  

KEY_CONTROLS = {}

class Keyboard(Container):
    def __init__(self, key_press_handler=None):
        super().__init__()
        
        self.key_states = {} 
        self.key_press_handler = key_press_handler

        self.keyboard_layout = [
            ["Q","W","E","R","T","Y","U","I","O","P"],
            ["A","S","D","F","G","H","J","K","L"], 
            ["ENTER","Z","X","C","V","B","N","M","DEL"]
        ]
        
        def create_key_button(text, key_width=52):
            if len(text) > 1: 
                key_width = 75 
            
            button = Container(
                data=text,
                width=key_width,
                height=58,
                bgcolor=DEFAULT_COLOR, # Initial color
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

        self.content = Column(
            controls=row_controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        )

    async def _handle_key_click(self, e):
            if self.key_press_handler:
                await self.key_press_handler(e)
    def setAnswerState(self,lst):
        for (boxColor, char) in lst:
            t = cast(Button,KEY_CONTROLS.get(char.lower()))
            if t.bgcolor == CORRECT_COLOR :continue
            t.bgcolor = boxColor
            t.update()
    def reset(self):
        for i in range(0,3):
            for char in self.keyboard_layout[i]:
                t = cast(Container, KEY_CONTROLS.get(char.lower()))
                t.bgcolor = DEFAULT_COLOR
                t.update()


