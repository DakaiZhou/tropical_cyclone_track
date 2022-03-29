import cv2
import os


def image2video(img_folder, vid_name, fps=15, fourcc=0, size=None):
    images = [img for img in os.listdir(img_folder) if img.endswith(".png")]
    images.sort()
    frame = cv2.imread(os.path.join(img_folder, images[0]))
    if size:
        vid_size = size
    else:
        height, width, layers = frame.shape
        vid_size = (width, height)

    video = cv2.VideoWriter(filename=vid_name, fourcc=fourcc, fps=fps, frameSize=vid_size)

    for image in images:
        video.write(cv2.imread(os.path.join(img_folder, image)))

    cv2.destroyAllWindows()
    video.release()
