from random import choice
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
# ------------------ Constants ------------- #
BACKGROUND_COLOR = "#B1DDC6"
random_word = {}
spanish_words_dict = {}

# ------------------ Generate Random Words ---------------------#
try:
    data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv("data/spanish words.csv")
    spanish_words_dict = original_data.to_dict(orient="records")
else:
    # orient = records....... gives us the key value pairs according to values in each row
    spanish_words_dict = data.to_dict(orient="records")


def next_card():
    """ changes card after each click of button and
    handle the flip of card by cancelling the previous after function changing wait time to 3sec for each new card"""
    global random_word, flip_timer
    windows.after_cancel(flip_timer)
    random_word = choice(spanish_words_dict)
    canvas.itemconfig(card, image=front_image)
    canvas.itemconfig(title, text="Spanish", fill="black")
    canvas.itemconfig(word, text=random_word['Spanish'], fill="black")
    flip_timer = windows.after(3000, func=flip_card)

# ------------------ Generate New CSV of unknown words ---------------------#


def is_known():
    print(len(spanish_words_dict))
    spanish_words_dict.remove(random_word)
    next_card()
    words_to_learn = pd.DataFrame(spanish_words_dict)
    words_to_learn.to_csv('data/words_to_learn.csv', index=False)


# ------------------ Flip Cards ---------------------#
def flip_card():
    """function to flip the card and change configs of canvas after each 3 sec wait time"""
    canvas.itemconfig(card, image=back_image)
    canvas.itemconfig(title, text="English", fill="White")
    canvas.itemconfig(word, text=random_word["English"], fill="White")


# ------------------ UI ---------------------#
windows = Tk()
windows.title("Flashy")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = windows.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
new_img = Image.open("images/card_back.png")
back_image = ImageTk.PhotoImage(new_img)
old_img = Image.open("images/card_front.png")
front_image = ImageTk.PhotoImage(old_img)
card = canvas.create_image(415, 265, image=front_image)
title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, 'italic'))
word = canvas.create_text(400, 263, text="Word", font=('Arial', 50, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

right_img = Image.open('images/right.png')
right = ImageTk.PhotoImage(right_img)
right_button = Button(image=right, bg=BACKGROUND_COLOR, borderwidth=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_img = Image.open("images/wrong.png")
wrong = ImageTk.PhotoImage(wrong_img)
wrong_button = Button(image=wrong, bg=BACKGROUND_COLOR, borderwidth=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()
windows.mainloop()
