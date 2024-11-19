import discord
from datetime import datetime, timedelta
import os
import csv
import runpy
from PIL import Image, ImageDraw, ImageFont
import io

my_secret = os.getenv('bottoken')
TOKEN = None
if my_secret:
    TOKEN = my_secret.strip()
    if TOKEN.startswith("“") and TOKEN.endswith("”"):
        TOKEN = TOKEN[1:-1]
    print("Bot token successfully retrieved.")
else:
    print("Bot token not found in the environment variables!")

csv_file_path = '/home/runner/Viva-Discord-Bot/Statistics/users.csv'
banned_words_file_path = '/home/runner/Viva-Discord-Bot/Moderation/bannedList.csv'


def initialize_csv():
    """Ensures the CSV file exists, creating it if necessary."""
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    if not os.path.isfile(csv_file_path):

        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Name', 'UserID', 'Position', 'Matches Played', 'Goals',
                'Assists', 'goalsConceded', 'Saves', 'Passes', 'Interceptions',
                'Tackles'
            ])
        print("CSV file initialized successfully.")
    else:
        print("CSV file already exists.")


def load_banned_words():
    """Load banned words from the CSV file."""
    banned_words = []
    if os.path.isfile(banned_words_file_path):
        with open(banned_words_file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    banned_words.append(row[0].strip())
    else:
        print("Banned words CSV file not found.")
    return banned_words


def user_exists(user_id):
    """Check if the user exists in the CSV file."""
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 2 and str(row[1]) == str(user_id):
                return True
    return False


def create_user_profile(user_id,
                        username,
                        position='Unknown',
                        matches_played=0,
                        goals=0,
                        assists=0,
                        goals_conceded=0,
                        saves=0,
                        passes=0,
                        interceptions=0,
                        tackles=0):
    """Create a user profile in the CSV file."""
    print(f"Creating profile for {username} with user_id {user_id}")
    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                username, user_id, position, matches_played, goals, assists,
                goals_conceded, saves, passes, interceptions, tackles
            ])
            print(f"Profile for {username} added to CSV.")
    except Exception as e:
        print(f"Error occurred while creating profile: {e}")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

banned_words = load_banned_words()

initialize_csv()

lastPing = None


@client.event
async def on_message(message):
    """Event triggered when a new message is sent."""
    global lastPing
    if message.author == client.user:
        return

    user_message = str(message.content).lower()

    # Check for banned words
    for word in banned_words:
        if word in user_message:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, Please refrain from using banned words."
            )
            return

    # Handle !ping command
    if "!ping" in user_message:
        current_time = datetime.now()

        if lastPing is None or (current_time -
                                lastPing) > timedelta(minutes=15):
            lastPing = current_time
            await message.channel.send("@here")
            await message.channel.send("Come and sign for a match")
        else:
            time_remaining = timedelta(minutes=15) - (current_time - lastPing)
            time_remaining_seconds = time_remaining.total_seconds()
            time_remaining_minutes = round(time_remaining_seconds / 60, 1)
            await message.channel.send(
                f"Calm down! You need to wait {time_remaining_minutes} minutes before using !ping again."
            )
        await message.delete()

    # Handle !register command
    elif message.content.startswith("!register"):
        # Safely extract the username
        username = message.content[len("!register "):].strip()

        if not username:
            await message.channel.send("Please provide a username.")
            return

        user_id = message.author.id

        if user_exists(user_id):
            await message.channel.send("You are already registered!")
            return

        # Create user profile in the CSV
        create_user_profile(user_id,
                            username,
                            position="Unknown",
                            matches_played=0,
                            goals=0,
                            assists=0,
                            goals_conceded=0,
                            saves=0,
                            passes=0,
                            interceptions=0,
                            tackles=0)

        # Create the role for the user
        role_name = "Member"
        guild = message.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            await message.author.add_roles(role)
            await message.channel.send(
                f"Thank you for registering, {username}! You have been assigned the '{role_name}' role."
            )
        else:
            try:
                role = await guild.create_role(name=role_name)
                await message.author.add_roles(role)
                await message.channel.send(
                    f"Thank you for registering, {username}! We created the '{role_name}' role and assigned it to you."
                )
            except discord.DiscordException as e:
                await message.channel.send(
                    f"An error occurred while assigning the role: {e}")

        # Confirm registration
        await message.channel.send(
            f"Your account has been created successfully, {username}!")

    elif message.content.startswith("!profile"):
        user_id = message.author.id

        user_data = None
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 2 and str(row[1]) == str(user_id):
                    user_data = row
                    break

        if user_data:
            username = user_data[0]

            # Construct the profile card file path
            card_image_path = f'/home/runner/Viva-Discord-Bot/Statistics/Profiles/player_card_{username}.png'

            # Debugging: Check the constructed file path
            print(f"Checking if file exists at: {card_image_path}")

            # Check if the file exists
            if os.path.isfile(card_image_path):
                with open(card_image_path, 'rb') as image_file:
                    image = discord.File(
                        image_file, filename=f"player_card_{username}.png")
                    await message.channel.send(
                        f"Here is your profile card, {username}!", file=image)
            else:
                await message.channel.send(
                    f"Sorry {username}, your profile card hasn't been generated yet."
                )
        else:
            await message.channel.send(
                "Sorry, you are not registered yet. Please use `!register <username>` to register."
            )


if TOKEN:
    client.run(TOKEN)
