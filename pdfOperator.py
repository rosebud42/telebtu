# Import libraries
from bs4 import BeautifulSoup
import requests
import pdfplumber
import os

from datetime import datetime
class PdfOp:
    menu_list = []
    days = ["PAZARTESİ","SALI","ÇARŞAMBA","PERŞEMBE","CUMA","CUMARTESİ","PAZAR"]
    log_file = "logs.txt"
    menu_name = "valid_pdf"
    menu_folder = f"menuler/{menu_name}.pdf"
    def download_file(self,link):
        response = requests.get(link)
        current_month = datetime.now().month
        if response.status_code == 200:
            for dosya in os.listdir("menuler"):
                dosya_path = os.path.join('menuler',dosya)
                if (dosya == f'{current_month-1}.pdf' or dosya == f'{current_month}.pdf' or dosya == f'{self.menu_name}.pdf'):
                    os.remove(dosya_path)
            with open(self.menu_folder, "wb") as file:
                file.write(response.content)
                print("Pdf downloaded successfully")
                return True
        else:
            print("Failed to download file!")    
    def manuel_pdf(self,file):
        current_month = datetime.now().month
        file_url = file.file_path
        response = requests.get(file_url)
        is_valid = False
        if response.status_code == 200:
            with open("menuler/not_checked_yet.pdf","wb") as file2:
                file2.write(response.content)
        else:
            return False
        with pdfplumber.open("menuler/not_checked_yet.pdf") as pdf:
                for page in pdf.pages:
                    if "BURSA TEKNİK ÜNİVERSİTESİ" and "YEMEK LİSTESİ" in page.extract_text().upper():
                        print("PDF is verified successfully.")
                        is_valid = True
        if is_valid:
            for dosya in os.listdir("menuler"):
                if (dosya == f'{current_month-1}.pdf' or dosya == f'{current_month}.pdf') or dosya == f'{self.menu_name}.pdf':
                    os.remove(f"menuler/{dosya}")
            os.rename("menuler/not_checked_yet.pdf",self.menu_folder)
            return True
        if not is_valid:
                os.remove("menuler/not_checked_yet.pdf")
                return False

    def get_pdf(self):
        response = requests.get("https://btu.edu.tr/tr/sayfa/detay/4398/beslenme-ve-di̇yeteti̇k")
        soup = BeautifulSoup(response.text, 'html.parser')



        for link in soup.find_all('td'):
            if "Aylık yemek listesi" in str(link):
                href = str(link.a.get('href'))
                if self.download_file(href):
                    return True
                

    def read_pdf(self):
        is_correct_menu = False
        toReturn = True
        try:
            with pdfplumber.open(self.menu_folder) as pdf:
                for page in pdf.pages:
                    if "BURSA TEKNİK ÜNİVERSİTESİ" and "YEMEK LİSTESİ" in page.extract_text().upper():
                        print("PDF is verified successfully.")
                        is_correct_menu = True
                if not is_correct_menu:
                    self.get_pdf()
                    print("The menu is not verified. Downloading again.")
                    toReturn = False                      
                menu = [page.extract_table() for page in pdf.pages]
                menu = menu[0] 
        except FileNotFoundError:

            self.get_pdf()
            try:
                with pdfplumber.open(self.menu_folder) as pdf:
                    menu = [page.extract_table() for page in pdf.pages]
                    menu = menu[0] 
            except FileNotFoundError:
                self.menu_list = False
                return False
        except Exception as ex:           
            self.get_pdf()

        try:
            filtered_menu = []
            if not menu:
                print("Menu's content is not correct! Dowloading again...")
                self.get_pdf()
                return False
            for row in menu:
                day = row[1]
                if day:
                    day = day.upper()
                if day in self.days:
                    filtered_menu.append(row)
            self.menu_list = filtered_menu
            if not toReturn: 
                return False
            return True
        except Exception:
            return False
    
    def getText(self,day):
        menu = self.menu_list
        date = menu[day][0]
        day_str = menu[day][1]
        meal_1 = menu[day][2]
        meal_2 = menu[day][3]
        meal_3 = menu[day][4]
        meal_4 = menu[day][5]
        cal = menu[day][6]
        if day_str == "PAZAR" or day_str == "CUMARTESİ":
            text=f"{date} {day_str} tarihli günün menüsü:\nHaftasonları yemek hizmeti yoktur. "
        else:
            text=f"{date} {day_str} tarihli günün menüsü:\nİçerik 1 : {meal_1}\nİçerik 2 : {meal_2}\nİçerik 3 : {meal_3}\nİçerik 4 : {meal_4}\nToplam kalori : {cal}"
        return text
    


        

    



