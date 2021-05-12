import discord
import config
import mysql.connector

client = discord.Client()
TOKEN = config.token()
INDELAYTITLE = config.indelayTitle()
INDELAYDESCRIPTION = config.indelayDescription()
INDELAYFOOTER = config.indelayFooter()
INDELAYFOOTERURL = config.indelayFooterURL()
TAKEPOINTSTITLE = config.takepointsTitle()
TAKEPOINTSDESCRIPTION = config.takepointsDescription()
TAKEPOINTSFOOTER = config.takepointsFooter()
TAKEPOINTSFOOTERURL = config.takepointsFooterURL()
DELAY = config.delay()
ATRIBUTOS = config.atributos()
HOST = config.host()
USER = config.user()
PASSWORD = config.password()
DATABASE = config.database()
PERMISSIONS = config.getPermissions()

mydb = mysql.connector.connect(
  host=HOST,
  user=USER,
  password=PASSWORD,
  database=DATABASE
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS PONTOS(USUARIO VARCHAR(255), QUANTIA INT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS ATRIBUTOS(USUARIO VARCHAR(255))")
for x in ATRIBUTOS:
    mycursor.execute("ALTER TABLE ATRIBUTOS ADD IF NOT EXISTS {} INT NOT NULL".format(x))

def inserirUser(user,quantia):
    sql = "INSERT INTO PONTOS (USUARIO, QUANTIA) VALUES (%s, %s)"
    val = (user, int(quantia))
    mycursor.execute(sql, val)

    mydb.commit()

def getUser(user):
    sql_select_query = "SELECT * FROM PONTOS WHERE USUARIO = %s"
    mycursor.execute(sql_select_query, (user,))
    record = mycursor.fetchall()

    for row in record:
        return row[1]

def hasUser(user):
    seleciona = "SELECT USUARIO FROM PONTOS WHERE USUARIO ='{}'".format(user)
    mycursor.execute(seleciona)
    resultado = mycursor.fetchall()
    if len(resultado)==0:
        inserirUser(user, 0)

def addPontos(user,quantia):
    sql = "UPDATE PONTOS SET QUANTIA = %s WHERE USUARIO = %s"
    val = (int(quantia),user)

    mycursor.execute(sql, val)

    mydb.commit()

def removePontos(user,quantia):
    sql = "UPDATE PONTOS SET QUANTIA = %s WHERE USUARIO = %s"
    val = (int(quantia),user)

    mycursor.execute(sql, val)

    mydb.commit()

def inserirUserAtributo(user):
    sql = "INSERT INTO ATRIBUTOS (USUARIO) VALUES (%s)"
    val = ((user,))
    mycursor.execute(sql, val)

    mydb.commit()

def getUserAtributo(user,atributo):
    sql_select_query = "SELECT {} FROM ATRIBUTOS WHERE USUARIO = %s".format(atributo)
    mycursor.execute(sql_select_query, (user,))
    record = mycursor.fetchall()

    for x in record:
        return x

def hasUserAtributo(user):
    seleciona = "SELECT USUARIO FROM ATRIBUTOS WHERE USUARIO ='{}'".format(user)
    mycursor.execute(seleciona)
    resultado = mycursor.fetchall()
    if len(resultado)==0:
        inserirUserAtributo(user)

def addAtributo(user,atributo,quantia):
    sql = "UPDATE ATRIBUTOS SET {} = %s WHERE USUARIO = %s".format(atributo)
    val = (int(quantia),user)

    mycursor.execute(sql, val)

    mydb.commit()

@client.event
async def on_ready():
    global inDelay
    inDelay = ['']
    print('Bot inicializado com sucesso!')

@client.event
async def on_message(msg):

    if msg.content.lower().startswith('!pontos'):

        if msg.author.top_role.name in PERMISSIONS:
            message = msg.content.split(' ')
            if len(message) != 4:
                embed = discord.Embed(
                    title="Digite '!pontos <adicionar/tirar> <quantia> <user>"
                )
                await msg.channel.send(embed=embed)
                return   

            if message[1].lower() == 'tirar':
                quantia = int(getUser(message[2])) - int(message[3]) 
                removePontos(message[2], quantia)
                embed = discord.Embed(
                    title="Você tirou {} pontos do usuário {}".format(message[3], message[2])
                )
                await msg.channel.send(embed=embed)
            if message[1].lower() == 'adicionar':
                quantia = int(getUser(message[2])) + int(message[3]) 
                removePontos(message[2], quantia)
                embed = discord.Embed(
                    title="Você adicionou {} pontos ao usuário {}".format(message[3], message[2])
                )
                await msg.channel.send(embed=embed)
    if msg.content.lower().startswith('!ss'):
        message = msg.content.split(' ')
        if len(message) != 3:
            embed = discord.Embed(
                title="Digite '!ss <atributo> <quantia>"
            )
            await msg.channel.send(embed=embed)
            return
        if message[1] in ATRIBUTOS:
            if int(getUser(msg.author.name)) >= int(message[2]):
                hasUserAtributo(msg.author.name)
                get = str(getUserAtributo(msg.author.name, message[1].lower()))
                quantia = int(get.replace("(", "").replace(",)", "")) + int(message[2])
                addAtributo(msg.author.name, message[1], quantia)
                rmPontos = int(getUser(msg.author.name)) - int(message[2])
                removePontos(msg.author.name, rmPontos)
                embed = discord.Embed(
                    title="Você adicionou {} pontos ao atributo de {}".format(message[2],message[1])
                )
                await msg.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Você não possui pontos o suficiente."
                )
                await msg.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Atributo inválido!"
            )
            await msg.channel.send(embed=embed)

    if msg.content.lower() == '!treinar':
        if msg.author.name in inDelay:
            embed = discord.Embed(
                title=INDELAYTITLE,
                description=INDELAYDESCRIPTION
            )
            embed.set_footer(text=INDELAYFOOTER, icon_url=INDELAYFOOTERURL)
            await msg.channel.send(embed=embed)
            return
        inDelay.append(msg.author.name)
        embed = discord.Embed(
            title=TAKEPOINTSTITLE,
            description=TAKEPOINTSDESCRIPTION
        )
        embed.set_footer(text=TAKEPOINTSFOOTER, icon_url=TAKEPOINTSFOOTERURL)
        await msg.channel.send(embed=embed)
        hasUser(msg.author.name)
        quantia = getUser(msg.author.name) + 2
        addPontos(msg.author.name,quantia)
        try:
            await client.wait_for('asdasdfsadasdsad',check=None,timeout=DELAY)
        except:
            inDelay.remove(msg.author.name)


client.run(TOKEN)