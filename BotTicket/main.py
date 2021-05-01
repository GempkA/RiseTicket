import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print("Bot iniciado!")
    print('Nome: {}'.format(client.user.name))
    print('ID: {}'.format(client.user.id))

    for canal in client.get_all_channels():

        if 'ticket-' in canal.name:
            await canal.delete(reason=None)

        if canal.name == 'ticket':

            await canal.purge(limit=10)

            embed = discord.Embed(
                title='TICKET',
                description='Clique na reação abaixo para abrir um ticket'
            )

            embed.set_footer(text='Atenciosamente, Equipe Teste',icon_url="https://i.imgur.com/uZIlRnK.png")

            message = await canal.send(embed=embed)
            await message.add_reaction('💖')

@client.event
async def on_reaction_add(reaction, user):

    msg = reaction.message

    if user != client.user:

        if reaction.emoji == '😀' and msg.channel.name == 'ticket-{}'.format(user.name).lower():
            await msg.channel.delete(reason=None)
            print('Canal {} deletado com sucesso!'.format(msg.channel.name))

        if reaction.emoji == '💖' and msg.channel.name == 'ticket':
            await msg.remove_reaction('💖', user)

            samechannel = ''
            for canal in client.get_all_channels():
                if canal.name == 'ticket-{}'.format(user.name).lower():
                    samechannel = canal.name

            if samechannel != 'ticket-{}'.format(user.name).lower():
                channel = await msg.guild.create_text_channel('ticket-{}'.format(user.name))
                print('Canal {} criado com sucesso!'.format(channel.name))
                embed = discord.Embed(
                    title='Olá, {}!'.format(user.name),
                    description='Digite aqui as suas dúvidas, que um membro da nossa staff irá atender-lhe o mais rápido possível!'
                )

                embed.set_footer(text='Atenciosamente, Equipe Teste', icon_url="https://i.imgur.com/uZIlRnK.png")
                message = await channel.send(embed=embed)
                await message.add_reaction('😀')

