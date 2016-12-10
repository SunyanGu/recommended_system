import re
from get_url import shop_information
import xlwt

def set_style(name,height,bold=False):
  style = xlwt.XFStyle() # 初始化样式

  font = xlwt.Font() # 为样式创建字体
  font.name = name # 'Times New Roman'
  font.bold = bold
  font.color_index = 4
  font.height = height

  # borders= xlwt.Borders()
  # borders.left= 6
  # borders.right= 6
  # borders.top= 6
  # borders.bottom= 6

  style.font = font
  # style.borders = borders

  return style


f = xlwt.Workbook() #创建工作簿
sheet2 = f.add_sheet(u'sheet2',cell_overwrite_ok=True) #创建sheet2
row0 = [u'dth_title',u'bd_lat',u'bd_long',u'人均消费']
#生成第一行
for i in range(0,len(row0)):
    sheet2.write(0,i,row0[i],set_style('Times New Roman',220,True))
num = 0


for i in shop_information.find({},{'_id':0,'average_cost':1,'coordinate':1,"service" : 1,"environmental" : 1,"taste" : 1,'shop_name':1,'url':1}):

    if i['average_cost'] and i['service'] and i['environmental'] and i['taste']:
        average_list = re.findall(r'(\w*[0-9]+)',i['average_cost'])
        if len(average_list) > 0:
            average = int(average_list[0])
        else:
            average = 0

        service_list = re.findall(r'\w\.\w', i['service'])
        if len(service_list) > 0:
            service = float(service_list[0])
        else:
            service = 0

        environmental_list = re.findall(r'\w\.\w', i['environmental'])
        if len(environmental_list) > 0:
            environmental = float(environmental_list[0])
        else:
            environmental = 0

        taste_list = re.findall(r'\w\.\w', i['taste'])
        if len(taste_list) > 0:
            taste = float(taste_list[0])
        else:
            taste = 0
        #print(average,service,environmental,taste)
        if average < 100 and average > 30 and (service + environmental + taste)/3 > 9.2:
            #print(i['shop_name'])
            num = num + 1
            print(num)
            print(i['coordinate'])
            #print(i['url'])
            sheet2.write(num,0,i['shop_name'])
            sheet2.write(num,1,str(i['coordinate'][1]))
            sheet2.write(num,2,str(i['coordinate'][0]))
            sheet2.write(num, 3, i['average_cost'])

f.save('shop.xlsx')  # 保存文件
