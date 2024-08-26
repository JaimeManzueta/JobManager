from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import time
import smtplib
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd






# Main GUI
GUI = Tk()
GUI.title('Job Management System')
GUI.geometry('1000x700')
GUI.resizable(False, False)
primary_color = '#3E4E5E'  # Dark blue for frames
secondary_color = '#F0F0F0'  # Light grey for the main window background
button_color = '#D1E0E0'  # Light blue for buttons

GUI.configure(bg=secondary_color)
 
# Global variables for cursor and database connection
cur = None
db = None
  
# Colors
primary_color = '#3E4E5E'  # Dark blue for frames
secondary_color = '#F0F0F0'  # Light grey for the main window background
button_color = '#D1E0E0'  # Light blue for buttons

def connectdb():
    def connect():
        global cur, db
        try:
            # Connect to the database
            db = mysql.connector.connect(
                host=hostEntry.get(),
                user=userEntry.get(),
                password=passwordEntry.get()
            )
            cur = db.cursor()
            messagebox.showinfo('Success', 'Connected to database')

            # Create the database and use it
            cur.execute("CREATE DATABASE IF NOT EXISTS jobmanager")
            cur.execute("USE jobmanager")

            # Create the table if it doesn't exist
            query = """
            CREATE TABLE IF NOT EXISTS jobmanager(
                id INTEGER PRIMARY KEY AUTO_INCREMENT, 
                ProspectName VARCHAR(255), 
                Email VARCHAR(255), 
                DateRetrieved DATE, 
                Result VARCHAR(255)
            )
            """
            cur.execute(query)
            db.commit()

            # Fetch and display data
            data_retrieved()

            # Close the connection window
            connwindow.destroy()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    # Create and configure the connection window
    connwindow = Toplevel()
    connwindow.grab_set()
    connwindow.geometry("430x250")
    connwindow.title("Database Connection")
    connwindow.configure(bg=primary_color)  # Set background color to primary_color

    label_font = ('arial', 12, 'bold')
    entry_font = ('roman', 12, 'bold')

    # Host Name
    hostnameLabel = Label(connwindow, text='Host Name', font=label_font, bg=primary_color, fg='white')
    hostnameLabel.grid(row=0, column=0, pady=15, padx=10, sticky=E)
    hostEntry = Entry(connwindow, font=entry_font, bd=2, bg=secondary_color)  # Set background color to secondary_color
    hostEntry.grid(row=0, column=1, padx=10, pady=10)

    # User Name
    usernameLabel = Label(connwindow, text='User Name', font=label_font, bg=primary_color, fg='white')
    usernameLabel.grid(row=1, column=0, pady=15, padx=10, sticky=E)
    userEntry = Entry(connwindow, font=entry_font, bd=2, bg=secondary_color)  # Set background color to secondary_color
    userEntry.grid(row=1, column=1, padx=10, pady=10)

    # Password
    passwordLabel = Label(connwindow, text='Password', font=label_font, bg=primary_color, fg='white')
    passwordLabel.grid(row=2, column=0, pady=15, padx=10, sticky=E)
    passwordEntry = Entry(connwindow, font=entry_font, bd=2, show='*', bg=secondary_color)  # Set background color to secondary_color
    passwordEntry.grid(row=2, column=1, padx=10, pady=10)

    # Connect Button
    connectButton = Button(connwindow, text='Connect', font=('arial', 12, 'bold'), command=connect, bg=button_color, fg='black')
    connectButton.grid(row=3, column=0, columnspan=2, pady=20)


