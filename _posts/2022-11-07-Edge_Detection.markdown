---
layout: post
title:  "Continuous Colour Edge Detection"
published: false
date:   2022-11-07 17:45:33 -0500
categories: projects
permalink: /continuous_color_edge/
---

### TO DO
- Describe coordinate system and angle conventions
- Describe why canny does not have polarity problem
- Image is to positive reals?
- Define edgel: https://en.wiktionary.org/wiki/edgel#:~:text=edgel%20(plural%20edgels),as%20the%20edge%20of%20something.
- Give reference for reflectance model, light source intensity
- Don't use tuple notation, switch to vectors everywhere
- Show examples of log thresholding working better?
- Discuss and demonstrate what happens thresholding linear images: if threshold is small, there should
  be a lot of edges detected in bright parts of the image



### Color change polarities

The direction of maximum color change $$\theta^*$$ obtained above is in the range $$[0, \pi)$$. The fact that $$F(\theta^*) = F(\theta^* + \pi)$$ can cause problems when we connect the edge points to identify curves in the image. We demonstrate this with an example in Figure 2, left side. We assume for simplicity that colors are encoded using linear RGB. A part of an image is shown where a black line passes through over a white background. Therefore that all $$3$$ channles of a single pixel have the same value.

We will desribe a method to chain edge points together later. A reasonable boundary between the right side of the black line could be the chain of points $$p_1$$, $$p_2$$, $$p_3$$, $$p_4$$, $$p_5$$, $$p_6$$, $$p_7$$. Assume that we are at $$p_3$$ and we are trying to choose between $$p_4$$ and $$p_8$$ as the next point. Both points have the same direction for the maximum color change, $$\theta^*_4 = \theta^*_8 =  135^\circ$$. (Recall that the $$\theta$$-s are in the range $$[0^\circ, 180)$$.) The points also have the same  color change magnitude $$\sqrt{F(\theta^*_4)} = \sqrt{F(\theta^*_8)}$$. But it looks like $$p_8$$ should belong the boundary of the black line on the left side. The problem is that we do know that the maximum color change at $$p_4$$ and $$p_8$$ is along a line passing at an angle of $$135^\circ$$, but we do not know whether the change is of the ``same type.'' In our example, the color change at $$p_4$$ and $$p_8$$ have different types. At $$p_8$$, color changes from dark to light because there are more black pixels below the diagonal of the red box. At $$p_4$$, color changes from light to dark because there are more white pixels below the diagonal of the blue box. We could describe the color change as dark to light and light to dark because we use only black and white in this example. However, for color images in general the color change at a boundary needs a more detailed description.

<style>
.row {
  display: flex;
}
.column {
  flex: 40%;
  padding: 30px;
}
.vertical_space {
  padding: 30px;
}

</style>
<figure>
<div class="row">
  <div class="column">
      <img src="/assets/drawings/polarities_bw.svg" alt="Polarity 1" style="width:100%;">
  </div>
  <div class="vertical_space">
  </div>
  <div class="column">
      <img src="/assets/drawings/polarities_rg.svg" alt="Polarity 2" style="width:100%;">
  </div>
</div>
<figcaption>Fig. 2. <i>Left:</i> Both arrows point the same direction. Not good.
<i>Right</i>
</figcaption>
</figure>
<p></p>

<style>
span.keeptogether {
  white-space: nowrap ;
}
</style>

### Light intensity invariance, gamma compression, and Fechner's law

Let's restrict our attention for now to single channel images $$f: \mathbf{R}^2 \rightarrow \mathbf{R^+}$$. We wish to compute edgels but independently of light source intensity. That is, we want edgels to depend only on (or at least as much as possible) the material properties of the objects in the scene. We make the following simplifying assumption. If light source intensity changes by a factor of $$\alpha$$ (and nothing else changes), then $$f$$ becomes $$\alpha f$$. 

Let $$\mathbf{a} \in \mathbf{R}^2$$ be a pixel location. Consider the gradient $$\nabla f(\mathbf{a})$$ of $$f$$ at $$\mathbf{a}$$, i.e., the vector whose direction indicates the direction of maximum pixel intensity change, and whose magnitude is the size of this change.
One way to measure edgel strength in an image $$f$$ would be to define it as $$\lVert \nabla f(\mathbf{a}) \rVert$$. However, then edgel strength in the image $$\alpha f$$ would become $$\lVert \nabla \alpha f(\mathbf{a}) \rVert = \alpha \lVert \nabla f(\mathbf{a}) \rVert$$, and we would not have invariance.

