import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

# Connection for MySQL server
def connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ktembhe@12',
            database='student_db'
        )
        return conn
    except Error as e:
        messagebox.showinfo("Error", "Failed to connect to MySQL server")
        return None

def createDatabaseAndTables():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS students_db")
            cursor.execute("USE students_db")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    STUDID VARCHAR(10) PRIMARY KEY,
                    FNAME VARCHAR(50),
                    LNAME VARCHAR(50),
                    ADDRESS VARCHAR(100),
                    PHONE VARCHAR(15)
                )
            """)
            conn.commit()
            conn.close()
        except Error as e:
            messagebox.showinfo("Error", "Failed to create database and tables")
    else:
        messagebox.showinfo("Error", "Failed to connect to MySQL server")


createDatabaseAndTables()


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

root = Tk()
root.title("Student Registration System")
root.geometry("800x720")
my_tree = ttk.Treeview(root)

# Placeholders for entry
ph1 = tk.StringVar()
ph2 = tk.StringVar()
ph3 = tk.StringVar()
ph4 = tk.StringVar()
ph5 = tk.StringVar()

# Placeholder set value function
def setph(word,num):
    if num ==1:
        ph1.set(word)
    if num ==2:
        ph2.set(word)
    if num ==3:
        ph3.set(word)
    if num ==4:
        ph4.set(word)
    if num ==5:
        ph5.set(word)

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    conn.close()
    return results

def add():
    studid = str(studidEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    address = str(addressEntry.get())
    phone = str(phoneEntry.get())

    if (studid == "" or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (address == "" or address == " ") or (phone == "" or phone == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (STUDID, FNAME, LNAME, ADDRESS, PHONE) VALUES (%s, %s, %s, %s, %s)",
                           (studid, fname, lname, address, phone))
            conn.commit()
            conn.close()
        except mysql.connector.Error as error:
            messagebox.showinfo("Error", f"Stud ID already exists. {error}")
            return

    refreshTable()

def reset():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return 
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

        refreshTable()

def delete():
    decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
    if decision != "yes":
        return 
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE STUDID='"+str(deleteData)+"'")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

        refreshTable()

def select():
    try:
        selected_item = my_tree.selection()[0]
        studid = str(my_tree.item(selected_item)['values'][0])
        fname = str(my_tree.item(selected_item)['values'][1])
        lname = str(my_tree.item(selected_item)['values'][2])
        address = str(my_tree.item(selected_item)['values'][3])
        phone = str(my_tree.item(selected_item)['values'][4])

        setph(studid,1)
        setph(fname,2)
        setph(lname,3)
        setph(address,4)
        setph(phone,5)
    except:
        messagebox.showinfo("Error", "Please select a data row")

def search():
    studid = str(studidEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    address = str(addressEntry.get())
    phone = str(phoneEntry.get())

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE STUDID='"+
    studid+"' or FNAME='"+
    fname+"' or LNAME='"+
    lname+"' or ADDRESS='"+
    address+"' or PHONE='"+
    phone+"' ")
    
    try:
        result = cursor.fetchall()

        for num in range(0,5):
            setph(result[0][num],(num+1))

        conn.commit()
        conn.close()
    except:
        messagebox.showinfo("Error", "No data found")

def update():
    selectedStudid = ""

    try:
        selected_item = my_tree.selection()[0]
        selectedStudid = str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data row")

    studid = str(studidEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    address = str(addressEntry.get())
    phone = str(phoneEntry.get())

    if (studid == "" or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (address == "" or address == " ") or (phone == "" or phone == " "):
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET STUDID='"+
            studid+"', FNAME='"+
            fname+"', LNAME='"+
            lname+"', ADDRESS='"+
            address+"', PHONE='"+
            phone+"' WHERE STUDID='"+
            selectedStudid+"' ")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error", "Stud ID already exist")
            return

    refreshTable()

label = Label(root, text="Student Registration System ", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=3, pady=40)

studidLabel = Label(root, text="Stud ID", font=('Arial', 12))
fnameLabel = Label(root, text="Firstname", font=('Arial', 12))
lnameLabel = Label(root, text="Lastname", font=('Arial', 12))
addressLabel = Label(root, text="Address", font=('Arial', 12))
phoneLabel = Label(root, text="Phone", font=('Arial', 12))


studidLabel.grid(row=1, column=0, padx=10, pady=5)
fnameLabel.grid(row=2, column=0, padx=10, pady=5)
lnameLabel.grid(row=3, column=0, padx=10, pady=5)
addressLabel.grid(row=4, column=0, padx=10, pady=5)
phoneLabel.grid(row=5, column=0, padx=10, pady=5)

studidEntry = Entry(root, width=30, bd=3, font=('Arial', 12), textvariable = ph1)
fnameEntry = Entry(root, width=30, bd=3, font=('Arial', 12), textvariable = ph2)
lnameEntry = Entry(root, width=30, bd=3, font=('Arial', 12), textvariable = ph3)
addressEntry = Entry(root, width=30, bd=3, font=('Arial', 12), textvariable = ph4)
phoneEntry = Entry(root, width=30, bd=3, font=('Arial', 12), textvariable = ph5)

studidEntry.grid(row=1, column=1, padx=10, pady=5)
fnameEntry.grid(row=2, column=1, padx=10, pady=5)
lnameEntry.grid(row=3, column=1, padx=10, pady=5)
addressEntry.grid(row=4, column=1, padx=10, pady=5)
phoneEntry.grid(row=5, column=1, padx=10, pady=5)

addBtn = Button(
    root, text="Add", padx=15, pady=5, width=10,
    bd=3, font=('Arial', 15), bg="#64c8f0", command=add)
updateBtn = Button(
    root, text="Update", padx=10, pady=5, width=10,
    bd=3, font=('Arial', 15), bg="#64c8f0", command=update)
deleteBtn = Button(
    root, text="Delete", padx=10, pady=5, width=10,
    bd=3, font=('Arial', 15), bg="#64c8f0", command=delete)
searchBtn = Button(
    root, text="Search", padx=10, pady=5, width=10,
    bd=3, font=('Arial', 15), bg="#64c8f0", command=search)
resetBtn = Button(
    root, text="Reset", padx=10, pady=5, width=10,
    bd=3, font=('Arial', 15), bg="#64c8f0", command=reset)
selectBtn = Button(
    root, text="Select", padx=10, pady=5, width=10,
    bd=3, font=('Arial', 15), bg="#64c8f0", command=select)

addBtn.grid(row=1, column=2, padx=10, pady=5)
updateBtn.grid(row=2, column=2, padx=10, pady=5)
deleteBtn.grid(row=3, column=2, padx=10, pady=5)
searchBtn.grid(row=4, column=2, padx=10, pady=5)
resetBtn.grid(row=5, column=2, padx=10, pady=5)
selectBtn.grid(row=6, column=2, padx=10, pady=5)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 15))

my_tree['columns'] = ("Stud ID","Firstname","Lastname","Address","Phone")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Stud ID", anchor=W, width=150)
my_tree.column("Firstname", anchor=W, width=150)
my_tree.column("Lastname", anchor=W, width=150)
my_tree.column("Address", anchor=W, width=150)
my_tree.column("Phone", anchor=W, width=150)

my_tree.heading("Stud ID", text="Student ID", anchor=W)
my_tree.heading("Firstname", text="Firstname", anchor=W)
my_tree.heading("Lastname", text="Lastname", anchor=W)
my_tree.heading("Address", text="Address", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=W)

refreshTable()

root.mainloop()
