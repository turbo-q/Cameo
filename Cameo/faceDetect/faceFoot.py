'''
@Descripttion: 
@version: 
@Author: forcehack
@Date: 2019-11-10 18:21:25
@LastEditors: forcehack
@LastEditTime: 2019-11-28 18:58:22
'''
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
    
    # 读取第一个参数
    name=sys.argv[1]
    # 读取第二个参数
    id=sys.argv[2]
# 创建并打开文件
    with open('./data/nameStore.txt','a') as f:
        # 将ID 和 name 保存下来
        f.write('{0};{1}'.format(id, name))
        # 关闭
        f.close()
        # 打开摄像头
    camera=cv2.VideoCapture(0)
    # 引入人脸级联分类器
    face_cascade=cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    count=0


    while True:

        success, frame = camera.read()
        # 转换为灰度图像
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # 多尺度检测
        faces=face_cascade.detectMultiScale(gray,1.03,5,minSize=(70,70),maxSize=(90,90))
        for (x,y,w,h) in faces:

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            img=gray[y:y+h,x:x+w]
                # 要求大小为200，200
            f=cv2.resize(img,(200,200))
            # 保存图片
            cv2.imwrite('./data/img/{1}{0}.pgm'.format(str(count),name),f)
            print('./data/img/{1}{0}.pgm 写入成功'.format(str(count),name))
            # 写csv文件保存数据
            with open('./data/faceCsv.txt','a') as f:
                f.write('{2}{0}.pgm;{1}\n'.format(str(count),id,name))
                print('csv写入成功')
                f.close()
            count+=1
# 显示摄像头
        cv2.imshow('face_foot',frame)
        # 如果按下q 则退出
        if cv2.waitKey(1000//12) &0xff==ord('q'):
            break
            # 关闭摄像头
    camera.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()




generate()




