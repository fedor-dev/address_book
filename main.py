import sqlite3
from random import randint
import tkinter as tk
import ttkbootstrap as ttk
import tkinter.messagebox
from tkinter import simpledialog, messagebox


class AddWin(simpledialog.Dialog):
    def __init__(self, master, title, lname=None, name=None, fname=None, phone=None, email=None, prim=None):
        self.lname = tk.StringVar(value=lname)
        self.name = tk.StringVar(value=name)
        self.fname = tk.StringVar(value=fname)
        self.phone = tk.StringVar(value=phone)
        self.email = tk.StringVar(value=email)
        self.prim = tk.StringVar(value=prim)
        self.result_ok = False
        super(AddWin, self).__init__(master, title=title)

    def body(self, master):
        self.wrap_fr = ttk.Frame(self)
        self.wrap_fr.columnconfigure(1, weight=1)
        self.wrap_fr.pack(expand=True, fill=tk.BOTH)
        self.lbl_lname = ttk.Label(self.wrap_fr, text='Last Name')
        self.lbl_name = ttk.Label(self.wrap_fr, text='Name')
        self.lbl_fname = ttk.Label(self.wrap_fr, text='Middle Name')
        self.lbl_phone = ttk.Label(self.wrap_fr, text='Phone')
        self.lbl_email = ttk.Label(self.wrap_fr, text='E-mail')

        self.ent_lname = ttk.Entry(self.wrap_fr, textvariable=self.lname)
        self.ent_name = ttk.Entry(self.wrap_fr, textvariable=self.name)
        self.ent_fname = ttk.Entry(self.wrap_fr, textvariable=self.fname)
        self.ent_phone = ttk.Entry(self.wrap_fr, textvariable=self.phone)
        self.ent_email = ttk.Entry(self.wrap_fr, textvariable=self.email)

        self.lbl_lname.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.lbl_name.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.lbl_fname.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.lbl_phone.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.lbl_email.grid(row=4, column=0, padx=5, pady=5, sticky='e')

        self.ent_lname.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        self.ent_name.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        self.ent_fname.grid(row=2, column=1, padx=5, pady=5, sticky='we')
        self.ent_phone.grid(row=3, column=1, padx=5, pady=5, sticky='we')
        self.ent_email.grid(row=4, column=1, padx=5, pady=5, sticky='we')

        self.prim_fr = ttk.LabelFrame(self.wrap_fr, text='Notes')
        self.prim_area = tk.Text(self.prim_fr, width=50, height=10)
        self.prim_scroll = ttk.Scrollbar(self.prim_fr, command=self.prim_area.yview)
        self.prim_area.configure(yscrollcommand=self.prim_scroll.set)
        self.prim_fr.grid(row=5, column=0, columnspan=2, padx=5)
        self.prim_area.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.prim_scroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.prim_area.insert('1.0', self.prim.get())

        self.focus_set()
        self.prim_area.focus_force()

    def buttonbox(self):
        self.fr_buttons = ttk.Frame(self.wrap_fr, border=1, relief='groove')
        self.fr_buttons.columnconfigure(0, weight=1)
        self.fr_buttons.columnconfigure(1, weight=1)
        self.fr_buttons.grid(row=6, column=0, columnspan=2, sticky='we')

        self.btn_ok = ttk.Button(self.fr_buttons, text='save', command=self.ok_pressed)
        self.btn_cancel = ttk.Button(self.fr_buttons, text='cancel', command=self.cancel_pressed)
        self.btn_ok.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.btn_cancel.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    def ok_pressed(self):
        self.lname = self.lname.get()
        self.name = self.name.get()
        self.fname = self.fname.get()
        self.phone = self.phone.get()
        self.email = self.email.get()
        self.prim = self.prim_area.get('1.0', 'end-1c')
        self.result_ok = True
        self.destroy()

    def cancel_pressed(self):
        self.lname = self.lname.get()
        self.name = self.name.get()
        self.fname = self.fname.get()
        self.phone = self.phone.get()
        self.email = self.email.get()
        self.prim = self.prim_area.get('1.0', 'end-1c')
        self.result_ok = False
        self.destroy()


