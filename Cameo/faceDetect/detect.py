import os
import cv2
import numpy as np
import sys


def read_img(path='./data/faceCsv.txt',sz=None):
    """

    :param path: 样本CSV 文件所在路径
    :param sz: 样本大小如果没有改变为200*200 将其改变
    :return: 训练样本
    """

    imgDataPath='./data/img'
    # 分别存储图像数组和标签
    X,y=[],[]
    for line in open(path):
       try:
        # 舍弃\n
        line=line.strip('\n')
        imgLine=line.split(';')[0]
        labelLine=line.split(';')[1]
        im=cv2.imread(os.path.join(imgDataPath,imgLine),cv2.IMREAD_GRAYSCALE)

        if sz is not None:
            im=cv2.resize(im,(200,200))

        X.append(np.asarray(im,dtype=np.uint8))
        y.append(labelLine)
       except:
           print ("Unexpexted error:",sys.exc_info()[0])
           raise
    return [X,y]



def face_rec():
    """
    names数组对应相应ID 对应的名字
    :return:
    """
    names={}
    for line in  open('./data/nameStore.txt') :
        try:
            # 舍弃\n
            line = line.strip('\n')
            id = line.split(';')[0]
            name = line.split(';')[1]
            names[id]=name

        except:
            print("Unexpexted error:", sys.exc_info()[0])
            raise

    if len(sys.argv)==2:
        [X,y]=read_img(sys.argv[1])
    else:
        [X, y] = read_img()

    # asarray 不占用新内存
    y=np.asarray(y,dtype=np.int32)
    # 创建人脸识别模型
    model=cv2.face.EigenFaceRecognizer_create()
    # 将X，y传入进行训练
    model.train(np.asarray(X),np.asarray(y))

    camera=cv2.VideoCapture(0)
    face_cascade=cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

    while True:
        success, frame = camera.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


        faces=face_cascade.detectMultiScale(gray,1.03,10,minSize=(70,70))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi=gray[y:y+h,x:x+w]
            try:
                roi=cv2.resize(roi,(200,200))
                # 传入数据进行预测
                params=model.predict(roi)
                print("Label:{0},Confidence:{1:.3f}".format(params[0],params[1]))

                cv2.putText(frame,names[str(params[0])],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
            except:
                continue

        cv2.imshow('camera', frame)
        if cv2.waitKey(1000//12) & 0xff==ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()



face_rec()










