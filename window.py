import tkinter as tk

background_color = "#000"
text_color = "#fff"

def background(color):
    global background_color
    background_color = color
    
    root.configure(bg=background_color)

def text_color_c(color):
    global text_color
    text_color = color

def write(write_text):
    global background_color
    global root
    global text
    text = tk.Label(root, text=write_text,font=("",25),bg=background_color,foreground=text_color)
    text.pack()

root = tk.Tk()
root.title("window")
root.geometry("700x450")
root.configure(bg=background_color)