Instead, we measure edgel strength at point $$\mathbf{a}$$ in an image $$\alpha f$$ as follows. We measure image intensity at $$\mathbf{a}$$, which is $$\alpha f(\mathbf{a})$$. Then we move from $$\mathbf{a}$$ in the direction of maximum intensity change a unit length amount, i.e., we move to $$\mathbf{a} + \frac{\nabla \alpha f(\mathbf{a})}{\lVert \nabla \alpha f(\mathbf{a}) \rVert} = \mathbf{a} + \frac{\nabla f(\mathbf{a})}{\lVert \nabla f(\mathbf{a}) \rVert}$$, and measure the intensity at that point, which is $$\alpha f\left(\mathbf{a} + \frac{\nabla f(\mathbf{a})}{\lVert \nabla f(\mathbf{a}) \rVert}\right)$$. Then we former intensity with the latter to obtain edgel strength
$$
\begin{align}
E(\alpha f) &= \frac{\alpha f\left(\mathbf{a} + \frac{\nabla f(\mathbf{a})}{\lVert \nabla f(\mathbf{a}) \rVert}\right)}{\alpha f(\mathbf{a})}\\
&= 
\frac{f\left(\mathbf{a} + \frac{\nabla f(\mathbf{a})}{\lVert \nabla f(\mathbf{a}) \rVert}\right)}{f(\mathbf{a})}\\
& \approx \frac{f(\mathbf{a}) + \nabla f(\mathbf{a}) \cdot \frac{\nabla f(\mathbf{a})}{\lVert \nabla f(\mathbf{a}) \rVert}}{f(\mathbf{a})}\label{linear_neighborhood}\\
& = \frac{f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert}{f(\mathbf{a})},\label{fraction_form}
\end{align}
$$
where expression \eqref{linear_neighborhood} is obtained using a first-order Taylor approximation at $$\mathbf{a}$$. Note that $$E$$ does not depend on $$\alpha$$, i.e., edge strength is independent of light intensity. A straighforward (but not very good in practice because of noise) way to find edgels using $$E$$ is to set a threshold $$t$$ and keep only those points as edges for which $$E(\alpha f) \geq t$$. Note that we do these operations on linear images (i.e., no gamma compression). Let's see a connection between this approach and gradient thresholding approaches applied to gamma compressed images. Let's take the log of both sides of
$$\frac{f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert}{f(\mathbf{a})} \geq t$$ to get

$$\begin{align}
\log(f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert) - \log{f(\mathbf{a})} \geq \log t. \label{log_expression}
\end{align}$$

The general idea for gradient based edge detetion is to threshold the gradient, i.e., to keep edgels $$\mathbf{a}$$ such that
$$\begin{align}
\lVert \nabla f(\mathbf{a}) \rVert \geq t'
\end{align}$$
for some threshold, or equivalently,
$$\begin{align}
( f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert ) - f(\mathbf{a}) \geq t'.\label{similar}
\end{align}$$

We observe that $$f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert$$ in \eqref{similar} is the same expression as the numerator in expression \eqref{fraction_form}, which as an (approximation) of an image intensity. Therefore the left hand side of \eqref{similar} corresponds to computing the gradient by taking the intensity difference between two nearby image locations. If we assume the image is gamma compressed using a gamma compression function $$g$$, we can rewrite \eqref{similar} as

