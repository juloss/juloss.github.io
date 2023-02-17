---
layout: post
title:  "RainbowTag Fiducal Marker"
date:   2022-11-08 17:45:33 -0500
categories: projects
permalink: /rainbowtag/
image1: /assets/images/marker.svg
image2: /assets/images/demo_images.svg
---

## In a nutshell

*RainbowTag* ([*paper here*](https://ieeexplore.ieee.org/document/9743123), [*code here*](https://github.com/juloss/rainbowtag), [*download slides*]({{ site.url }}/assets/slides/RT_short.odp)) is a color-based fiducial marker together with a detection algorithm that is robust to (motion) blur and marker deformations. Below is an example marker. Although lighting conditions affect color appearance, the RainbowTag detection algorithm is designed work reliably in everyday lighting conditions (e.g.,  lightbulbs with various color temperature or sunlight). 

![RainbowTag marker]({{ page.image1 }}){:.centered}{:width="20%"} 

# Advantages of RainbowTag:

Works well when (see experimental demonstration in [*paper*](https://ieeexplore.ieee.org/document/9743123))
- there is blur (e.g., because of movement),
- markers are partially occluded,
- markers are folded,
- markers are placed on an uneven surface,
- markers are far from the camera.


# Disadvantages of RainbowTag:
- current implementation (python using numba for certain tasks) is not very fast, about 3-4 fps on a Surface Book 2 laptop (for 1920 x 1080 images),
- it does not work with black and white images,
- there are only 30 different markers.
<br/><br/>


## Demos

##### *Note:* *(1)* All markers (RainbowTag, Aruco, ChromaTag) have area $$ 26.5 \pm 0.5 \text{cm}^2$$. In the videos and images below, RainbowTag markers look larger than Aruco and ChromaTag markers because Aruco and ChromaTag have a white frame around them that is not visible on the white background. RainbowTag uses a black frame which is visible. *(2)* Four detector algorithms are running in the videos and images: RainbowTag, Aruco 6x6, Aruco 4x4, ChromaTag.

# Detection Videos


#### Markers in occlusion 
##### (camera: Sony Alpha 5000)

<center>
<video width="100%" muted controls>
    <source src="../assets/videos/stick.mp4" type="video/mp4">
</video>
</center>
<br/><br/>

#### Small and blurry markers
##### (camera: Sony Alpha 5000)

<center>
<video width="100%" muted controls>
    <source src="../assets/videos/sony_camera.mp4" type="video/mp4">
</video>
</center>
<br/><br/>

#### Markers on uneven surface
##### (camera: Sony Alpha 5000)

<center>
<video width="100%" muted controls>
    <source src="../assets/videos/slowmo_uneven.mp4" type="video/mp4">
</video>
</center>
<br/><br/>

#### Folded marker detection
##### (camera: Sony Alpha 5000)

<center>
<video width="100%" muted controls>
    <source src="../assets/videos/slowmo_cube.mp4" type="video/mp4">
</video>
</center>
<br/><br/>


#### Weak yellowish illumination
##### (camera: Samsung Galaxy S5 phone camera)

<center>
<video width="60%" muted controls>
    <source src="../assets/videos/galaxyS5.mp4" type="video/mp4">
</video>
</center>  
<br/><br/>


#### Next to window (daylight)
##### (camera: Umidigi F2 phone camera)

<center>
<video width="60%" muted controls>
    <source src="../assets/videos/umidigiF2.mp4" type="video/mp4">
</video>
</center>  
<br/><br/>


# Detection Demo Images

![Detection demo images]({{ page.image2 }}){:.centered}{:width="80%"}

Rows are described from top to bottom and from left to right. The left side of an image shows the marker, and the right side shows the marker with detection overlayed. $$d$$ is the distance between the camera and the markers.

*Row 1:*
**(1)**  $$d=1.1$$m, 6500K lightbulb.
**(2)** $$d=2.1$$m, 2700K lightbulb.
**(3)** and **(4)** Detection algorithm with same settings (i.e., same white point) in both conditions (3) (2700K lightbulb) and (4) (6500K lightbulb), $$d=1.1$$m.

*Row 2:* 
**(1)** High blur: $$v = 0.45 \frac{m}{s}$$, shutter speed $$=\frac{1}{15}s$$, $$d=2.1m$$, 2700K lightbulb.

etc.