def add_button():
    global Topwindowentry, Midtopwindowentry, Bottomewindowentry, Lastwindowentry

    connectwindow = Toplevel()
    connectwindow.geometry('400x320')
    connectwindow.title('Add Prospect')
    connectwindow.resizable(False, False)
    connectwindow.configure(bg=secondary_color)

    label_font = ('arial', 11, 'bold')
    entry_font = ('arial', 12, 'bold')

    # ID
    TopwindowLabel = Label(connectwindow, text='ID', font=label_font, bg=primary_color, fg='white')
    TopwindowLabel.grid(row=0, column=0, pady=10, padx=10, sticky=E)
    Topwindowentry = Entry(connectwindow, font=entry_font, width=25)
    Topwindowentry.grid(row=0, column=1, pady=10, padx=10)

    # Prospect Name
    MIDtopwindowlabel = Label(connectwindow, text='Prospect Name', font=label_font, bg=primary_color, fg='white')
    MIDtopwindowlabel.grid(row=1, column=0, pady=10, padx=10, sticky=E)
    Midtopwindowentry = Entry(connectwindow, font=entry_font, width=25)
    Midtopwindowentry.grid(row=1, column=1, pady=10, padx=10)

    # Email Address
    Bottomwindowlabel = Label(connectwindow, text='Email Address', font=label_font, bg=primary_color, fg='white')
    Bottomwindowlabel.grid(row=2, column=0, pady=10, padx=10, sticky=E)
    Bottomewindowentry = Entry(connectwindow, font=entry_font, width=25)
    Bottomewindowentry.grid(row=2, column=1, pady=10, padx=10)

    # Result
    Lastwindowlabel = Label(connectwindow, text='Result', font=label_font, bg=primary_color, fg='white')
    Lastwindowlabel.grid(row=3, column=0, pady=10, padx=10, sticky=E)
    Lastwindowentry = Entry(connectwindow, font=entry_font, width=25)
    Lastwindowentry.grid(row=3, column=1, pady=10, padx=10)

    # Button
    actionButton = Button(connectwindow, text="Add", font=("arial", 11, "bold"), command=data_retrieved, bg=button_color, fg='black')
    actionButton.grid(row=4, column=0, columnspan=2, pady=20)



