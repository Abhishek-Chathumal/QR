import pandas as pd
import qrcode
from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk

class QRCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Generator")
        self.master.geometry("400x400")
        
        self.data = pd.read_csv('Book1.csv')
        self.current_index = 0
        self.generated_qrs = set()
        
        self.label = Label(master, text="")
        self.label.pack(pady=20)
        
        self.qr_label = Label(master)
        self.qr_label.pack(pady=20)
        
        self.next_button = Button(master, text="Next", command=self.next_record)
        self.next_button.pack(pady=20)
        
        self.generate_qr()
    
    def generate_qr(self):
        record = self.data.iloc[self.current_index]
        record_str = record.to_string(index=False)
        
        if self.current_index in self.generated_qrs:
            messagebox.showwarning("Warning", "QR code already generated for this record.")
            #self.next_button.config(state="disabled")
            return
        
        qr = qrcode.make(record_str)
        qr_image = ImageTk.PhotoImage(qr)
        
        self.qr_label.config(image=qr_image)
        self.qr_label.image = qr_image
        self.label.config(text=f"Record {self.current_index + 1}")
        
        self.generated_qrs.add(self.current_index)
    
    def next_record(self):
        self.current_index = (self.current_index + 1) % len(self.data)
        self.generate_qr()

if __name__ == "__main__":
    root = Tk()
    app = QRCodeGenerator(root)
    root.mainloop()
