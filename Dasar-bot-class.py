import discord
import requests
import random
import os
import asyncio
import detect
from discord.ext import commands
from bot_logic import gen_pass
from logic_poke import Pokemon
from detect_objects import detect
# from model import get_class


description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# command prefix 
bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})') # type: ignore
    print('------')

# adding two numbers
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def minus(ctx, left: int, right: int):
    await ctx.send(left - right)

@bot.command()
async def times(ctx, left: int, right: int):
    await ctx.send(left * right)


@bot.command()
async def div(ctx, left: int, right: int):
    await ctx.send(left / right)

# spamming word
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        
# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if num == 1:
        await ctx.send('It is Head!')
    if num == 2:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1,6)
    if nums == 1:
        await ctx.send('It is 1!')
    elif nums == 2:
        await ctx.send('It is 2!')
    elif nums == 3:
        await ctx.send('It is 3!')
    elif nums == 4:
        await ctx.send('It is 4!')
    elif nums == 5:
        await ctx.send('It is 5!')
    elif nums == 6:
        await ctx.send("it is 6!")
    elif nums == 7:
        await ctx.send("it is !")
    elif nums == 8:
        await ctx.send("it is 8!")
    elif nums == 9:
        await ctx.send("it is 9!")
    elif nums == 10:
        await ctx.send("it is 10!")
    
@bot.command()
async def mem(ctx):
     # try by your self 2 min
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
 
    await ctx.send(file=picture)

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}') # type: ignore
    # provide what you can help here


# overwriting kalimat.txt

@bot.command()

async def tulis(ctx, *, my_string: str):

    with open('kalimat.txt', 'w', encoding='utf-8') as t:

        text = ""

        text += my_string

        t.write(text)

# append kalimat.txt

@bot.command()

async def tambahkan(ctx, *, my_string: str):

    with open('kalimat.txt', 'a', encoding='utf-8') as t:

        text = "\n"

        text += my_string

        t.write(text)

# reading kalimat.txt

@bot.command()

async def baca(ctx):

    with open('kalimat.txt', 'r', encoding='utf-8') as t:

        document = t.read()

        await ctx.send(document)

# random local meme image

@bot.command()

async def meme(ctx):

    img_name = random.choice(os.listdir('meme'))

    with open(f'meme/{img_name}', 'rb') as f:

    # with open(f'meme/enemies-meme.jpg', 'rb') as f:

        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!

        picture = discord.File(f)

    await ctx.send(file=picture)

