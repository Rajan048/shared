from tkinter import *
from tkinter import messagebox
import sqlite3

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login | Student Result Management System")
        self.root.geometry("400x500+500+150")
        self.root.config(bg="white")

        self.username = StringVar()
        self.password = StringVar()

        Label(self.root, text="Login", font=("goudy old style", 25, "bold"), bg="white", fg="#333").pack(pady=30)

        Label(self.root, text="Username", font=("goudy old style", 15), bg="white").pack(pady=5)
        Entry(self.root, textvariable=self.username, font=("goudy old style", 15), bg="lightyellow").pack(pady=5, ipadx=10)

        Label(self.root, text="Password", font=("goudy old style", 15), bg="white").pack(pady=5)
        Entry(self.root, textvariable=self.password, font=("goudy old style", 15), bg="lightyellow", show="*").pack(pady=5, ipadx=10)

        Button(self.root, text="Login", font=("goudy old style", 15, "bold"),
               bg="#03a9f4", fg="white", cursor="hand2", command=self.login).pack(pady=20)

        Button(self.root, text="Register New Account", font=("goudy old style", 12),
               bg="white", fg="green", bd=0, cursor="hand2", command=self.register_window).pack()

        Button(self.root, text="Forgot Password?", font=("goudy old style", 12),
               bg="white", fg="red", bd=0, cursor="hand2", command=self.forgot_password_window).pack(pady=10)

        self.init_db()

    def init_db(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cur.execute("SELECT * FROM users WHERE username=?", ("admin",))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        con.commit()
        con.close()

    def login(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            if self.username.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM users WHERE username=? AND password=?", (self.username.get(), self.password.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Login Successful", parent=self.root)
                    self.root.destroy()
                    from report import reportClass
                    root = Tk()
                    reportClass(root)
                    root.mainloop()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def register_window(self):
        self.reg_win = Toplevel(self.root)
        self.reg_win.title("Register")
        self.reg_win.geometry("400x300+520+200")
        self.reg_win.config(bg="white")

        self.reg_username = StringVar()
        self.reg_password = StringVar()

        Label(self.reg_win, text="Register New Account", font=("goudy old style", 18, "bold"), bg="white", fg="#333").pack(pady=20)

        Label(self.reg_win, text="Username", font=("goudy old style", 14), bg="white").pack()
        Entry(self.reg_win, textvariable=self.reg_username, font=("goudy old style", 14), bg="lightyellow").pack(pady=5)

        Label(self.reg_win, text="Password", font=("goudy old style", 14), bg="white").pack()
        Entry(self.reg_win, textvariable=self.reg_password, font=("goudy old style", 14), bg="lightyellow", show="*").pack(pady=5)

        Button(self.reg_win, text="Register", font=("goudy old style", 14, "bold"), bg="#4caf50", fg="white",
               command=self.register_user).pack(pady=20)

    def register_user(self):
        if self.reg_username.get() == "" or self.reg_password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.reg_win)
            return
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.reg_username.get(), self.reg_password.get()))
            con.commit()
            messagebox.showinfo("Success", "Registration Successful", parent=self.reg_win)
            self.reg_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists", parent=self.reg_win)
        finally:
            con.close()

    def forgot_password_window(self):
        self.forget_win = Toplevel(self.root)
        self.forget_win.title("Forgot Password")
        self.forget_win.geometry("400x250+520+220")
        self.forget_win.config(bg="white")

        self.reset_username = StringVar()
        self.new_password = StringVar()

        Label(self.forget_win, text="Reset Password", font=("goudy old style", 18, "bold"), bg="white", fg="#333").pack(pady=20)

        Label(self.forget_win, text="Username", font=("goudy old style", 14), bg="white").pack()
        Entry(self.forget_win, textvariable=self.reset_username, font=("goudy old style", 14), bg="lightyellow").pack(pady=5)

        Label(self.forget_win, text="New Password", font=("goudy old style", 14), bg="white").pack()
        Entry(self.forget_win, textvariable=self.new_password, font=("goudy old style", 14), bg="lightyellow", show="*").pack(pady=5)

        Button(self.forget_win, text="Reset", font=("goudy old style", 14, "bold"), bg="#f44336", fg="white",
               command=self.reset_password).pack(pady=15)

    def reset_password(self):
        con = sqlite3.connect("rms.db")
        cur = con.cursor()
        try:
            if self.reset_username.get() == "" or self.new_password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.forget_win)
            else:
                cur.execute("SELECT * FROM users WHERE username=?", (self.reset_username.get(),))
                if cur.fetchone() is None:
                    messagebox.showerror("Error", "Username not found", parent=self.forget_win)
                else:
                    cur.execute("UPDATE users SET password=? WHERE username=?", (self.new_password.get(), self.reset_username.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Password updated", parent=self.forget_win)
                    self.forget_win.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.forget_win)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()
