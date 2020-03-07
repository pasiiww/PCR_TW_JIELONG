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
JIETOU = 0
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
        if i['name'] == '接頭霸王' and 'clicked' in i and i['clicked'] == True:
            JIETOU = 1
        nametoindex[i['name']+str(i["iconID"])] = index
        index += 1
        if 'clicked' in i and i['clicked'] == True:
            clicked.add(i['name']+str(i["iconID"]))

print("图鉴已收集: "+str(len(clicked)-JIETOU))


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

def image_merge(images,wd = 5,fix_size = None): 
    width, height = 76,76
    nums = len(images)
    if nums > wd:
        new_width = wd * width
        new_height = int(0.99999 + nums/wd) * height
        
    else:
        new_width = nums * width
        new_height = height

    if fix_size:
        new_img = Image.new('RGB', fix_size, (255,255,255)) 
    else:
        new_img = Image.new('RGB', (new_width, new_height), (255,255,255)) 

    x = y = 0
    for img in images: 
        new_img.paste(img, (x, y)) 
        x += width 
        if x >= width * wd:
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
        x.sort(key=lambda i:i[2]+i[0] in clicked)
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
        if i[2]+i[0] in clicked:
            draw = ImageDraw.Draw(img)
            #text_border(draw,2,2,i[2][:3],(255,250,205),(0,0,0))
            text_border(draw,2,22,"〇",(255,250,205),(254,67,101))
        imgs.append(img)
        pinyin.append(i[1])
        mean.append(i[2] + i[0])

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

wdsize = 10
def checkclicked(startindex = 0,one_page_num = 50):
    imgs = []
    ind = startindex
    while (ind < len(fjson['data'])) and (ind < startindex + one_page_num):
        i = fjson['data'][ind]
        id_ = i['iconID']
        name_ = i['name']
        
        clicked_ = (name_ + str(id_) in clicked)
        icon = get_single_icon(str(id_) )
        draw = ImageDraw.Draw(icon)
        
        if clicked_:
            text_border(draw,2,2,name_[:3],(255,250,205),(0,0,0))
            text_border(draw,2,22,name_[3:],(255,250,205),(0,0,0))
            
            text_border(draw,56,56,"〇",(255,250,205),(254,67,101))
        else:
            text_border(draw,2,2,name_[:3],(255,250,205),(155,155,155))
            text_border(draw,2,22,name_[3:],(255,250,205),(155,155,155))
        imgs.append(icon)
        ind += 1

    retires_box = (0+2,944+2,0+78,944+78)
    retires = im.crop(retires_box)
    draw = ImageDraw.Draw(retires)
    if ind < len(fjson['data']):
        text_border(draw,10,30,"下一页",(255,250,205),(0,0,0))
    else:
        text_border(draw,10,30,"下一页",(255,250,205),(155,155,155))
        
    imgs.append(retires)

    retires_box = (0+2,944+2,0+78,944+78)
    retires = im.crop(retires_box)
    draw = ImageDraw.Draw(retires)
    if ind > one_page_num:
        text_border(draw,10,30,"上一页",(255,250,205),(0,0,0))
    else:
        text_border(draw,10,30,"上一页",(255,250,205),(155,155,155))
        
    imgs.append(retires)
    retires_box = (0+2,944+2,0+78,944+78)
    retires = im.crop(retires_box)
    draw = ImageDraw.Draw(retires)
    
    text_border(draw,20,30,"保存",(255,250,205),(0,0,0))
    
    imgs.append(retires)

    return image_merge(imgs,wdsize,(76 * wdsize , 76 * int((one_page_num+3)/wdsize+0.99))),ind
    

def anaytext(text):
    if not text:
        text = input()
        return anaytext(text)
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




