from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameentry.get()=='' or passwordentry.get()=='':
        messagebox.showerror('ERROR','Fildes cannot be empty')
    elif usernameentry.get()=='Admin' and passwordentry.get()=='@1234':
        messagebox.showinfo('Success','        Welcome        ')
        window.destroy()
        import sms
    else:
        messagebox.showerror('ERROR','please enter correct credentials')

window=Tk()
window.geometry('1280x853+0+0')

window.title('Login System of Student Management System')
window.resizable(False,False)
backgroundImage=ImageTk.PhotoImage(file='lpage.jpg')
bglabel=Label(window,image=backgroundImage)
bglabel.place(x=0,y=0)
lframe=Frame(window,bg='white')
lframe.place(x=440,y=250)
logo=PhotoImage(file='logo.png')
logolabel=Label(lframe,image=logo,bg='white')
logolabel.grid(row=0,column=0,columnspan=2,pady=10,padx=20)
userimage=PhotoImage(file='user.png')
usernamelabel=Label(lframe,image=userimage,text='Username',compound='left',font=('times new roman',20,'bold'),bg='white')
usernamelabel.grid(row=1,column=0,pady=10,padx=20)
usernameentry=Entry(lframe,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
usernameentry.grid(row=1,column=1,pady=10,padx=20)
passwordimage=PhotoImage(file='password.png')
passwordlabel=Label(lframe,image=passwordimage,text='Password',compound='left',font=('times new roman',20,'bold'),bg='white')
passwordlabel.grid(row=2,column=0,pady=10,padx=20)
passwordentry=Entry(lframe,font=('times new roman',20,'bold'),bd=5,fg='royalblue',show='*')
passwordentry.grid(row=2,column=1,pady=10,padx=20)
loginbutton=Button(lframe,text='Login',font=('times new roman',15,'bold'),width=15,fg='white',bg='cornflowerblue',
                   activebackground='cornflowerblue',activeforeground='white',cursor='hand2',command=login )
loginbutton.grid(row=3,column=1,pady=10)
window.mainloop()