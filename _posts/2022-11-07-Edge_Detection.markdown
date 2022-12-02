---
layout: post
title:  "Continuous Colour Edge Detection"
published: true
date:   2022-11-07 17:45:33 -0500
categories: projects
permalink: /continuous_color_edge/
---

### Introduction

Blabla.

### Part 1 - Di Zenzo's color gradient

Our algorithm uses [Di Zenzo's](https://www.sciencedirect.com/science/article/abs/pii/0734189X86902239) method of computing the direction of maximum color change at every point in the image. We briefly review his algorithm here for the special case of 3 channel images. Let $$f: \mathbf{R}^2 \rightarrow \mathbf{R}^3$$ be a $$3$$-channel image. We define the color difference between image locations $$a$$ and $$b$$ ($$a, b \in \mathbf{R}^2$$) as the squared Euclidean distance between $$f(a)$$ and $$f(b)$$, i.e., as $$\lVert f(b) - f(a) \rVert_2^2$$. 

Assume we are at point $$(x_0, y_0)$$ in the image, and we want to determine in which direction $$f$$ changes the most. Let $$\theta$$ be a direction and $$\epsilon$$ a small step size. If we move from $$(x_0, y_0)$$ in the direction $$\theta$$ an $$\epsilon$$ amount then we arrive at $$(x_0 + \epsilon \cos\theta, y_0 + \epsilon \sin\theta)$$.
We approximate the color difference between $$(x_0, y_0)$$ and $$(x_0 + \epsilon \cos\theta, y_0 + \epsilon \sin\theta)$$ using a linear Taylor approximation. Let the partial derivatives of $$f$$ with respect to $$x$$ and $$y$$ evaluated at $$(x_0, y_0)$$ be the vectors $$\mathbf{u} = \left. \frac{\partial f}{\partial x} \right|_{x_0, y_0}$$ and $$\mathbf{v} = \left. \frac{\partial f}{\partial y} \right|_{x_0, y_0}$$, respectively. Then

$$\begin{align}
\big\lVert f(x_0, y_0) - f(x_0 + &\epsilon \cos\theta, y_0 + \epsilon \sin\theta) \big\rVert_2^2\\
\approx & \big\lVert (\epsilon \cos\theta) \cdot \mathbf{u} + (\epsilon \sin\theta) \cdot \mathbf{v} \big\rVert_2^2\\
= &\big((\epsilon \cos\theta) \cdot \mathbf{u} + (\epsilon \sin\theta) \cdot \mathbf{v}\big) \cdot \big((\epsilon \cos\theta) \cdot \mathbf{u} + (\epsilon \sin\theta) \cdot \mathbf{v}\big) \\
= &\epsilon^2 \bigl((\cos^2\theta) \cdot (\mathbf{u} \cdot \mathbf{u}) + (2 \cos\theta \sin\theta) \cdot (\mathbf{u} \cdot \mathbf{v}) + (\sin^2\theta) \cdot (\mathbf{v} \cdot \mathbf{v}) \bigr)\label{maximize_this}.
\end{align}$$
<center>
<video width="80%" muted autoplay loop poster preload controls>
    <source src="../color_difference.mp4" type="video/mp4">
</video>
</center>

We wish to maximize \eqref{maximize_this}. Since $$\epsilon$$ is a constant, we can drop it and maximize 

$$F(\theta) = (\cos^2\theta) \cdot (\mathbf{u} \cdot \mathbf{u}) + (2 \cos\theta \sin\theta) \cdot (\mathbf{u} \cdot \mathbf{v}) + (\sin^2\theta) \cdot (\mathbf{v} \cdot \mathbf{v})$$

instead.

Using the identities $$\cos^2\theta =\frac{1}{2} (1 + \cos2 \theta)$$, $$2 \sin\theta \cos\theta = \sin2 \theta$$, and $$\sin^2\theta =\frac{1}{2} (1 - \cos2 \theta)$$, we obtain

$$\begin{align}
F(\theta) = \frac{1}{2} \big( (\mathbf{u} \cdot \mathbf{u} + \mathbf{v} \cdot \mathbf{v}) + (\cos2\theta) \cdot (\mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v}) + (2 \sin2\theta ) \cdot (\mathbf{u} \cdot \mathbf{v})\big)\label{double_angle}.
\end{align}
$$

Setting $$\frac{d F}{d \theta} = 0$$ gives
$$\begin{align}
\tan 2\theta = \frac{2 \mathbf{u} \cdot \mathbf{v}}{\mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v}}\label{two_theta}
,\end{align}$$
so
$$\begin{align}
\theta = \frac{1}{2} \arctan \frac{2 \mathbf{u} \cdot \mathbf{v}}{\mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v}}.\label{final}
\end{align}$$

