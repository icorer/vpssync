#coding=utf-8
#读取七牛配置文件信息 backup.config
'''
AK Value 
SK Value
Cloud Bucket 
Source floder 备份目录路径
'''


import os 
#安装模板
print ("Check and configure the runtime environment...")
try:
	os.system("pip install sevencow > debug_info.dat");
	os.remove("debug_info.dat");
except:
	data=raw_input("Error: pip qiniu sdk is wrong!");
	exit();

print("Start running...\n");
from sevencow import Cow
#读取参数

try:
    fhandle=open("backup.config","rb");
except :
    print("Error: backup.config is not exists!");
    fhandle=open("backup.config","wb");
    fhandle.write("AK\nSK\nCloud Bucket\nSource Floder");
    fhandle.close();
    data=raw_input("We help you created a template file,please edit the file.");
    exit();

#文件存在，开始读取并判断参数
lines={};
i=0;
for data in fhandle.readlines():
    data=data.replace("\r\n","");
    data=data.replace("\n","");
    i=i+1;
    lines[i]=data;

ak=lines[1];
while len(ak)!=40: #AK 密钥验证
    ak=raw_input("AK Key is wrong,Input:");
sk=lines[2];
while len(sk)!=40: #SK 密钥验证
    sk=raw_input("SK Key is wrong,Input:");

bucket=lines[3];
cow_handle=Cow(ak,sk);
cow_bucket = cow_handle.get_bucket(bucket)
bucket=lines[3]; #获取bucket验证
try:
    cow_bucket.list_files();
except:
    data=raw_input("Error:don not have this name of Bucket!");
    exit();
backup_dir=lines[4];
while os.path.exists(backup_dir)!=True: #对目录进行验证
    backup_dir=raw_input("Directory does not exist , please re-input:");

#创建备份目录
save_disk="./save_disk/";
if os.path.exists(save_disk)!=True:
    os.mkdir(save_disk);

#压缩文件
import tarfile
import time
tar_save_name=raw_input("Input the the name of backup tar file :");
tar_save_name=tar_save_name.replace("\r\n","");
tar_save_name=tar_save_name.replace("\n","");
if tar_save_name=="":
	tar_save_name=time.strftime("%Y%m%d%H%M%S")+".tar.gz"; #云端保存名称
else:
	tar_save_name=tar_save_name+".tar.gz";
tar_save_location=save_disk+tar_save_name; #备份压缩文件保存位置

print("Begin Create a tar.gz file...");
tar_handle=tarfile.open(tar_save_location,"w:gz"); #创建压缩文件
print("Start packing directory...");
tar_handle.add(backup_dir);#添加备份目录
tar_handle.close();
print("Directory compression is completed.");

#上传文件
print("Syncing files , do not close the program...");
try:
    cow_bucket.put(tar_save_location,keep_name=True,override=True);
except:
    print("error: Upload failed!");
    exit();

try:
    cow_bucket.move(tar_save_location,tar_save_name);
except:
    bucket=raw_input("Error: Cloud rename fails ,Check the file with the same name!");
    exit();

print "\nCloud File Name: ",tar_save_name;
#bucket=raw_input("\nOK,It is done!");
'''
import smtplib
mail_server="smtp.qq.com";
mail_port=465 ;
mail_from_address="";
mail_to_address="";
mail_subject="文件备份完毕";
mail_login_name="";
mail_login_pawssword="";

import time
msg_info="目录：[ "+backup_dir+" ] 备份工作已经完毕！" + time.strftime("%Y年%m月%H时%M分%S秒");

mail=smtplib.SMTP_SSL(mail_server,mail_port);
mail.login(mail_login_name,mail_login_pawssword);
mail.sendmail(mail_from_address,mail_to_address,"From:"+mail_from_address+"\nTo:"+mail_to_address+"\nSubject:"+mail_subject+"\n\n"+msg_info);
mail.quit();
'''