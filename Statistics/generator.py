import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import csv
import re

### READ CSV

csv_file_path = '/home/runner/Viva-Discord-Bot/Statistics/users.csv'
data = pd.read_csv(csv_file_path)

### CHOOSE FONT

font1 = ImageFont.truetype(
    '/home/runner/Viva-Discord-Bot/Statistics/fonts/ARIAL.TTF', 55)
font2 = ImageFont.truetype(
    '/home/runner/Viva-Discord-Bot/Statistics/fonts/ARIAL.TTF', 35)

### PLAYER DATA FROM FIRST LINE


def create_player_card(player_data, save_path):
    # Read image
    image_path = '/home/runner/Viva-Discord-Bot/Statistics/Card Canvas.png'
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Extract player data
    player_name = player_data['Name']
    position = player_data['Position']
    origPosition = ""

    ###

    rating = 1

    ###

    player_name = player_data['Name']

    position = player_data['Position']
    origPosition = ""

    matchesPlayed = player_data['Matches Played']

    goals = player_data['Goals']
    assists = player_data['Assists']

    saves = player_data['Saves']
    goalsConceded = player_data['goalsConceded']

    passes = player_data['Passes']
    interceptions = player_data['Interceptions']
    tackles = player_data['Tackles']

    if position == "RB":
        origPosition = "RB"
        position = "FB"
    elif position == "LB":
        origPosition = "LB"
        position = "FB"
    elif position == "LW":
        origPosition = "LW"
        position = "WING"
    elif position == "RW":
        origPosition = "RW"
        position = "WING"

    ### CARD STATS

    if position == "GK":
        statsRequired = [saves, goalsConceded]
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text((350, 480), f"Saves: {saves}", font=font2, fill="white")
        draw.text(
            (220, 510),
            f"Goals Conceded (Avg): {round(goalsConceded/matchesPlayed, 1)}",
            font=font2,
            fill="white")
        draw.text((390, 750), "GK", font=font1, fill="white")
        rating = 85
        print("Card made!")

        ### calculate rating modifier ###

    elif position == "FB":
        statsRequired = [interceptions, goalsConceded]
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text(
            (350, 480),
            f"Interceptions (Avg): {round(interceptions/matchesPlayed, 1)}",
            font=font2,
            fill="white")
        draw.text(
            (220, 510),
            f"Goals Conceded (Avg): {round(goalsConceded/matchesPlayed, 1)}",
            font=font2,
            fill="white")
        if origPosition == "LB":
            draw.text((390, 750), "LB", font=font1, fill="white")
        elif origPosition == "RB":
            draw.text((390, 750), "RB", font=font1, fill="white")

    elif position == "CB":
        statsRequired = [interceptions, tackles]
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text(
            (350, 480),
            f"Interceptions (AVG): {round(interceptions/matchesPlayed, 1)}",
            font=font2,
            fill="white")
        draw.text((220, 510),
                  f"Tackles (Avg): {round(tackles/matchesPlayed, 1)}",
                  font=font2,
                  fill="white")
        draw.text((390, 750), "CB", font=font1, fill="white")

    elif position == "CM":
        statsRequired = [assists, interceptions]
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text((350, 480), f"assists: {assists}", font=font2, fill="white")
        draw.text(
            (220, 510),
            f"interceptions (Avg): {round(interceptions/matchesPlayed, 1)}",
            font=font2,
            fill="white")
        draw.text((390, 750), "CM", font=font1, fill="white")

    elif position == "WING":
        statsRequired = [assists, goals]
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text((350, 480), f"goals: {goals}", font=font2, fill="white")
        draw.text((220, 510), f"assists: {assists}", font=font2, fill="white")
        if origPosition == "LW":
            draw.text((390, 750), "LW", font=font1, fill="white")
        elif origPosition == "RW":
            draw.text((390, 750), "RW", font=font1, fill="white")

    elif position == "CF":
        statsRequired = [goals, assists]
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text((350, 480), f"goals: {goals}", font=font2, fill="white")
        draw.text((220, 510), f"assists: {assists}", font=font2, fill="white")
        draw.text((390, 750), "CF", font=font1, fill="white")

    elif position == "nA":
        draw.text((350, 390), player_name, font=font1, fill="white")
        draw.text((350, 480), "PLAY SOME MATCHES", font=font2, fill="white")
        draw.text((390, 750), "n/a", font=font1, fill="white")
    ### SAVE CARD

    image.save(save_path)
    print(f"Card saved for {player_name}")


for idx, (index, player_data) in enumerate(data.iterrows()):

    player_name = player_data['Name']

    save_player_name = re.sub(r'[\\/*?:"<>|]', "_", player_name)

    save_path = f'/home/runner/Viva-Discord-Bot/Statistics/Profiles/player_card_{save_player_name}.png'

    create_player_card(player_data, save_path)
