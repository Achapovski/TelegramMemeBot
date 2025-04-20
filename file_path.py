import os

# print(os.listdir(), os.scandir(), sep="\n")


for i in os.scandir():
    print(i.path, i.name, i.stat())
