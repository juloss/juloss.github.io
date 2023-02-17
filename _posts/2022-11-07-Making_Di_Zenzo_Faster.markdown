---
layout: post
title:  "Computing Di Zenzo's multichannel image gradient faster"
published: true
date:   2022-11-07 17:45:33 -0500
categories: projects
permalink: /di_zenzo_faster_gradient/
---


### Introduction

[Di Zenzo's](https://www.sciencedirect.com/science/article/abs/pii/0734189X86902239) algorithm computes the direction of ``maximum color change'' at each point in an image. More precisely, 

Here we describe an algorithm that is equivalent to Di Zenzo's algorithm but does the computations in a slightly more efficient way. Di Zenzo maximizes a certain function $$\max_\theta F(\theta)$$ (defined later) over $$\theta$$ by setting $$\frac{dF}{d\theta} = 0$$. This results in two values for $$\theta$$ such that for one of them $$F$$ achieves its maximum and for the other its minimum. To find the maximum of $$F$$, we need to evaluate $$F$$ at both values and choose the larger one.

We show that it is possible to find the $$\theta$$ that maximizes $$F$$ without evaluating $$F$$ at all, and to find the maximum of $$F$$ by evaluating $$F$$ only once. In fact, we can simply replace the arctan function in Di Zenzo's closed-formula by the arctan2, and this way the modified formula gives the value of $$\theta^*$$ such that $$F(\theta^*)$$ is maximum. This computation does not involve evaluating $$F$$. If we also want the maximum value of $$F$$, naturally, we need to compute $$F(\theta^*)$$. In our implementation, finding the maximum value of $$F$$ at each point of a 960x720 image saved us about 0.03s. (So it's not a big deal. :) )

### Derivation of faster formula

We present the argument for $$3$$-channel images but the argument trivially generalizes to $$n$$-channel images. Let $$f: \mathbf{R}^2 \rightarrow \mathbf{R}^3$$ be a $$3$$-channel image. We define the color difference between image locations $$(a_0, a_1) \in \mathbf{R}^2$$ and $$(b_0, b_1) \in \mathbf{R}^2$$ as the Euclidean distance between them, i.e., $$\lVert f(b) - f(a) \rVert$$. For convencience, we work with $$\lVert f(b) - f(a) \rVert^2$$ instead of $$\lVert f(b) - f(a) \rVert$$, which makes no difference in practice. Assume we are at point $$(a_0, a_1)$$ in the image, and we want to determine in which direction the color difference is the largest. Let $$\theta$$ be a direction and $$\epsilon$$ a small step size. If we move from $$(a_0, a_1)$$ in the direction $$\theta$$ an $$\epsilon$$ amount then we arrive at $$(a_0 + \epsilon \cos\theta, a_1 + \epsilon \sin\theta)$$.
We approximate the color difference between $$(a_0, a_1)$$ and $$(a_0 + \epsilon \cos\theta, a_1 + \epsilon \sin\theta)$$ using a first-order Taylor approximation. Let the partial derivatives of $$f$$ with respect to $$x$$ and $$y$$ evaluated at $$(a_0, a_1)$$ be the vectors $$\mathbf{u} = \left. \frac{\partial f}{\partial x} \right|_{a_0, a_1}$$ and $$\mathbf{v} = \left. \frac{\partial f}{\partial y} \right|_{a_0, a_1}$$, respectively. Then

$$\begin{align}
\big\lVert f(a_0, a_1) - f(a_0 + &\epsilon \cos\theta, a_1 + \epsilon \sin\theta) \big\rVert^2\\
\approx & \big\lVert (\epsilon \cos\theta) \cdot \mathbf{u} + (\epsilon \sin\theta) \cdot \mathbf{v} \big\rVert^2\\
= &\big((\epsilon \cos\theta) \cdot \mathbf{u} + (\epsilon \sin\theta) \cdot \mathbf{v}\big) \cdot \big((\epsilon \cos\theta) \cdot \mathbf{u} + (\epsilon \sin\theta) \cdot \mathbf{v}\big) \\
= &\epsilon^2 \bigl((\cos^2\theta) \cdot (\mathbf{u} \cdot \mathbf{u}) + (2 \cos\theta \sin\theta) \cdot (\mathbf{u} \cdot \mathbf{v}) + (\sin^2\theta) \cdot (\mathbf{v} \cdot \mathbf{v}) \bigr)\label{maximize_this}.
\end{align}$$

We wish to maximize \eqref{maximize_this}. Since $$\epsilon$$ is a constant, we can drop it ($$\epsilon = 1$$) and maximize 

$$F(\theta) = (\cos^2\theta) \cdot (\mathbf{u} \cdot \mathbf{u}) + (2 \cos\theta \sin\theta) \cdot (\mathbf{u} \cdot \mathbf{v}) + (\sin^2\theta) \cdot (\mathbf{v} \cdot \mathbf{v})$$

instead.
<style>
figure {
  border: 1px #cccccc solid;
  padding: 4px;
  margin: auto;
}

