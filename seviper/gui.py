import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
import pytkgif
import boa
import seviper.base_data as base_data

GOOD_EFFECTIVE_BATTLE_MESSAGE = "効果 は 抜群だ！"
BAD_EFFECTIVE_BATTLE_MESSAGE = "効果 は いまひとつのようだ..."

class HpBar:
    def __init__(self, master, max_hp, current_hp, details_font_size, image_path):
        assert max_hp >= current_hp
        self.image_path = image_path
        self.master = master
        self.max_hp = max_hp
        self.current_hp = current_hp

        self.image_label = ttk.Label(master)
        self.details_font = tk_font.Font(family="Lucida Grande", size=details_font_size)
        self.details_label = tk.Label(master=master, text=str(max_hp) + " / " + str(current_hp), font=self.details_font)

        hp_percent = int((self.current_hp / self.max_hp) * 100)
        self.image = tk.PhotoImage(file=image_path + "/" + str(hp_percent) + ".png")
        self.image_label.configure(image=self.image)
        self.is_animetion_stop = False

    def __update(self):
        hp_percent = int((self.current_hp / self.max_hp) * 100)
        self.image = tk.PhotoImage(file=self.image_path + "/" + str(hp_percent) + ".png")
        self.image_label.configure(image=self.image)
        self.details_label.configure(text=str(self.max_hp) + " / " + str(self.current_hp))

    def increment(self):
        self.current_hp += 1
        self.__update()

    def decrement(self):
        self.current_hp -= 1
        self.__update()

    def run_animation(self, next_current_hp, interval):
        if next_current_hp < self.current_hp:
            f = self.decrement
        else:
            f = self.increment

        def run_next_frame_animation(_):
            if self.current_hp == next_current_hp:
                return
            f()
            self.master.after(interval, run_next_frame_animation, None)
        run_next_frame_animation(None)

