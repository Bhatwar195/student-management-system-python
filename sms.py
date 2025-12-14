from tkinter import *
import time
from tkinter import ttk,messagebox,filedialog
from ttkthemes import ThemedTk
import pymysql
import pandas
#functinality part
global con,mycursor  

def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studenttable.get_children()
    newlist=[]
    for index in indexing:
       content=studenttable.item(index)
       datalist=content['values']
       newlist.append(datalist)
    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','D.O.B',
                                 'Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is save succesfully')



def update_student():
    def update_data():
        q='update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
        mycursor.execute(q,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),
                            genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
        con.commit()
        messagebox.showinfo('Success',f'Id {idEntry.get()} is modified succesfully',parent=update_window)
        update_window.destroy()
        show_student() 

    update_window=Toplevel()
    update_window.title('Update Student')
    update_window.grab_set()
    update_window.resizable(False,False)
    idLabel=Label(update_window,text='ID',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    idEntry.grid(row=0,column=1,padx=10,pady=15)

    nameLabel=Label(update_window,text='NAME',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    nameEntry.grid(row=1,column=1,padx=10,pady=15)

    phoneLabel=Label(update_window,text='PHONE',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    phoneEntry.grid(row=2,column=1,padx=10,pady=15)

    emailLabel=Label(update_window,text='EMAIL',font=('times new roman',20,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    emailEntry.grid(row=3,column=1,padx=10,pady=15)

    addressLabel=Label(update_window,text='ADDRESS',font=('times new roman',20,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    addressEntry.grid(row=4,column=1,padx=10,pady=15)

    genderLabel=Label(update_window,text='GENDER',font=('times new roman',20,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    genderEntry.grid(row=5,column=1,padx=10,pady=15)

    dobLabel=Label(update_window,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(update_window,font=('romsn',15,'bold'),width=25)
    dobEntry.grid(row=6,column=1,padx=10,pady=15)

    update_student_button=ttk.Button(update_window,text='UPDATE STUDENT',command=update_data)
    update_student_button.grid(row=7,columnspan=2,pady=15)

    indexing=studenttable.focus()
    content=studenttable.item(indexing)
    if not indexing:
        messagebox.showerror('Error','please select a row to update')
        return
    listdata=list(content['values'])
    idEntry.insert(0,listdata[0])
    nameEntry.insert(0,listdata[1])
    phoneEntry.insert(0,listdata[2])
    emailEntry.insert(0,listdata[3])
    addressEntry.insert(0,listdata[4])
    genderEntry.insert(0,listdata[5])
    dobEntry.insert(0,listdata[6])
# show student table on main content
def show_student():
    q='select * from student'
    mycursor.execute(q)
    fetched_data=mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())
    for data in fetched_data:
            studenttable.insert('',END,values=data)

def delete_student():
    indexing=studenttable.focus()
    print(indexing)
    content=studenttable.item(indexing)
    content_id=content['values'][0]
    q='delete from student where id=%s '
    mycursor.execute(q,content_id,)
    con.commit()
    messagebox.showinfo('Deleted',f' Id {content_id} is deleted succesfully')
    q='select * from student'
    mycursor.execute(q)
    fetched_data=mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())
    for data in fetched_data:
            studenttable.insert('',END,values=data)



def search_student():
    def search_data():
        q='select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
        mycursor.execute(q,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),
                            genderEntry.get(),dobEntry.get()))
        studenttable.delete(*studenttable.get_children())
        fetched_data=mycursor.fetchall()
        if not fetched_data:
            messagebox.showinfo('No Data', 'No matching student found.', parent=search_window)
        for data in fetched_data:
            studenttable.insert('',END,values=data)
        search_window.destroy()
    search_window=Toplevel()
    search_window.title('Search Student')
    search_window.grab_set()
    search_window.resizable(False,False)
    idLabel=Label(search_window,text='ID',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    idEntry.grid(row=0,column=1,padx=10,pady=15)

    nameLabel=Label(search_window,text='NAME',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    nameEntry.grid(row=1,column=1,padx=10,pady=15)

    phoneLabel=Label(search_window,text='PHONE',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    phoneEntry.grid(row=2,column=1,padx=10,pady=15)

    emailLabel=Label(search_window,text='EMAIL',font=('times new roman',20,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    emailEntry.grid(row=3,column=1,padx=10,pady=15)

    addressLabel=Label(search_window,text='ADDRESS',font=('times new roman',20,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    addressEntry.grid(row=4,column=1,padx=10,pady=15)

    genderLabel=Label(search_window,text='GENDER',font=('times new roman',20,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    genderEntry.grid(row=5,column=1,padx=10,pady=15)

    dobLabel=Label(search_window,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(search_window,font=('romsn',15,'bold'),width=25)
    dobEntry.grid(row=6,column=1,padx=10,pady=15)

    search_student_button=ttk.Button(search_window,text='SEARCH STUDENT',command=search_data)
    search_student_button.grid(row=7,columnspan=2,pady=15)




def add_student():
   
    def add_data():
        if idEntry.get()==''or nameEntry.get()==''or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or dobEntry.get()=='' :
            messagebox.showerror('Error','All Feilds are required',parent=add_window)
        else:
            try:
                q='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(q,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),
                                    addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime))
                con.commit()
                result=messagebox.askyesno('Confirm','Data added succesfully. Do you want to clean the form ?',parent=add_window)
                if result==True:
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    phoneEntry.delete(0,END)
                    emailEntry.delete(0,END)
                    genderEntry.delete(0,END)
                    addressEntry.delete(0,END)
                    dobEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox.showerror('Error','ID cannot be repeted',parent=add_window)
                return
            
            
            q='select * from student'
            mycursor.execute(q)
            fetched_data=mycursor.fetchall()
            studenttable.delete(*studenttable.get_children())
            for data in fetched_data:
                # data_list = list(data)
                studenttable.insert('', END, values=data)


    add_window=Toplevel()
    add_window.title('Add Student')
    add_window.grab_set()
    add_window.resizable(False,False)
    idLabel=Label(add_window,text='ID',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    idEntry.grid(row=0,column=1,padx=10,pady=15)

    nameLabel=Label(add_window,text='NAME',font=('times new roman',20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    nameEntry.grid(row=1,column=1,padx=10,pady=15)

    phoneLabel=Label(add_window,text='PHONE',font=('times new roman',20,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    phoneEntry.grid(row=2,column=1,padx=10,pady=15)

    emailLabel=Label(add_window,text='EMAIL',font=('times new roman',20,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    emailEntry.grid(row=3,column=1,padx=10,pady=15)

    addressLabel=Label(add_window,text='ADDRESS',font=('times new roman',20,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    addressEntry.grid(row=4,column=1,padx=10,pady=15)

    genderLabel=Label(add_window,text='GENDER',font=('times new roman',20,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    genderEntry.grid(row=5,column=1,padx=10,pady=15)

    dobLabel=Label(add_window,text='D.O.B',font=('times new roman',20,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(add_window,font=('romsn',15,'bold'),width=25)
    dobEntry.grid(row=6,column=1,padx=10,pady=15)

    add_student_button=ttk.Button(add_window,text='ADD STUDENT',command=add_data)
    add_student_button.grid(row=7,columnspan=2,pady=15)

def connect_database():
   
    def connect():
        global con,mycursor
        try:
            #con=pymysql.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            con=pymysql.connect(host='localhost',user='root',password='************')
            mycursor=con.cursor()
            messagebox.showinfo('Success',' Database Conneted successful ',parent=connectWindow)
        except Exception as e:
            messagebox.showerror('Error', f'Invalid Details\n{e}', parent=connectWindow)
            print(e)
        try:
            q='Create database studentms'
            mycursor.execute(q)
            q='use studentms'
            mycursor.execute(q)
            q='create table student(id int not null primary key,name varchar(50),mobile varchar(15),email varchar(50),address varchar(100),' \
            'gender varchar(20),dob varchar(20),date varchar(50),time varchar(50))'
            mycursor.execute(q)
        except:
            q='use studentms'
            mycursor.execute(q)
        messagebox.showinfo('Success','Database Connection is succesful',parent=connectWindow)
        connectWindow.destroy()
        addstudentbutton.config(state=NORMAL)
        searchstudentbutton.config(state=NORMAL)
        updatestudentbutton.config(state=NORMAL)
        showstudentbutton.config(state=NORMAL)
        exportstudentbutton.config(state=NORMAL)
        deletestudentbutton.config(state=NORMAL)
            

    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False,False)
    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',15,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)
    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1 ,pady=20,padx=40)
    usernameLabel=Label(connectWindow,text='User Name',font=('arial',15,'bold'))
    usernameLabel.grid(row=1,column=0,padx=20)
    usernameEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    usernameEntry.grid(row=1,column=1,pady=20,padx=40)
    passwordLabel=Label(connectWindow,text='Password',font=('arial',15,'bold'))
    passwordLabel.grid(row=2,column=0,padx=20)
    passwordEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2,show='*')
    passwordEntry.grid(row=2,column=1,pady=20,padx=40)
    connectbButton=ttk.Button(connectWindow,text='Connect',command=connect)
    connectbButton.grid(row=3,columnspan=2)
                          
count=0
text=''
def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%y')
    currenttime=time.strftime('%H:%M:%S')
    datetimelabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimelabel.after(1000,clock)

def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderlabel.config(text=text)
    count+=1
    sliderlabel.after(300,slider)

#GUI part
root=ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+50+20')
root.title('Student Management System')
root.resizable(False,False)

datetimelabel=Label(root,text='hello',font=('times new roman',20,'bold'),)
datetimelabel.place(x=5,y=5)
clock()
s='Student Management System'
sliderlabel=Label(root,font=('arial',28,'italic bold'),width=30,bg='royalblue')
sliderlabel.place(x=250,y=0) 
slider()

connectbutton=ttk.Button(root,text='Connect Database',command=connect_database)
connectbutton.place(x=980,y=5)

leftframe=Frame(root)
leftframe.place(x=40,y=70,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logo_label=Label(leftframe,image=logo_image)
logo_label.grid(row=0,column=0,pady=7)

addstudentbutton=ttk.Button(leftframe,text='Add Students',width=25,state=DISABLED,command=add_student)
addstudentbutton.grid(row=1,column=0,pady=16)

searchstudentbutton=ttk.Button(leftframe,text='Search Students',width=25,state=DISABLED,command=search_student)
searchstudentbutton.grid(row=2,column=0,pady=20)

deletestudentbutton=ttk.Button(leftframe,text=' Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentbutton.grid(row=3,column=0,pady=20)  

updatestudentbutton=ttk.Button(leftframe,text='Update Students',width=25,state=DISABLED,command=update_student)
updatestudentbutton.grid(row=4,column=0,pady=20)

showstudentbutton=ttk.Button(leftframe,text='Show Students',width=25,state=DISABLED,command=show_student )
showstudentbutton.grid(row=5,column=0,pady=20)

exportstudentbutton=ttk.Button(leftframe,text='Export data',width=25 ,state=DISABLED,command=export_data)
exportstudentbutton.grid(row=6,column=0,pady=20)

exitbutton=ttk.Button(leftframe,text='Exit',width=25,command=iexit )
exitbutton.grid(row=7,column=0,pady=20)

rightframe=Frame(root)
rightframe.place(x=350,y=80,width=820,height=600)

scrollbarX=Scrollbar(rightframe,orient=HORIZONTAL)
scrollbarY=Scrollbar(rightframe,orient=VERTICAL)

studenttable=ttk.Treeview(rightframe,columns=('Id','Name','Mobile','Email','Address','Gender','D.O.B',
                                 'Added Date','Added Time')
                                 ,xscrollcommand=scrollbarX.set,yscrollcommand=scrollbarY.set)
scrollbarX.config(command=studenttable.xview)
scrollbarY.config(command=studenttable.yview)
scrollbarX.pack(side=BOTTOM,fill=X)
scrollbarY.pack(side=RIGHT,fill=Y)
studenttable.pack(fill=BOTH,expand=1) 
studenttable.heading('Id',text='Id')
studenttable.heading('Name',text='Name')
studenttable.heading('Mobile',text='Mobile No')
studenttable.heading('Email',text='Email Address')
studenttable.heading('Address',text='Address')
studenttable.heading('Gender',text='Gender')
studenttable.heading('D.O.B',text='D.O.B')
studenttable.heading('Added Date',text='Added Date')
studenttable.heading('Added Time',text='Added Time')
studenttable.column('Id',width=50,anchor=CENTER)
studenttable.column('Name',width=300,anchor=CENTER)
studenttable.column('Mobile',width=200,anchor=CENTER)
studenttable.column('Email',width=300,anchor=CENTER)
studenttable.column('Address',width=300,anchor=CENTER)
studenttable.column('Gender',width=100,anchor=CENTER)
studenttable.column('D.O.B',width=100,anchor=CENTER)
studenttable.column('Added Date',width=100,anchor=CENTER)
studenttable.column('Added Time',width=100,anchor=CENTER)

style=ttk.Style()
style.configure('Treeview',roeheight=40,font=('arial','12'),foreground='red4')

studenttable.config(show='headings')
root.mainloop()