def Update_button():
    global cur, db, databasetable

    label_font = ('arial', 11, 'bold')
    entry_font = ('arial', 12, 'bold')

    def update_data():
        try:
            record_id = Top2windowentry.get()
            prospect_name = Midtop2windowentry.get()
            email = Bottome2windowentry.get()
            result = Last2windowentry.get()

            if not record_id:
                messagebox.showerror('Error', 'ID must be provided.')
                return

            if not (prospect_name and email and result):
                messagebox.showerror('Error', 'All fields must be filled out.')
                return

            # Update the record in the database
            query = """
            UPDATE jobmanager
            SET ProspectName = %s, Email = %s, Result = %s
            WHERE id = %s
            """
            cur.execute(query, (prospect_name, email, result, record_id))
            db.commit()

            # Confirm update and clear form if needed
            messagebox.showinfo('Success', 'Record updated successfully.')
            Top2windowentry.delete(0, END)
            Midtop2windowentry.delete(0, END)
            Bottome2windowentry.delete(0, END)
            Last2windowentry.delete(0, END)
            
            refresh_table()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def refresh_table():
        # Clear the current data in the Treeview
        databasetable.delete(*databasetable.get_children())

        try:
            # Retrieve all records from jobmanager table
            query = 'SELECT * FROM jobmanager'
            cur.execute(query)
            fetched_data = cur.fetchall()

            # Insert new fetched data
            for data in fetched_data:
                databasetable.insert('', END, values=data)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def select_record(event):
        try:
            # Fetch selected record from dropdown
            selected_id = record_var.get()
            if selected_id:
                query = 'SELECT * FROM jobmanager WHERE id = %s'
                cur.execute(query, (selected_id,))
                record = cur.fetchone()

                if record:
                    Top2windowentry.delete(0, END)
                    Midtop2windowentry.delete(0, END)
                    Bottome2windowentry.delete(0, END)
                    Last2windowentry.delete(0, END)
                    
                    Top2windowentry.insert(0, record[0])  # ID
                    Midtop2windowentry.insert(0, record[1])  # ProspectName
                    Bottome2windowentry.insert(0, record[2])  # Email
                    Last2windowentry.insert(0, record[4])  # Result
                else:
                    messagebox.showerror('Error', 'Record not found.')

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    connectwindow2 = Toplevel()
    connectwindow2.geometry('400x320')
    connectwindow2.title('Update Prospect')
    connectwindow2.resizable(False, False)
    connectwindow2.configure(bg=secondary_color)

    # Record ID Dropdown
    record_var = StringVar(connectwindow2)
    record_var.set('Select Record')  # Default value

    record_label = Label(connectwindow2, text='Select Record', font=label_font, bg=primary_color, fg='white')
    record_label.grid(row=0, column=0, pady=10, padx=10, sticky=E)
    
    record_menu = OptionMenu(connectwindow2, record_var, *get_record_ids())
    record_menu.grid(row=0, column=1, pady=10, padx=10)
    record_var.trace('w', select_record)  # Trigger update when selection changes

    # ID
    Top2windowLabel = Label(connectwindow2, text='ID', font=label_font, bg=primary_color, fg='white')
    Top2windowLabel.grid(row=1, column=0, pady=10, padx=10, sticky=E)
    Top2windowentry = Entry(connectwindow2, font=entry_font, width=25)
    Top2windowentry.grid(row=1, column=1, pady=10, padx=10)

    # Prospect Name
    MIDtop2windowlabel = Label(connectwindow2, text='Prospect Name', font=label_font, bg=primary_color, fg='white')
    MIDtop2windowlabel.grid(row=2, column=0, pady=10, padx=10, sticky=E)
    Midtop2windowentry = Entry(connectwindow2, font=entry_font, width=25)
    Midtop2windowentry.grid(row=2, column=1, pady=10, padx=10)

    # Email Address
    Bottom2windowlabel = Label(connectwindow2, text='Email Address', font=label_font, bg=primary_color, fg='white')
    Bottom2windowlabel.grid(row=3, column=0, pady=10, padx=10, sticky=E)
    Bottome2windowentry = Entry(connectwindow2, font=entry_font, width=25)
    Bottome2windowentry.grid(row=3, column=1, pady=10, padx=10)

    # Result
    Last2windowlabel = Label(connectwindow2, text='Result', font=label_font, bg=primary_color, fg='white')
    Last2windowlabel.grid(row=4, column=0, pady=10, padx=10, sticky=E)
    Last2windowentry = Entry(connectwindow2, font=entry_font, width=25)
    Last2windowentry.grid(row=4, column=1, pady=10, padx=10)

    # Button
    action2Button = Button(connectwindow2, text="Update", font=("arial", 11, "bold"), command=update_data, bg=button_color, fg='black')
    action2Button.grid(row=5, column=0, columnspan=2, pady=20)

def get_record_ids():
    try:
        query = 'SELECT id FROM jobmanager'
        cur.execute(query)
        ids = [str(record[0]) for record in cur.fetchall()]
        return ids
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error fetching record IDs: {e}")
        return []


def delete_button():
    global cur, db, databasetable

    label_font = ('arial', 11, 'bold')
    entry_font = ('arial', 12, 'bold')

    def delete_data():
        try:
            selected_item = databasetable.selection()  # Get selected item

            if not selected_item:
                messagebox.showerror('Error', 'No record selected.')
                return

            # Get the ID of the selected record
            selected_id = databasetable.item(selected_item[0], 'values')[0]

            if not selected_id:
                messagebox.showerror('Error', 'ID must be provided.')
                return

            # Delete the record from the database
            query = "DELETE FROM jobmanager WHERE id = %s"
            cur.execute(query, (selected_id,))
            db.commit()

            # Confirm deletion and refresh the table
            messagebox.showinfo('Success', 'Record deleted successfully.')
            refresh_table()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def refresh_table():
        # Clear the current data in the Treeview
        databasetable.delete(*databasetable.get_children())

        try:
            # Retrieve all records from jobmanager table
            query = 'SELECT * FROM jobmanager'
            cur.execute(query)
            fetched_data = cur.fetchall()

            # Insert new fetched data
            for data in fetched_data:
                databasetable.insert('', END, values=data)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    connectwindow3 = Toplevel()
    connectwindow3.geometry('400x320')
    connectwindow3.title('Delete Prospect')
    connectwindow3.resizable(False, False)
    connectwindow3.configure(bg=secondary_color)

    # Instructions
    instruction_label = Label(connectwindow3, text='Select a record from the table to delete', font=('arial', 12, 'bold'), bg=secondary_color, fg='white')
    instruction_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    # Button to delete selected record
    action3Button = Button(connectwindow3, text="Delete Selected", font=("arial", 11, "bold"), command=delete_data, bg=button_color, fg='black')
    action3Button.grid(row=1, column=0, columnspan=2, pady=20)

    # Update the table with current data
    refresh_table()