$$\begin{align}
g(f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert)) - g(f(\mathbf{a}) \geq t'.
\end{align}$$

*Therefore expression \eqref{log_expression} (our light source intensity invariant thresholding) is the same as ``traditional'' gradient thresholding applied an image $$f$$ after $$\log$$ is used as a gamma compression function.*

In fact, the $$\ln$$ is not too different from standard gamma compression functions, as show in the figure below. GIVE REF. CHANGE CURVE. 0-1, optimize log parameters. STILL NEEDS WORK.
<figure>
<center>
  <img src="/assets/drawings/gamma_compression_curves.svg" alt="Gamma compression curves" style="width:70%;">
</center>
<figcaption>Fig. 3. Gamma compression curves.
</figcaption>
</figure>
<p></p>


There are (at least) two problems with the $$\log$$ function in expression \eqref{log_expression}:
- $$\lim_{x \to 0^+}\log x=-\infty$$. We would prefer not to have to work with large negative values. We can simply add replace $$f(x)$$ with $$c \cdot f(x) + 1$$, for some sufficiently large $$c$$, if we are willing to accept a very small amount of distortion.
- Images have noise, especially at low intensities. A small amount of noise $$n$$ can result in a large change of the value of $$\log(x + n)$$ when $$x$$ is small. To make sure noise does not produces fake edgels, we would like to have a larger threshold for smaller values of $$x$$.


We observe the follwing:
- Gamma compression is similar to taking the log of the image, although instead of taking the $$\log$$ the image pixel intensities, they are raised to some power (e.g., $$\frac{1}{2.4}$$). Therefore thresholding the gradients of a gamma compressed image should result in better light source strength intensity invariance than thresholding the gradients in a linear image. However, computing gradient directions from a gamma compressed image are distorted. Assuming the linear values are in the interval $$[0, 100]$$, we plot gamma compression and the natural logarithm function, $$\ln$$ in Figure 3. Note how close $$\ln x$$ is to $$x^\frac{1}{3}$$.


#### Fechner's law and Steven's law in human vision

We observe a similarity between how humans perceive brightness as a function of light intensity and the light source intensity invariant thresholding above. Fechner's law in psychophysics states that $$\psi(I) = k \log I$$, where $$\psi$$ is the perceived magnitude of a sensation, $$k$$ is a constant, and $$I$$ is stimulus intensity. Applied to light, $$\psi$$ is perceived brightness, $$k$$ is a constant specific to human vision, and $$I$$ is light intensity. If we accept that Fechner's law holds approximately, then the question arises whether the phenomenon described by Fechner's law has anything to do with humans having vision that is highly invariant with respect to light intensity.

We note that Stevens' power law is often considered to better describe the relation between perceived magnitude of a sensation and stimuls intensity. It states that $$\psi(I)=cI^{a}$$, where $$\psi$$ and $$I$$ are the same as before, $$c$$ is a proportionality constant that depends on the units used, and, $$a$$ is an exponent that depends on the type of stimulation or sensory modality. For vision under certain viewing conditions, $$a$$ can be set $$0.33$$. If we set $$k = 1$$, then the curve from Stevens' power law is the same gamma compression with exponent $$0.33$$, shown in the orange curve in Figure 3.


### Generalization to 3-channel images

Let $$f: \mathbf{R}^2 \rightarrow \mathbf{R}^3$$ be a $$3$$-channel image. We generalize expression \eqref{fraction_form} for vector valued $$f$$ as follows. We change the expression
$$\begin{align}
\frac{f(\mathbf{a}) + \lVert \nabla f(\mathbf{a}) \rVert}{f(\mathbf{a})}\label{fraction_again}
\end{align}
$$
to
$$\begin{align}
\frac{\lVert f(\mathbf{a}) \rVert + \sqrt{F(\theta^*_\mathbf{a})}}{\lVert f(\mathbf{a}) \rVert},\label{general}
\end{align}
$$
where $$\theta^*_\mathbf{a}$$ is the angle at $$\mathbf{a}$$ that maximizes $$F$$. It is not hard to verify that expression \eqref{general} is equivalent to \eqref{fraction_again} for single channel images.


### Neighborhoods
<figure>
<center>
    <video width="80%" muted autoplay loop poster preload controls>
        <source src="../assets/animations/neighborhood_pixels_by_angle.mp4" type="video/mp4">
    </video>
</center>
<figcaption>Fig. 4.
</figcaption>
</figure>


### To be continued...





<!-- At the center of each pixel, we compute and record
- the direction $$\theta^*$$ of maximum color change, and the
- the magnitude of the color change, which we define as $$\sqrt{F(\theta^*)}$$.

We take the square root because we used squared color differences in $$F$$ and we want linear color differences.

Similarly to other edge detectors, we will threshold color differences based on magnitude. However, it would be nice to get some sort of invariance with respect to illumination strength. If $$f$$ is our image function and light gets $$\alpha$$ times stronger, then $$f$$ becomes $$\alpha f$$ (note that this holds only for *linear color spaces, i.e., when gamma compression is not applied*).  -->



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
