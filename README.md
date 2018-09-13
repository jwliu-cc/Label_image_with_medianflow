Label_image_with_medianflow
===========================

This is a program that help data makers to label image semi-automatically. It
will create and save bounding-boxes and labels in a '.xml' document which is the
same as that labeled by 'labelimg.exe'. It is based on medianflow-traker.

说明：
------

本程序针对整段视频中所有label都出现且目标运动变化不大的条件

-   库

    lxml,opencv3.4,os,math

    os和math为python原装

    lxml和opencv都可以用conda命令安装

-   使用方法：

    1.  更改程序中的global
        parameter以适配自己的环境，注意label数组的内容和顺序。

    2.  运行程序，会在视频所在位置生成储存数据用的文件夹，按R键可以对视频进行旋转，按空格键暂停标注数据，用鼠标框选bounding-box，框选时，绿色框表示框选中，红色框表示框选结束可以添加。按A键将目标添加至跟踪器，注意框选顺序要和label数组中的顺序相同（每框选一次结束后想添加到跟踪器都需要按A确认添加）。添加结束后，再按空格键，视频继续播放，并显示跟踪框选效果，同时开始储存数据。可按S中途停止储存，空格键继续储存。

这是一个demo程序，仍然存在很多bug，操作上有时误按A和空格都会造成数据的错误，因此标注结束后应当进行审查，用labelimg进行审查，更正错误标框。

我的测试结果是：一个10分钟的视频，标注加审核修改的时间用时约30分钟，因跳帧（frame_skip变量)储存，共获得数据图片1111张。
