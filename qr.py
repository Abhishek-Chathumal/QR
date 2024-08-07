import pandas as pd
import qrcode
from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk

class QRCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Generator")
        self.master.geometry("400x500")

        # Specify the full path to the CSV file
        csv_path = 'Book1.csv'

        try:
            self.data = pd.read_csv(csv_path)
            if self.data.empty:
                messagebox.showerror("Error", "The CSV file is empty.")
                self.master.destroy()
                return
            print("CSV columns:", self.data.columns)  # Print column names for debugging
        except FileNotFoundError:
            messagebox.showerror("Error", f"CSV file not found at {csv_path}")
            self.master.destroy()
            return

        self.current_index = 0
        self.total_records = len(self.data)

        self.label = Label(master, text="")
        self.label.pack(pady=10)

        self.qr_label = Label(master)
        self.qr_label.pack(pady=10)

        self.next_button = Button(master, text="Next", command=self.next_record)
        self.next_button.pack(pady=10)

        self.generate_qr()

    def generate_qr(self):
        if self.current_index >= self.total_records:
            messagebox.showinfo("Info", "All records have been processed.")
            self.next_button.config(state="disabled")
            return

        record = self.data.iloc[self.current_index]
        
        ssid = record['SSID']
        security = record['Security'] if pd.notna(record['Security']) else "WPA"
        password = record['Password']
        
        record_str = f"WIFI:S:{ssid};T:{security};P:{password};;"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(record_str)
        qr.make(fit=True)

        qr_image = qr.make_image(fill='black', back_color='white')
        qr_image = ImageTk.PhotoImage(qr_image)

        self.qr_label.config(image=qr_image)
        self.qr_label.image = qr_image
        self.label.config(text=f"Record {self.current_index + 1} of {self.total_records}")

    def next_record(self):
        self.current_index += 1
        if self.current_index >= self.total_records:
            self.current_index = 0  # Wrap around to the first record
        self.generate_qr()

if __name__ == "__main__":
    root = Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
