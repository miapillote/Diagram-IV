import glob
import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
import skimage as ski
import pdf2image
import os
import filecmp
from PIL import Image

class HandwritingCompresser:

  def __init__(self, file_path):
    if HandwritingCompresser.get_filetype(file_path) == 'pdf':
      self.original = HandwritingCompresser.pdf_to_image(file_path)
    else:
      self.original = file_path
    self.processed = None

  def compress(self, threshold = 0.95):
    raw_image = iio.imread(uri=self.original)
    denoised_image = HandwritingCompresser.process_image(raw_image, threshold)
    #HandwritingCompresser.show_image(denoised_image)
    new_file = Image.fromarray(denoised_image.astype(np.uint8) * 255)
    self.processed = HandwritingCompresser.replace_file_extension(self.original, '_processed.png')
    new_file.save(self.processed)
    return new_file

  @staticmethod
  def process_image(raw_image, threshold):
    gray_image = ski.color.rgb2gray(raw_image)
    denoised_image = ski.filters.gaussian(gray_image, sigma=1.0)
    return denoised_image > threshold

  @staticmethod
  def get_filetype(file_path):
    return os.path.split(file_path)[1].split('.')[1]

  @staticmethod
  def pdf_to_image(pdf_path):
    image = pdf2image.convert_from_path(pdf_path)
    file_path = HandwritingCompresser.replace_file_extension(pdf_path, '.jpg')
    for count, page in enumerate(image):
      image[count].save(file_path, 'JPEG')
    return file_path

  @staticmethod
  def show_graylevel_histogram(image):
    histogram, bin_edges = np.histogram(image, bins=256, range=(0.0, 1.0))

    fig, ax = plt.subplots()
    ax.plot(bin_edges[0:-1], histogram)
    ax.set_title("Grayscale Histogram")
    ax.set_xlabel("gray value")
    ax.set_ylabel("pixel count")
    ax.set_xlim(0, 1.0)

  @staticmethod
  def show_image(image):
    fig, ax = plt.subplots()
    ax.imshow(image, cmap = 'gray')

  @staticmethod
  def replace_file_extension(file_path, new_extension):
    return os.path.splitext(file_path)[0] + new_extension

  ######### Tests #########

  @staticmethod
  def test_pdf_to_image():
    assert filecmp.cmp(HandwritingCompresser.pdf_to_image('/content/handwriting_test.pdf'), '/content/img.jpg', shallow=False)

  @staticmethod
  def test_get_filetype():
    assert HandwritingCompresser.get_filetype('/content/handwriting_test.jpg') == 'jpg'

  @staticmethod
  def test_replace_file_extension():
    file_path = '/content/handwriting_test.pdf'
    new_extension = '.jpg'
    assert HandwritingCompresser.replace_file_extension(file_path, new_extension) == '/content/handwriting_test.jpg'

# processed_writing = HandwritingCompresser('/content/handwriting_test.pdf')
# processed_writing.compress()
