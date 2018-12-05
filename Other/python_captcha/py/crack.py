# coding:utf-8
from PIL import Image
import time
import hashlib
import math
import os
'''
im = Image.open("captcha.gif")
# 将图片转换为8位像素模式
im.convert("P")
# 打印颜色直方图   白色序号255
#print(im.histogram())
im2 = Image.new("P", im.size, 255)  # 创建一个白色的图片
#im2.show()

for x in range(im.size[1]): # im.size[1] 为宽
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        if pix == 220 or pix == 227:
            im2.putpixel((y, x), 0)     # 改变单个像素点颜色，y,x为坐标 0为颜色
#im2.show()

#提取单个字符图片
inletter = False    # 末尾变量
foundletter = False # 开头变量
start = 0
end = 0
letters = []
for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y, x))
        if pix != 255: #如果像素点不等于255 就是像素点不为白色,则令末尾变量为真
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))

    inletter = False
# 得到每个图片的开头和结尾的序号
#print(letters)

count = 0
for letter in letters:
    #m = hashlib.md5()
    # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    #m.update(("%s%s" % (time.time(), count)).encode('utf-8')) # 哈希加密后需要编码，在每次update后面加上一个encode
    #im3.save("./%s.gif" % (m.hexdigest()))
    count += 1
'''
# 使用向量空间搜索引擎来做字符识别
class VectorCompare:
    # 计算矢量大小
    # 计算平方和
    def magnitude(self,concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2  # total = total + count**2
        return math.sqrt(total)  # sqrt 开平方

    # 计算矢量之间的cos值
    def relation(self, concordancel, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordancel.items():
            # if concordance2.has_key(word):报错'dict' object has no attribute 'has_key'
            # 改成word in concordance2
            if word in concordance2:
            #if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue/(self.magnitude(concordancel) * self.magnitude(concordance2))

# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

v = VectorCompare()

iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# 加载训练集
imageset = []
for letter in iconset:
    for img in os.listdir('../iconset/%s/' % (letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("../iconset/%s/%s" % (letter, img))))
        imageset.append({letter: temp})

#count = 0

im = Image.open("../captcha.gif")
# 将图片转换为8位像素模式
#im.convert("P")
# 打印颜色直方图   白色序号255
# print(im.histogram())
im2 = Image.new("P", im.size, 255)  # 创建一个白色的图片
im.convert("P")
temp = {}

for x in range(im.size[1]): # im.size[1] 为宽
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        if pix == 220 or pix == 227:
            im2.putpixel((y, x), 0)     # 改变单个像素点颜色，y,x为坐标 0为颜色
im2.show()
# 提取单个字符图片
inletter = False  # 末尾变量
foundletter = False  # 开头变量
start = 0
end = 0
letters = []
for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y, x))
        if pix != 255:  # 如果像素点不等于255 就是像素点不为白色,则令末尾变量为真
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))

    inletter = False
# 得到每个图片的开头和结尾的序号
# print(letters)

count = 0

# 对验证码图片进行分割
for letter in letters:
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
    # m.update(("%s%s" % (time.time(), count)).encode('utf-8')) # 哈希加密后需要编码，在每次update后面加上一个encode
    # im3.save("./%s.gif" % (m.hexdigest()))
    #count += 1
    guess = []

    for image in imageset:
        # image.iteritems:报错'dict' object has no attribute 'iteritems'
        # 改成image.items()
        for x, y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0], buildvector(im3)), x))

    guess.sort(reverse=True)
    print("", guess[0])
    count += 1



'''
his = im.histogram()
values = {}
for i in range(256):
    values[i] = his[i]
for j, k in sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]: # reverse为True 降序排列 为False 升序排列
    # x: x[1]  意思是x为 j,k ，然后将第二项 k 作为关键字  然后给sorted排序
    print(j, k)
    # 220 227 分别为红色和灰色 255为白色
'''