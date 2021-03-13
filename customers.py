import tkinter as tk
import sqlite3
import time
from tkinter.constants import END
from tkinter import messagebox
from tkinter.ttk import *


    
class MyApp():
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Customers Data")
        self.app.geometry("800x600") #ขนาดหน้าจอ
        self.app.resizable(width=False, height=False) #ล็อคขนาดหน้าจอ

        #Frame1
        self.frame1 = Frame(self.app)
        self.frame1.grid(row=0, column=0)

        #Frame1 Text
        self.text_main = Label(self.frame1, text="Customers Data")
        self.text_id = Label(self.frame1, text="ID")
        self.text_fname = Label(self.frame1, text="Frist Name")
        self.text_lname = Label(self.frame1, text="Last Name")
        self.text_tel = Label(self.frame1, text="Phone Number")
        self.text_idd = Label(self.frame1, text="00")
        #Frame1 Entry
        self.ent_fname = Entry(self.frame1, textvariable=tk.StringVar) #ให้ข้อความใน Entry เป็น String
        self.ent_lname = Entry(self.frame1, textvariable=tk.StringVar)
        self.ent_tel = Entry(self.frame1, textvariable=tk.StringVar)
        #Frame1 Button
        self.btn_submit = Button(self.frame1, text="Submit", command=self.insert_data)
        self.btn_delete = Button(self.frame1, text="Delete", command=self.delete_data)
        self.btn_update = Button(self.frame1, text="Edit", command=self.update_data)
        self.btn_exit = Button(self.frame1, text="Exit", command=self.close)

        #Table detail
        self.datat = Treeview(self.app, columns=("id", "fname", "lname", "tel"), show="headings", height=20)
        self.datat.heading("id", text="ID")#ตั้งชื่อหัวตาราง
        self.datat.heading("fname", text="ชื่อ") #ตั้งชื่อหัวตาราง
        self.datat.heading("lname", text="นามสกุล")#ตั้งชื่อหัวตาราง
        self.datat.heading("tel", text="เบอร์โทร")#ตั้งชื่อหัวตาราง
        self.datat.bind("<Double-1>", self.treeDoubleclick) #doubleclick on tree

        #Layout
        self.text_main.grid(row=0, column=0, padx=15, pady=15,columnspan=5)
        self.text_id.grid(row=1, column=0, padx=15, pady=15)
        self.text_idd.grid(row=1, column=1, padx=15, pady=15)
        self.text_fname.grid(row=1, column=2, padx=15, pady=15)
        self.ent_fname.grid(row=1, column=3, padx=15, pady=15)
        self.text_lname.grid(row=2, column=0, padx=15, pady=15)
        self.ent_lname.grid(row=2, column=1, padx=15, pady=15)
        self.text_tel.grid(row=2, column=2, padx=15, pady=15)
        self.ent_tel.grid(row=2, column=3, padx=15, pady=15)
        self.btn_submit.grid(row=3, column=0, padx=5, pady=5)
        self.btn_delete.grid(row=3, column=1, padx=5, pady=5)
        self.btn_update.grid(row=3, column=2, padx=5, pady=5)
        self.btn_exit.grid(row=3, column=3, padx=5,pady=5)
        self.datat.grid(row=10, column=0, rowspan=5, pady=30)

        #start wit fn
        self.create_db()
        self.select_data()
        self.app.mainloop()

    def insert_data(self):
        self.btn_submit['state'] = "disabled" #ปิดปุ่ม
        with sqlite3.connect("customers.sqlite") as con:
            fname = self.ent_fname.get()
            lname = self.ent_lname.get()
            tel = self.ent_tel.get()
            mdata = (fname, lname, tel)
            if fname == "" or lname == "" or tel == "":
                self.errorB() # โชวกล่องข้อความว่า Error
                self.app.after(500, self.select_data) #refresh
                self.app.after(1000, self.enable_btn) #เปิดปุ่ม
            else:
                sql_cmd = """
                insert into customers(fname, lname, tel) values(?, ?, ?);
                """
                con.execute(sql_cmd, mdata)
                self.app.after(500, self.select_data) #refresh
                self.app.after(1000, self.enable_btn) #เปิดปุ่ม    
                self.zero_all()  #ล้างกล่องข้อความ          
        
    def delete_data(self): #ลบข้อมูลตาม id
        self.btn_delete['state'] = "disabled"
        id = self.text_idd['text']
        with sqlite3.connect("customers.sqlite") as con:
            if self.ent_fname.get() == "" or self.ent_lname.get() == "" or self.ent_tel.get() == "":
                self.errorB() # โชวกล่องข้อความว่า Error
                self.app.after(500, self.select_data) #refresh
                self.app.after(1000, self.enable_btn) #เปิดปุ่ม
            else:
                sql_cmd = """
                delete from customers where id = ?
                """
                con.execute(sql_cmd, (id,))
                self.app.after(500, self.select_data) #refresh
                self.app.after(1000, self.enable_btn) #เปิดปุ่ม
                self.zero_all()  #ล้างกล่องข้อความ    
        
    def update_data(self):
        self.btn_update['state'] = "disabled"
        id = self.text_idd['text']
        fname = self.ent_fname.get()
        lname = self.ent_lname.get()
        tel = self.ent_tel.get()
        with sqlite3.connect("customers.sqlite") as con:
            if fname == "" or lname == "" or tel == "":
                self.errorB() # โชวกล่องข้อความว่า Error
                self.app.after(500, self.select_data) #refresh
                self.app.after(1000, self.enable_btn) #เปิดปุ่ม
            else:
                sql_cmd = """
                update customers set fname = ?, lname = ?, tel = ? where id = ?
                """
                con.execute(sql_cmd, (fname, lname, tel, id))
                self.app.after(500, self.select_data) #refresh
                self.app.after(1000, self.enable_btn) #เปิดปุ่ม
                self.zero_all()  #ล้างกล่องข้อความ
        
    def select_data(self):
        self.delete_tree()
        with sqlite3.connect("customers.sqlite") as con:
            sql_cmd = """
            select * from customers
            """
            for row in con.execute(sql_cmd):
                self.datat.insert("","end",values=row)
                

                
    def delete_tree(self):  # ลบข้อมูลใน treeview
        x = self.datat.get_children();
        for i in x:
            self.datat.delete(i)
                
    def treeDoubleclick(self, event): #event? Double click Table
        select = self.datat.item(self.datat.selection()[0]) #select data in treeview
        #print(select['values'])
        self.text_idd.configure(text=select['values'][0]) #แก้ id
        #self.ent_id.delete(0, END) #ลบข้อความใน Entry
        self.ent_fname.delete(0, END) #ลบข้อความใน Entry
        self.ent_lname.delete(0, END) #ลบข้อความใน Entry
        self.ent_tel.delete(0, END) #ลบข้อความใน Entry
        #self.ent_id.insert(0, select['values'][0]) #เพิ่มข้อความ ตำแหน่ง, ข้อความ
        self.ent_fname.insert(0, select['values'][1]) #เพิ่มข้อความ ตำแหน่ง, ข้อความ
        self.ent_lname.insert(0, select['values'][2]) #เพิ่มข้อความ ตำแหน่ง, ข้อความ
        self.ent_tel.insert(0, "0" + str(select['values'][3])) #เพิ่มข้อความ ตำแหน่ง, ข้อความ

    #fn ย่อยๆ
    def close(self):
        exit()        
    def errorB(self): 
        self.ermb = messagebox.showerror("Eror", "This is A Error") #กล่อง Error

    def enable_btn(self): #เปิดใช้งานปุ่ม
        self.btn_submit['state'] = "enable" #เปิดปุ่ม    
        self.btn_delete['state'] = "enable"
        self.btn_update['state'] = "enable"
        
    def zero_all(self): #ล้างกล่องข้อความ    
        self.text_idd.configure(text="00")
        self.ent_fname.delete(0, END) #ลบข้อความใน Entry
        self.ent_lname.delete(0, END) #ลบข้อความใน Entry
        self.ent_tel.delete(0, END) #ลบข้อความใน Entry
    
    def create_db(self):
        with sqlite3.connect("customers.sqlite") as con:
            sql_cmd = """
                CREATE TABLE IF NOT EXISTS "customers" (
            "id"	INTEGER,
            "fname"	TEXT NOT NULL,
            "lname"	TEXT NOT NULL,
            "tel"	TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
            con.execute(sql_cmd)

if __name__ == "__main__":
    app = MyApp()

