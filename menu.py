from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from db.mongodb import mongodb

class DecanatMenu(tk.Tk): 
    def __init__(self):
        super().__init__()

        self.title("Decanat DataBase")
        self.geometry("600x450")
        self['bg'] = '#F2D0EC'
        
        #creating table
        self.table = ttk.Treeview(self)
        self.table['columns']= ('id', 'course','group', 'student', 'subject')
        self.table.column("#0", width=0,  stretch=tk.NO)
        self.table.column("id", anchor=tk.CENTER, width=80)
        self.table.column("course", anchor=tk.CENTER, width=50)
        self.table.column("group", anchor=tk.CENTER, width=50)
        self.table.column("student", anchor=tk.CENTER, width=200)
        self.table.column("subject", anchor=tk.CENTER, width=200)

        self.table.heading("id",text="ID студента")
        self.table.heading("course",text="Курс")
        self.table.heading("group",text="Група")
        self.table.heading("student",text="Прізвище та ім'я студента")
        self.table.heading("subject",text="Дисципліна")

        self.table.pack(pady=15)

        #counter for number of records
        self.count = 0
        records = mongodb.read()
        #filling the table
        for record in records:
            self.table.insert("", tk.END, values=record)
            self.count+=1       


        def open_add_win():
            self.win = tk.Tk()
            self.win.title('Додати студента...')
            self.win.geometry("350x150")
            self.win['bg'] = '#DFF0E9'

            #text boxes
            st_course = tk.Entry(self.win, width=30)
            st_course.grid(row=0, column=1, padx=20, pady=(10,0))
            st_group = tk.Entry(self.win, width=30)
            st_group.grid(row=1, column=1)
            st_name = tk.Entry(self.win, width=30)
            st_name.grid(row=2, column=1)
            st_subject = tk.Entry(self.win, width=30)
            st_subject.grid(row=3, column=1)

            #labels for text boxes
            st_course_label = tk.Label(self.win, text="Курс", bg='#DFF0E9')
            st_course_label.grid(row=0, column=0, padx=45, pady=(10,0))
            st_group_label = tk.Label(self.win, text="Група", bg='#DFF0E9')
            st_group_label.grid(row=1, column=0)
            st_name_label = tk.Label(self.win, text="Прізвище та ім\'я", bg='#DFF0E9')
            st_name_label.grid(row=2, column=0)
            st_subject_label = tk.Label(self.win, text="Дисципліна", bg='#DFF0E9')
            st_subject_label.grid(row=3, column=0)

            #function for adding
            def add_student():
                data = [self.count, st_course.get(), st_group.get(), st_name.get(), st_subject.get()]
                #clear the text boxes
                st_course.delete(0, tk.END)
                st_group.delete(0, tk.END)
                st_name.delete(0, tk.END)
                st_subject.delete(0, tk.END)
                
                error = False
                for el in data:
                    if el == "":
                        error = True
                    
                if error == False:
                    mongodb.create(1, data)
                    self.table.insert("", tk.END, values=data)
                    self.win.destroy()
                else:
                    self.win.destroy()
                    messagebox.showerror('ПОМИЛКА', 'Не коректно введені дані!')

            #save button
            self.add_btn = tk.Button(self.win, text="Додати", command=add_student)
            self.add_btn.grid(row=6, column=0, columnspan=2, padx=20, pady=10, ipadx=100)
        

        def open_update_win():
            selected = self.table.selection()
            for item in selected:
                _id = self.table.item(item, "values")[0]
            student = mongodb.get_student(_id)

            self.win_edit = tk.Tk()
            self.win_edit.title('Оновити інформацію...')
            self.win_edit.geometry("350x150")
            self.win_edit['bg'] = '#DFF0E9'

            #text boxes
            st_course = tk.Entry(self.win_edit, width=30)
            st_course.grid(row=0, column=1, padx=20, pady=(10,0))
            st_group = tk.Entry(self.win_edit, width=30)
            st_group.grid(row=1, column=1)
            st_name = tk.Entry(self.win_edit, width=30)
            st_name.grid(row=2, column=1)
            st_subject = tk.Entry(self.win_edit, width=30)
            st_subject.grid(row=3, column=1)

            #labels for text boxes
            st_course_label = tk.Label(self.win_edit, text="Курс", bg='#DFF0E9')
            st_course_label.grid(row=0, column=0, padx=45, pady=(10,0))
            st_group_label = tk.Label(self.win_edit, text="Група", bg='#DFF0E9')
            st_group_label.grid(row=1, column=0)
            st_name_label = tk.Label(self.win_edit, text="Прізвище та ім\'я", bg='#DFF0E9')
            st_name_label.grid(row=2, column=0)
            st_subject_label = tk.Label(self.win_edit, text="Дисципліна", bg='#DFF0E9')
            st_subject_label.grid(row=3, column=0)

            st_course.insert(0, student[1])
            st_group.insert(0, student[2])
            st_name.insert(0, student[3])
            st_subject.insert(0, student[4])
            
            #function for updating
            def update_student():
                data = [_id, st_course.get(), st_group.get(), st_name.get(), st_subject.get()]
                #clear the text boxes
                st_course.delete(0, tk.END)
                st_group.delete(0, tk.END)
                st_name.delete(0, tk.END)
                st_subject.delete(0, tk.END)
                
                error = False
                for el in data:
                    if el == "":
                        error = True
                    
                if error == False:
                    mongodb.update(data)
                    self.table.delete(item)
                    self.table.insert("", tk.END, values=data)
                    self.win_edit.destroy()
                else:
                    self.win_edit.destroy()
                    messagebox.showerror('ПОМИЛКА', 'Не коректно введені дані!')
            
            #save button
            self.add_btn = tk.Button(self.win_edit, text="Оновити", command=update_student)
            self.add_btn.grid(row=6, column=0, columnspan=2, padx=20, pady=10, ipadx=100)


        def open_next_table():
            self.win = tk.Tk()
            self.win.title('Table without subjects')
            self.win.geometry("600x350")
            self.win['bg'] = '#DFF0E9'

            #creating table
            self.table = ttk.Treeview(self.win)
            self.table['columns']= ('id', 'course','group', 'student')
            self.table.column("#0", width=0,  stretch=tk.NO)
            self.table.column("id", anchor=tk.CENTER, width=80)
            self.table.column("course", anchor=tk.CENTER, width=50)
            self.table.column("group", anchor=tk.CENTER, width=50)
            self.table.column("student", anchor=tk.CENTER, width=200)

            self.table.heading("id",text="ID студента")
            self.table.heading("course",text="Курс")
            self.table.heading("group",text="Група")
            self.table.heading("student",text="Прізвище та ім'я студента")
            self.table.pack(pady=15)

            #counter for number of records
            self.count = 0
            records1 = mongodb.read()
            for row in records1:
                mongodb.create(2, row[:4])
                self.table.insert("", tk.END, values=row[:4])
                self.count+=1   

        #function for deleting
        def delete_student():
            selected = self.table.selection()
            for item in selected:
                _id = self.table.item(item, "values")[0]
                self.table.delete(item)
                mongodb.delete(_id)             

        self.but_create = tk.Button(text="Додати студента", command=open_add_win)
        self.but_create.pack(pady=2, ipadx=74)
        self.but_update = tk.Button(text="Змінити дані студента", command=open_update_win)
        self.but_update.pack(pady=2, ipadx=59)
        self.but_delete = tk.Button(text="Видалити студента з бази", command=delete_student)
        self.but_delete.pack(pady=2, ipadx=50) 
        self.but_sqlite = tk.Button(text="Відкрити наступну таблицю", command=open_next_table)
        self.but_sqlite.pack(pady=2, ipadx=50) 
         
if __name__ == "__main__":
    app = DecanatMenu()
    app.mainloop()