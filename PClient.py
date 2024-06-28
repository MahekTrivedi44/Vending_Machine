#Mahek M00979199
import socket  # For socket communication
import tkinter as tk  # For GUI
from tkinter import ttk, messagebox  # Additional GUI components
from PIL import ImageTk, Image  # For image manipulation
import csv  # For CSV file operations
import matplotlib.pyplot as plt  # For plotting graphs
import os  # For file operations

class BackgroundImageApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Vending machine")
        self.root.geometry("1050x590")
        self.root.resizable(False, False)
        # Load background image
        self.bg_image = Image.open("DC.png")
        self.copy_of_image = self.bg_image.copy()
        self.photo = ImageTk.PhotoImage(self.bg_image)
        self.label = ttk.Label(root, image=self.photo)
        self.label.bind('<Configure>', self.resize_image)
        self.label.pack(fill=tk.BOTH, expand=tk.YES)
        # Adding the labels for products
        positions = [(68, 176), (181, 176), (303, 176), (414, 176), (542, 176),
                     (68, 342), (181, 342), (303, 342), (414, 342), (542, 342),
                     (68, 515), (181, 515), (303, 515), (414, 515), (542, 515)]
        texts = ["1001-2$", "1002-1.5$", "1003-3$", "1004-2.5$", "1005-1$",
                 "2001-3$", "2002-4.5$", "2003-6$", "2004-3.5$", "2005-4$",
                 "3001-2$", "3002-3.5$", "3003-5$", "3004-1.5$", "3005-2$"]
        for text, (x, y) in zip(texts, positions):
            self.create_label(text, x, y)
        # Adding KeypadApp at position (710, 95)
        self.add_keypad_app(710, 95)
        messagebox.showinfo("Welcome", "Welcome to the Vending Machine!")
    # Method to create label for products
    def create_label(self, text, x, y):
        label = tk.Label(self.root, text=text, font=("Comic Sans MS", 12, "bold"), fg="white", bg="#f6b2b8")
        label.place(x=x, y=y)
        return label
    # Method to add KeypadApp to the main application
    def add_keypad_app(self, x, y):
        keypad_frame = tk.Frame(self.root, bg="#f6b2b8")
        keypad_frame.place(x=x, y=y)
        keypad_app = KeypadApp(keypad_frame)
    # Method to resize the background image according to window size
    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        image = self.copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  