# API to get random dog and duck image 
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('dog')
async def dog(ctx):
    '''Setiap kali permintaan dog (anjing) dipanggil, program memanggil fungsi get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Setiap kali permintaan duck (bebek) dipanggil, program memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

# The '$go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    # if author not in Pokemon.pokemons.keys():
    pokemon = Pokemon(author)  # Creating a new Pokémon
    await ctx.send(await pokemon.info())  # Sending information about the Pokémon
    image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
    if image_url:
        embed = discord.Embed()  # Creating an embed message
        embed.set_image(url=image_url)  # Setting up the Pokémon's image
        await ctx.send(embed=embed)  # Sending an embedded message with an image
    else:
        await ctx.send("Failed to upload an image of the pokémon.")

#show local drive    
@bot.command()
async def local_drive(ctx):
    try:
      folder_path = "./files"  # Replace with the actual folder path
      files = os.listdir(folder_path)
      file_list = "\n".join(files)
      await ctx.send(f"Files in the files folder:\n{file_list}")
    except FileNotFoundError:
      await ctx.send("Folder not found.")
#show local file
@bot.command()
async def showfile(ctx, filename):
  """Sends a file as an attachment."""
  folder_path = "./files/"
  file_path = os.path.join(folder_path, filename)
  try:
    await ctx.send(file=discord.File(file_path))
  except FileNotFoundError:
    await ctx.send(f"File '{filename}' not found.")
# upload file to local computer
@bot.command()
async def simpan(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            # file_url = attachment.url  IF URL
            await attachment.save(f"./files/{file_name}")
            await ctx.send(f"Menyimpan {file_name}")
    else:
        await ctx.send("Anda lupa mengunggah :(")
        

# Intents are needed to handle events like member joining, etc.
intents = discord.Intents.default()
intents.message_content = True

@bot.command()
async def impossible(ctx):
    number_to_guess = random.randint(1, 100)
    attempts_left = 10  
    await ctx.send("Game Dimulai! Pilih nomor 1 - 100 😆😆. kamu punya 10 percobaan.")

    # Start a loop to keep asking for guesses
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    while attempts_left > 0:
    
        guess_msg = await bot.wait_for('message', check=check)
        

        try:
            guess = int(guess_msg.content)
        except ValueError:
            await ctx.send("pilih nomor 1 sampai 100.")
            continue
        
        
        if guess < 1 or guess > 100:
            await ctx.send("pilih antara 1 dan 100.")
            continue

        if guess == number_to_guess:
            await ctx.send(f"WIHHH BENERRRR {number_to_guess} NOMOR YANG BENARR🎉")
            return  

        elif guess < number_to_guess:
            attempts_left -= 1
            await ctx.send(f"kurang banyak percobaan sisa {attempts_left} lagi.")
        
        elif guess > number_to_guess:
            attempts_left -= 1
            await ctx.send(f"kebanyakan percoban sisa {attempts_left} lagi.")
        
        if attempts_left == 0:
            await ctx.send(f"HAHAH KLAHHHH NOMORNYA ITU  {number_to_guess}. jangan coba coba lagi")
            return  

# Tic-Tac-Toe Game class
class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [" " for _ in range(9)]  # 3x3 board
        self.players = [player1, player2]  # Player1 is 'X' and Player2 is 'O'
        self.turn = 0  # Player 1 starts
        self.game_over = False

    def print_board(self):
        return f"""```
     {self.board[0]} | {self.board[1]} | {self.board[2]}
    -----------
     {self.board[3]} | {self.board[4]} | {self.board[5]}
    -----------
     {self.board[6]} | {self.board[7]} | {self.board[8]}
    ```"""

    def make_move(self, position):
        if self.board[position] == " " and not self.game_over:
            self.board[position] = 'X' if self.turn % 2 == 0 else 'O'
            self.turn += 1
            return True
        return False

    def check_win(self):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " ":
                self.game_over = True
                return self.board[condition[0]]  # Return winner ('X' or 'O')
        if " " not in self.board:
            self.game_over = True
            return "Tie"
        return None

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.turn = 0
        self.game_over = False

# Command to start a new game
@bot.command(name="tictactoe")
async def tictactoe(ctx, opponent: discord.Member):
    if ctx.author == opponent:
        await ctx.send("You cannot play with yourself!")
        return
    
    game = TicTacToe(ctx.author, opponent)
    
    # Send a message with the initial board
    msg = await ctx.send(f"Game started! {ctx.author.mention} (X) vs {opponent.mention} (O)\n{game.print_board()}\n")
    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    await msg.add_reaction('3️⃣')
    await msg.add_reaction('4️⃣')
    await msg.add_reaction('5️⃣')
    await msg.add_reaction('6️⃣')
    await msg.add_reaction('7️⃣')
    await msg.add_reaction('8️⃣')
    await msg.add_reaction('9️⃣')

    def check(reaction, user):
        return user in [ctx.author, opponent] and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    
    # Start the game loop
    while not game.game_over:
        reaction, user = await bot.wait_for('reaction_add', check=check)

        
        # Get the index of the board from the emoji
        position = int(str(reaction.emoji)[0]) - 1
        if game.make_move(position):
            await msg.edit(content=f"{game.print_board()}\nIt's {game.players[game.turn % 2].mention}'s turn!")

            # Check if there's a winner
            winner = game.check_win()
            if winner:
                if winner == "Tie":
                    await msg.edit(content=f"{game.print_board()}\nThe game is a tie!")
                else:
                    winner = game.players[(game.turn - 1) % 2].mention
                    await msg.edit(content=f"{game.print_board()}\n{winner} wins!")

        else:
            await ctx.send(f"{user.mention}, invalid move! Please try again.")
    
    # Wait a bit before deleting the reactions
    await asyncio.sleep(10)
    await msg.clear_reactions()

choices = ["rock", "paper", "scissors"]

@bot.command()
async def rps(ctx):
    await ctx.send("Ketik salah satu: `rock`, `paper`, atau `scissors`.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in choices

    try:
        msg = await bot.wait_for('message', check=check, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.send("Waktu habis! Coba lagi.")
        return

    user_choice = msg.content.lower()
    bot_choice = random.choice(choices)

    if user_choice == bot_choice:
        result = "Seri!"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result = "Hoki aja bangga"
    else:
        result = "WLEEE SKILL ISSSUEEEE 😆😆"

    await ctx.send(f"Kamu memilih **{user_choice}**.\nBot memilih **{bot_choice}**.\n**{result}**")



#Computer Vision Deteksi objek
@bot.command()
async def deteksi(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            #file_url = attachment.url IF URL
            await attachment.save(f"./CV/{file_name}")
            await ctx.send(detect(input_image=f"./CV/{file_name}", output_image=f"./CV/{file_name}", model_path="yolov3.pt"))
            with open(f'CV/{file_name}', 'rb') as f:
                picture = discord.File(f)
            await ctx.send(file=picture)
    else:
        await ctx.send("Anda lupa mengunggah gambar :(")
