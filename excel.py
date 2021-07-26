import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
c1 = sheet.cell(row= 1, column=1)
c1.value = "ehqhd"
wb.save('/Users/choi/Desktop/datamapping/test.xlsx')