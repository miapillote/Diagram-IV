import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage import measure
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

class ImgToScad:
    __init__(self, img_file, sample_density = 3):
        self.original = img_file
        self.sample_density = sample_density
        self.all_points = []

    def run(self):
        binary = self.binarize()
        skeleton = skeletonize(binary // 255)
        contours = measure.find_contours(skeleton, 0.5)
        for contour in contours:
            self.resample_contour(countour)
        print("Completed transformation. Use (self).save_to_scad(\'destination_path\' to save the results.")

    def binarize(self):
        # Load and binarize the image
        img = cv2.imread(self.original, cv2.IMREAD_GRAYSCALE)
        return _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    def resample_contour(self, contour):
        if len(contour) < 5:
            continue  # Skip very short or noisy contours

        y, x = contour[:, 0], contour[:, 1]

        try:
            # Smooth and resample each contour
            tck, _ = splprep([x, y], s=1)
            u_new = np.linspace(0, 1, num=max(10, len(x) // self.sample_density))  # Adjustable density
            x_new, y_new = splev(u_new, tck)

            for x_, y_ in zip(x_new, y_new):
                self.all_points.append((x_, y_))
        except:
            # If a contour can't be interpolated, just skip it
            continue

    def save_to_scad(self, file_path): 
        # TODO: check for .scad
        with open(file_path, "w") as f:
        f.write("bead_points = [\n")
        for x_, y_ in self.all_points:
            f.write(f"    [{x_:.2f}, {y_:.2f}],\n")
        f.write("];\n")
        print(f"Exported {len(self.all_points)} bead points.")

    def preview(self):
        plt.figure(figsize=(8, 8))
        for x_, y_ in self.all_points:
            plt.plot(x_, y_, 'bo', markersize=1)
        plt.gca().invert_yaxis()
        plt.title("Preview of Bead Placement")
        plt.show()

    
