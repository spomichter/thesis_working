import cv2

# sift
sift = cv2.SIFT_create()

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

img1 = cv2.imread('mask1.png')
img2 = cv2.imread('mask1.png')

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

# img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[200:500], img2, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, img2, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imshow('SIFT', img3)

cv2.waitKey(0)