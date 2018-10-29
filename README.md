# TangibleUserInterface
A project allow users to interactive with a 3D box in Unity by moving and swiching the upper face of a physical cube.

Screenshot & Demo Video
-----------------------
To see a demo video, please click the screenshot below
[![tangibleUserInterface](https://github.com/ShirleyDong/tangibleUserInterface/blob/master/Screen%20Shot%202018-10-29%20at%201.15.21%20PM.png)](https://www.youtube.com/watch?v=sGbt2mjmxBE "OpenCV+ Python Colour Tracking in Unity")

## Structure
![Structure](https://github.com/ShirleyDong/tangibleUserInterface/blob/master/structure.JPG)
### Python+OpenCV Program
Track and detect the color object in webcam.<br/>
Pass the 2D coordinate data to C# program in Unity by UDP socket.
### Unity project
Apply the 2D coodinate data to 3D cube in Unity scene.<br/>
Track the hand by LeapMotionController.

## Prerequisites
Unity 5<br/>
Python 3.7.1<br/>
LeapMotionController

## Execution(can not be reverse)
1.Execute the python program pass.py</br>
2.Run the unity scene myScene








