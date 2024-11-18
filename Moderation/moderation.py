import csv

banned_words = []


def load_banned_words():
    global banned_words
    banned_words = []

    with open("Moderation/bannedList.csv", "r") as file:
        reader = csv.reader(file)
        bannedlist = list(reader)
        for row in bannedlist:
            banned_words.append(row[0])


load_banned_words()

print(banned_words)
