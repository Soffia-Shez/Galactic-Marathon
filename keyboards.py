from pyrogram.types import KeyboardButton
from pyrogram.types import ReplyKeyboardMarkup
from pyrogram import emoji

boton_info = KeyboardButton(f'{emoji.INFORMATION}Info')
boton_game = KeyboardButton (f'{emoji.VIDEO_GAME}Juego')
boton_perfil = KeyboardButton(f'{emoji.MONKEY_FACE}Perfil')

boton_piedra_papel_o_tijera = KeyboardButton(f'{emoji.ROCK}Piedra, papel, tijera')
boton_aventura = KeyboardButton(f'{emoji.WOMAN_DANCING}Aventura')
boton_volver = KeyboardButton(f'{emoji.BLUE_CIRCLE}Volver')

boton_piedra = KeyboardButton (f'{emoji.ROCK}Piedra')
boton_papel = KeyboardButton (f'{emoji.NEWSPAPER}Papel')
boton_tijera = KeyboardButton(f'{emoji.SCISSORS}Tijera')
boton_back = KeyboardButton (f'{emoji.BACK_ARROW}Volver')

kb_main =ReplyKeyboardMarkup(
    keyboard= [
        [boton_info,boton_perfil, boton_game]
    ],
    resize_keyboard=True
)

juegos_disponibles = ReplyKeyboardMarkup(
    keyboard=[
        [boton_piedra_papel_o_tijera],
        [boton_aventura, boton_volver]
    ],
    resize_keyboard=True
)

Juego_piedra = ReplyKeyboardMarkup (
    keyboard=[
        [boton_piedra],
        [boton_papel, boton_tijera],
        [boton_back]
    ],
    resize_keyboard= True
)
