#Mahek M00979199
#Import necessary libraries
import socket
import csv
import threading
from datetime import datetime
import os

#Define the CardTransactionServer class to handle card transactions
class CardTransactionServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  #Listen for up to 5 connections
        print("Server listening on port", self.port)
    
    def start(self):
        #Continuously accept connections
        while True:
            conn, addr = self.server_socket.accept()
            print("Connected to", addr)
            #Create a new thread for each client connection
            client_thread = ClientThread(conn)
            client_thread.start()

#Define the ClientThread class to handle client connections
class ClientThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        #Continuously receive and process data from the client
        while True:
            data = self.conn.recv(1024).decode()
            if not data:
                break

            #Check if the received data is card details
            if data.startswith("ProdDetails:"):
                card_details = data.replace("ProdDetails:", "")
                self.save_prod_details(card_details)
            else:
                try:
                    #Check if the received data is a valid product ID
                    num = int(data)
                    if 1001 <= num <= 3005:
                        with open('product_quantities.csv', mode='r') as file:
                            reader = csv.DictReader(file)
                            rows = list(reader)
                            for row in rows:
                                if row['ID'] == str(num):
                                    if int(row['Quantity']) > 0:
                                        #Update product quantity and send success message
                                        row['Quantity'] = str(int(row['Quantity']) - 1)
                                        with open('product_quantities.csv', mode='w', newline='') as write_file:
                                            writer = csv.DictWriter(write_file, fieldnames=['ID', 'Quantity'])
                                            writer.writeheader()
                                            writer.writerows(rows)
                                            self.conn.sendall("Product purchased successfully".encode())
                                    else:
                                        #Send out of stock message
                                        self.conn.sendall("Out of Stock".encode())
                                        
                                    break
                            else:
                                #Send invalid product ID message
                                self.conn.sendall("Invalid Product ID".encode())
                    else:
                        #Send invalid product ID message
                        self.conn.sendall("Invalid Product ID".encode())
                except ValueError:
                    #Send invalid input message
                    self.conn.sendall("Invalid Input".encode())

        #Close the connection
        self.conn.close()

    def save_prod_details(self, card_details):
        PROD_DETAILS_HEADERS = ['Transaction_Time', 'Card_Name', 'Card_Number', 'CIV', 'Expiry_Date', 'Total_Price']
        PROD_DETAILS_FILE = "transactions.csv"

        #Save card details along with transaction time
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prod_details_list = [transaction_time] + card_details.split(",")
        with open(PROD_DETAILS_FILE, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:  #Check if file is empty
                writer.writerow(PROD_DETAILS_HEADERS)
            writer.writerow(prod_details_list)


#Define the main function to start the server
def main():
    # Check if CSV file exists, if not, create it
    csv_filename = 'product_quantities.csv'
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Quantity'])
            ID = ['1001', '1002', '1003', '1004', '1005', '2001', '2002', '2003', '2004', '2005', '3001', '3002', '3003', '3004', '3005']
            for i in ID:
                writer.writerow([i, 10])
    host = '192.168.56.1'
    port = 12345
    card_transaction_server = CardTransactionServer(host, port)
    card_transaction_server.start()

if __name__ == "__main__":
    main()
