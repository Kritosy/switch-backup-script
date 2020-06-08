import paramiko
import time
import xlrd
import os
import datetime

def PrintInfo( hostname,username,password): #连接并打印交换机信息，存放至变量info
	client = paramiko.SSHClient() 			#创建SSH连接
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())	#自动确认陌生设备
	client.connect(hostname=hostname,username=username,password=password) #连接
	chan = client.invoke_shell()			#打开channel
	chan.send('screen-length 0 tem \n')		#输入命令
	time.sleep(1)
	chan.send('dis cur \n')
	time.sleep(5)							#设置等待时间
	info = chan.recv(99999).decode()		#接收输出信息,并编码
	client.close()							#断开连接
	return info

def CreateFile(unit,hostname,data,path):    #unit是部门名称，可根据实际情况取舍
	FileName = hostname + unit +'.txt'      #创建单个文件
	path1 = os.path.join(path,FileName)     #这个路径是为了方便将输出文件放入当前目录中备份文件夹下
	with open(path1,'a') as file_handle:	#将获取的信息写入文件
		file_handle.write(data)

def MakeDir(path):							#在脚本运行路径下新建一个备份文件夹，判断是否存在
	if os.path.exists(path):
		print('Dir ' + path + ' already existed')
	else:
		os.mkdir(path)
		print('Dir ' + path + ' created')

DirPath = datetime.datetime.now().strftime("%Y-%m-%d") + 'backup' #根据系统时间给备份文件夹起名
MakeDir(DirPath)												  #新建备份文件夹			
database = xlrd.open_workbook('IP.xlsx') 	#读取excel
table = database.sheet_by_name('Sheet1')
i = 1
while table.cell_value(i,0) < 3:       		#循环读取具体信息
	unit = table.cell_value(i,1)
	hostname = table.cell_value(i,2)
	username = table.cell_value(i.3)
	password = table.cell_value(i,4)
	DeviceInfo = PrintInfo(hostname,username,password)
	CreateFile(unit,hostname,DeviceInfo,DirPath)
	print(unit + ' is done!')
	i = i+1
