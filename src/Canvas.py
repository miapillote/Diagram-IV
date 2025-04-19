"""

Specifications:
- Take a list of points (or bitmap*):
    - Scale them to the desired specifications
    - Slice them into smaller canvases suitable for the 3d printer
    - Return the list of scaled points:
        - Give the option of saving the files to a given directory

* It may be advantageous to take the points as a bitmap and then use the ImgToScad.pyu class to translate each individual file to the appropriate set of
coordinates in case some part of that processing takes too long.
"""