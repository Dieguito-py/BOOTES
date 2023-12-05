import tkinter as tk
from tkinter import ttk
from tkintermap import MapView

class RealTimeLocationApp:   #just test
    def __init__(self, root):
        self.root = root
        self.root.title("Localização em Tempo Real")
        self.latitude = 0.0
        self.longitude = 0.0
        
        self.create_map()
        self.create_info_panel()

    def create_map(self):
        self.map_view = MapView(self.root)
        self.map_view.pack(expand=True, fill="both")

    def update_location(self):
        self.latitude += 0.01
        self.longitude += 0.01

        self.map_view.center = (self.latitude, self.longitude)

        self.latitude_label['text'] = f"Latitude: {self.latitude:.6f}"
        self.longitude_label['text'] = f"Longitude: {self.longitude:.6f}"

        self.root.after(1000, self.update_location)

    def create_info_panel(self):
        info_frame = ttk.Frame(self.root)
        info_frame.pack(padx=10, pady=10)

        self.latitude_label = ttk.Label(info_frame, text="Latitude: ")
        self.latitude_label.grid(row=0, column=0, padx=5, pady=5)

        self.longitude_label = ttk.Label(info_frame, text="Longitude: ")
        self.longitude_label.grid(row=1, column=0, padx=5, pady=5)

        self.update_location()

def main():
    root = tk.Tk()
    app = RealTimeLocationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
