from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist, columns=['ID', 'NAME', 'MOBILE', 'ADDED DATE', 'ADDED TIME'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')

def update_student():
    def update_data():
        date = time.strftime('%d/%m/%Y')
        currenttime = time.strftime('%H:%M:%S')

        query = 'UPDATE student SET name=%s, mobile=%s, date=%s, time=%s WHERE id=%s'
        mycursor.execute(query, (nameEntry.get(), mobilenoEntry.get(), date, currenttime, idEntry.get()))
        con.commit()

        messagebox.showinfo('Success', f'ID {idEntry.get()} is modified successfully', parent=update_window)
        update_window.destroy()
        show_student()

    update_window = Toplevel(root)
    update_window.title("Update Student")
    update_window.grab_set()
    update_window.geometry("400x300")
    update_window.resizable(False, False)

    Label(update_window, text='ID', font=('times new roman', 20, 'bold')).grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(update_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    Label(update_window, text='NAME', font=('times new roman', 20, 'bold')).grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(update_window, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    Label(update_window, text='MOBILE NO', font=('times new roman', 20, 'bold')).grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobilenoEntry = Entry(update_window, font=('roman', 15, 'bold'))
    mobilenoEntry.grid(row=2, column=1, pady=15, padx=10)

    ttk.Button(update_window, text='UPDATE', command=update_data).grid(row=3, columnspan=2, pady=20)

    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    listdata = content['values']

    if not listdata:
        messagebox.showerror('Error', 'Please select a student record to update!', parent=root)
        update_window.destroy()
        return

    idEntry.insert(0, listdata[0])
    nameEntry.insert(0, listdata[1])
    mobilenoEntry.insert(0, listdata[2])

def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'ID {content_id} is deleted successfully')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def search_student():
    def search_data():
        query = 'select * from student where id=%s or name=%s or mobile=%s'
        mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobilenoEntry.get()))
        studentTable.delete(*studentTable.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            studentTable.insert('', END, values=data)

    search_window = Toplevel(root)
    search_window.title("Search Student")
    search_window.grab_set()
    search_window.geometry("400x300")
    search_window.resizable(False, False)

    idLabel = Label(search_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(search_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(search_window, text='NAME', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(search_window, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    mobilenoLabel = Label(search_window, text='MOBILE NO', font=('times new roman', 20, 'bold'))
    mobilenoLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobilenoEntry = Entry(search_window, font=('roman', 15, 'bold'))
    mobilenoEntry.grid(row=2, column=1, pady=15, padx=10)

    search_student_button = ttk.Button(search_window, text='SEARCH', command=search_data)
    search_student_button.grid(row=3, columnspan=2, pady=20)

def add_student():
    def add_data():
        if idEntry.get() == '' or nameEntry.get() == '' or mobilenoEntry.get() == '':
            messagebox.showerror('ERROR', 'ALL FIELDS ARE REQUIRED!', parent=add_window)
        else:
            try:
                # Get current date and time
                date = time.strftime('%d/%m/%Y')
                currenttime = time.strftime('%H:%M:%S')

                # Insert data into the database
                query = 'INSERT INTO student VALUES (%s, %s, %s, %s, %s)'
                mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobilenoEntry.get(), date, currenttime))
                con.commit()

                # Ask user if they want to clear the form
                result = messagebox.askyesno('Confirm', 'Do you want to clear the form?', parent=add_window)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    mobilenoEntry.delete(0, END)
            except pymysql.err.IntegrityError:
                messagebox.showerror('Error', 'ID cannot be repeated', parent=add_window)
                return

            # Refresh the student table
            query = 'SELECT * FROM student'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                studentTable.insert('', END, values=data)

    add_window = Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("400x300")
    add_window.resizable(False, False)

    idLabel = Label(add_window, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(add_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(add_window, text='NAME', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(add_window, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    mobilenoLabel = Label(add_window, text='MOBILE NO', font=('times new roman', 20, 'bold'))
    mobilenoLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobilenoEntry = Entry(add_window, font=('roman', 15, 'bold'))
    mobilenoEntry.grid(row=2, column=1, pady=15, padx=10)

    add_student_button = ttk.Button(add_window, text='ADD', command=add_data)
    add_student_button.grid(row=3, columnspan=2, pady=20)

def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return

        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key, name varchar(30), mobile varchar(11), date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    root.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('arial', 20, 'bold'))
    hostEntry.grid(row=0, column=1, padx=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('arial', 20, 'bold'))
    usernameEntry.grid(row=1, column=1, padx=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('arial', 20, 'bold'))
    passwordEntry.grid(row=2, column=1, padx=20)

    connectButton = ttk.Button(connectWindow, text='Connect', width=20, command=connect)
    connectButton.grid(row=3, columnspan=2, pady=20)

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('STUDENT MANAGEMENT SYSTEM')

root.configure(bg='#FAF3E0')  

def clock():
    timeString = time.strftime('%H:%M:%S')
    dateString = time.strftime('%d/%m/%Y')
    datetimeLabel.config(text=f'{dateString}\n{timeString}')
    datetimeLabel.after(1000, clock)

datetimeLabel = Label(root, text='hello', font=('Helvetica', 18, 'bold'), fg='#4B371C', bg='#FAF3E0', padx=10, pady=5)
datetimeLabel.place(x=5, y=5)
clock()

s = ' STUDENT MANAGEMENT SYSTEM'
sliderLabel = Label(root, text=s, font=('Helvetica', 28, 'italic bold'), fg='#D2691E', bg='#FAF3E0', width=30)
sliderLabel.place(x=200, y=5)

def slider():
    current = sliderLabel.cget('text')
    s = current[1:] + current[0]
    sliderLabel.config(text=s)
    sliderLabel.after(400, slider)  # Increased the interval to 400ms to slow it down


slider()

connectButton = ttk.Button(root, text='Connect Database', width=25, command=connect_database)
connectButton.place(x=50, y=80)

leftFrame = Frame(root, bg='#FAF3E0')
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='images/mortarboard.png')
logo_label = Label(leftFrame, image=logo_image, bg='#FAF3E0')
logo_label.grid(row=0, column=0, padx=10, pady=10)

connectButton = ttk.Button(leftFrame, text='Connect Database', width=25, command=connect_database)
connectButton.grid(row=1, column=0, padx=10, pady=10)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED, command=add_student)
addstudentButton.grid(row=2, column=0, padx=10, pady=10)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED, command=search_student)
searchstudentButton.grid(row=3, column=0, padx=10, pady=10)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED, command=update_student)
updatestudentButton.grid(row=4, column=0, padx=10, pady=10)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, padx=10, pady=10)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=6, column=0, padx=10, pady=10)

exportstudentButton = ttk.Button(leftFrame, text='Export Student Data', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=7, column=0, padx=10, pady=10)


exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
exitButton.grid(row=8, column=0, padx=10, pady=10)

rightFrame = Frame(root, bg='white')
rightFrame.place(x=400, y=80, width=750, height=600)

scroll_y = Scrollbar(rightFrame, orient=VERTICAL)
scroll_x = Scrollbar(rightFrame, orient=HORIZONTAL)
studentTable = ttk.Treeview(rightFrame, columns=('id', 'name', 'mobile', 'date', 'time'),
                             yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=studentTable.yview)
scroll_x.config(command=studentTable.xview)

studentTable.heading('id', text='ID')
studentTable.heading('name', text='Name')
studentTable.heading('mobile', text='Mobile')
studentTable.heading('date', text='Added Date')
studentTable.heading('time', text='Added Time')
studentTable['show'] = 'headings'
studentTable.pack(fill=BOTH, expand=1)

root.mainloop()