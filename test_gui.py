import tkinter as tk
import seviper.gui as gui
import boa

main_master = tk.Tk()
main_master.geometry("500x500")

ui_history = boa.load_pickle("C:/Python35/pyckage/seviper/64.pkl")
replay = gui.Replay(main_master, ui_history, "C:/Python35/pyckage/arbok/image/hp_bar/", "C:/Python35/pyckage/arbok/image/gif/")
replay_start_button = tk.Button(master=main_master, text="リプレイ開始")
replay_start_button.pack()

def replay_start_button_event(event):
    replay_start_button.pack_forget()
    replay.run_animation()
    replay_start_button.bind("<Button-1>", replay_start_button_event)

replay_start_button.bind("<Button-1>", replay_start_button_event)
main_master.mainloop()
