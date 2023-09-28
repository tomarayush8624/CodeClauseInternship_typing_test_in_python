import tkinter as tk
import random
import requests

BASE = 'https://ron-swanson-quotes.herokuapp.com/v2/quotes'
ENDPOINT = 'random'
FONT = ("consolas", 30)

window = tk.Tk()
window.geometry('1400x700')
window.title("Typing Test GUI with Tkinter")


def get_quote():
    req = requests.get(f"{BASE}/{ENDPOINT}")
    req.raise_for_status()
    return req.json()[0]


def handlekeypress(event=None):
    # global words_right, words_left
    global curr_letter_no
    try:
        if event.char.lower() == words_right.cget('text')[0].lower():
            curr_letter_no += 1
            words_right.configure(text=words_right.cget('text')[1:])
            words_left.configure(text=words_left.cget('text') + event.char.lower())
            currentalphabet.configure(text=words_right.cget('text')[0])
    except tk.TclError:
        pass


def fetch_text():
    quote = get_quote()

    while len(quote) < 212:
        quote = quote + " " + get_quote()

    return quote


# Setting up the Static Titles
tk.Label(window, text='Speed Typing with Python', font=FONT).pack(pady=30)


def start():
    global time, time_left, curr_letter_no
    time = tk.Label(window, text=f"60 seconds left", font=FONT, fg="green")
    time.pack(pady=30)
    time_left = 60
    main_view()


def main_view():
    pass
    global curr_letter_no
    global words_right, words_left, currentalphabet
    text = fetch_text()

    # track time
    global should_continue
    should_continue = True
    global time_left
    time_left = 60
    window.after(1000, time_deduct)

    curr_letter_no = 0
    window.bind('<Key>', handlekeypress)

    # Letters displayed on the screen

    # Letters that are already written by the user
    words_left = tk.Label(window, text=text[0:curr_letter_no], fg='green', font=FONT)
    words_left.place(relx=0.5, rely=0.5, anchor=tk.E)

    # Letters that the user is about to write
    words_right = tk.Label(window, text=text[curr_letter_no:], font=FONT)
    words_right.place(relx=0.5, rely=0.5, anchor=tk.W)

    currentalphabet = tk.Label(window, text=text[curr_letter_no], font=FONT, fg='grey')
    currentalphabet.place(relx=0.5, rely=0.6, anchor=tk.N)



def time_deduct():
    global time_left, should_continue
    if should_continue:
        time_left -= 1
        time.configure(text=f"{time_left} Seconds Left", fg="green")
        # global should_continue

        if time_left < 0:
            time.configure(text="Times Up (you have 0 second left)", fg="red")
            should_continue = False
            exit_screen()
        elif time_left <= 10:
            time.configure(fg="red")

        window.after(1000, time_deduct)


def exit_screen():
    words_right.destroy()
    words_left.destroy()
    currentalphabet.destroy()

    typing_speed = round(curr_letter_no / (5 * 1), 2)

    global your_speed
    your_speed = tk.Label(window, text=f"Your typing Speed is {typing_speed}WPM", font=FONT)
    your_speed.pack(pady=30)
    global restart_btn
    restart_btn = tk.Button(window, text="Try Again",height=2, width=7, command=restart_app)
    restart_btn.pack(pady=30)


def restart_app():
    your_speed.destroy()
    restart_btn.destroy()
    main_view()



start()
window.mainloop()
