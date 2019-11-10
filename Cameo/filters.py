# 滤波函数和类

import cv2
import numpy
import utils

# 画线条
def strokeEdges(src,dst,blurKsize=7,edgeKsize=5):
    if blurKsize >=3:
        # 如果滤波核大于3在做处理
        # 中值模糊
        blurredSrc=cv2.medianBlur(src,blurKsize)
        graySrc=cv2.cvtColor(blurredSrc,cv2.COLOR_BGR2GRAY)

    else:
        # 没有核，则不能做模糊处理
        graySrc=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

    # 每个通道的位深度 ，该例中每个通道为8为
    # 指定滤波范围
    # 边缘处指定为255 拉普拉斯算子
    cv2.Laplacian(graySrc,cv2.CV_8U,graySrc,ksize=edgeKsize)

    # 归一化处理
    normalizedInverseAlpha=(1.0/255)*(255-graySrc)
    channels=cv2.split(src)
    for channel in channels:
        channel[:]=channel*normalizedInverseAlpha
    # 合并数组 将边缘变黑
    cv2.merge(channels,dst)

class VConvolutionFilter(object):
    """一般的卷积滤波器"""
    def __init__(self,kernel):
        self._kernel=kernel

    def apply(self,src,dst):
        # 目标图像和源图像有样的为深度
        cv2.filter2D(src,-1,self._kernel,dst)

class SharpenFilter(VConvolutionFilter):

    """特定的锐化滤波器"""

    def __init__(self):
        kernel=numpy.array([[-1,-1,-1],
                            [-1,9,-1],
                            [-1,-1,-1]
                            ])

        VConvolutionFilter.__init__(self,kernel)

class FindEdgesFilter(VConvolutionFilter):

    """边缘滤波器核"""

    def __init__(self):

        kernel=numpy.array([[-1,-1,-1],
                            [-1,8,-1],
                            [-1,-1,-1]
                            ])

        VConvolutionFilter.__init__(self,kernel)

class BlurFilter(VConvolutionFilter):
    """模糊滤波器，为了达到模糊效果通常权重和为1，且邻近像素权重均为正"""

    def __init__(self):
        kernel=numpy.array([[0.04,0.04,0.04,0.04,0.04],
                            [0.04, 0.04, 0.04, 0.04, 0.04],
                            [0.04, 0.04, 0.04, 0.04, 0.04],
                            [0.04, 0.04, 0.04, 0.04, 0.04],
                            [0.04, 0.04, 0.04, 0.04, 0.04]
                            ])
        VConvolutionFilter.__init__(self,kernel)

class EmbossFilter(VConvolutionFilter):
    """浮雕效果"""
    def __init__(self):
        kernel=numpy.array([[-2,-1,0],
                        [-1,1,1],
                        [0,1,2]
                        ])

        VConvolutionFilter.__init__(self,kernel)








