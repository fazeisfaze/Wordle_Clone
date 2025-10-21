
from flet import (Alignment, Border, BorderSide, Container, Column, Control, CrossAxisAlignment, MainAxisAlignment, Offset,Row, Card, Duration,AnimationCurve, Stack, Text, Colors, Page, Animation, alignment, border, padding,FontWeight)
import flet as ft
from flet.core.alignment import center
from typing import Counter, Dict, Tuple, cast,List
from asyncio import sleep
import Word 

TEXT_COLOR = "#F8F8F8"
BG_ABSENT = "#3A3A3C"
BG_RIGHT = "#538D4E"
BG_MISPLACE ="#B59F3B"
BORDER_COLOR = "#3A3A3C"
ACTIVE_BORDER_COLOR ="#565758" 

BOARD_DICT: Dict[Tuple[int,int] | int, Container | Row]= {}
class Board(Container):
    def __init__(self):
        self.curX= 0
        self.curY= -1
        super().__init__()
        def createAnsBox():

             return Stack(
              controls= [
                    Container(
                        
                        width= 70,
                        height=70,
                        alignment=alignment.center,
                        border=border.all(3,BORDER_COLOR),
                        content= Text(
                            visible=False,
                            weight=FontWeight.W_700,
                            size = 30,
                            color=TEXT_COLOR,
                        ),
                        animate_scale= Animation(200, AnimationCurve.EASE_OUT)
            
            )

            ]
        )
        col = Column(
           horizontal_alignment=CrossAxisAlignment.CENTER, 
           spacing=8
        ); 
        for i in range(0, 6):
            row_control = ft.Row(
                spacing=8, # Can reintroduce simple spacing
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[createAnsBox() for j in range(0, 5)]
            )
            # Store the INNER Container (stack.controls[0]) for animation access
            for j, stack in enumerate(row_control.controls):
                BOARD_DICT[(i, j)] = stack.controls[0] 
            col.controls.append(row_control)
        self.alignment = alignment.center    
        self.width = 500
        self.content = col
    async def add(self, data: str):
        if self.curY >= 4:
            return None # Row is full, ignore the input
        self.curY+=1
        tile_container = BOARD_DICT[(self.curX, self.curY)]
        tile_container.border = border.all(3,ACTIVE_BORDER_COLOR)
        if not isinstance(tile_container.content, Text):
            return None
        text_control: Text = tile_container.content
        text_control.value = data.upper() # Wordle uses uppercase
        text_control.visible = True
        await self.bounce_tile(self.curX, self.curY)
        

    def pop(self):
        if self.curY <0 :
            return None
        if (self.curY >= 5):
            self.curY = 4
        tile_container = BOARD_DICT[(self.curX, self.curY)]
        if not isinstance(tile_container.content, Text):
            return None
        text_control: Text = tile_container.content
        text_control.value = "" # Wordle uses uppercase
        text_control.visible = False
        tile_container.border = border.all(3,BORDER_COLOR)
        self.curY-=1;

    async def bounce_tile(self, r, c):
        tile_container = cast(ft.Container, BOARD_DICT.get((r, c)))

        if not tile_container:
            return

        BOUNCE_SCALE = 1.15  # Grow to 115% of the size
        ORIGINAL_SCALE = 1.0 
        
        tile_container.scale = BOUNCE_SCALE
        tile_container.update()
        await sleep(0.1) 
        
        tile_container.animate_scale = ft.Animation(
            duration=300,
            curve=ft.AnimationCurve.ELASTIC_OUT # Use ELASTIC_OUT for the springy effect
        )
        
        tile_container.scale = ORIGINAL_SCALE
        tile_container.update()
        
        await sleep(0.3)
    def isFull(self)->bool:
        return not(self.curY >= -1 and self.curY <= 3)
    def getGuess(self):
        res =""
        for i in range(0,5):
            t = cast(Container,BOARD_DICT.get((self.curX,i)))
            if not isinstance(t.content,Text):
                return
            res = res + t.content.value
        return res

    def getGuessWord(self):
        (_,guess_tile_data) = self.getCurrentLine()
        return "".join(guess_tile_data).lower()
    def setAnswerState(self,lst):
       (guess_tile,_) = self.getCurrentLine()
       for cnt, t in enumerate(guess_tile):
            (boxColor,_) = lst[cnt]
            t.border = border.all(0.1, boxColor)
            t.bgcolor = boxColor
            t.update()
       self.curX+=1
       self.curY =-1

    def getCurrentLine(self)->Tuple[List[Container], List[str]]:
        guess_tile = []
        guess_tile_data = []
        for i in range(0,5):
            t = cast(Container,BOARD_DICT.get((self.curX,i)))
            if not isinstance(t.content,Text):
                return ([],[])
            guess_tile.append(t)
            guess_tile_data.append((t.content.value))
        return (guess_tile, guess_tile_data)

    def getValidateColor(self, answer:str):

        answer_chars: list[str|None] = list(answer)
        (guess_tile, guess_tile_data) = self.getCurrentLine()
        colors = [""] * 5
        for i in range(0,5):
            if (guess_tile_data[i] == answer[i]):
                colors[i] = BG_RIGHT
                answer_chars[i] = None
        for i in range(0,5):
            if (colors[i] == BG_RIGHT) :
                continue
            if guess_tile_data[i] in answer_chars:
                colors[i] = BG_MISPLACE
            else:
                colors[i] = BG_ABSENT
        res:list[tuple[str,str]] = []
        for cnt,t in enumerate(guess_tile_data):
            res.append((colors[cnt],t))
        return res
    def reset(self):
        for i in range(0,6):
             for j in range(0,5):
                    t = cast(Container,BOARD_DICT.get((i,j)))
                    if not isinstance(t.content,Text):
                        return ([],[])
                    t.content.visible = False
                    t.bgcolor = Colors.TRANSPARENT
                    t.border =border.all(3,BORDER_COLOR)
                    t.update()

        self.curX = 0
        self.curY = -1
            


        

