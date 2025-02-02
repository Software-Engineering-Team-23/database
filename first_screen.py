import tkinter as tk
import sql


class firstScreen:
    def __init__(self,window):
        window.title("Entry Terminal")
        window.geometry("800x700")
        window.configure(bg="black")
        self.player_entries = {}

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
            entry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            entry_right = tk.Entry(row_frame, bg="white", fg="black")
            entry_right.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Bind entry submission to the "Enter" key and call self.submit() method
            entry_left.bind("<Return>", lambda event, e=entry_left: self.submit(e))
            entry_right.bind("<Return>", lambda event, e=entry_right: self.submit(e))

    def submit(self, entry):
        value = entry.get()
        print("submitted", value)
        # Fetch all players in database
        # Index each player's data and compare
        players = sql.fetch_players()
        existing_ids = [data[0] for data in players] # ID numbers
        existing_codenames = [data[1] for data in players] # Codenames after ID

        if int(value) in existing_ids:
            # If ID exists, get codename
            # Assumes uniqe IDs (set)
            try:
                codename = existing_codenames[existing_ids.index(int(value))]
                print(f"Player ID {value} with codename {codename} found.")
            except Exception as e:
                print("Error fetching codename: ", e)
        else:
            # If ID does not exist, create new codename and database entry
            try:
                print(f"Player ID {value} not found.")
                new_codename = input("Enter new codename\n> ")
                sql.create_player(player_id=value, codename=new_codename)
            except Exception as e:
                print("Error creating new player entry: ", e)
        sql.fetch_players() # Refresh data

window = tk.Tk()
gui = firstScreen(window)
window.mainloop()