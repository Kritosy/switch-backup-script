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
	info = chan.recv(99999).decode()		#接收输出信息,并
	client.close()							#断开连接
	return info

def CreateFile(unit,hostname,data,path):
	FileName = hostname + unit +'.txt'
	path1 = os.path.join(path,FileName)
	with open(path1,'a') as file_handle:
		file_handle.write(data)

def MakeDir(path):
	if os.path.exists(path):
		print('Dir ' + path + ' already existed')
	else:
		os.mkdir(path)
		print('Dir ' + path + ' created')

FilePath = datetime.datetime.now().strftime("%Y-%m-%d") + 'backup'
MakeDir(FilePath)
database = xlrd.open_workbook('IP.xlsx')
table = database.sheet_by_name('Sheet1')
i = 1
username = 'lysxxzx'
password = 'lys@2018xxzx'
while table.cell_value(i,0) < 3:
	unit = table.cell_value(i,1)
	hostname = table.cell_value(i,2)
	DeviceInfo = PrintInfo(hostname,username,password)
	CreateFile(unit,hostname,DeviceInfo,FilePath)
	print(unit + ' is done!')
	i = i+1