import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import mysql.connector

def export_data():
    global cur, databasetable

    def export_csv(data, columns):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                df = pd.DataFrame(data, columns=columns)
                df.to_csv(filename, index=False)
                messagebox.showinfo('Success', f'Data successfully exported to {filename}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export CSV: {e}')

  

    def fetch_data():
        try:
            query = 'SELECT * FROM jobmanager'
            cur.execute(query)
            data = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return data, columns
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")
            return [], []

    def on_export_choice(choice):
        data, columns = fetch_data()
        if data:  # Only proceed if data is not empty
            if choice == 'csv':
                export_csv(data, columns)
            

    export_choice_window = tk.Toplevel()
    export_choice_window.title("Export Data")
    export_choice_window.geometry("300x150")
    export_choice_window.configure(bg='gray')

    label = tk.Label(export_choice_window, text="Export The File", font=('arial', 12, 'bold'), bg='gray', fg='white')
    label.pack(pady=10)

    btn_csv = tk.Button(export_choice_window, text="Export as CSV", command=lambda: on_export_choice('csv'), bg='lightgray', fg='black')
    btn_csv.pack(pady=5)


def data_retrieved():
    global cur, db, databasetable
    
    try:
        if db is None or cur is None:
            messagebox.showerror('Error', 'Database connection not established.')
            return

        # Clear the Treeview
        for item in databasetable.get_children():
            databasetable.delete(item)

        # Fetch data from the database
        query = 'SELECT * FROM jobmanager'
        cur.execute(query)
        fetched_data = cur.fetchall()

        # Check if there is data to display
        if fetched_data:
            for data in fetched_data:
                databasetable.insert('', END, values=data)
        else:
            messagebox.showinfo('Info', 'No data found in the database.')

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error: {e}")



# This is an Email Function
def send_email():
    try:
        if to_entry.get() == '' or subject_entry.get() == '' or body_text.get("1.0", END).strip() == '':
            messagebox.showerror('Error', 'All fields must be filled out.')
        else:
            to_address = to_entry.get()
            subject = subject_entry.get()
            body = body_text.get("1.0", END).strip()
            final_message = 'Subject: {}\n\n{}'.format(subject, body)
            
            # Select email service here
            email_service = "Outlook"  # Change this to "Gmail" if you want to use Gmail

            if email_service == "Outlook":
                server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                server.starttls()
                server.login("jaimemanzueta@outlook.com", "JOCELIN12")
                sender_email = "jaimemanzueta@outlook.com"
            elif email_service == "Gmail":
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("your_gmail_address@gmail.com", "your_gmail_password")
                sender_email = "your_gmail_address@gmail.com"
            else:
                raise ValueError("Unsupported email service")

            server.sendmail(sender_email, to_address, final_message)
            server.quit()
            
            messagebox.showinfo("Success", "Email sent successfully.")
    except Exception as e:
        messagebox.showerror('Error', f'Failed to send email. Reason: {e}')


# Frames
topframe = Frame(GUI, bg=primary_color)
topframe.place(x=10, y=0, width=980, height=40)

leftframe = Frame(GUI, bg=primary_color)
leftframe.place(x=10, y=50, width=300, height=300)

rightframe = Frame(GUI, bg=primary_color)
rightframe.place(x=320, y=50, width=670, height=300)

bottomframe = Frame(GUI, bg=primary_color)
bottomframe.place(x=10, y=360, width=980, height=330)

# Top Frame
titleLabel = Label(topframe, text='Job Management System', font=('arial', 14, 'bold'), bg=primary_color, fg='white')
titleLabel.pack(pady=5)