figcaption {
  background-color: grey;
  color: white;/assets/drawings/polarities.svg
  font-style: italic;
  padding: 2px;
  text-align: left;
}
</style>
<figure>
<center>
    <video width="80%" muted autoplay loop poster preload controls>
        <source src="../assets/animations/color_difference.mp4" type="video/mp4">
    </video>
</center>
<figcaption>Fig. 1. Function \(F(\theta)\) plotted for \(\theta \in [0^{\circ}, 360^{\circ})\),
\(\mathbf{u}=\mathbf{[}1 \;\; .9 \;\; .6\mathbf{]}^T\), and \(\mathbf{v}=\mathbf{[}.2 \;\; .3 \;\; .4\mathbf{]}^T\). As we move around \((0, 0)\) at distance \(1\), the blue curve is the value of \(F(\theta)\).
</figcaption>
</figure>
<p></p>
Using the identities $$\cos^2\theta =\frac{1}{2} (1 + \cos2 \theta)$$, $$2 \sin\theta \cos\theta = \sin2 \theta$$, and $$\sin^2\theta =\frac{1}{2} (1 - \cos2 \theta)$$, we obtain

$$\begin{align}
F(\theta) &= \frac{1}{2} \big( (\mathbf{u} \cdot \mathbf{u} + \mathbf{v} \cdot \mathbf{v}) + (\cos2\theta) \cdot (\mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v}) + (\sin2\theta ) \cdot (2 \mathbf{u} \cdot \mathbf{v})\big)\label{two_theta}\\

&= \frac{1}{2} \left( (\mathbf{u} \cdot \mathbf{u} + \mathbf{v} \cdot \mathbf{v}) + \begin{bmatrix} \cos2\theta \\ \sin2\theta \end{bmatrix} \cdot \begin{bmatrix} \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v} \\ 2 \mathbf{u} \cdot \mathbf{v} \end{bmatrix}\right)\\

&= \frac{1}{2} \left( (\mathbf{u} \cdot \mathbf{u} + \mathbf{v} \cdot \mathbf{v}) + \left \lVert \begin{bmatrix} \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v} \\ 2 \mathbf{u} \cdot \mathbf{v} \end{bmatrix}\right \rVert \cdot \cos(\varphi) \right) \label{angle_between_vecs},

\end{align}$$

where $$\varphi$$ is the angle between $$2\theta$$ and the angle of the vector $$\begin{bmatrix} \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v} \\ 2 \mathbf{u} \cdot \mathbf{v} \end{bmatrix}$$. (We used the equality $$\mathbf{a} \cdot \mathbf{b} = \lVert \mathbf{a} \rVert \lVert \mathbf{b} \rVert \cos \alpha$$, where $$\alpha$$ is the angle between $$\mathbf{a}$$ and $$\mathbf{b}$$, and observed that $$\begin{bmatrix} \cos2\theta \\ \sin2\theta \end{bmatrix}$$ has length $$1$$.) The direction of $$\begin{bmatrix} \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v} \\ 2 \mathbf{u} \cdot \mathbf{v} \end{bmatrix}$$ is $$\mathrm{arctan2}(2 \mathbf{u} \cdot \mathbf{v}, \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v})$$. 

 We can see from equation \eqref{angle_between_vecs} that because the length of a vector is always non-negtive, $$F$$ is maximized when $$\cos \varphi$$ is maximized. To maximize $$\cos \varphi$$, we set $$\varphi = 0$$. Therefore $$2\theta - \mathrm{arctan2}(2 \mathbf{u} \cdot \mathbf{v}, \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v}) = 0$$, and it follows that the value $$\theta^*$$ that maximizes $$F$$ is

$$
\begin{align}
\theta^* = \frac{1}{2} \mathrm{arctan2}(2 \mathbf{u} \cdot \mathbf{v}, \mathbf{u} \cdot \mathbf{u} - \mathbf{v} \cdot \mathbf{v}).\label{final}
\end{align}
$$

### Remarks
- Since $$\theta$$ appears in equation \eqref{two_theta} only in the form $$2 \theta$$, it follows that $$F(\theta^*) = F(\theta^* + k \pi)$$ for any $$k \in \mathbf{Z}$$. Therefore we can assume that $$\theta^* \in [0, \pi)$$.

- The $$\mathrm{arctan2}$$ function is not defined when both its arguments are $$0$$. In equation \eqref{final} this happens when $$\mathbf{u}$$ and $$\mathbf{v}$$ are perpendicular to each other and their magnitudes are the same. For example, when $$\mathbf{u}=\mathbf{[}1 \;\; 0 \;\; 0\mathbf{]}^T$$ and $$\mathbf{v}=\mathbf{[}0 \;\; 1 \;\; 0\mathbf{]}^T$$. If we have an RGB image, this corresponds to the situation that $$R$$ changes most along the $$x$$-axis and $$G$$ changes most along the $$y$$ axis, and the magnitude of the changes are the same. So the $$R$$ and $$G$$ channels change at the same rate but in perpendicular directions, and therefore $$F$$ becomes a constant. That is, the color changes the same amount in any direction. This cannot be interpreted as an edge, and we ignore such locations. In fact, we expect that at image boundaries, the lines along which the color channels change the most should be approximately parallel.
