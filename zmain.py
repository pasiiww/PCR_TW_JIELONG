


from pypinyin import lazy_pinyin, Style
from listm import yuntop,ptoyun,listma,idicon
yuntop['ㄩ'] = 'v'
yuntoicron = {}
same = ['jh','ch','sh','r','z','c','s']
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
'iu':'ou' ,'uen':'un',
've':'yue','van':'yuan','vn':'yun','r':'er'
}
same2 = {'zhi':'jh','chi':'ch','shi':'sh','ri':'r','zi':'z','ci':'c','si':'s'}


def trans_text_tolist(text,pinyin=False):
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

def get(text,pinyin=False,drawmean = True):
    x = trans_text_tolist(text,pinyin)
    imgs = []
    pinyin = []
    mean = []
    for i in x:
        img = get_single_icon(i[0])
        if drawmean:
            draw = ImageDraw.Draw(img)
            
            text_border(draw,2,2,i[2][:3],(255,250,205),(0,0,0))
            text_border(draw,56,56,i[2][-1],(255,250,205),(0,0,0))
        imgs.append(img)
        pinyin.append(i[1])
        mean.append(i[2])
    #print(pinyin)
    return image_merge(imgs),pinyin,mean

import cv2
import numpy


text = '花'
pic,pinyin,mean = get(text)
img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  


def show(text):
    global pic,img,pinyin

    def MouseEvent(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global pic,img,pinyin
            #print(pinyin)
            #print(x,y)
            width, height = 76,76
            yn = int(y/height)
            xn = int(x/width)
            n = yn * 5 + xn 
            if n >= len(pinyin):
                return
            next_text = pinyin[n]
            pic,pinyin,mean = get(next_text,True)
            img = cv2.cvtColor(numpy.asarray(pic),cv2.COLOR_RGB2BGR)  
    
    cv2.namedWindow('test')
    cv2.setMouseCallback('test', MouseEvent) 

    while True:
        cv2.imshow('test', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break
    cv2.destroyAllWindows()


show(text)






