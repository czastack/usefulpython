""" 隐藏win10资源管理器中视频、图片、文档、下载、音乐、桌面、3D对象七个文件夹 """

import winreg


Explorer = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer')
key = winreg.OpenKey(Explorer, r'FolderDescriptions')

names = (
    '{0ddd015d-b06c-45d5-8c4c-f59713854639}',  # 图片
    '{35286a68-3c57-41a1-bbb1-0eae73d76c95}',  # 视频
    '{7d83ee9b-2244-4e70-b1f5-5393042af1e4}',  # 下载
    '{a0c69a99-21c8-4671-8703-7934162fcf1d}',  # 音乐
    '{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}',  # 桌面
    '{f42ee2d3-909f-4907-8871-4c22fc0bf756}',  # 文档
)

for name in names:
    child = winreg.OpenKey(key, name + r'\PropertyBag', 0, winreg.KEY_ALL_ACCESS)
    # print(winreg.QueryValueEx(child, "ThisPCPolicy"))
    winreg.SetValueEx(child, "ThisPCPolicy", 0, 1, "Hide")

# 3D对象
NameSpace = winreg.OpenKey(Explorer, r'MyComputer\NameSpace')
winreg.DeleteKey(NameSpace, '{0DB7E03F-FC29-4DC6-9020-FF41B59E513A}')
