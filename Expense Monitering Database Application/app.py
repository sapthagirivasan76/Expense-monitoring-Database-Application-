import tkinter as  tk
from tkinter import  ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from tkinter import StringVar
import calendar
import  db

root =  tk.Tk()
root.title ("Sap expense moniter")
root.geometry ("1100x650")
root.configure(bg="#e5e3e7")

# ---------------------------- INPUT SECTION ----------
tk.Label(root, text="Date:", bg="#e9eef3").grid( row=0,column=0,  padx=10,   pady=5)

date_entry  = DateEntry(root, date_pattern="yyyy-mm-dd")
date_entry.grid( row=0, column=1)

tk.Label(root, text="Category:", bg="#e9eef3").grid(row=0,  column=2)
category_combo = ttk.Combobox(root, values=["Food",  "Travel", "Shopping", "billing" "Other"])
category_combo.grid(row=0, column=3)


tk.Label(root, text= "Amount:", bg="#e9eef3").grid(row=1, column=0)
amount_entry =   tk.Entry(root)
amount_entry.grid(row=1, column=1)

tk.Label(root, text="Description:", bg="#e9eef3").grid(row=1, column=2)
desc_entry  = tk.Entry(root, width=30)
desc_entry.grid(row= 1, column =3)

# ---------- FUNCTIONS -------------------------------------------
def load_data():
    for row in table.get_children():
        table.delete(row)
    for expense in db.fetch_expenses():
        table.insert("", "end", values=expense)

def add_expense():
    if not amount_entry.get() or not category_combo.get():
        messagebox.showwarning("Error",   "Fill all fields")
        return

    db.insert_expense(
        date_entry.get(),
        category_combo.get(),
        amount_entry.get(),
        desc_entry.get()
    )
    load_data()

def delete_expense():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Error", "Select an expense to delete")
        return

    expense_id = table.item(selected[0])["values"][0]
    db.delete_expense(expense_id)
    load_data()

def show_monthly_report():
    if not month_combo.get() or not year_combo.get():
        messagebox.showwarning("Error", "Select month and year")
        return
    
    total = db.monthly_total(month_combo.get(), year_combo.get())
    
    mon_num= int(month_combo.get())
    mon_name =  calendar.month_name[mon_num]
    
    result_var.set(f"Total Expense of the month {mon_name} is : ₹ {total}")

# --------------------------------------------------- BUTTONS -------------------------------------------
tk.Button(root, text=  "Add  Expense",
          bg= "green", fg="white", width=40,
          command=add_expense).grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(root, text=  "Delete Expense",
          bg="red", fg= "white", width=40,
          command=delete_expense).grid(row=2, column=2, columnspan=2)

# -------------------------------------------- TABLE ------------------------------------------------
columns = ("Id", "Date",  "Category", "Amount", "Description")
table = ttk.Treeview(root, columns =columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

table.grid(row=3, column= 0, columnspan=4, padx=10, pady=10, sticky="nsew")

# --------------------------------------------------------------------- MONTHLY REPORT ----------
tk.Label(root, text="Month:", bg= "#e9eef3").grid(row=4, column=0)
month_combo = ttk.Combobox(root, values=list(range(1,13)), width=5)
month_combo.grid(row= 4, column =1)

tk.Label(root, text= "Year:", bg="#e9eef3").grid(row= 4, column =2)
year_combo =  ttk.Combobox(root, values =[2024, 2025, 2026], width=8)
year_combo.grid(row =4, column=3)

tk.Button(root, text="View Monthly Report",
          bg="green", fg="white",
          command=show_monthly_report,
          width=20).grid(row=6, column= 0, columnspan =4, pady=10)


result_var = StringVar()
tk.Label(root, textvariable=result_var,
         font= ("Arial", 15, "bold"),
         bg ="#e9eef3").grid(row=8, column =0, columnspan=4)

load_data()
root.mainloop()
