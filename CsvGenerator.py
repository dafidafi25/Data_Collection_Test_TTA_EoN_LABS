class Csv_Writter():
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    format_header = 'formattedTime-value'
    def __init__(self, file) -> None:
        self.file  = file
        self.initiate_files(file)
        pass

    def initiate_files(self, file):
        
        is_file_exist = False
        is_header_exist = False
        
        #Checking if file exist, and header exist if file exist
        try:
            with open(f'./{self.file}.csv','r') as csv_file:
                is_file_exist = True
                header = csv_file.readline()
                
                if header[0:len(header)-1] == self.format_header:
                    is_header_exist = True
                else:
                    print(f'Header Doesn\'t exist, creating ....')
                    print(f'Current Header {header}')
                csv_file.close()
        except:
            print("File Doesn't Exist, creating file .....")
        
        # Creating Header for CSV
        if not is_file_exist or not is_header_exist:
            with open(f'./{self.file}.csv','w') as csv_file:
                csv_file.write(f'{self.format_header}\n')
                csv_file.close()
    #time,formattedTime,formattedAxisTime,value,hasData,formattedValue
    def write_data(self,data):
        with open(f'./{self.file}.csv','a') as csv_file:
            if csv_file.writable():
                try:
                    csv_file.write(f'{data["formattedTime"]}-{data["value"][0]}\n')
                except Exception as err:
                    print(err)
                pass
            
            csv_file.close()

    def reset_files(self):
        with open(f'./{self.file}.csv','w') as csv_file:
            csv_file.write(f'{self.format_header}\n')
            csv_file.close()


if __name__=="__main__":
    hourly = Csv_Writter(Csv_Writter.HOURLY)
    daily = Csv_Writter(Csv_Writter.DAILY)
    weekly = Csv_Writter(Csv_Writter.WEEKLY)

    text = dict({'formattedTime' : "daily_date", 'value': [1]})