Let's understand the solutions of equation \eqref{final}.

Let $$\theta^*$$ be a solution of \eqref{final}. We can see from \eqref{two_theta} and recalling that $$\tan$$ has a periodicity of $$\pi$$ that $$\theta^* + \frac{\pi}{2}$$ is also a solution. If these solutions are not equal, then one of $$F(\theta^*)$$ and $$F(\theta^* + \frac{\pi}{2})$$ must be a minimum and the other maximum.




### To be continued...





<!-- # Pseudo code

1. Load needed data:
    - neighborhood_table, table_eop, neighborhood_offsets_in_direction_table
    - color processing profile (e.g., cielab, linear_srgb_with_cube_root_compression)
2. Estimate partial derivatives of input image using a Scharr filter.

# Motivation and Intuition

1. In the Canny edge detector and its variants, edge linking is usually performed after maximum suppression. Due to noise, maximum suppresion could break curves because it could remove intermediate points. The present edge links points detectod on boundaries without doing maximum suppresion first.
2. The color edge detector of Di Zenzo ([*paper here*](https://people.csail.mit.edu/tieu/notebook/imageproc/dizenzo86.pdf)) can combined with the CIELAB colorspace (with nice properties) is a natural way, and to the best of our knowledge, it hasn't been done.
3. Copmpare polarity to stuff in Forsyth 2nd ed. Chapter 5.1.
We use polarity to follow only the same curve. For a 3 channel image, polarity is a triple $$p \in \{-1, 0, 1\}^3$$. MAKE image demo.


# Motivation

The role of this package is to give good quality (as unbroken as possible) contours. Further contour processing will be done in another package.

# Initial Setup

## Without package installation
1. Before processing images, run the build_tables.py script. This will produce files for later use in working folder.
2. Run aot_compilation_functions.py. This will compile the python/numpy code
using numba and make an extension module.

## With package installation
See package installation below. Once the package is installed, use the following:
from contour_detection import get_contours, draw_contours

# Run image processing
Call run.py. Image can be passed to get_contours method.
(Import get_contours from aot_main_pipeline. Pass an image to the method
to extract contours. Visualize with draw_contours method in draw_contours.py.)

# Profiles
There are 3 ways of preprocessing images.
1. Contour tracking is done on linear sRGB image after log compression.
2. Contour tracking is done on linear sRGB image after cube root compression.
3. Contour tracking is done on cielab image.

# Package making

A package is a folder containing modules.
import: imports a module
from X import Y: imports something called Y living in module X

To install my package, I use setuptools.
In setup.py, py_modules specifies all the relevant modules (not sure what that means exactly, but it seems I have to list all .py files there.)
Files where I save data for later use go into data_files. To acces these datafiles (during the inner workings of the package), I use

this_dir, _ = os.path.split(__file__)
neighborhood_table = np.load(os.path.join(this_dir, 'neighborhood_table.npy'))
table_eop = np.load(os.path.join(
    this_dir, 'neighborhood_table_end_markers.npy'))

when the data file is a numpy file.

The parts 
from aot_compilation_functions import cc and
ext_modules=[cc.distutils_extension()]
are there so that the numba ahead-of-time compiled code also gets included in the package.

To install the package, use
python setup.py install

Now my package behaves like any other package, i.e., I can use
"import module" for any module that I specified in the py_modules list. 

It seems MANIFEST.in is not necessary, it still works.

# Package Use

HITTING ENCODING IS NOT CAREFULLY CHECKED: c[1] and c[2] should describe
what curve hits on left (see below) c[3] and c[4] should describe what curve 
hits on right. 

GO OVER CODE IN local_maxima_tracker.py, track_from_point_in_both_directions

get_contours is the main method in the package. It returns a tuple t.
t[0] is "filtered_annotated_curves". This is numba typed dictionary of 5-tuples. (it is a slow data structure, if performance is important, this should be changed)
A "filtered annotated curve tuple" c has entries as follows:
c[0] is the points of the curve, a 2D numpy array with int32 coordinates
c[1] is the id of another curve, such that c hits this curve with its left end (left end means point c[0][0]). The id is a 64-bit int.
c[2] is the location where the other curve is hit. It is a 1D numpy array of type int32.
c[3] and c[4] are for the right side of the curve (right end is c[0][-1]).
NOTE: the curve can hit itself.

curve_hit_id = 0 means the curve hit nothing (0 stands for background). In this case,
curve hit location is [-1, -1]. -->