class Replay:
    def __init__(self, master, ui_history, hp_bar_image_path, gif_path):
        master.geometry("610x450")
        self.ui_history = ui_history
        self.hp_bar_image_path = hp_bar_image_path
        self.gif_path = gif_path
        self.font_size = 15

        font = tk_font.Font(family="Lucida Grande", size=self.font_size)
        self.main_frame = tk.Frame(master=master)

        self.p1_widget_frame = tk.Frame(master=self.main_frame)
        p1_poke_name = ui_history[0].real_p1_poke_name

        self.p1_level_label = tk.Label(master=self.p1_widget_frame,
                                       text=str(ui_history[0].real_p1_level) + "Lv", font=font)
        self.p1_poke_name_label = tk.Label(master=self.p1_widget_frame, text=p1_poke_name, font=font)
        self.p1_fighter_gifs = {
            p1_poke_name:pytkgif.Gif(self.p1_widget_frame, pytkgif.Gif.load_images(gif_path + "mirror/" + p1_poke_name + ".gif")[:-1]),
            None:pytkgif.Gif(self.p1_widget_frame, pytkgif.Gif.load_images(gif_path + "None.gif"))
        }
        self.p1_hp_bar = HpBar(self.p1_widget_frame, ui_history[0].real_p1_max_hp,
                               ui_history[0].real_p1_current_hp, self.font_size, hp_bar_image_path)

        self.p2_widget_frame = tk.Frame(master=self.main_frame)
        p2_poke_name = ui_history[0].real_p2_poke_name

        self.p2_level_label = tk.Label(master=self.p2_widget_frame,
                                       text=str(ui_history[0].real_p2_level) + "Lv", font=font)
        self.p2_poke_name_label = tk.Label(master=self.p2_widget_frame, text=p2_poke_name, font=font)
        self.p2_fighter_gifs = {
            p2_poke_name:pytkgif.Gif(self.p2_widget_frame, pytkgif.Gif.load_images(gif_path + "normal/" + p2_poke_name + ".gif")[:-1]),
            None:pytkgif.Gif(self.p2_widget_frame, pytkgif.Gif.load_images(gif_path + "None.gif")[:-1])
        }
        self.p2_hp_bar = HpBar(self.p2_widget_frame, ui_history[0].real_p2_max_hp,
                               ui_history[0].real_p2_current_hp, self.font_size, hp_bar_image_path)

        self.battle_message_entry = tk.Entry(master=master, width=80, font=font)
        self.master = master

    def run_animation(self):
        level_label_pos = {"row":0, "column":0}
        poke_name_label_pos = {"row":1, "column":0}
        fighter_gif_label_pos = {"row":2, "column":0}
        hp_bar_image_label_pos = {"row":3, "column":0}
        hp_bar_details_label_pos = {"row":4, "column":0}

        self.p1_level_label.grid(**level_label_pos)
        self.p1_poke_name_label.grid(**poke_name_label_pos)
        self.p1_fighter_gifs[self.p1_poke_name_label.cget("text")].image_label.grid(**fighter_gif_label_pos)

        for gif in self.p1_fighter_gifs.values():
            gif.run_animation(50)

        self.p1_hp_bar.image_label.grid(**hp_bar_image_label_pos)
        self.p1_hp_bar.details_label.grid(**hp_bar_details_label_pos)

        self.p2_level_label.grid(**level_label_pos)
        self.p2_poke_name_label.grid(**poke_name_label_pos)
        self.p2_fighter_gifs[self.p2_poke_name_label.cget("text")].image_label.grid(**fighter_gif_label_pos)

        for gif in self.p2_fighter_gifs.values():
            gif.run_animation(50)

        self.p2_hp_bar.image_label.grid(**hp_bar_image_label_pos)
        self.p2_hp_bar.details_label.grid(**hp_bar_details_label_pos)

        self.main_frame.pack()
        self.p1_widget_frame.grid(row=0, column=0)
        self.p2_widget_frame.grid(row=0, column=2)

        row_size, column_size = self.main_frame.grid_size()
        for row in range(row_size):
            self.main_frame.grid_columnconfigure(row, minsize=205)
        self.main_frame.grid_rowconfigure(0, minsize=350)
        self.battle_message_entry.pack()

        interval = 60

        def update_level_label(level_label, next_level):
            str_level = level_label.cget("text")[:2]
            if next_level is None and str_level != "None":
                level_label.grid_forget()
                level_label.configure(text="None")
            elif (str(next_level) != str_level):
                level_label.grid_forget()
                level_label.grid(**level_label_pos)
                level_label.configure(text=str(next_level) + "Lv")

        def update_fighter_gif(fighter_gifs, widget_frame, poke_name_label, next_poke_name, is_p1):
            if next_poke_name not in fighter_gifs:
                path = {True:self.gif_path + "mirror/", False:self.gif_path + "normal/"}[is_p1]
                fighter_gifs[next_poke_name] = pytkgif.Gif(widget_frame, pytkgif.Gif.load_images(path + next_poke_name + ".gif")[:-1])
                fighter_gifs[next_poke_name].run_animation(50)

            poke_name = poke_name_label.cget("text")

            if next_poke_name != poke_name:
                if poke_name == "None":
                    fighter_gifs[None].image_label.grid_forget()
                else:
                    fighter_gifs[poke_name].image_label.grid_forget()

                fighter_gifs[next_poke_name].image_label.grid(**fighter_gif_label_pos)

        def update_poke_name_label(poke_name_label, next_poke_name):
            poke_name = poke_name_label.cget("text")

            if next_poke_name is None:
                poke_name_label.grid_forget()
                poke_name_label.configure(text="None")
            elif next_poke_name != poke_name:
                poke_name_label.grid(**poke_name_label_pos)
                poke_name_label.configure(text=next_poke_name)

        def update_hp_bar(master, hp_bar, next_max_hp, next_current_hp):
            is_hp_bar_animation_phase = False
            if next_max_hp is None:
                hp_bar.image_label.grid_forget()
                hp_bar.details_label.grid_forget()
            elif (next_max_hp != hp_bar.max_hp) or (not hp_bar.image_label.winfo_ismapped()):
                hp_bar.image_label.grid_forget()
                hp_bar.details_label.grid_forget()
                hp_bar = HpBar(master, next_max_hp, next_current_hp, self.font_size, self.hp_bar_image_path)
                hp_bar.image_label.grid(**hp_bar_image_label_pos)
                hp_bar.details_label.grid(**hp_bar_details_label_pos)
            elif next_current_hp != hp_bar.current_hp:
                hp_bar.image_label.grid_forget()
                hp_bar.details_label.grid_forget()
                hp_bar.image_label.grid(**hp_bar_image_label_pos)
                hp_bar.details_label.grid(**hp_bar_details_label_pos)
                if next_current_hp < hp_bar.current_hp:
                    hp_bar.decrement()
                else:
                    hp_bar.increment()
                is_hp_bar_animation_phase = True
            return hp_bar, is_hp_bar_animation_phase

        def run_next_frame_animation(index):
            if len(self.ui_history) == index:
                return

            battle_ui = self.ui_history[index]

            next_p1_level = battle_ui.real_p1_level
            next_p2_level = battle_ui.real_p2_level
            next_p1_poke_name = battle_ui.real_p1_poke_name
            next_p2_poke_name = battle_ui.real_p2_poke_name
            next_p1_max_hp = battle_ui.real_p1_max_hp
            next_p2_max_hp = battle_ui.real_p2_max_hp
            next_p1_current_hp = battle_ui.real_p1_current_hp
            next_p2_current_hp = battle_ui.real_p2_current_hp

            update_level_label(self.p1_level_label, next_p1_level)
            update_level_label(self.p2_level_label, next_p2_level)

            update_fighter_gif(self.p1_fighter_gifs, self.p1_widget_frame, self.p1_poke_name_label, next_p1_poke_name, True)
            update_fighter_gif(self.p2_fighter_gifs, self.p2_widget_frame, self.p2_poke_name_label, next_p2_poke_name, False)

            update_poke_name_label(self.p1_poke_name_label, next_p1_poke_name)
            update_poke_name_label(self.p2_poke_name_label, next_p2_poke_name)

            self.p1_hp_bar, is_p1_hp_bar_animation_phase = \
                update_hp_bar(self.p1_widget_frame, self.p1_hp_bar, next_p1_max_hp, next_p1_current_hp)
            self.p2_hp_bar, is_p2_hp_bar_animation_phase = \
                update_hp_bar(self.p2_widget_frame, self.p2_hp_bar, next_p2_max_hp, next_p2_current_hp)

            next_battle_message = battle_ui.battle_message

            if next_battle_message != self.battle_message_entry.cget("text"):
                self.battle_message_entry.delete(0, tk.END)
                self.battle_message_entry.insert(tk.END, next_battle_message)

            if any([is_p1_hp_bar_animation_phase, is_p2_hp_bar_animation_phase]):
                interval = 30
            elif next_battle_message in [GOOD_EFFECTIVE_BATTLE_MESSAGE, BAD_EFFECTIVE_BATTLE_MESSAGE, "効果がない"]:
                interval = 600
            elif "戻れ！" in next_battle_message and next_battle_message.count("！") == 2:
                interval = 600
            elif "行け！" in next_battle_message and next_battle_message.count("！") == 2:
                interval = 600
            elif any([move_name in next_battle_message for move_name in base_data.MOVEDEX]) and "！" in next_battle_message:
                interval = 120
            elif ("戻" not in next_battle_message) and ("行" not in next_battle_message) and ("！" in next_battle_message):
                interval = 600
            else:
                interval = 45
            self.master.after(interval, run_next_frame_animation, index + 1)

        run_next_frame_animation(0)

if __name__ == "__main__":
    main_master = tk.Tk()
    main_master.geometry("500x500")

    #ui_historyがないので現在は動かない
    replay = Replay(main_master, ui_history)
    replay_start_button = tk.Button(master=main_master, text="リプレイ開始")
    replay_start_button.pack()

    def replay_start_button_event(event):
        replay_start_button.pack_forget()
        replay.run_animation()

    replay_start_button.bind("<Button-1>", replay_start_button_event)

    main_master.mainloop()
