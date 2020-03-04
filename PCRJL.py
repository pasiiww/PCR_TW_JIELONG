import cv2
import numpy
from pypinyin import lazy_pinyin, Style
from listm import yuntop,ptoyun,listma,idicon
import json

yuntop['ㄩ'] = 'v'
yuntoicron = {}
same = ['jh','ch','sh','r','z','c','s']

last_pinyin = None
returnpy = None
lastadd = None
def initlize():
    
    for i in listma:
        y = i[3]
        p = yuntop[y]
        
        if p in same:
            #print(p)
            p = 'same'
        if p not in yuntoicron:
            yuntoicron[p] = [(i[0],yuntop[i[4]],i[2])]
            #print((i[0],yuntop[i[4]]))
        else:
            yuntoicron[p].append((i[0],yuntop[i[4]],i[2]))
    
    return 




xiuzhen = {
'iu':'ou' ,'uen':'un','ui':'uei','ueng':'eng',
've':'yue','van':'yuan','vn':'yun','r':'er'
}
same2 = {'zhi':'jh','chi':'ch','shi':'sh','ri':'r','zi':'z','ci':'c','si':'s'}


dests = []
import os
if os.path.exists('goal.txt'):
    goal = open('goal.txt',encoding='utf-8')
    dest = goal.readline()
    d = dest.split(" ")
    #print(dest,d)
    for i in d:
        if i in same2:
            i = 'same'
        if i in xiuzhen:
            i = xiuzhen[i]
        if len(i) :
            dests.append(i)
        #dest = goal.readline()
    goal.close()


nametoindex = {}
clicked = set()
fjson = None
if os.path.exists('clicked.json'):
    f = open('clicked.json',encoding='utf-8',mode = 'r')
    fjson = json.load(f )
    f.close()
    index = 0
    for i in fjson['data']:
        nametoindex[i['name']] = index
        index += 1
        if 'clicked' in i and i['clicked'] == True:
            clicked.add(i['name'])

print("图鉴已收集: "+str(len(clicked)))
def trans_text_tolist(text,pinyin=False):
    global last_pinyin
    if pinyin:
        if text in same:
            return yuntoicron['same']
        else:
            return yuntoicron[text]
    #tailtext = text[-1]
    a = lazy_pinyin(text,Style.FINALS)
    b = lazy_pinyin(text)
    #print(a[-1],b[-1])
    p = a[-1]
    if b[-1] in same2:
        p = 'same'
    elif a[-1] in xiuzhen:
        p = xiuzhen[a[-1]]
    if last_pinyin == None:
        last_pinyin = p
    return yuntoicron[p]
   


from PIL import Image
im = Image.open("icons.png")


def get_single_icon(id_):
    index = idicon[id_]
    box = (index[0]+2,index[1]+2,index[0]+78,index[1]+78)
    region = im.crop(box)
    return region
                    
    #region.show()

def image_merge(images): 
    width, height = 76,76
    nums = len(images)
    if nums > 5:
        new_width = 5 * width
        new_height = int(0.99999 + nums/5) * height
        
    else:
        new_width = nums * width
        new_height = height

    new_img = Image.new('RGB', (new_width, new_height), (255,255,255)) 

    x = y = 0
    for img in images: 
        new_img.paste(img, (x, y)) 
        x += width 
        if x >= width * 5:
            x = 0
            y += height

    return new_img
  

initlize()

from PIL import ImageFont, ImageDraw
font = ImageFont.truetype("simhei.ttf", 20 , encoding="utf-8")


def text_border(draw, x, y, text, shadowcolor, fillcolor):
    # thin border
    #draw.text((0,0), text, font=font, fill=(0, 0, 0))
    #return
    #print( x, y, text, shadowcolor, fillcolor)
    draw.text((x - 1, y), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - 1), text, font=font, fill= shadowcolor)
    draw.text((x, y + 1), text, font=font, fill= shadowcolor)
 
    # thicker border
    draw.text((x - 1, y - 1), text, font=font, fill= shadowcolor)
    draw.text((x + 1, y - 1), text, font=font, fill= shadowcolor)
    draw.text((x - 1, y + 1), text, font=font, fill= shadowcolor)
    draw.text((x + 1, y + 1), text, font=font, fill= shadowcolor)
 
    # now draw the text over it
    draw.text((x, y), text, font=font, fill= fillcolor)

