from details import Details

class AddressBookFileManager():

    @staticmethod
    def write_detail(details_list , file = "address_book.txt"):
        try:
            with open(file , "w")  as out:
                for contact in  details_list:
                    out.write(str(contact)+"\n"+"-"*40+"\n")
            print("Written")
        except Exception as e:
            print(f"Failed to write : {e}")
    
    def read_details(file = "address_book.txt"):
        try:
            with open(file , "r") as r:
                content = r.read()
                print(content)
        except FileNotFoundError:
            print("File Not Found")
        except Exception as e:
            print(f" Cannot read file: {e}")



    