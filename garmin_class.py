from tkinter import messagebox

class GarminApp:
    def __init__(self) -> None:
        self.name: str = "Michael Liu"
        self.age: int = 17
        self.height: float = 177
        self.weight: float = 63.5
        self.gender: str = "Male"
        self.bmi: float = (self.weight)/((self.height/100)**2)
        self.total_runs: int = 0
        self.total_swims: int = 0
        self.total_bikes: int = 0
        self.activities: list[dict[str, str, float, float]] = []
        self.encryption_key: dict[str, str] = { #Ecryption key for data
            "a": "/", "A": ";",
            "b": "y", "B": "k",
            "c": "B", "C": "9",
            "d": "&", "D": "5",
            "e": "=", "E": "S",
            "f": "%", "F": "V",
            "g": "3", "G": "}",
            "h": "Z", "H": ":",
            "i": "?", "I": "0",
            "j": "*", "J": "2",
            "k": "+", "K": "7",
            "l": "~", "L": "U",
            "m": "$", "M": "^",
            "n": "`", "N": "#",
            "o": "|", "O": "8",
            "p": "1", "P": "6",
            "q": "_", "Q": "]",
            "r": "[", "R": "{",
            "s": "I", "S": "M",
            "t": "E", "T": ".",
            "u": "}", "U": "@",
            "v": "(", "V": ")",
            "w": "!", "W": "R",
            "x": "X", "X": "y",
            "y": "#", "Y": "%",
            "z": ">", "Z": "<",
            "0": "a",
            "1": "b",
            "2": "c",
            "3": "d",
            "4": "e",
            "5": "f",
            "6": "g",
            "7": "h",
            "8": "i",
            "9": "j",
            "-": "m",
            ".": "n",
            ",": ","
            }
        
    def submit_data(self, name_: str, age_: int, height_: float, weight_: float, gender_: str) -> None: #For load screen
        self.name = name_
        self.age = age_
        self.height = height_
        self.weight = weight_
        self.gender = gender_
        self.bmi = (weight_)/(((height_)/100)**2)
        
    def encrypt(self, text: str) -> str: #Ecryption function
        encrypted = ''
        for char in text:
            encrypted += self.encryption_key.get(char, char)
        return encrypted

    def decrypt(self, text: str) -> str: #Decryption function
        reversed_key = {value: key for key, value in self.encryption_key.items()}
        decrypted = ''
        for char in text:
            decrypted += reversed_key.get(char, char)
        return decrypted

    def save_all(self) -> None: #Save function using Ecryption
        try:
            with open(f"{self.name.replace(" ", "_")}.txt", "w") as f:
                profile_line = f"{self.name},{self.age},{self.height},{self.weight},{self.gender},{self.bmi},{self.total_runs},{self.total_swims},{self.total_bikes}\n"
                encrypted_profile = self.encrypt(profile_line)
                f.write(encrypted_profile)
                for act in self.activities:
                    act_line = f"{act['date']},{act['type']},{act['distance']},{act['time']}\n"
                    f.write(self.encrypt(act_line))
        except:
            messagebox.showwarning("Save Error", "Error")

    def load_file(self, name: str) -> None: #Load function using Decryption
        try:
            with open(f"{name.replace(" ", "_")}.txt", "r") as f:
                lines = f.readlines()
                decrypted_lines = [self.decrypt(line.strip()) for line in lines]
                profile = decrypted_lines[0].split(",")
                self.name = profile[0]
                self.age = int(profile[1])
                self.height = float(profile[2])
                self.weight = float(profile[3])
                self.gender = profile[4]
                self.bmi = float(profile[5])
                self.total_runs = int(profile[6])
                self.total_swims = int(profile[7])
                self.total_bikes = int(profile[8])
                self.activities = []
                for line in decrypted_lines[1:]: #Add all activities back to self.activities
                    date, typ, dist, time = line.strip().split(",")
                    self.activities.append({
                        "date": date,
                        "type": typ,
                        "distance": float(dist),
                        "time": float(time)
                    })
        except FileNotFoundError:
            messagebox.showwarning("Load Error", "No saved file found.")
        except:
            messagebox.showwarning("Error", "")

    def calculate_calories_burned(self, distance: float, activity_type: str) -> float:
        match activity_type: #Calculate calories burned
            case "Run": #Adjust for type of activity
                type_factor = 1.1
            case "Swim":
                type_factor = 1.4
            case "Bike":
                type_factor = 0.6
        match self.gender: #Adjust for gender
            case "Male":
                gender_factor = 1
            case "Female":
                gender_factor = 0.95
        age_factor = max(0.85, 1 - ((self.age - 30) * 0.005)) #Adjust for age

        calories_burned = distance * self.weight * type_factor * gender_factor * age_factor
        return round(calories_burned, 2)

    def calculate_bmi(self) -> None: #BMI calculation
        self.bmi = (self.weight)/((self.height/100)**2)

    def update_settings(self, field: str, value: float | str | int) -> None: #Update user settings
        try:
            match field: #Math which field the user wants to update
                case "Name":
                    if len(value) <= 20:
                        self.name = value
                    else:
                        messagebox.showwarning("Invalid Input", "Please enter a name with length between 0 and 20 characters")
                case "Age":
                    if value >= 0 and value <= 100 and type(value) == int:
                        self.age = int(value)
                    else:
                        messagebox.showwarning("Invalid Input", "Please enter a valid integer age between 0 and 100")
                case "Gender":
                    if value in ["Male", "Female"]:
                        self.gender = value
                    else:
                        messagebox.showwarning("Invalid Input", "Please enter Male or Female (First Letter Uppercase)")
                case "Weight":
                    if self.weight >= 0 and self.weight <= 500:
                        self.weight = float(value)
                        self.calculate_bmi()
                    else:
                        messagebox.showwarning("Invalid Input", "Please enter a valid weight between 0 and 500 kg")
                case "Height":
                    if self.height >= 0 and self.height <= 300:
                        self.height = float(value)
                        self.calculate_bmi()
                    else:
                        messagebox.showwarning("Invalid Input", "Please enter a valid height between 0 and 300 cm")
        except:
            messagebox.showwarning("Invalid Input")
    
    def update_activity(self, now: str, activity: str, distance: float, time: float) -> None: #Adding a new activity
        match activity: #Match which type of activity the user is adding
            case "Run":
                self.total_runs += 1
            case "Swim":
                self.total_swims += 1
            case "Bike":
                self.total_bikes += 1
        self.activities.insert(0 ,{ 
        'date': now,
        'type': activity,
        'distance': distance,
        'time': time
        })


