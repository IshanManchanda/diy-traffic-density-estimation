
import cv2
import numpy as np
from pathlib import Path
import os

base_path = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(
	base_path, "empty.jpg"
)
video_path = os.path.join(base_path, "trafficvideo.mp4")


def main():
    input_img = cv2.imread(img_path)

    cap = cv2.VideoCapture(video_path)

## getting frame dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

##declaring the varibale to store the transformed frames
    out = cv2.VideoWriter('output_video_.avi',
                          cv2.VideoWriter_fourcc(*'XVID'), 15, (1920, 1080))

#coordinates of road in real frame

    img_coord = np.array([[980, 200], [1260, 200], [800, 400], [1260, 400]])

# coordinates of road in transformed frame

    new_coor = np.float32([[472, 100], [1000, 100], [472, 400], [1000, 400]])
#applying homogra[hic transformation

    p, s = cv2.findHomography(img_coord, new_coor)

    while cap.isOpened():

        ret, frame1 = cap.read()
        if ret == True:
           gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
           perspective = cv2.warpPerspective(gray, p, (1920, 1080))
           #frame cropping
           src = perspective[100:401, 450:1001]
           #writing frame in the video
           out.write(perspective)
           if cv2.waitKey(1) == 27:
              break
        else:
          break

    out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
