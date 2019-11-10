import cv2
import sys

def generate():
    """
    用于生成样本

    参数1：姓名
    参数2：ID值 使用数字
    :return: null
    """
    if len(sys.argv)<2:
        print("Please input your name")
        print("USAGE: faceFoot.py name ID")
        sys.exit()
    if len(sys.argv) < 3:
        print("Please input your ID")
        print("USAGE: faceFoot.py name ID")
        sys.exit()

    name=sys.argv[1]
    id=sys.argv[2]

    with open('./data/nameStore.txt','a') as f:
        # 将ID 和 name 保存下来
        f.write('{0};{1}'.format(id, name))
        f.close()
    camera=cv2.VideoCapture(0)
    face_cascade=cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    count=0


    while True:
        success, frame = camera.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.03,5,minSize=(70,70),maxSize=(90,90))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            img=gray[y:y+h,x:x+w]
                # 要求大小为200，200
            f=cv2.resize(img,(200,200))
            cv2.imwrite('./data/img/{1}{0}.pgm'.format(str(count),name),f)
            print('./data/img/{1}{0}.pgm 写入成功'.format(str(count),name))
            # 写csv文件
            with open('./data/faceCsv.txt','a') as f:
                f.write('{2}{0}.pgm;{1}\n'.format(str(count),id,name))
                print('csv写入成功')
                f.close()
            count+=1

        cv2.imshow('face_foot',frame)
        if cv2.waitKey(1000//12) &0xff==ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()




generate()




