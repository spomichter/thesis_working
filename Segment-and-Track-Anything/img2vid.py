import cv2
import os
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

# set the directory containing the images
for i in range (0, 60):
    img_dir = '/home/yashas/Documents/thesis/test-images/group_1/traj' + str(i) + '/images0/'
    print(img_dir)

    # check if the directory exists
    if not os.path.exists(img_dir):
        print('Directory does not exist:', img_dir)
        continue

    # set the output video file name and codec
    # out_file = './assets/images0.mp4'
    out_file = img_dir + 'images0.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # get the dimensions of the first image
    # img_path = os.path.join(img_dir, os.listdir(img_dir)[0])
    paths = sorted_alphanumeric(os.listdir(img_dir))
    paths = [x for x in paths if x.endswith('.png') or x.endswith('.jpg')]
    img_path = os.path.join(img_dir, paths[0])
    print(img_path)
    img = cv2.imread(img_path)
    height, width, channels = img.shape

    # create the VideoWriter object
    out = cv2.VideoWriter(out_file, fourcc, 10, (width, height))

    # loop through the images and write them to the video
    directory = sorted_alphanumeric(os.listdir(img_dir))
    for img_name in directory:
        # print(img_name)
        if img_name.endswith('.png') or img_name.endswith('.jpg'):
            img_path = os.path.join(img_dir, img_name)
            img = cv2.imread(img_path)
            out.write(img)

    # release the VideoWriter object and close the video file
    out.release()