pic,pinyin,mean,img = None,None,None,None
def show(text):
    global pic,img,pinyin,mean,returnpy,img
    global last_pinyin,lastadd
    def MouseEvent(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global pic,img,pinyin,last_pinyin,mean,returnpy,lastadd,img
            #print(pinyin)
            #print(x,y)
            width, height = 76,76
            yn = int(y/height)
            xn = int(x/width)
            n = yn * 5 + xn 
            if n == len(pinyin):
                lastadd = None
                returnpy = None
                
                for i in clicked:
                    fjson['data'][nametoindex[i]]['clicked'] = True
                f = open('clicked.json',encoding='utf-8',mode = 'w')
                json.dump(fjson,f,ensure_ascii=False,indent=4)
                f.close()

                print("请输入：")
                cv2.destroyAllWindows()
                text = input()
                text = anaytext(text)
                cv2.namedWindow('test')
                cv2.setMouseCallback('test', MouseEvent) 
                pic,pinyin,mean = get(text)
                last_pinyin  = text
                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
            elif n == len(pinyin) + 1:
                if lastadd:
                    clicked.remove(lastadd)
                lastadd = None
                last_pinyin = returnpy
                returnpy = None
                pic,pinyin,mean = get(last_pinyin,False)
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
            #fjson = json.load(f)
            for i in clicked:
                fjson['data'][nametoindex[i]]['clicked'] = True
            f = open('clicked.json',encoding='utf-8',mode = 'w')
            json.dump(fjson,f,ensure_ascii=False,indent=4)
            f.close()
            break
    
    cv2.destroyAllWindows()

Flag = True
start_index = 0
returnind = 0
one_page_num = 57
def showalllist():
    global start_index,wdsize,returnind,img,Flag
    def MouseEvent(event, x, y, flags, param):
        global start_index,one_page_num,wdsize,returnind,img,Flag
        if event == cv2.EVENT_LBUTTONDOWN:
            width, height = 76,76
            yn = int(y/height)
            xn = int(x/width)
            n = yn * wdsize + xn 
            if n == returnind - start_index:
                start_index += one_page_num
                if start_index >= len(fjson['data']):
                    start_index = 0
                pic, returnind = checkclicked(start_index,one_page_num)
                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR) 
                return 
            elif n == returnind + 1 - start_index:
                start_index -= one_page_num
                if start_index < 0 :
                    start_index = len(fjson['data']) - one_page_num 
                pic, returnind = checkclicked(start_index,one_page_num)
                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
                return
            elif n == returnind + 2 -start_index:
                Flag = False
                #text = anaytext(text)
                #show(text)
                return
            elif n > returnind + 3 - start_index:
                return
            else:
                
                index = start_index + n
                icon = fjson['data'][index]
                
                if icon['name'] + str(icon['iconID']) not in clicked:
                    print(icon["name"],'add')
                    clicked.add(icon['name'] + str(icon['iconID']))
                    fjson['data'][index]['clicked'] = True
                elif icon['name']+ str(icon['iconID']) in clicked:
                    print(icon["name"],'remove')
                    clicked.remove(icon['name'] + str(icon['iconID']))
                    fjson['data'][index]['clicked'] = False
                pic, returnind = checkclicked(start_index,one_page_num)
                img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
    
    cv2.namedWindow('test')
    cv2.setMouseCallback('test', MouseEvent) 
    pic, returnind = checkclicked(0,one_page_num)
    img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR) 

    while Flag == True:
        cv2.imshow('test', img)
        if cv2.waitKey(1) != -1 :  
            break

    f = open('clicked.json',encoding='utf-8',mode = 'w')
    json.dump(fjson,f,ensure_ascii=False,indent=4)
    f.close()
    cv2.destroyAllWindows()
    return

print("请输入开始的字,之后按任意键退出,输入1设置已收集的图鉴（回车结束）")
text = input()
while not text:
    text = input()
if text and text[0] == '1':
    print("请选择已经开通的图鉴")
    showalllist()
    if "接頭霸王20055" in clicked:
        JIETOU = 1
    print("图鉴已收集: "+str(len(clicked)-JIETOU))
    text = input("请输入开始的字/韵母：")
    
text = anaytext(text)
pic,pinyin,mean = get(text)
img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
show(text)







