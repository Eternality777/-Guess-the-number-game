# Importing necessary libraries
from tkinter import *  # Importing tkinter for GUI
from PIL import Image, ImageTk  # Importing PIL for working with images
import random  # Importing random for generating random numbers
import pygame  # Importing pygame for playing sound effects

# Initialize pygame
pygame.init()

# Create the main window
root = Tk()
root.geometry('640x480')
root.title('Guess the number game')
root.config(bg='#363636')  # Set background color

# Label for instruction
lb = Label(root, text="Guess the number between 1 and 10", font=('Arial,20,bold'), bg='#363636', fg='white')
lb.pack()

# Entry widget for user input
num = Entry(root, font=('Arial,20,bold'), borderwidth=5)
num.pack()

# Text variable for displaying attempts left
text = StringVar()
text.set("You have 10 attempts left")
attempt_text = Label(root, textvariable=text, bg='#363636', fg='white', font=('Arial,20,bold'))
attempt_text.pack(pady=30)

# Variables for game logic
attempts = 9
answer = random.randint(1, 10)

# Open and load GIF file for animation
gif_filename = "gif_withoutbg.gif"
gif = Image.open(gif_filename)

# Load sound effects for game events
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
attempt_sound = pygame.mixer.Sound("damage.wav")

# Function to play win animation and sound
def win_animation():
    win_sound.play()
    animate_once("win.gif")

# Function to play lose animation and sound
def lose_animation():
    lose_sound.play()
    animate_once("losegif.gif")

# Function to play sound for each attempt
def play_attempt_sound():
    attempt_sound.play()

# List to store frames of GIF for animation
frames = []
for frame in range(0, gif.n_frames):
    gif.seek(frame)
    frame_image = gif.copy()
    frame_image = frame_image.convert('RGBA')
    frames.append(ImageTk.PhotoImage(frame_image))

# Function to display each frame of the animation
def display_frame(frame_index, max_frames, stop_at_frame=None):
    if frame_index < max_frames:
        heart_label.config(image=frames[frame_index])
        if frame_index != stop_at_frame:
            root.after(75, display_frame, frame_index + 1, max_frames, stop_at_frame)

# Function to start the animation
def start_animation(stop_at_frame):
    display_frame(0, len(frames), stop_at_frame)
    static_label.pack_forget()

# Function to animate GIF once for win or lose events
def animate_once(gif_filename):
    win_or_lose_frames = []
    gif = Image.open(gif_filename)
    for frame in range(0, gif.n_frames):
        gif.seek(frame)
        frame_image = gif.copy()
        frame_image = frame_image.convert('RGBA')
        win_or_lose_frames.append(ImageTk.PhotoImage(frame_image))

    def display(frame_index):
        if frame_index < len(win_or_lose_frames):
            label.config(image=win_or_lose_frames[frame_index])
            root.after(125, display, frame_index + 1)
        else:
            label.after(500, label.pack_forget) 

    label = Label(root, bg='#363636')
    label.pack()
    display(0)

# Load win and lose GIF images
win_gif = Image.open("win.gif")
win_gif = win_gif.convert('RGBA')
win_gif = ImageTk.PhotoImage(win_gif)

lose_gif = Image.open("losegif.gif")
lose_gif = lose_gif.convert('RGBA')
lose_gif = ImageTk.PhotoImage(lose_gif)

# Labels for displaying win and lose animations
win_gif_label = Label(root, bg='#363636')
lose_gif_label = Label(root, bg='#363636')

# Function to check user input
def Checknum(event=None):
    global attempts
    global text

    guess_str = num.get().strip()
    if guess_str == "":
        text.set("Please enter a number")
        return 
    guess_num = int(guess_str)
    if guess_num < 1 or guess_num > 10:
        text.set("Please enter a number between 1 and 10")
        return
    attempts -= 1    
    if guess_num == answer:
        text.set("You won! \n Congratulations!")
        num.config(state='disabled')  # Disable the entry widget
        button1.pack_forget()  # Hide the Check button
        root.unbind('<Return>')  # Unbind the Enter key
        static_label.pack_forget()  # Hide the GIF label
        heart_label.pack_forget()
        win_animation()
        return  # Return to exit the function and prevent further execution
    elif attempts + 1 <= 0:
        text.set("No more attempts left. Game over.")
        num.config(state='disabled')  # Disable the entry widget
        button1.pack_forget()  # Hide the Check button
        root.unbind('<Return>')  # Unbind the Enter key
        static_label.pack_forget()  # Hide the GIF label
        heart_label.pack_forget()
        lose_animation()
        return
    elif guess_num < answer:
        text.set("You have " + str(attempts + 1) + " attempts left \n Go higher") 
        start_animation(len(frames) * (10 - attempts - 1) // 10)
        play_attempt_sound()
    elif guess_num > answer:
        text.set("You have " + str(attempts + 1) + " attempts left \n Go lower")
        start_animation(len(frames) * (10 - attempts - 1) // 10)
        play_attempt_sound()

# Label for displaying the heart animation
heart_label = Label(root, bg='#363636')
heart_label.pack()

# Load static GIF image for background
static_gif_filename = "gif_withoutbg.gif"
static_gif = Image.open(static_gif_filename)
static_gif = static_gif.convert('RGBA')
static_gif = ImageTk.PhotoImage(static_gif)

# Label to display the static GIF image
static_label = Label(root, image=static_gif, bg='#363636')
static_label.pack()

# Button to trigger the Checknum function
button1 = Button(root, text="Check", font=('Arial,20,bold'), bg='#B3B3B3', fg='black', command=Checknum)
button1.pack(pady=10)

# Button to quit
button2 = Button(root, text="Quit", font=('Arial,20,bold'), bg='#B3B3B3', fg='black', command=root.destroy)
button2.pack()
#Bindind the Enter key to input
root.bind('<Return>', Checknum)
# Start the main event loop to run the tkinter application
root.mainloop()