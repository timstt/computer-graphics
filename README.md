# Computer Graphics and Visualization

Laboratory assignments for the **Computer Graphics and Visualization** course (Software Engineering, Taras Shevchenko National University of Kyiv), implemented in **Python**.

The labs cover digital image processing: format conversion, color and contrast adjustment, compositing, histograms, edge-detection masks, and noise filtering with quality evaluation.

## Labs

| Lab | Topic | What it does | Folder |
|-----|-------|--------------|--------|
| 1 | Basic image processing | Format conversion (JPG / PNG / BMP), resizing, color transformations, color balance correction | [lab1](./lab1) |
| 2 | Transparency, cropping, contrast | Everything from lab 1 plus alpha-channel transparency, cropping, contrast enhancement | [lab2](./lab2) |
| 3 | Combining images, watermark, slideshow | Merging images, text watermark, Tkinter slideshow with a simple GUI | [lab3](./lab3) |
| 4 | Color image analysis | Brightness matrix, histograms, binarization, grayscale shades, negative | [lab4](./lab4) |
| 5 | Edge detection with filters | Directional compass masks (south-east, south) applied by convolution on the brightness channel | [lab5](./lab5) |
| 6 | Image noise and filtering quality | Gaussian and salt-and-pepper noise, linear and non-linear filters (mean, Gaussian, median, min, max, midpoint, trimmed mean, geometric mean), distortion metrics | [lab6](./lab6) |

## Tech stack

- Python 3
- Pillow (PIL)
- NumPy
- Matplotlib
- Tkinter

## Getting started

```bash
git clone https://github.com/timstt/computer-graphics.git
cd computer-graphics
pip install pillow numpy matplotlib
```

Run a lab and follow the prompts (paths to the input image and output folder):

```bash
python lab5/lab5/lab5.py
```

## Author

**Tymofii Stukalo**, software engineering student.
GitHub: [@timstt](https://github.com/timstt)
