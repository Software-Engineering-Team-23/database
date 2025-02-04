import tkinter as tk
from tkinter import messagebox, simpledialog
import sql


class firstScreen:
    def __init__(self,window):
        window.title("Entry Terminal")
        window.geometry("800x700")
        window.configure(bg="black")
        self.player_entries = {} # Key-value dictionary with key=ID_entry and value=name_label

        title = tk.Label(window, text="Edit Game",bg = "blue", fg="white", font=("Arial", 27, "bold"))
        title.pack()

        main_frame = tk.Frame(window, bg="gray")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=200, pady=40)

        red_frame = tk.Frame(main_frame,bg="red", width=500,height=900)
        red_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH,expand=True)
        self.make_rows(red_frame, "red", 20)

        green_frame = tk.Frame(main_frame,bg = "green", width=500,height=900)
        green_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH,expand=True)
        self.make_rows(green_frame, "green", 20)

        button_frame = tk.Frame(main_frame, bg="gray",width=200,height=300, highlightbackground="black", highlightthickness=4)
        button_frame.pack(pady=5, padx=5)
        button_frame.pack_propagate(False)

        button = tk.Button(button_frame, text="F1 Edit Game", bg = "black", fg="white",width= 100)
        button.pack(padx=5,pady=5)
        button = tk.Button(button_frame, text="F3 Start Game", bg = "black", fg="white",width= 100)
        button.pack(padx=5,pady=5)
        button = tk.Button(button_frame, text="F8 View Game", bg = "black", fg="white",width= 100)
        button.pack(padx=5,pady=5)
        button = tk.Button(button_frame, text="F12 Clear Game", bg = "black", fg="white",width= 100)
        button.pack(padx=5,pady=5)


    def make_rows(self, frame, bg_color, num_rows):
        for row in range(num_rows):
            row_frame = tk.Frame(frame, bg=bg_color)
            row_frame.pack(fill=tk.X, padx=5, pady=1)

            label = tk.Label(row_frame, text=f"{row}", bg=bg_color, font=("Helvetica", 20))
            label.pack(side=tk.LEFT, padx=5)

            # Split entry fields into two for ID and codename
            entry_left = tk.Entry(row_frame, bg="white", fg="black")
            entry_left.field_type = "integer" # Player ID only accepts int values
            entry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Display codename next to ID entry field
            name_label = tk.Label(row_frame, bg="white", fg="black")
            self.player_entries[entry_left] = name_label
            name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # For equipment ID. Uncomment as needed
            # entry_right = tk.Entry(row_frame, bg="white", fg="black")
            # entry_right.field_type = "string" # Tweak this type as needed
            # entry_right.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Bind entry submission to the "Enter" key and call self.submit() method
            entry_left.bind("<Return>", lambda event, e=entry_left: self.submit(e))
            # entry_right.bind("<Return>", lambda event, e=entry_right: self.submit(e))

    def submit(self, entry):
        # Get entry value and type
        value = entry.get().strip()
        value_type = entry.field_type
        # Validate entry submission by checking required type of field (integer)
        try:
            # If ID field is empty, clear name field
            if value == "":
                self.player_entries[entry].config(text="")
                return # Break out of function here, otherwise ValueError raised
            value = int(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid submission. Enter an integer ID")
            return

        print("\nSubmitted", value)

        # Fetch all players in database
        # Index each player's data and compare
        players = sql.fetch_players()
        existing_ids = [data[0] for data in players] # ID numbers
        existing_codenames = [data[1] for data in players] # Codenames after ID

        if value in existing_ids:
            # If ID exists, get codename
            # Assumes unique IDs (set)
            try:
                # Fetch codename corresponding to ID and then update name_label to display it
                codename = existing_codenames[existing_ids.index(value)]
                print(f"Player ID {value} with codename {codename} found")
                messagebox.showinfo("Info", f"Player ID {value} with codename '{codename}' found")
                self.player_entries[entry].config(text=codename)
            except Exception as e:
                print("Error fetching codename: ", e)
        else:
            # If ID does not exist, create new codename and database entry
            try:
                print(f"Player ID {value} not found.")
                while True:
                    new_codename = simpledialog.askstring("Input", "Enter new codename")
                    if new_codename and new_codename not in existing_codenames:
                        # Create new database player row and then update name_label to display it
                        sql.create_player(player_id=value, codename=new_codename)
                        messagebox.showinfo("Info", f"Player ID {value} with codename '{new_codename}' created!")
                        self.player_entries[entry].config(text=new_codename)
                        break
                    else:
                        messagebox.showerror("Error", "Invalid codename")
            except Exception as e:
                print("Error creating new player entry: ", e)
        
        sql.fetch_players() # Refresh data


window = tk.Tk()
gui = firstScreen(window)
window.mainloop()