import random
def get(text,pinyin=False,drawmean = True,shuff = False):
    global dests,returnpy
    x = trans_text_tolist(text,pinyin)
    if shuff:
        random.shuffle(x)
    if len(dests):
        x.sort(key=lambda i:i[1] in dests or i[2] in dests,reverse = True)
    else:
        x.sort(key=lambda i:i[2] in clicked)
    imgs = []
    pinyin = []
    mean = []
    for i in x:
        img = get_single_icon(i[0])
        if drawmean and len(dests) == 0:
            draw = ImageDraw.Draw(img)
            text_border(draw,2,2,i[2][:3],(255,250,205),(0,0,0))
            text_border(draw,56,56,i[2][-1],(255,250,205),(0,0,0))
        elif i[1] in dests or i[2] in dests:
            draw = ImageDraw.Draw(img)
            text_border(draw,2,2,i[2][:3],(255,250,205),(0,0,0))
            text_border(draw,56,56,i[2][-1],(255,250,205),(0,0,0))
        if i[2] in clicked:
            draw = ImageDraw.Draw(img)
            #text_border(draw,2,2,i[2][:3],(255,250,205),(0,0,0))
            text_border(draw,2,22,"〇",(255,250,205),(254,67,101))
        imgs.append(img)
        pinyin.append(i[1])
        mean.append(i[2])

    retires_box = (0+2,944+2,0+78,944+78)
    retires = im.crop(retires_box)
    draw = ImageDraw.Draw(retires)
    text_border(draw,20,20,"重新",(255,250,205),(0,0,0))
    text_border(draw,20,40,"开局",(255,250,205),(0,0,0))
    imgs.append(retires)
    if returnpy:
        #print(returnpy)
        return_box = (0+2,944+2,0+78,944+78)
        returnb = im.crop(retires_box)
        draw = ImageDraw.Draw(returnb)
        text_border(draw,20,20,"返回",(255,250,205),(0,0,0))
        text_border(draw,20,40,"上层",(255,250,205),(0,0,0))
        imgs.append(returnb)
    #retires.show()
    #print(pinyin)
    return image_merge(imgs),pinyin,mean



def anaytext(text):
    a = lazy_pinyin(text,Style.FINALS)
    b = lazy_pinyin(text)
    #print(a[-1],b[-1])
    p = a[-1]
    if b[-1] in same2:
        p = 'same'
    elif a[-1] in xiuzhen:
        p = xiuzhen[a[-1]]
    
    if p not in  yuntoicron:
        text = input("好像没找到这个音: " + p + "的接龙，要不换一个吧\n")
        return anaytext(text)
    return text

print("请输入开始的字,之后按任意键退出")
text = input()
text = anaytext(text)
pic,pinyin,mean = get(text)
img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  


def show(text):
    global pic,img,pinyin,mean,returnpy
    global last_pinyin,lastadd
    def MouseEvent(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global pic,img,pinyin,last_pinyin,mean,returnpy,lastadd
            #print(pinyin)
            #print(x,y)
            width, height = 76,76
            yn = int(y/height)
            xn = int(x/width)
            n = yn * 5 + xn 
            if n == len(pinyin):

                f = open('clicked.json',encoding='utf-8',mode = 'w')
                #fjson = json.load(f)
                for i in clicked:
                    fjson['data'][nametoindex[i]]['clicked'] = True
                json.dump(fjson,f,ensure_ascii=False,indent=4)
                f.close()

                print("请输入：")
                cv2.destroyAllWindows()
                text = input()
                text = anaytext(text)
                cv2.namedWindow('test')
                cv2.setMouseCallback('test', MouseEvent) 
                pic,pinyin,mean = get(text)
                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
            elif n == len(pinyin) + 1:
                if lastadd:
                    clicked.remove(lastadd)
                last_pinyin = returnpy
                returnpy = None
                pic,pinyin,mean = get(last_pinyin,True)
                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
                
                return
            elif n > len(pinyin) + 1:
                return
            else:
                if mean[n] not in clicked:
                    lastadd = mean[n]
                    clicked.add(mean[n])
                else:
                    lastadd = None
                
                returnpy = last_pinyin

                next_text = pinyin[n]
                if next_text == last_pinyin:
                    pic,pinyin,mean = get(next_text,True,shuff=True)
                else:
                    pic,pinyin,mean = get(next_text,True)
                    last_pinyin = next_text

                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
    
    cv2.namedWindow('test')
    cv2.setMouseCallback('test', MouseEvent) 

    while True:
        cv2.imshow('test', img)
        if cv2.waitKey(1) != -1 :  
            f = open('clicked.json',encoding='utf-8',mode = 'w')
            #fjson = json.load(f)
            for i in clicked:
                fjson['data'][nametoindex[i]]['clicked'] = True
            json.dump(fjson,f,ensure_ascii=False,indent=4)
            f.close()
            break
    
    cv2.destroyAllWindows()


show(text)







