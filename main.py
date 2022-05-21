from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
#-------------- Process ----------------------------#

try:
    data = pandas.read_csv("data\words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data\english_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")    # меняет формат словаря


def next_card():
    global current_card, flip_time
    window.after_cancel(flip_time)
    current_card =  random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill='Black')
    canvas.itemconfig(card_word, text=current_card["English"], fill='Black')
    canvas.itemconfig(card_bg, image=card_front)
    flip_time = window.after(3000, func=flip_card)     # запускает 3сек заново

def flip_card():
    canvas.itemconfig(card_title, text="Перевод", fill='white')       # меняет titel
    canvas.itemconfig(card_word, text=current_card["Russian"], fill='white')      # меняет слово
    canvas.itemconfig(card_bg, image=card_back)       # меняет картинку карточки

def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)      # отформатированный словарь
    data.to_csv("data\words_to_learn.csv", index=False)    # создаёт новый файл

    next_card()

#------------- User Interface (UI) ---------------------------#

window = Tk()
window.title("Flash Card")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

flip_time = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
card_front = PhotoImage(file="images\card_front.png")
card_back = PhotoImage(file="images\card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 20, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Arial", 40, "italic"))
#buttons

x_image = PhotoImage(file="images\wrong.png")
x_button = Button(image=x_image, highlightthickness=0, command=next_card)
x_button.grid(column=0, row=1)

v_image = PhotoImage(file="images\\right.png")
v_button = Button(image=v_image, highlightthickness=0, command=is_known)
v_button.grid(column=1, row=1)


next_card()

window.mainloop()



