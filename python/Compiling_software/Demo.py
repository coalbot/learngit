#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,shutil,re,string,sys,shutil,win32com.client 


#os.system("pause")

def mkdir(path):#新建文件夹
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def PP_file_name(file_dir):#查找子目录文件
    for root, dirs, files in os.walk(file_dir):
        return files

def re_fine(run_file_name,pattern):#正则匹配
        for index in range(len(run_file_name)):
                if pattern.findall(run_file_name[index]):
                        return(run_file_name[index])


#读取软件所在位置
current_path = os.getcwd()
#判断软件所在位置是否正确
A = input("当前目录是： " + current_path + " 吗？\n[y/n]")#
if A == "n":
    current_path = input("请输入类似 " + current_path + "的地址。\n")


#######################################################################################
#初始化
Set_path = current_path + "\\" + r"Set"
mkdir(Set_path)


print("把需要要编译的文件放入Set文件夹内\nPut the files you need to compile into the Set folder")#
os.system("pause")

#######################################################################################
#读取编译软件所在位置

pyinstaller_file = PP_file_name(current_path)
pattern = re.compile("(.*?)pyinstaller(.*?).exe(.*?).lnk")
pyinstaller_file = re_fine(pyinstaller_file,pattern)

if not pyinstaller_file:
    print("请把pyinstaller.exe的快捷方式放到当前目录下\nPlease put the pyinstaller.py shortcut in the current directory")
    os.system("pause")

pyinstaller_file = current_path + "\\" + pyinstaller_file

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(pyinstaller_file)

pyinstaller_path = shortcut.Targetpath
#判断编译软件位置是否正确
B = input("pyinstaller的安装目录是: " + pyinstaller_path + " 吗？\n[y/n]")

if B == "n":
        pyinstaller_path = input("请输入类似 " + pyinstaller_path + "的地址。\n")


#######################################################################################
#读取待添加文件所在位置的文件
test_file_name = PP_file_name(Set_path)
pattern = re.compile("(.*?).py")
test_file_name = re_fine(test_file_name,pattern)

if not test_file_name:
    test_file_name = "Demo.py"

        
#选择待添加文件的文件名
C = input("你想要编译的软件名是： " + test_file_name + " 吗？\n[y/n]")
if C == "n":
    test_file_name = input("请输入类似 " + test_file_name + "的名字。\n")
    

test_file_name = ''.join(re.split('.py',test_file_name))


#######################################################################################
#询问是否改变图标
ico_path = current_path + "\\" + r"ICO"

D = input("您是否要更换自己的图标呢？\n[y/n]")
if D == "n":
    print("您的图标将不会被更换")
    ico_flag = 0
else:
    print("把需要要编译的文件放入ICO文件夹内\nPut the files you need to compile into the ICO folder")#
    mkdir(ico_path)
    os.system("pause")
    
    ico_file_name = PP_file_name(ico_path)
    pattern = re.compile("(.*?).ico")
    ico_file_name = re_fine(ico_file_name,pattern)

    if not ico_file_name:
        print("您并没有将ICO格式的图片放在ICO文件夹里呢")
        os.system("pause")
    ico_flag = 1
    
    
    
#######################################################################################


#确定生成文件位置
save_path = current_path + "\\" + test_file_name

#######################################################################################

#待添加文件所在位置

Set_file_path = Set_path + "\\" + test_file_name + r".py"

#判断待添加文件位置是否存在待添加文件
while not os.path.exists(Set_file_path):
    E = input("您似乎并没有将待编译的文件放在Set文件夹里，请问您是否要继续进行编译呢？\n[y/n]")
    if E == "n":
        break

#######################################################################################

#判断生成文件位置是否存在生成文件夹

if os.path.exists(save_path):
    G = input("您之前似乎编译过呢，是否将之前的文件删除并重新编译呢？\n[y/n]")
    if G == "n":
        print("看来您并不想重新编译，下次再来吧")
        Compile_flag = 0
        ico_flag = 0
    else:
        shutil.rmtree(save_path)
        print("文件夹删除成功！")
        Compile_flag = 1
else:
    Compile_flag = 1
    
#######################################################################################

#判断待添加图标位置是否存在待添加图标 

while (ico_flag == 1):
    ico_file_name = PP_file_name(ico_path)
    pattern = re.compile("(.*?).ico")
    ico_file_name = re_fine(ico_file_name,pattern)
    if ico_file_name:
        F = input("您确定要使用" + ico_file_name + "作为你的图标吗\n[y/n]")
        if F == "n":
            ico_file_name = input("请输入您的类似 Demo.ico 的图标名并将需要要编译的文件放入ICO文件夹内或选择输入其他以不更换图标")
            pattern = re.compile("(.*?).ico")
            ico_file_name = re_fine(ico_file_name,pattern)
            if not ico_file_name:
                print("您的图标将不会被更换")
                ico_flag = 0
                break
        else:
            ico_file_path = ico_path + "\\" + ico_file_name
            print("您的图标将会被更换")
            ico_flag = 2
            break
    else:
        F = input("您还是没有将ICO图标放在ICO文件夹里，您确定要更换图标吗\n[y/n]")
        if F == "n":
            print("您的图标将不会被更换")
            ico_flag = 0
            break




#######################################################################################

if Compile_flag:
    print("编译中，请稍等......")
    if ico_flag:
        system_shell = pyinstaller_path +  r" -F " +  r" -i " + ico_file_path + " " + Set_file_path
    else:
        system_shell = pyinstaller_path +  r" -F " + Set_file_path
    os.system(system_shell)
    
    mkdir(save_path)
    shutil.move(current_path + "\\" + r"dist",save_path)
    shutil.move(current_path + "\\" + r"build",save_path)
    shutil.move(current_path + "\\" + test_file_name + r".spec",save_path)
    print("编译成功啦!!!，软件放在" + test_file_name + "文件夹下的dist文件夹里，请查收。")
    os.system("pause")








