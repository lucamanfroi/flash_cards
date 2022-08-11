from tkinter import *
import pandas
import random as r

BACKGROUND_COLOR = "#B1DDC6"


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = r.choice(to_learn)
    canvas.itemconfig(card_img, image=front_card_img)
    canvas.itemconfig(card_title, text='French', fill='#000')
    canvas.itemconfig(card_word, text=f'{current_card["French"]}', fill='#000')
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_img, image=back_card_img)
    canvas.itemconfig(card_title, text='English', fill='#fff')
    canvas.itemconfig(card_word, text=f'{current_card["English"]}', fill='#fff')


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

window = Tk()
window.title('Flash Cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

data = pandas.read_csv('data/french_words.csv')
to_learn = data.to_dict('records')
current_card = {}

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card_img = PhotoImage(file='images/card_front.png')
back_card_img = PhotoImage(file='images/card_back.png')
card_img = canvas.create_image(400, 263, image=front_card_img)
card_title = canvas.create_text(400, 150, font=('Arial', 40, 'italic'))  # Language title
card_word = canvas.create_text(400, 263, font=('Arial', 60, 'bold'))  # Word
canvas.grid(column=0, row=0, columnspan=2)

red_button_img = PhotoImage(file='images/wrong.png')
red_button = Button(image=red_button_img, highlightthickness=0, borderwidth=0, command=next_card)
red_button.grid(column=0, row=1, pady=10)
green_button_img = PhotoImage(file='images/right.png')
green_button = Button(image=green_button_img, highlightthickness=0, borderwidth=0, command=is_known)
green_button.grid(column=1, row=1)

next_card()

window.mainloop()