# Left Frame
addButton = Button(leftframe, text='Add Prospect', font=('arial', 12, 'bold'), command=add_button, bg=button_color, fg='black')
addButton.grid(row=1, column=0, pady=20, padx=80)

updateButton = Button(leftframe, text='Update Prospect', font=('arial', 12, 'bold'), bg=button_color,command= Update_button, fg='black')
updateButton.grid(row=2, column=0, pady=20, padx=80)

deleteButton = Button(leftframe, text='Delete Prospect', font=('arial', 12, 'bold'), bg=button_color,command=delete_button, fg='black')
deleteButton.grid(row=3, column=0, pady=20, padx=80)

sendButton = Button(leftframe, text='Send To Prospect', font=('arial', 12, 'bold'), command=send_email, bg=button_color, fg='black')
sendButton.grid(row=4, column=0, pady=20, padx=80)

# Right Frame
prospectLabel = Label(rightframe, text="Prospect's Messagebox", font=('arial', 12, 'bold'), bg=primary_color, fg='white')
prospectLabel.grid(row=0, column=0, columnspan=2, pady=10)

msglabel = Label(rightframe, text="TO", font=('arial', 12, 'bold'), bg=primary_color, fg='white')
msglabel.grid(row=1, column=0, sticky=E, padx=10, pady=5)
to_entry = Entry(rightframe, width=93)
to_entry.grid(row=1, column=1, sticky=W, padx=10, pady=10)

msg2label = Label(rightframe, text="Subject", font=('arial', 12, 'bold'), bg=primary_color, fg='white')
msg2label.grid(row=2, column=0, sticky=E, padx=10, pady=5)
subject_entry = Entry(rightframe, width=93)
subject_entry.grid(row=2, column=1, sticky=W, padx=10, pady=10)

msg3label = Label(rightframe, text="Body", font=('arial', 12, 'bold'), bg=primary_color, fg='white')
msg3label.grid(row=3, column=0, sticky=NE, padx=10, pady=5)
body_text = Text(rightframe, width=70, height=10)
body_text.grid(row=3, column=1, sticky=W, padx=10, pady=10)


# Bottom Frame

databasename = Label(bottomframe, text="Database", font=('arial', 14, 'bold'), bg=primary_color, fg='white')
databasename.grid(row=0, column=0, pady=10, padx=450)

yscrollbar_y = Scrollbar(bottomframe, orient=VERTICAL)
databasetable = ttk.Treeview(bottomframe, columns=('id', 'Prospect Name', 'Email Address', 'Date Retrieved', 'Result'),
                             yscrollcommand=yscrollbar_y.set, show="headings")
yscrollbar_y.grid(row=1, column=1, sticky=NS, pady=10, padx=(0,10))  # Adjusted padding

databasetable.grid(row=1, column=0, pady=10, padx=(10,0))  # Adjusted padding

databasetable.heading('id', text='ID')
databasetable.heading('Prospect Name', text='Prospect Name')
databasetable.heading('Email Address', text='Email Address')
databasetable.heading('Date Retrieved', text='Date Retrieved')
databasetable.heading('Result', text='Result')

databasetable.column('id', width=70)
databasetable.column('Prospect Name', width=250)
databasetable.column('Email Address', width=250)
databasetable.column('Date Retrieved', width=250)
databasetable.column('Result', width=70)

# Import to Database Button
exportbutton = Button(bottomframe, text='Export', font=('arial', 10, 'bold'), bg=button_color, command= export_data, fg='black')
exportbutton.grid(row=2, column=0, pady=10)

# Connect to Database Button
connectDBButton = Button(bottomframe, text='Connect to Database', font=('arial', 10, 'bold'), command=connectdb, bg=button_color, fg='black')
connectDBButton.grid(row=3, column=0, pady=10)

# Centering the Database components in the bottom frame
bottomframe.grid_columnconfigure(0, weight=1)
bottomframe.grid_rowconfigure(0, weight=1)



GUI.mainloop()
