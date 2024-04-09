import tkinter as tk
import cv2, pyocr
from PIL import Image
import tempfile as tmp
import numpy as np

file=input("select file：")
img=cv2.imread(file,1)
#img=cv2.imread("10.jpg",1)scale=1.0 #倍率
height,width=img.shape[0],img.shape[1];centre=(int(width/2),int(height/2))
base=tk.Tk();base.geometry(),base.title('hoge')

scale,px,deg,deg0,deg0_,deg1,deg1_=1,20,0,0,0,0,0
event=0

class Rtxt:
    cv2.namedWindow('imgWindow'),cv2.namedWindow('imgWindow_')
    def do_():
        def execute():
            print(height)
            pBefore=np.float32([[0,0],[0,height],[width,height],[width,0]]) #[x,y]
            pAfter=np.float32([[deg1,0-deg0],[deg1_,height],[width-deg1_,height],[width-deg1,0-deg0_]])
            transP=cv2.getPerspectiveTransform(pBefore,pAfter)
            img2=cv2.warpPerspective(img,transP,(width,height))

            trans=cv2.getRotationMatrix2D(centre, deg, scale)
            img0=cv2.warpAffine(img2, trans, (width, height))
            def draw(event=0,dX=0,dY=0,flags=None,params=None): #描画
                if event==cv2.EVENT_LBUTTONDOWN:
                    dX=dX;dY=dY
                    print(dX,dY)
                    cv2.circle(img0, (dX, dY), px, (255, 51, 204), -1)
                    cv2.circle(img, (dX, dY), px, (255, 51, 204), -1)

                cv2.imshow('imgWindow',img2) #第1引数=window名, 第2引数=画像名

                #================#
                tpImg=cv2.addWeighted(img, 0, img0, 1, 0.0) #透過画像
                i=0
                for i in range(12):
                    i+=1
                    lineP=int(height-(height*((13-i)/13)))
                    cvLine=cv2.line(tpImg,(0,lineP),(width,lineP),(0, 255, 51),thickness=2)
                    tpBack=[
                        cvLine,cvLine,cvLine,cvLine,cvLine,cvLine,cvLine,cvLine,cvLine,cvLine,cvLine,cvLine
                    ];cv2.imshow('imgWindow',tpBack[11])
                cv2.setMouseCallback('imgWindow',draw)
                return pBefore,pAfter,transP,img2,trans,img0
            draw();return draw()[5]
        def trackbar1(position1):global deg1;deg1=position1;execute()
        def trackbar1_(position1_):global deg1_;deg1_=position1_;execute()
        def trackbar0(position0):global deg0;deg0=position0;execute()
        def trackbar0_(position0_):global deg0_;deg0_=position0_;execute()
        def trackbar(position):global deg;deg=position;execute()
        def pen(pxWeight):global px;px=pxWeight;execute()
        def sizing(rate):global scale;scale=rate;execute()

        def start():
            execute()
            tmpdir=tmp.TemporaryDirectory() #一時フォルダを作成
            print(tmpdir.name)
            newFname=str(tmpdir.name)+"/hoge.jpg"
            cv2.imwrite(newFname, execute()) #一時フォルダに変更後の画像ファイルを保存
            glayIm=cv2.imread(newFname, 0) #二値化したいので第2引数には0
            cv2.imshow("glay", glayIm)
            cv2.imwrite(newFname, glayIm)
            print(newFname)
            engines=pyocr.get_available_tools() #OCRエンジン取得
            engine=engines[0]
            txt=engine.image_to_string(Image.open(newFname),lang="jpn") #読み込み
            txt0=txt.replace(' ','') #空白削除
            print(txt0)
            tmpdir.cleanup()
            #clea=input("close?")
            #if clea=="i":tmpdir.cleanup()

        btn=tk.Button(base,text="Read",command=start);btn.place(x=50,y=50)
        cv2.createTrackbar('scale','imgWindow_',scale,100,sizing)
        cv2.createTrackbar('pen','imgWindow_',px,100,pen)
        cv2.createTrackbar('Affine','imgWindow_',deg,360,trackbar)
        cv2.createTrackbar('projectionLeft','imgWindow_',deg0,360,trackbar0)
        cv2.createTrackbar('projectionRight','imgWindow_',deg0_,360,trackbar0_)
        cv2.createTrackbar('projectionTop','imgWindow_',deg1,int(width/2),trackbar1)
        cv2.createTrackbar('projectionBottom','imgWindow_',deg1_,int(width/2),trackbar1_)
    do_()
    base.mainloop()
    cv2.waitKey(0)&0xFF;cv2.destroyAllWindows();cv2.waitKey(1)&0xFF;cv2.destroyAllWindows()
Rin=Rtxt()
