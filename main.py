from pyrogram import Client, filters
import config
import keyboards
import datetime
import random

date_time = datetime.datetime.now()
date_time = datetime.datetime.now()

def button_filter (button):
  async def func(_, __, msg):
    return msg.text == button.text
  return filters.create(func, "ButtonFilter", button = button)

bot_raquel = Client(
    api_id = config.API_ID,
    api_hash = config.API_HASH,
    bot_token= config.BOT_TOKEN,
    name= "Rraquel_madeinMedellin_bot"
)


@bot_raquel.on_message(filters.command("start"))
async def start(bot_raquel, message):
    await message.reply("¡Bienvenido! Le saluda Raquel.",
                        reply_markup=keyboards.kb_main)

@bot_raquel.on_message(filters.command("sticker"))
async def sticker (bot_raquel, message):
    await bot_raquel.send_sticker(message.chat.id, "CAACAgIAAxkBAAEOsJhoSyxRin5bCMoqTdIU-U7Ur5NNuQAC4AMAAkcVaAnD2anUyhq1azYE")

@bot_raquel.on_message(filters.command("info") | button_filter(keyboards.boton_info))
async def info (bot_raquel, message):
    await message.reply("Los comandos que hasta el momento se encuentran disponibles son: 1. /start 2. /sticker 3. /info 4. /time")

@bot_raquel.on_message(filters.command("time"))
async def time (bot_raquel, message):
    await message.reply("Hora:")
    await message.reply(date_time.time())
    await message.reply("Fecha:")
    await message.reply(date_time.date())

@bot_raquel.on_message (filters.command("game") | button_filter(keyboards.boton_game))
async def game_on (bot_raquel, message):
    await message.reply("Juegos para su elección:",
                        reply_markup=keyboards.juegos_disponibles)

@bot_raquel.on_message (filters.command("PPT") | button_filter(keyboards.boton_piedra_papel_o_tijera))
async def PPT (bot_raquel, message):
    await message.reply("Su turno",
                        reply_markup=keyboards.Juego_piedra)

@bot_raquel.on_message(button_filter(keyboards.boton_piedra) |
                       (keyboards.boton_papel) |
                       (keyboards.boton_tijera) |
                       (keyboards.boton_back)
                       )
async def choice_ppp (bot_raquel, message):
    piedra = keyboards.boton_piedra.text
    papel = keyboards.boton_papel.text
    tijera = keyboards.boton_tijera.text
    usuario = message.text
    computador = random.choice ([piedra, papel, tijera])
    await message.reply (f'Mi elección: {computador}')
    if usuario == computador:
     await message.reply ("Es un empate.")
    elif (usuario == piedra and computador == tijera) or (usuario == tijera and computador == papel) or (usuario == papel and computador == piedra):

        await message.reply ("Has ganado.")

    else:
        await message.reply ("Gané Jajaja")


@bot_raquel.on_message(filters.text) #filters.text hace que se tome solamente los mensajes con texto.
async def echo(client, message):
    texto_del_usuario = message.text.lower()
    if texto_del_usuario== "hola":
        await message.reply("¡Hola, me da mucho gusto leerte!") # message.reply le dice al bot que responda al mensaje con...
    elif texto_del_usuario== "chao" or texto_del_usuario == "bye":
        await message.reply("Hasta la próxima, ten un lindo día.")
    else:
            await message.reply(f"Escribiste: {message.text}")



print("Raquel se ha inicializado...")
bot_raquel.run()
