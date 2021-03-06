# 21m359-final
Accessible music project.
Beth Hadley, Erin Main.

for 21M.359, Spring 2015, taught by Eran Egozy.

## VISION & GOAL
We believe that creating music in a classical sense - singing in a choir or playing in a band - is a very compelling experience. However, many people are unable to engage in this experience. Many people with physical limitations, such as limited mobility, have difficulty performing traditional instruments. Others may have cognitive challenges that prevent them from learning the technical aspects of an instrument. In this project, we aimed to enable all people - regardless of physical or mental facility - to engage in music making in a very compelling and traditional way.

The performance system enables two individuals to perform a duet together. The piece we chose to implement is the Ave Maria (http://conquest.imslp.info/files/imglnks/usimg/8/8f/IMSLP258490-PMLP13993-Gounod_-_Ave_Maria_ArrVnPf.pdf). We provide two instruments, one to perform the top line and the other to perform the bottom line. The top line is performed with a kinect-based instrument that tracks an individual's motion. They can articulate notes and also change the note's volume. The bottom line is performed with a glove circuit that Erin designed and fabricated. You can bend your fingers to perform the notes in the piece.

## HOW TO RUN
To run our system, ensure the boolean settings kUseKinect and kUsingGlove are set correctly. run kivy duet.py The system is designed to be run in full screen mode (sorry we didn't quite get it to resize dynamically just because we ran out of time...), so maximize the screen immediately when it opens. Then press 'p' on the keybaord when you're ready to play. You can play the bottom notes by pressing keys 1,2,3,4,5. You can play the top notes by moving your cursor left and right across the vertical line, or your hand if you're using the kinect. By default the kinect tracks your right hand. However you can select other joints to track - have a friend press 's' on the keyboard (for "settings") and this will display a body image on the screen. Use your right hand to select the joint you desire to track - currenlty only left and right hands and head are options. Have your friend press 'p' once you've selected the joint you wish to use. If you selected head, the system will freeze for a few seconds while it calibrates to your head height.

## DESIGN DECISION - Line Synchronization
The synchronization between the top and bottom lines is a little tricky. The lateral motion of both lines is controlled by the bottom line. The top line should sound notes as they progress across the vertical "now" bar. If the top line plays too far ahead or too far beind, the system will jump the user to the note they should be playing at that time. We decided on this as our final design because we felt it bridged the gap well between providing enough musical expression to performers while still facilitating duet performance for those who may find the system challenging.

## CONCLUDING REMARKS
We really enjoyed working through numerous challenges - both technical and creative - with this project. We are both very proud of the final product, and it serves as an example of how technology can enable musical experiences that would not otherwise be possible.