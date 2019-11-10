import  cv2
from  managers import WindowManager,CaptureManager
import  filters

class Cameo(object):
    def __init__(self):
        # 引入窗口管理类
        self._windowManager=WindowManager('Cameo',self.onKeypress)
        # 引入摄像头捕捉类
        self._captureManager=CaptureManager(cv2.VideoCapture(0),self._windowManager,True)
        # 引入滤波器类
        self._curveFilter=filters.FindEdgesFilter()
    def run(self):
        """Run the main loop"""

        # 创建一个窗口
        self._windowManager.createWindow()



        while self._windowManager.isWindowCreated:

            # 获取帧是否成功grab()
            self._captureManager.enterFrame()
            frame=self._captureManager.frame

            filters.strokeEdges(frame,frame)
            self._curveFilter.apply(frame,frame)


            self._captureManager.exitFrame()


            self._windowManager.processEvents()

    def onKeypress(self,keycode):

        """Handle a keypress

        space  ->  Take a screenshot
        tab    ->  Start/stop recording a screencast
        escape ->  Quit

        """
        if keycode==32:#space
            self._captureManager.writeImage('screennshot.png')
        elif keycode==9:#tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('scrrencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode==27:#escape
            self._windowManager.detroyWindow()


if __name__=='__main__':
    Cameo().run()

