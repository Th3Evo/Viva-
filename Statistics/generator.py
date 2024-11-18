import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import csv

### READ CSV

csv_file_path = '/home/runner/Viva Discord Bot/Statistics/users.csv'
data = pd.read_csv(csv_file_path)

### write CSV

csv_file_path2 = '/home/runner/Viva Discord Bot/Statistics/players.csv'
thisHelps = csv_file_path2

### READ IMAGE

image_path = '/home/runner/Viva Discord Bot/Statistics/Card Canvas.png'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

### CHOOSE FONT

font1 = ImageFont.truetype("fonts/ARIAL.TTF", 55)
font2 = ImageFont.truetype("fonts/ARIAL.TTF", 35)

### PLAYER DATA FROM FIRST LINE

player_data = data.iloc[0]

###

rating = 1

###

player_name = player_data['Name']

position = player_data['Position']

matchesPlayed = player_data['Matches Played']

goals = player_data['Goals']
assists = player_data['Assists']

saves = player_data['Saves']
goalsConceded = player_data['goalsConceded']

passes = player_data['Passes']
interceptions = player_data['Interceptions']

### CARD STATS

if position == "GK":
    statsRequired = [saves, goalsConceded]
    draw.text((350, 390), player_name, font=font1, fill="white")
    draw.text((350, 480), f"Saves: {saves}", font=font2, fill="white")
    draw.text((220, 510),
              f"Goals Conceded (Avg): {goalsConceded/matchesPlayed}",
              font=font2,
              fill="white")
    draw.text((390, 750), "GK", font=font1, fill="white")
    rating = 85

    ### calculate rating modifier ###

### SAVE CARD

image.save('/home/runner/MMR/modified_player_card.png')

with open(thisHelps, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([player_name, position, rating])