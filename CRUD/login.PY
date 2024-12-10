from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif usernameEntry.get() == 'JAMIERA' and passwordEntry.get() == '9303':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import sms
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')

window = Tk()
window.title('Login System')
window.geometry('1280x700+0+0')
window.resizable(False, False)

gif_path = 'images/Untitled design.gif'
gif = Image.open(gif_path)

gif_frames = []
for frame in range(gif.n_frames):
    gif.seek(frame)
    gif_frames.append(ImageTk.PhotoImage(gif.copy().convert('RGBA')))

gif.close()

bgLabel = Label(window)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

def update_bg(index):
    bgLabel.config(image=gif_frames[index])
    window.after(100, update_bg, (index + 1) % len(gif_frames))

update_bg(0)

canvas = Canvas(window, width=450, height=350, bg='ORANGE', highlightthickness=0)
canvas.create_oval(10, 10, 440, 340, fill='ORANGE', outline='ORANGE')
canvas.place(x=415, y=175)

loginFrame = Frame(canvas, bg='ORANGE', padx=20, pady=20)
loginFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

logoImage = PhotoImage(file='images/mortarboard.png')
logoLabel = Label(loginFrame, image=logoImage, bg='ORANGE')
logoLabel.grid(row=0, column=0, columnspan=2, pady=(10, 20))

usernameImage = PhotoImage(file='images/user (1).png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 17, 'bold'), bg='ORANGE')
usernameLabel.grid(row=1, column=0, pady=10)
usernameEntry = Entry(loginFrame, font=('times new roman', 17), bd=2, fg='black', width=22, relief=FLAT)
usernameEntry.grid(row=1, column=1, pady=10, padx=10)

passwordImage = PhotoImage(file='images/lock.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 17, 'bold'), bg='ORANGE')
passwordLabel.grid(row=2, column=0, pady=10)
passwordEntry = Entry(loginFrame, font=('times new roman', 17), bd=2, fg='black', width=22, relief=FLAT, show='*')
passwordEntry.grid(row=2, column=1, pady=10, padx=10)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=14, fg='WHITE',
                     bg='cornflowerblue', activebackground='cornflowerblue', activeforeground='WHITE',
                     cursor='hand2', command=login, relief=FLAT)
loginButton.grid(row=3, column=1, pady=20)

window.mainloop()