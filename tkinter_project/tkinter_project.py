import tkinter as tk
root = tk.Tk()

name_textbox = tk.Entry(root)
name_textbox.pack()
checkbutton = tk.Checkbutton(root, text="Check me")  # Create a checkbox
checkbutton.pack()
message = tk.Message(root, text="This is a message")  # Create a message widget
frame_dd = tk.Frame(root, bg = "lightblue", bd = 5, relief = "sunken")
frame_dd.pack()

# main_label = tk.Label(root, bg = "lightblue", bd= 5, width=800, height=900)
# main_label.pack()

button = tk.Button(root, bg = "lightblue" )

entry = tk.Entry(root, width= 60, bg= 'black',fg="white")
entry.pack()

text = tk.Text(root,height=5, width=7).pack()


check_var = tk.IntVar()
# checkbox = tk.Checkbutton(root,text= "Click Me", variable=check_var, command = checkbox_callback).pack()
# checkbox = tk.Checkbutton(root,text= "Click Me", variable=check_var2).pack()

# def radio_callback():
#     # Get the value of the selected radio button
#     value = radio_var.get()
#     print(f"The value of the selected radio button is {value}")

# # Create a StringVar to hold the value of the selected radio button
# radio_var = tk.StringVar(value="")  # Initially set to empty to be unchecked

# # Create the first radio button
# rad_but1 = tk.Radiobutton(root, text="Option 1", variable=radio_var, value="2", command=radio_callback)
# rad_but1.pack()

# Create the second radio button
# rad_but2 = tk.Radiobutton(root, text="Option 2", variable=radio_var, value="1", command=checkbox_callback)
# rad_but2.pack()


# # def checkbox_callback():
#     # Get the value of the selected radio button
#     value = check_val.get()
#     print(f"The value of the selected radio button is {value}")

# check_val = tk.StringVar(value="")
# check_1 = tk.Checkbutton(root, text="Option 1", variable=check_val, value = 1, command=checkbox_callback).pack()
# check_2 = tk.Checkbutton(root, text="Option 2", variable=check_val, value = 1, command=checkbox_callback).pack()



scale = tk.Scale(root, from_= 0, to=100, orient="horizontal",bg="black", fg="green").pack()

scroll = tk.Scrollbar(root, orient="vertical").pack()

def get_selected_item():
    # Get the index of the selected item
    selected_index = listbox.curselection()
    if selected_index:
        # Get the item at the selected index
        selected_item = listbox.get(selected_index)
        print(f"Selected item: {selected_item}")

# Create a Listbox widget
listbox = tk.Listbox(root)
listbox.insert(0, "What is your first name?")
listbox.insert(1, "What is your last name?")
listbox.insert(2, "What is your pet name?")
listbox.pack()

# Add a Button to trigger getting the selected item
button = tk.Button(root, text="Get Selected Item", command=get_selected_item)
button.pack()



drop_1 = tk.StringVar(value = "Select the Option")
options= ["What is this?", "What is that?", "What is other?"]
select_opt = tk.OptionMenu(root, drop_1, *options).pack()

def get_val():
   drop_1.get().pack()

button2 = tk.Button(root, text="Click me to get Text", command = get_val).pack()


def say_hello():
    print("Hello!")


menu_bar = tk.Menu(root)  # Create a menu bar
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Say Hello", command=say_hello)
menu_bar.add_cascade(label="File", menu=file_menu)

root.config(menu=menu_bar)


spinbox = tk.Spinbox(root, from_=0, to=10)  # Create a spinbox for selecting numbers between 0 and 10
spinbox.pack()

root.mainloop()
