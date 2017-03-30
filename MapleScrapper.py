# Kenny Chen
# 

from lxml import html
import requests
from lxml import etree
import xlwt
from xlutils.copy import copy    
from xlrd import open_workbook

#book exists
try:
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")

    start = 45751
    
    for x in range(10000000):
            print(x*5+start)
            
            page = requests.get('http://maplestory.nexon.net/rankings/world-ranking/reboot?pageIndex=' + str(x*5+start) + '#ranking')
            tree = html.fromstring(page.content)

            img = tree.xpath("//tr/td/img/@title")
            row = tree.xpath("//tr/td/text()")

            for i in range(5):
                
                sheet1.write(x*5+i, 0, int(row[i*7]))
                sheet1.write(x*5+i, 1, row[i*7+2])
                sheet1.write(x*5+i, 2, img[i])
                sheet1.write(x*5+i, 3, int(row[i*7+3].strip()))
                book.save("new.xls")


    
except:
#book does not exist
    page = requests.get('http://maplestory.nexon.net/rankings/world-ranking/reboot#ranking')
    tree = html.fromstring(page.content)

    row = tree.xpath("//tr/td/text()")
    img = tree.xpath("//tr/td/img/@title")

    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet 1")


    sheet1.write(0, 0, "Rank")
    sheet1.write(0, 1, "Name")
    sheet1.write(0, 2, "Job")
    sheet1.write(0, 3, "Level")

    try:
        for i in range(5):
            sheet1.write(i+1, 0, int(row[i*7]))
            sheet1.write(i+1, 1, row[i*7+2])
            sheet1.write(i+1, 2, img[i])
            sheet1.write(i+1, 3, int(row[i*7+3].strip()))


        for x in range(1000):
            page = requests.get('http://maplestory.nexon.net/rankings/world-ranking/reboot?pageIndex=' + str(x*5+6) + '#ranking')
            tree = html.fromstring(page.content)

            img = tree.xpath("//tr/td/img/@title")
            row = tree.xpath("//tr/td/text()")

            for i in range(5):
                sheet1.write(x*5+6+i, 0, int(row[i*7]))
                sheet1.write(x*5+6+i, 1, row[i*7+2])
                sheet1.write(x*5+6+i, 2, img[i])
                sheet1.write(x*5+6+i, 3, int(row[i*7+3].strip()))
        
    except:
        book.save("highscore.xls")

    book.save("highscore.xls")

