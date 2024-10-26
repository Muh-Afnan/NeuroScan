import numpy as np
import cv2
import matplotlib.pyplot as plt


image = cv2.imread("images/volume_1.jpg", cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


noise_removed_NLM = cv2.fastNlMeansDenoisingColored(image,  h=11, templateWindowSize=6,searchWindowSize=18)
noise_removed_BD3M = cv2.bilateralFilter(image, d=10,sigmaColor=65, sigmaSpace=65)
normalized_image = noise_removed.astype(np.float32) / 255.0

combined = cv2.hconcat([image,noise_removed_NLM,noise_removed_BD3M])
combined = cv2.resize(combined,(1188,417))

cv2.imshow("Combined", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
