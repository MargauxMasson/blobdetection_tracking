# USAGE
# python blobdetection_tracking.py --image1 data/Right2.jpg --image2 data/Left2.jpg

# import the necessary packages
import argparse
import imutils
import cv2
def center(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	coordinates = []

	# find contours in the thresholded image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	i = 0

	# loop over the contours
	for c in cnts:
		# compute the center of the contour
		M = cv2.moments(c)
		if M["m00"] > 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

		# draw the contour and center of the shape on the image
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
		cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(image, str(i), (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		i = i+1
		coordinates.append([cX, cY])

		# show the image
		# cv2.imshow("Image", image)

	if i == 0:
		print('No object detected')
	else :
		print('Objects detected: ', i)
		# print(coordinates)
	# cv2.imwrite("results/blobdetection_centers.jpg", image)
	cv2.waitKey(0)
	return coordinates

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image1", required=True,
	help="path to the input image")
ap.add_argument("-i2", "--image2", required=True,
	help="path to the input image2")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image1"])
if image is None:
    print('Could not open or find the image1:', args.input)
    exit(0)
image2 = cv2.imread(args["image2"])
if image2 is None:
    print('Could not open or find the image2:', args.input)
    exit(0)
results1 = center(image)
results2 = center(image2)
xCoord = []
yCoord = []

r = 0
l = 0

if len(results1) < len(results2):
	for i in range(len(results1)):
		xCoord.append(results1[i][0] - results2[i][0])
		yCoord.append(results1[i][1] - results2[i][1])
		if xCoord[i] > 0:
			r = r+1
		else:
			l = l+1
else :
	for i in range(len(results2)):
		xCoord.append(results1[i][0] - results2[i][0])
		yCoord.append(results1[i][1] - results2[i][1])
		if xCoord[i] > 0:
			r = r+1
		else:
			l = l+1
# print(yCoord)

if r > l:
	print("camera goes to the right")
else:
	print('camera goes to the left')