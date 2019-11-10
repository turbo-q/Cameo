import numpy
import cv2
import time


class CaptureManager(object):
    def __init__(self,capture,previewWindowManger=None,sholdMirrorPreview=False):

        # 窗口管理
        self.previewWindowManger=previewWindowManger
        # 是否镜像
        self.sholdMirrorPreview=sholdMirrorPreview

        # 定义私有属性(一个下划线可以被本身和子类访问，两个下划线只能被本身访问)
        self._capture=capture

        self._channel=0
        self._enteredFrame=False
        self._frame=None
        self._imageFilename=None
        self._videoFilename=None
        self._videoEncoding=None
        self._videoWriter=None

        self._startTime=None
        # 长整形
        self._framesElapsed=0
        self._fpsEstimate=None


    @property
    def channel(self):
        return self._channel

    # 设置通道
    # ##.channel=0
    @channel.setter
    def channel(self,value):
        if value!=self._channel:
            self._channel=value
            self._frame=None

    # 获取帧
    @property
    def frame(self):
        # 如果帧获取成功且帧为空

        if self._enteredFrame and self._frame is None:
            _,self._frame=self._capture.retrieve()

            return  self._frame

    # 正在写图片
    @property
    def isWritingImage(self):

        return self._imageFilename is not None

    # 正在写视频
    @property
    def isWritingVideo(self):
        return  self._videoFilename is not None


    def enterFrame(self):
        """Capture the next frame,if any"""

        #断言函数，处理下一帧前需判断上一帧是否退出
        # 如果未True  说明上一帧还没完
        assert not self._enteredFrame,\
        'previous enterFrame() had no matching exitFrame()'


        if self._capture is not  None:
            # get success
            self._enteredFrame=self._capture.grab()



    def exitFrame(self):
        """Draw to the window,Write to files.Release the frame"""

        #     没有读取成功

        # if self.frame is None:
        #     self._enteredFrame=False
        #     return



        if self._framesElapsed==0:
            self._startTime=time.time()

        else:
            timeElapsed=time.time()-self._startTime

            self._fpsEstimate=self._framesElapsed/timeElapsed

        self._framesElapsed+=1

        # Draw to Window ,

        if self.previewWindowManger is not  None:
            if self.sholdMirrorPreview:
                mirroredFrame=numpy.fliplr(self._frame).copy()
                self.previewWindowManger.show(mirroredFrame)
            else:
                self.previewWindowManger.show(self._frame)

        # Write to the image file

        if self.isWritingImage:
            cv2.imwrite(self._imageFilename,self._frame)
            # 写完清空
            self._imageFilename=None

        # Write to the video file

        self._writeVideoFrame()

        # Release the frame

        self._frame=None
        self._enteredFrame=False


    def writeImage(self,filename):
        """ Write the next exited frame to an image file."""

        self._imageFilename=filename

    def startWritingVideo(self,filename,encoding=cv2.VideoWriter_fourcc('I','4','2','0')):
        """ Start writing exited frames to a video file"""
        self._videoFilename=filename
        self._videoEncoding=encoding

    def stopWritingVideo(self):
        """ Stop writing exited frames to a video file"""
        self._videoFilename=None
        self._videoEncoding=None
        self._videoWriter=None

    def _writeVideoFrame(self):

        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps=self._capture.get(cv2.CAP_PROP_FPS)

            if fps==0.0:
                # Thecapture's fps is unknown so use an estimate

                if self._framesElapsed < 20:

                    #Wait until more frames elapse so that the estimate is more stable
                    return
                else:

                    fps=self._fpsEstimate

            size=(int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter=cv2.VideoWriter(self._videoFilename,self._videoEncoding,fps,size)

            self._videoWriter.write(self._frame)


class WindowManager(object):
    def __init__(self,windowName,keypressCallback=None):
        self.keypressCallback=keypressCallback

        self._windowName=windowName
        self._isWindowCreated=False

    @property
    def isWindowCreated(self):
        return  self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated=True

    def show(self,frame):
        cv2.imshow(self._windowName,frame)

    def detroyWindow(self):
        cv2.destroyAllWindows()
        self._isWindowCreated=False

    def processEvents(self):

        keycode=cv2.waitKey(1)

        if self.keypressCallback is not None and keycode != -1:

            keycode &= 0xFF
            self.keypressCallback(keycode)



