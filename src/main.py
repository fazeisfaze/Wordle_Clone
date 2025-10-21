from signal import pause
import Board
import Keyboard
import Word

from flet import (Column, ControlEvent, KeyboardEvent, SnackBarBehavior,CrossAxisAlignment, OutlinedBorder, RoundedRectangleBorder, SnackBar, Text, Colors, Page, Divider, FontWeight)
import flet as ft
from asyncio import sleep

class Wordle(Column):
    def __init__(self):
        super().__init__(spacing=0)
        self.horizontal_alignment = CrossAxisAlignment.CENTER
        self.board = Board.Board()
        self.keyboard = Keyboard.Keyboard(self.on_control_event)
        self.wordle = Word.Word().getRandomizeWord()
        self.controls = [
            self.board,
            Divider(height=70, color="transparent"), 
            self.keyboard,
        ]

        self.snack_bar = SnackBar(
            content=Text(
                weight=FontWeight.W_900,
                size=20
            ),
            shape=RoundedRectangleBorder(5),
            bgcolor=Colors.RED_400,
            show_close_icon=True,
            duration=2000,
            behavior=SnackBarBehavior.FIXED
        )

    def did_mount(self):
        if not isinstance(self.page, Page):
            return None
        self.page.overlay.append(self.snack_bar)
        self.page.on_keyboard_event = self.on_keyboard_event
        self.page.update()
    def show_alert(self, ctx: str, color, duration = 2000):
        self.snack_bar.open = True
        self.snack_bar.content.value = ctx
        self.snack_bar.bgcolor =color
        self.snack_bar.duration = duration
        self.page.update()
    async def LogicProcess(self,key: str):
        if key.isalpha() and len(key) == 1:
            await self.board.add(key)
            self.board.update()
        elif key == "BACKSPACE":
            self.board.pop()
            self.board.update()
        elif key == "ENTER":
            if self.board.isFull():
                GuessWord = self.board.getGuessWord()
                if not Word.Word().isAWord(GuessWord):
                    self.show_alert("You must enter English word!", Colors.RED_400)
                    return
                listValidateColor = self.board.getValidateColor(self.wordle)
                self.board.setAnswerState(listValidateColor)
                self.keyboard.setAnswerState(listValidateColor)
                if (self.board.curX>= 6):
                    self.page.on_keyboard_event = None
                    if (GuessWord == self.wordle.lower()):
                        self.show_alert(("Congratulation!"),Colors.GREEN_400)
                    else:
                        self.show_alert("Correct Words: "+self.wordle, Colors.YELLOW_400)
                    await sleep(1.5)
                    self.page.on_keyboard_event = self.on_keyboard_event
                    self.wordle = Word.Word().getRandomizeWord()
                    self.board.reset()
                    self.keyboard.reset()

            else:
                self.show_alert("You must enter 5-letter word!",Colors.RED_400)

    async def on_control_event(self, e : ControlEvent):
        key =  e.control.content.value.upper() 
        if (key == "DEL"): key = "BACKSPACE"
        await self.LogicProcess((key))
    
    async def on_keyboard_event(self, e: KeyboardEvent):
        key = e.key.upper()
        await self.LogicProcess(key)

def main(page: Page):
    page.title = "Wordle"
    page.fonts= {
        "Franklin": "https/github.com/google/fonts/raw/main/apache/franklingothic/FranklinGothic-Medium.ttf"
    }
    page.theme = ft.Theme(font_family="Franklin")
    page.bgcolor ="#121213"
    page.window.min_width= 700
    page.window.min_height = 780
    page.window.max_height = 900
    page.window.max_width = 800
    page.window.resizable = True
    page.window.center()

    app = Wordle()

    page.add(app)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
