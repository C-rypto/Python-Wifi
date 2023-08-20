import re
import tkinter as tk
from tkinter import filedialog
import itertools as its

window = tk.Tk()
window.withdraw()

print("---密码本生成器---")
words = input("输入密码元素(如:abcd1234):")

while 1:
    try:
        repeat = int(input("输入密码长度(整数):"))
        break
    except ValueError:
        print("你输入的不是整数，请重新输入。")

input("按[Enter回车]选择密码本保存文件夹")
path = filedialog.askdirectory()

file_name = input("输入密码本文件名:")
file_name += ".txt"

codebook_path = path + "/" + file_name

print("密码本路径为:",codebook_path)

pwds = its.product(words,repeat=repeat)
with open(codebook_path,"a") as f:
    for i in pwds:
        f.write("".join(i))
        f.write("".join("\n"))