class DBconect:
    def __enter__(self):
        self.con = sqlite3.connect('addressbook.db')
        self.cur = self.con.cursor()
        return self

    def __init__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.cur.close()
        self.con.close()


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename='vapor')
        self.title('addressbook')
        self.geometry('1600x900')

        self.to_search = tk.StringVar()
        self.contacts_count = tk.StringVar()
        self.themename = tk.StringVar(value='vapor')

        self.fr = ttk.Frame(self, border=1, relief='ridge')
        self.btn_add = ttk.Button(self.fr, text='add', command=self.add_contact)
        self.btn_mod = ttk.Button(self.fr, text='change', command=self.mod_contact)
        self.btn_rm = ttk.Button(self.fr, text='remove', command=self.rm_contact)
        # self.fr_1 = ttk.Frame(self.fr, border=1, padx=10, pady=10, ipadx=10, ipady=10)
        # self.tem_1 = ttk.Radiobutton(self.fr_1, text='simplex', command=lambda: self.themename='simplex')

        themenames = ['solar', 'superhero', 'darkly', 'cyborg', 'vapor', 'cosmo', 'flatly', 'journal', 'litera',
                      'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
        self.themes_combobox = ttk.Combobox(self.fr, values=themenames, textvariable=self.themename)
        self.themes_combobox.bind('<<ComboboxSelected>>', lambda e: self.style.theme_use(self.themename.get()))

        self.ent_search = ttk.Entry(self.fr, width=30, textvariable=self.to_search)
        self.lbl_search = ttk.Label(self.fr, text='search')

        self.data_fr = ttk.Frame(self)
        self.data_columns = ('id', 'lname', 'name', 'fname', 'phone', 'email', 'prim')
        self.data_view = ttk.Treeview(self.data_fr, show='headings', columns=self.data_columns)
        self.data_scroll = ttk.Scrollbar(self.data_fr, command=self.data_view.yview, orient=tk.VERTICAL)
        self.data_view.configure(yscrollcommand=self.data_scroll.set)
        self.data_view['displaycolumns']=self.data_columns[1:]
        self.data_view.heading('lname', text='Last name')
        self.data_view.heading('name', text='Name')
        self.data_view.heading('fname', text='Middle name')
        self.data_view.heading('phone', text='Phone')
        self.data_view.heading('email', text='E-mail')
        self.data_view.heading('prim', text='Notes')

        self.footer_frame = ttk.Frame(self, border=1, relief='groove')
        self.lbl_count = ttk.Label(self.footer_frame, textvariable=self.contacts_count)

        self.fr.pack(padx=10, pady=10, ipadx=10, ipady=10, fill=tk.X)
        for i in (self.btn_add, self.btn_mod, self.btn_rm):
            i.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=5)
        self.themes_combobox.pack(side=tk.LEFT, padx=10, pady=10)
        self.ent_search.pack(side=tk.RIGHT, padx=10)
        self.lbl_search.pack(side=tk.RIGHT)

        self.data_fr.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.data_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.data_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.fill_data_view(self.get_all_db_data())
        self.footer_frame.pack(padx=10, pady=10, fill=tk.X)
        self.lbl_count.pack(side=tk.RIGHT, padx=10, pady=10)


        self.bind('<Escape>', lambda e: self.on_close())
        self.ent_search.focus()


        self.to_search.trace_add('write', callback=self.do_search)

    def mod_contact(self, e=None):

        to_mod = self.data_view.selection()
        if to_mod and len(to_mod) == 1:
            item_values = self.data_view.item(to_mod[0], 'values')
            mod_win = AddWin(self, title='change contact', lname=item_values[1], name=item_values[2],
                             fname=item_values[3], phone=item_values[4], email=item_values[5], prim=item_values[6])
            if mod_win.result_ok and ((mod_win.lname, mod_win.name, mod_win.fname, mod_win.phone, mod_win.email, mod_win.prim) != item_values[1:]):
                sql = '''
                UPDATE people 
                SET
                lname=?,
                name=?,
                fname=?,
                phone=?,
                email=?,
                prim=?
                WHERE id=?
                '''
                with DBconect() as db:
                    db.cur.execute(sql, (mod_win.lname, mod_win.name, mod_win.fname, mod_win.phone,
                                         mod_win.email, mod_win.prim, item_values[0]))
                if self.to_search.get():
                    self.fill_data_view(self.get_db_search(self.to_search.get()))
                else:
                    self.fill_data_view(self.get_all_db_data())
        else:
            messagebox.showinfo(message='choose one contact please')

    def do_search(self, var, ind, mod):
        people = self.get_db_search(self.to_search.get())
        self.fill_data_view(people)

    def on_close(self):
        answer = tkinter.messagebox.askyesno(title='close window', message='do you want to exit?')
        if answer:
            self.destroy()

    def get_all_db_data(self):
        sql = 'SELECT * FROM people ORDER BY lname'
        res = []
        with DBconect() as db:
            db.cur.execute(sql)
            res = db.cur.fetchall()
        return res

    def fill_data_view(self, people):
        self.data_view.delete(*self.data_view.get_children())
        for man in people:
            self.data_view.insert('', 'end', values=man)
        with DBconect() as db:
            sql = 'SELECT COUNT(*) FROM people '
            db.cur.execute(sql)
            res = db.cur.fetchone()[0]
            self.contacts_count.set(value=f'total contacts: {res}')

    def add_contact(self):
        add_win = AddWin(self, title='Add new contact')
        if add_win.result_ok and any((add_win.fname, add_win.name, add_win.lname)):
            sql = f'''INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)'''
            with DBconect() as db:
                db.cur.execute(sql, (None, add_win.lname, add_win.name, add_win.fname, add_win.phone,
                                     add_win.email, add_win.prim))
            if self.to_search.get():
                self.fill_data_view(self.get_db_search(self.to_search.get()))
            else:
                self.fill_data_view(self.get_all_db_data())
        elif any((add_win.phone, add_win.email, add_win.prim)) and isinstance(add_win.fname, str):
            messagebox.showinfo(message='You need enter last name, name or middle name')

    def get_db_search(self, s):
        s = s.capitalize()
        sql = f'''SELECT * FROM people WHERE lname LIKE "{s}%" ORDER BY lname'''
        with DBconect() as db:
            db.cur.execute(sql)
            res = db.cur.fetchall()
        return res

    def rm_contact(self):
        to_remove = self.data_view.selection()
        if to_remove:
            answer = tkinter.messagebox.askyesno(title='remove contacts', message='do you want to remove selected contacts?')
            if answer:
                with DBconect() as db:
                    for item in to_remove:
                        sql = 'DELETE FROM people WHERE id = ? '
                        item_values = self.data_view.item(item, 'values')
                        db.cur.execute(sql, (item_values[0],))
                if self.to_search.get():
                    self.fill_data_view(self.get_db_search(self.to_search.get()))
                else:
                    self.fill_data_view(self.get_all_db_data())
        else:
            tkinter.messagebox.showinfo(message='select contacts to remove')


def dbcreate():
    sql = """
    CREATE TABLE IF NOT EXISTS people (
        id integer primary key autoincrement,
        lname text,
        name text,
        fname text,
        phone text, 
        email text,
        prim text
    );
    """
    with DBconect() as db:
        db.cur.execute(sql)


def gen_date():
    try:
        with open('names.txt', encoding='utf-8') as f:
            people = []
            for fio in f:
                fio = fio.split()
                nums = [str(randint(0, 9)) for i in range(10)]
                phone = f"+1-{''.join(nums[:3])}-{''.join(nums[3:6])}-{''.join(nums[6:8])}-{''.join(nums[8:])}"
                email = 'fedy@gamil.tu'
                man = [fio[0], fio[1], fio[2], phone, email, '']
                people.append(man)
            with DBconect() as db:
                sql = "INSERT INTO people VALUES (?,?,?,?,?,?,?)"
                for man in people:
                    db.cur.execute(sql, [None]+man)
            return people
    except Exception as e:
        print(e)
        exit()


if __name__ == '__main__':
    dbcreate()
    # gen_date()
    app = App()
    app.mainloop()