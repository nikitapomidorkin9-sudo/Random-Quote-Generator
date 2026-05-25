from tkinter import *
import random
import json
import os
from datetime import datetime


QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"


DEFAULT_QUOTES = [
    {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон",
     "topic": "Жизнь"},
    {"text": "Будьте тем изменением, которое хотите видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Не бойтесь совершенства, вам его не достичь.", "author": "Сальвадор Дали", "topic": "Искусство"},
    {"text": "В двух словах я могу объяснить всё, что узнал о жизни: она продолжается.", "author": "Роберт Фрост",
     "topic": "Жизнь"},
    {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс",
     "topic": "Работа"},
    {"text": "Сложнее всего начать действовать, всё остальное зависит от упорства.", "author": "Амелия Эрхарт",
     "topic": "Мотивация"},
    {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс", "topic": "Мудрость"},
]

quotes = []
history = []


def load_quotes():
    global quotes
    if os.path.exists(QUOTES_FILE):
        try:
            with open(QUOTES_FILE, "r", encoding="utf-8") as f:
                quotes = json.load(f)
        except:
            quotes = DEFAULT_QUOTES.copy()
    else:
        quotes = DEFAULT_QUOTES.copy()
        save_quotes()


def save_quotes():
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)


def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []
        save_history()


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)



def update_history_listbox():

    lb.delete(0, END)

    author_filter = filter_author_var.get()
    topic_filter = filter_topic_var.get()

    filtered = []
    for q in history:
        if author_filter != "Все" and q["author"] != author_filter:
            continue
        if topic_filter != "Все" and q["topic"] != topic_filter:
            continue
        filtered.append(q)

    for q in filtered:
        short_text = q["text"][:70] + "..." if len(q["text"]) > 70 else q["text"]
        item = f"{short_text} — {q['author']} [{q['topic']}]"
        lb.insert(END, item)

    res_filter.config(text=f"Показано записей: {len(filtered)}", fg="blue")


def update_filter_options():

    if not history:
        authors = []
        topics = []
    else:
        authors = sorted(set(q["author"] for q in history))
        topics = sorted(set(q["topic"] for q in history))

    cur_author = filter_author_var.get()
    cur_topic = filter_topic_var.get()

    author_menu['menu'].delete(0, 'end')
    author_menu['menu'].add_command(label="Все", command=lambda: filter_author_var.set("Все"))
    for a in authors:
        author_menu['menu'].add_command(label=a, command=lambda value=a: filter_author_var.set(value))
    if cur_author not in authors and cur_author != "Все":
        filter_author_var.set("Все")


    topic_menu['menu'].delete(0, 'end')



    topic_menu['menu'].add_command(label="Все", command=lambda: filter_topic_var.set("Все"))
    for t in topics:
        topic_menu['menu'].add_command(label=t, command=lambda value=t: filter_topic_var.set(value))
    if cur_topic not in topics and cur_topic != "Все":
        filter_topic_var.set("Все")


    update_history_listbox()


def generate_quote():
    if not quotes:
        res_gen.config(text="Ошибка: нет ни одной цитаты! Добавьте цитату.", fg="red")
        return

    random_quote = random.choice(quotes).copy()
    random_quote["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(random_quote)
    save_history()
    update_filter_options()

    gen_label_text.set(f"Сгенерировано:\n{random_quote['text']}\n— {random_quote['author']} ({random_quote['topic']})")
    res_gen.config(text="Цитата добавлена в историю!", fg="green")


def add_quote():
    text = text_entry.get("1.0", END).strip()
    author = author_entry.get().strip()
    topic = topic_entry.get().strip()

    if not text:
        res_add.config(text="Ошибка: текст цитаты не может быть пустым!", fg="red")
        return
    if not author:
        res_add.config(text="Ошибка: автор не может быть пустым!", fg="red")
        return
    if not topic:
        res_add.config(text="Ошибка: тема не может быть пустой!", fg="red")
        return

    new_quote = {"text": text, "author": author, "topic": topic}
    quotes.append(new_quote)
    save_quotes()

    text_entry.delete("1.0", END)
    author_entry.delete(0, END)
    topic_entry.delete(0, END)

    res_add.config(text="Цитата добавлена! Теперь доступна для генерации.", fg="green")



window = Tk()
window.title("Random Quote Generator")
window.geometry("1200x700")
window.configure(bg="#f0f0f0")

load_quotes()
load_history()


Label(text="Random Quote Generator", font="Arial 24 bold", bg="#f0f0f0", fg="#333333").place(x=400, y=20)


Label(text="Добавить новую цитату", font="Arial 14 bold", bg="#f0f0f0").place(x=50, y=80)
Label(text="Текст:", font="Arial 12", bg="#f0f0f0").place(x=50, y=120)
text_entry = Text(font="Arial 12", width=45, height=5, bg="white", relief="solid")
text_entry.place(x=50, y=150)

Label(text="Автор:", font="Arial 12", bg="#f0f0f0").place(x=50, y=280)
author_entry = Entry(font="Arial 12", width=30, bg="white", relief="solid")
author_entry.place(x=50, y=310)

Label(text="Тема:", font="Arial 12", bg="#f0f0f0").place(x=50, y=350)
topic_entry = Entry(font="Arial 12", width=30, bg="white", relief="solid")
topic_entry.place(x=50, y=380)

Button(text="Добавить цитату", font="Arial 12", command=add_quote, bg="#4CAF50",
       fg="white", padx=10, pady=5).place(x=50, y=430)
res_add = Label(font="Arial 10", text="", bg="#f0f0f0")
res_add.place(x=50, y=480)


Label(text="Генератор цитат", font="Arial 14 bold", bg="#f0f0f0").place(x=600, y=80)
Button(text="Сгенерировать случайную цитату", font="Arial 12", command=generate_quote,
       bg="#2196F3", fg="white", padx=10, pady=5).place(x=600, y=120)

gen_label_text = StringVar()
gen_label_text.set("Здесь появится сгенерированная цитата")
generated_display = Label(textvariable=gen_label_text, font="Arial 11", bg="#ffffff",
                          relief="solid", wraplength=500, justify="left", padx=10, pady=10)
generated_display.place(x=600, y=180, width=550, height=150)

res_gen = Label(font="Arial 10", text="", bg="#f0f0f0")
res_gen.place(x=600, y=350)


Label(text="Фильтрация истории", font="Arial 14 bold", bg="#f0f0f0").place(x=50, y=540)
Label(text="Автор:", font="Arial 12", bg="#f0f0f0").place(x=50, y=580)
filter_author_var = StringVar(value="Все")
filter_author_var.trace('w', lambda *args: update_history_listbox())  # автообновление
author_menu = OptionMenu(window, filter_author_var, "Все")
author_menu.config(font="Arial 12", width=20)
author_menu.place(x=140, y=575)

Label(text="Тема:", font="Arial 12", bg="#f0f0f0").place(x=350, y=580)
filter_topic_var = StringVar(value="Все")
filter_topic_var.trace('w', lambda *args: update_history_listbox())  # автообновление
topic_menu = OptionMenu(window, filter_topic_var, "Все")
topic_menu.config(font="Arial 12", width=20)
topic_menu.place(x=430, y=575)

res_filter = Label(font="Arial 10", text="", bg="#f0f0f0")
res_filter.place(x=50, y=620)


lb = Listbox(font="Arial 11", width=95, height=15, bg="white", relief="solid", selectbackground="#4CAF50")
lb.place(x=50, y=660, width=1100)


update_filter_options()
window.mainloop()







