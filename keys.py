import json
import os
import random
import sys
import threading
import customtkinter
import pynput.keyboard
import pygame
import customtkinter as ctk
import tkinter
import tkinter.messagebox

title = f"Keys 2.0.1"

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

data = {
    "sounds": {
        "examplesound1": {
            "press-sound": "sound/path/here",
            "release-sound": None
        },
        "examplesound2": {
            "press-sound": "sound/path/here",
            "release-sound": "sound/path/here"
        }

    },
    "keys": {
        "default": "examplesound1",
        "Key.space": "examplesound1",
        "Key.enter": ["examplesound1", "examplesound2"]
    },
    "ignored-keys": ["Key.esc"]
}

volume = 1

pygame.init()
pygame.mixer.init()

pressed_keys = {}

if not os.path.exists("config.json"):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=2)


with open("config.json", "r") as f:
    config = json.load(f)
    if "ignored-keys" not in config or "sounds" not in config or "keys" not in config:
        with open("config.json.old", "w") as f2:
            f2.write(f.read())
        with open("config.json", "w") as f:
            json.dump(data, f, indent=2)
        tkinter.messagebox.showerror(title,
                                     "Outdated or damaged configuration. Created a backup and regenerated config.\nThe program will exit now.")
        os._exit(0)


def onKeyPress(key):
    global pressed_keys
    try:
        if str(key)[0] == "'":
            key = str(key).replace("'", "")
        elif str(key)[0] == '"':
            key = str(key).replace('"', "")
        if str(key) not in pressed_keys:
            if str(key) not in config["ignored-keys"]:
                if str(key) in config["keys"]:
                    if type(config["keys"][str(key)]) == list:
                        pressed_keys[str(key)] = random.choice(config["keys"][str(key)])
                    else:
                        if config["keys"][str(key)] is not None:
                            pressed_keys[str(key)] = config["keys"][str(key)]
                else:
                    if type(config["keys"]["default"]) == list:
                        pressed_keys[str(key)] = random.choice(config["keys"]["default"])
                    else:
                        pressed_keys[str(key)] = config["keys"]["default"]
                sound = config["sounds"][pressed_keys[str(key)]]["press-sound"]
                if sound is not None:
                    s = pygame.mixer.Sound(sound)
                    s.set_volume(volume)
                    s.play()

    except Exception as e:
        err = sys.exc_info()
        tkinter.messagebox.showerror(title,
                                     f"An exception occoured: \nexc_info():\n * Err_type: {err[0]}\n * Value: {err[1]}")


def onKeyRelease(key):
    if str(key)[0] == "'":
        key = str(key).replace("'", "")
    elif str(key)[0] == '"':
        key = str(key).replace('"', "")
    if str(key) in pressed_keys:
        sound = config["sounds"][pressed_keys[str(key)]]["release-sound"]
        del pressed_keys[str(key)]
        if sound is not None:
            s = pygame.mixer.Sound(sound)
            s.set_volume(volume)
            s.play()


def keyboard_listener():
    with pynput.keyboard.Listener(on_press=onKeyPress, on_release=onKeyRelease) as listener:
        listener.join()


class Main(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.geometry("300x75")
        self.minsize(300, 75)
        self.label1 = ctk.CTkLabel(master=self,
                                   text="Volume: 100%")
        self.label1.grid(row=0,
                         column=0,
                         sticky="W",
                         padx=8,
                         pady=(10, 0))

        self.volume_slider = ctk.CTkSlider(master=self,
                                           from_=0,
                                           to=100,
                                           orientation="horizontal",
                                           command=self.sliderCallback,
                                           number_of_steps=100,
                                           progress_color="#232426")
        self.volume_slider.grid(row=1,
                                column=0,
                                padx=10,
                                pady=(0, 5),
                                sticky="WES")

        self.volume_slider.set(100)

        ctk.CTkLabel(master=self,
                     text="github.com/szabolcs2008",
                     height=10,
                     text_color="#999999").grid(row=2,
                                                column=0,
                                                sticky="WS",
                                                padx=2,
                                                pady=(0, 1))

        threading.Thread(target=keyboard_listener).start()

    def sliderCallback(self, value):
        global volume
        volume = value / 100
        self.label1.configure(text=f"Volume: {int(value)}%")

    def run(self):
        self.mainloop()
        os._exit(0)


if __name__ == "__main__":
    Main().run()
