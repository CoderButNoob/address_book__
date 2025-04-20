import csv
from details import Details

class AddressBookFileManagerCSV():

    @staticmethod
    def write_csv(details , file="address_book.csv"):
        with open(file , mode = 'w' , newline='') as out:
            csv_write =  csv.DictWriter(out, Details.model_fields.keys())
            csv_write.writeheader()
            for contact in details:
                csv_write.writerow(contact.dict())
        print("Written to csv")
    
    @staticmethod
    def read_csv(details , file="address_book.csv"):
        try:
            with open(file , mode= 'r') as f:
                csv_read = csv.DictReader(f)
                for row in csv_read:
                    details.append(Details(**row))
            print(f"Data Loaded from {file}")
        except FileNotFoundError:
            print("File not Found")