class KeypadApp:
    def __init__(self, master):
        # Initialize the keypad application
        self.master = master
        self.product_details = {}
        self.prices = {}
        self.input_var = tk.StringVar()
        self.input_var.set("")
        self.t=0 
        self.entry = tk.Entry(master, textvariable=self.input_var, justify='right', font=('Arial', 14))
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='ew')
        self.p = 0
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.', 'C'
        ]
        row = 1
        col = 0
        for button in buttons:
            tk.Button(master, text=button, width=5, height=2, command=lambda b=button: self.add_to_input(b)).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1
        tk.Button(master, text="Show Graph", command=self.show_graph).grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        tk.Button(master, text="ADD", width=5, height=2, command=self.save_variable).grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        tk.Button(master, text="Proceed To Payment", width=20, height=2, command=self.proceed_to_payment).grid(row=7, column=0, columnspan=5, padx=5, pady=5)
    def show_graph(self):
        # Calculate total price for each product
        total_prices = {}
        for product_id, quantity in self.product_details.items():
            total_prices[product_id] = self.prices[product_id] * quantity
        # Plotting the graph
        plt.figure(figsize=(8, 6))
        plt.bar(total_prices.keys(), total_prices.values(), color='skyblue')
        plt.xlabel('Product ID')
        plt.ylabel('Total Price ($)')
        plt.title('Total Price of Each Product')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Displaying the graph
        plt.show()
    # Method to add input to the entry field
    def add_to_input(self, value):
        current_input = self.input_var.get()
        if value == 'C':
            self.input_var.set("")
        else:
            self.input_var.set(current_input + value)
    #Method to print message when payment is cancelled
    def cancel(self, window=None):
        if window:
            window.destroy()
            messagebox.showinfo("Payment Canceled", "Sorry, we could not provide you with what you would like today. We hope to be seeing you again soon. Wish you a Good day!")      
    #Method to communicate with server for card details
    def values(self):
        card_name = self.card_name_var.get()
        card_number = self.card_number_var.get()
        expiry_month = self.expiry_month_var.get()
        expiry_year = self.expiry_year_var.get()
        prod_details = f'"{card_name}","{card_number}","civ:***","{expiry_month}/{expiry_year}","{self.p}"'
        communicate_with_server("ProdDetails:" + prod_details)
    #Calculate total price
    def save_variable(self):        
        num = self.input_var.get()
        response=communicate_with_server(num)
        self.prices = {
        '1001': 2, '1002': 1.5, '1003': 3, '1004': 2.5, '1005': 1,
        '2001': 3, '2002': 4.5, '2003': 6, '2004': 3.5, '2005': 4,
        '3001': 2, '3002': 3.5, '3003': 5, '3004': 1.5, '3005': 2}
        ID=['1001', '1002', '1003', '1004', '1005', '2001', '2002', '2003', '2004', '2005', '3001', '3002', '3003', '3004', '3005']
        Price=[2,1.5,3,2.5,1,3,4.5,6,3.5,4,2,3.5,5,1.5,2]
        try:
            a = ID.index(num)
            if response!= "Out of Stock":
                self.p += Price[a]
                if num in self.product_details:
                    self.product_details[num] += 1
                else:
                    self.product_details[num] = 1
        except ValueError:
            messagebox.showerror("Error", "Invalid product ID!")
    def proceed_to_payment(self):
        # Create the payment window
        payment_window = tk.Toplevel(self.master)
        payment_window.title("Payment Method")
        payment_window.geometry("424x600")    
        # Load the background image and resize it
        payment_bg = tk.PhotoImage(file="Paymentbg.png")
        resized_bg = payment_bg.subsample(1, 1)  # Adjust the subsample values as needed
        # Create a label to display the background image
        bg_label = tk.Label(payment_window, image=resized_bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = resized_bg  # Keep a reference to avoid garbage collection
        # Calculate total price and create labels for amount to pay and buttons for payment methods
        total_price = f"Total Price: ${self.p:.2f}"
        tk.Label(payment_window, text=total_price, font=("Comic Sans MS", 15), fg="#377B4C", bg="#FFF6EA").place(x=132, y=215)
        # Add a section to display product details
        product_details_label = tk.Label(payment_window, text="Product Details", font=("Comic Sans MS", 12), fg="#377B4C", bg="#FFF6EA")
        product_details_label.place(x=155, y=250)
        # Display each product's details
        for i, (product_id, quantity) in enumerate(self.product_details.items(), start=1):            
            product_info = f"{product_id} -- {quantity} -- ${self.prices[product_id] * quantity:.2f}"         
            tk.Label(payment_window, text=product_info, font=("Comic Sans MS", 10), fg="#377B4C", bg="#FFF6EA").place(x=155, y=280 + (i - 1) * 30)
        # Add payment buttons
        tk.Button(payment_window, text="Pay by Cash", command=lambda: self.pay_by_cash(payment_window), font=("Comic Sans MS", 11), fg="#377B4C", bg="#FFF6EA").place(x=170, y=405)
        tk.Button(payment_window, text="Pay by Card", command=lambda: self.pay_by_card(payment_window), font=("Comic Sans MS", 11), fg="#377B4C", bg="#FFF6EA").place(x=170, y=455)
    def pay_by_cash(self, payment_window):
        payment_window.destroy()
        cash_payment_window = tk.Toplevel(self.master)
        cash_payment_window.title("Cash Payment")
        cash_payment_window.geometry("500x203")
        # Load the background image and resize it to 500x203
        bg_image = tk.PhotoImage(file="Paybg.png")
        resizedbg = bg_image.subsample(1, 1)# Adjust the subsample factor as needed
        # Create a label to hold the background image
        bg_label = tk.Label(cash_payment_window, image=resizedbg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = resizedbg  
        tk.Label(cash_payment_window, text=f"Total amount to Pay: {self.p}$", font=("Comic Sans MS", 15), fg="#2C4975", bg="#CFEADB").place(x=225,y=32)
        tk.Label(cash_payment_window, text="Enter the amount:", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").place(x=260,y=70)
        self.amount_var = tk.StringVar()
        tk.Entry(cash_payment_window, textvariable=self.amount_var).place(x=265,y=100)
        tk.Button(cash_payment_window, text="Submit", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB", command=lambda: self.process_cash_payment(cash_payment_window)).place(x=252,y=130)
        tk.Button(cash_payment_window, text="Cancel", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB", command=lambda: self.cancel(cash_payment_window)).place(x=345,y=130)
    #Processing cash payment, asking to pay if insufficient/returning change
    def process_cash_payment(self,cash_payment_window):
        self.amount_to_pay=self.p
        try:
            cash_amount = float(self.amount_var.get())
            self.t+=cash_amount
            if self.t < self.amount_to_pay:
                remaining_amount = self.amount_to_pay - self.t
                messagebox.showerror("Error", f"Insufficient amount! Please pay ${remaining_amount:.2f} more.")
            elif self.t == self.amount_to_pay:
                messagebox.showinfo("Success", "Payment successful! Thank you! Goodbye!")
                cash_payment_window.destroy()
                root.destroy()
                prod_details = f'"--Cash--","--NA--","--NA--","--NA--","{self.p}"'
                communicate_with_server("ProdDetails:" + prod_details)
            else:
                change = self.t - self.amount_to_pay
                messagebox.showinfo("Success", f"Payment successful! Your change: ${change:.2f} Thank you! Goodbye!")
                cash_payment_window.destroy()
                root.destroy
                prod_details = f'"--Cash--","--NA--","--NA--","--NA--","{self.p}"'
                communicate_with_server("ProdDetails:" + prod_details)                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
    def pay_by_card(self, payment_window):
        payment_window.destroy()
        card_payment_window = tk.Toplevel(self.master)
        card_payment_window.title("Card Payment")
        card_payment_window.geometry("300x424")
        # Load the background image and resize it to 500x203
        bgimage = tk.PhotoImage(file="Cardbg.png")
        resizedBG = bgimage.subsample(1, 1)# Adjust the subsample factor as needed
        # Create a label to hold the background image
        bg_label = tk.Label(card_payment_window, image=resizedBG)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = resizedBG 
        tk.Label(card_payment_window, text=f"Total amount to Pay: {self.p}$", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack(pady=10)
        tk.Label(card_payment_window, text="Enter Card Details:", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack()
        tk.Label(card_payment_window, text="Card Holder Name:", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack()
        self.card_name_var = tk.StringVar()
        tk.Entry(card_payment_window, textvariable=self.card_name_var).pack()
        tk.Label(card_payment_window, text="Card Number:", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack()
        self.card_number_var = tk.StringVar()
        tk.Entry(card_payment_window, textvariable=self.card_number_var).pack()
        tk.Label(card_payment_window, text="CIV:", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack()
        self.civ_var = tk.StringVar()
        tk.Entry(card_payment_window, textvariable=self.civ_var, show="*").pack()
        tk.Label(card_payment_window, text="Expiry (MM/YYYY):", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack()
        expiry_frame = tk.Frame(card_payment_window)
        expiry_frame.pack()
        self.expiry_month_var = tk.StringVar()
        tk.Entry(expiry_frame, textvariable=self.expiry_month_var, width=2).pack(side=tk.LEFT)
        tk.Label(expiry_frame, text="/", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB").pack(side=tk.LEFT)
        self.expiry_year_var = tk.StringVar()
        tk.Entry(expiry_frame, textvariable=self.expiry_year_var, width=4).pack(side=tk.LEFT)
        tk.Button(card_payment_window, text="Submit", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB", command=lambda:self.process_card_payment(card_payment_window)).pack(pady=7)
        tk.Button(card_payment_window, text="Cancel", font=("Comic Sans MS", 12), fg="#2C4975", bg="#CFEADB", command=lambda: self.cancel(card_payment_window)).pack(pady=7)
    #Process card payment,  handle errors
    def process_card_payment(self,card_payment_window):
        card_name = self.card_name_var.get()
        card_number = self.card_number_var.get()
        civ = self.civ_var.get()
        expiry_month = self.expiry_month_var.get()
        expiry_year = self.expiry_year_var.get()
        if not (card_name and card_number and civ and expiry_month and expiry_year):
            messagebox.showerror("Error", "Please fill all fields.")
        elif len(card_number) != 16:
            messagebox.showerror("Error", "Invalid Card Number.")
        elif len(civ) != 3:
            messagebox.showerror("Error", "Invalid CIV.")
        elif not (expiry_month.isdigit() and expiry_year.isdigit()):
            messagebox.showerror("Error", "Invalid Expiry Date.")
        elif int(expiry_year) < 2023 or not (1 <= int(expiry_month) <= 12):
            messagebox.showerror("Error", "Invalid Expiry Date.")
        else:
            messagebox.showinfo("Payment Successful", "Payment successful. Thank you! Goodbye!")
            card_payment_window.destroy()
            root.destroy()
            self.values()
#Function to communicate with server
def communicate_with_server(product_id):
    host = '192.168.56.1'
    port = 12345
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.sendall(product_id.encode())
        response = client_socket.recv(1024).decode()
        messagebox.showinfo("Server Response", response)
        return response
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        client_socket.close()
root = tk.Tk()
app = BackgroundImageApp(root)
root.mainloop()
