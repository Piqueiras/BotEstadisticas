import config
import database
import graphics
import highlighter

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
    database.increase_value(config.JSON_PATH, interaction.user.name, 60 * horas + minutos)
    await interaction.response.send_message(
        f"{interaction.user.display_name} ha estudiado `{horas} horas {minutos} minutos` \nTiene un total de {database.total_value(config.JSON_PATH,interaction.user.name)} minutos")

#FUNCION QUE MODIFICA
@tree.command(name="reset", description="PELIGRO: Reinicia todas tus estadísticas")
async def reset(interaction: discord.Interaction):
    database.delete_user(config.JSON_PATH,interaction.user.name)
    await interaction.response.send_message(
        f"{interaction.user.display_name} ahora tiene 0 horas de estudio")

#FUNCION QUE MODIFICA
@tree.command(name="deshacer", description="Borra tus estadísticas de hoy")
async def borrar(interaction: discord.Interaction):
    database.delete_day(config.JSON_PATH,interaction.user.name)
    await interaction.response.send_message(
        f"{interaction.user.display_name} ahora tiene 0 horas de estudio hoy")

@tree.command(name="total", description="Muestra el total de horas que has estudiado")
async def total(interaction: discord.Interaction):
    horas = database.total_value(config.JSON_PATH,interaction.user.name) // 60
    minutos = database.total_value(config.JSON_PATH,interaction.user.name) - horas * 60
    await interaction.response.send_message(
        f"{interaction.user.display_name} lleva estudiadas {horas} horas y {minutos} minutos"
    )

@tree.command(name="estadisticas", description="Muestra tus horas de estudio por día")
async def estadisticas(interaction: discord.Interaction):
    await interaction.response.send_message(
        database.user_stats(config.JSON_PATH,interaction.user.name))


@tree.command(name="mensualidad", description="Información detallada sobre tu estudio durante un mes")
@discord.app_commands.describe(ano="Año", mes="Mes (en número)")
async def mensualidad(interaction: discord.Interaction, ano: int, mes: int):
    mensaje = database.month_info(config.JSON_PATH,interaction.user.name, ano, mes)
    await interaction.response.send_message(mensaje)

@tree.command(name="podio", description="Grafica top estudios")
async def top_study_time(interaction: discord.Interaction):
    graphics.generate_leaderboard(config.JSON_PATH,"leaderboard.png")
    await interaction.response.send_message(file=discord.File("leaderboard.png"))
    
@tree.command(name="grafico", description="Grafico estudio por dia")
async def grafico(interaction: discord.Interaction):
    graphics.user_graph(interaction.user.name,config.JSON_PATH,interaction.user.name+".png")
    await interaction.response.send_message(file=discord.File(interaction.user.name+".png"))

@tree.command(name="racha",description="Calcula tu racha total")
async def racha(interaction: discord.Interaction):
    racha, fecha = database.consecutive_days(config.JSON_PATH,interaction.user.name)
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

color = {
    'rojo':1,
    'pistacho':2,
    'oro':3,
    'azul':4,
    'rosa':5,
    'cian':6,
    'blanco':7
}

formato = {
    'normal':0,
    'negrita':1,
    'subrayado':4
}

@tree.command(name="calendario",description="Muestra info de los días que has estudiado")
@discord.app_commands.describe(ano="Año")
async def calendario(interaction: discord.Interaction, ano: int):
    await interaction.response.send_message("```ansi\n"+highlighter.year_highlight(ano,
                                                                             database.user_yearly_dates(config.JSON_PATH,
                                                                                                        interaction.user.name,
                                                                                                        ano),
                                                                             f'\u001b[{formato["subrayado"]};3{color["oro"]}m',
                                                                             '\u001b[0m')+"```")
#Confia bro

keepAlive()
client.run(config.TOKEN)