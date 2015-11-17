'''
2D Gabor filters.


Gabor filter =  sinusoid_carrier * gaussian_filter  (A complex sinusouid signal modulated by a gaussian).

Gabor filter is defined by:
- K:  Scales the magnitude of the Gaussian envelope
- a, b: Scale the two axis of the Gaussian envelope
- theta: Rotation angle of the Gaussian envelope
- x0, y0: Location of the peak of the Gaussian envelope
- u0, v0: Spatial frequencies of the sinusoid carrier in Cartesian coordinates.
- P: Phase of the sinusoid carrier

See Javier R. Movellan, "Tutorial on Gabor Filters" (http://mplab.ucsd.edu/tutorials/gabor.pdf)
'''

import numpy as np
import matplotlib.pyplot as plt


def gaussian_envelope2d(K=1.0, theta=0, x0=0, y0=0, a=1, b=1, size=(128, 128)):
    '''
    Returns a 2D gaussian envelope. (An envelope can be used to modulate a signal)

    - K:  Scales the magnitude of the Gaussian envelope
    - a, b: Scale the two axis of the Gaussian envelope
    - theta: Rotation angle of the Gaussian envelope
    - x0, y0: Location of the peak of the Gaussian envelope
    - size: Size of the image.

    See http://mplab.ucsd.edu/tutorials/gabor.pdf
    '''

    x = np.linspace(-1 / a, 1 / a, size[0])
    y = np.linspace(-1 / b, 1 / b, size[1])
    xx, yy = np.meshgrid(x, y)
    theta = np.deg2rad(theta)
    xr = (xx - x0) * np.cos(theta) + (yy - y0) * np.sin(theta)
    yr = -(xx - x0) * np.sin(theta) + (yy - y0) * np.cos(theta)
    w = K * np.exp(-np.pi * ((a ** 2) * (xr ** 2) + (b ** 2) * (yr ** 2)))
    return w


def sinusoid_carrier2d(a=1, b=1, u0=1 / 80., v0=1 / 80., P=0, size=(128, 128)):
    '''
    Returns a complex sinusoid function.

    - a, b: Scale of the two axis.
    - u0, v0: Spatial frequencies of the sinusoid carrier in Cartesian coordinates.
    - P: Phase of the sinusoid carrier
    - size: Size of the image.

    See http://mplab.ucsd.edu/tutorials/gabor.pdf
    '''
    # TODO User alternative polar coordinates to express u0 and v0 in terms of
    # Fo y w
    x = np.linspace(-1 / a, 1 / a, size[0])
    y = np.linspace(-1 / b, 1 / b, size[1])
    xx, yy = np.meshgrid(x, y)
    z = 1j
    s = np.exp(z * (2 * np.pi * (u0 * xx + v0 * yy) + P))
    return s


def gabor_filter2d(K=1.0, theta=0, x0=0, y0=0, a=1, b=1, u0=1. / 80.,
                   v0=1. / 80., P=0, size=(128, 128), show=True):
    '''
    Returns a 2D Gabor Filter (real and imag).
    Gabor filter =  sinusoid_carrier * gaussian_filter  (A complex sinusouid signal modulated by a gaussian).

    - K:  Scales the magnitude of the Gaussian envelope
    - a, b: Scale the two axis of the Gaussian envelope
    - theta: Rotation angle of the Gaussian envelope
    - x0, y0: Location of the peak of the Gaussian envelope
    - u0, v0: Spatial frequencies of the sinusoid carrier in Cartesian coordinates.
    - P: Phase of the sinusoid carrier
    - size: Size of the image.

    See http://mplab.ucsd.edu/tutorials/gabor.pdf
    '''

    g = gaussian_envelope2d(K, theta, x0, y0, a, b, size)
    s = sinusoid_carrier2d(a, b, u0, v0, P, size)
    gabor_real = s.real * g
    gabor_imag = s.imag * g

    if show:
        plt.subplot(2, 2, 1)
        plt.imshow(g)
        plt.title("Gaussian envelope")
        plt.subplot(2, 2, 2)
        plt.imshow(s.real)
        plt.title("Sinusoid carrier")
        plt.subplot(2, 2, 3)
        plt.imshow(gabor_real)
        plt.title("Gabor filter (real)")
        plt.subplot(2, 2, 4)
        plt.imshow(gabor_imag)
        plt.title("Gabor filter (imag)")
        plt.show()
    return gabor_real, gabor_imag

if __name__ == '__main__':
    gabor_filter2d(a=1 / 50., b=1 / 40., theta=-45, P=0, size=(128, 128))