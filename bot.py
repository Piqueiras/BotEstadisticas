import config
import database
import graphics

import discord
from discord import app_commands

from keepalive import keepAlive

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#FUNCION QUE MODIFICA
@tree.command(name="estudio", description="Registra tu tiempo de estudio hoy")
@discord.app_commands.describe(horas="Cuantas horas has estudiado?", minutos="Cuantos minutos has estudiado?")
async def estudio(interaction: discord.Interaction, horas: int, minutos: int):
    if horas<0 or minutos<0:
        await interaction.response.send_message("No se puede valores negativos. Para eliminar use /deshacer")
        return
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    database.increase_value(db, interaction.user.name, 60 * horas + minutos)
    await interaction.response.send_message(
        f"{interaction.user.display_name} ha estudiado `{horas} horas {minutos} minutos` \nTiene un total de {database.total_value(db,interaction.user.name)} minutos")
    database.write_json_file(config.JSON_PATH,db)

#FUNCION QUE MODIFICA
@tree.command(name="reset", description="PELIGRO: Reinicia todas tus estadísticas")
async def reset(interaction: discord.Interaction):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    database.delete_user(db,interaction.user.name)
    await interaction.response.send_message(
        f"{interaction.user.display_name} ahora tiene 0 horas de estudio")
    database.write_json_file(config.JSON_PATH,db)

#FUNCION QUE MODIFICA
@tree.command(name="deshacer", description="Borra tus estadísticas de hoy")
async def borrar(interaction: discord.Interaction):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    database.delete_day(db,interaction.user.name)
    await interaction.response.send_message(
        f"{interaction.user.display_name} ahora tiene 0 horas de estudio hoy")
    database.write_json_file(config.JSON_PATH,db)

@tree.command(name="total", description="Muestra el total de horas que has estudiado")
async def total(interaction: discord.Interaction):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    horas = database.total_value(db,interaction.user.name) // 60
    minutos = database.total_value(db,interaction.user.name) - horas * 60
    await interaction.response.send_message(
        f"{interaction.user.display_name} lleva estudiadas {horas} horas y {minutos} minutos"
    )

@tree.command(name="estadisticas", description="Muestra tus horas de estudio por día")
async def estadisticas(interaction: discord.Interaction):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    await interaction.response.send_message(
        database.user_stats(db,interaction.user.name))


@tree.command(name="mensualidad", description="Información detallada sobre tu estudio durante un mes")
@discord.app_commands.describe(ano="Año", mes="Mes (en número)")
async def mensualidad(interaction: discord.Interaction, ano: int, mes: int):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    mensaje = database.month_info(db,interaction.user.name, ano, mes)
    print(mensaje)
    await interaction.response.send_message(mensaje)

@tree.command(name="podio", description="Grafica top estudios")
async def top_study_time(interaction: discord.Interaction):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    graphics.generate_leaderboard(db,"leaderboard.png")
    await interaction.response.send_message(file=discord.File("leaderboard.png"))

@tree.command(name="racha",description="Calcula tu racha total")
async def racha(interaction: discord.Interaction):
    db : database.UserData = database.read_json_file(config.JSON_PATH)
    racha, fecha = database.consecutive_days(db,interaction.user.name)
    if racha is None:
        await interaction.response.send_message("Mejor estudia, ¿no?")
        return
    if racha == 0:
        await interaction.response.send_message("Hoy no has estudiado: no puedes tener racha!")
        return
    if racha == 1:
        await interaction.response.send_message("Hoy acabas de empezar tu racha")
        return
    
    await interaction.response.send_message(f"Llevas una racha de {racha} desde el dia {fecha}")
    

keepAlive()
client.run(config.TOKEN)