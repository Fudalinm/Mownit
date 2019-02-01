# Zadanie 2. Korzystając z DFT2D zaimplementuj nieco zmodyfikowaną i uproszczoną wersję
# kompresji obrazu jpeg (tablice kwantyzacji:)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

from math import floor


def runSecond():
    q = [[16, 11, 10, 16, 24, 40, 51, 61],
         [12, 12, 14, 19, 26, 58, 60, 55],
         [14, 13, 16, 24, 40, 57, 69, 56],
         [14, 17, 22, 29, 51, 87, 80, 62],
         [18, 22, 37, 56, 68, 109, 103, 77],
         [24, 35, 55, 64, 81, 104, 113, 92],
         [49, 64, 78, 87, 103, 121, 120, 101],
         [72, 92, 95, 98, 112, 100, 103, 99]
         ]
    # wczytujemy szare zdjecie jako tablice
    img = mpimg.imread("myGray.jpg")
    # czytamy sobie ich rozmiar
    h, w = img.shape
    print(h, w)
    fft = np.fft.fft2(img)
    fh, fw = fft.shape
    # iterujemy po calej macierzy fourierowskiej
    for i in range(0, fh):
        for j in range(0, fw):
            x = int(round(((i / fh) * 7)))  # chcemy wartosc z przedzialu 0 do 7 wlacznie na podstawie i i fh
            y = int(round(((j / fw) * 7)))  # chcemy wartosc z przedzialu 0 do 7 wlacznie na podstawie
            # po zakomentowaniu tej linijki sie nie obraca
            # print(fft[i, j])
            fft[i, j] = fft[i, j] / complex(q[x][y])
            fft[i, j] = floor(fft[i, j].real) + floor(fft[i, j].imag) * 1j
            # print(fft[i, j], complex(q[x][y]))
            # odtworzenie obrazu
            fft[i, j] = fft[i, j] * complex(q[x][y])

    imgplot = plt.imshow(img, cmap='gray')
    plt.show()
    # teraz fourier w druga strone
    img2 = np.fft.ifft2(fft)
    abs_img2 = np.abs(img2)
    imgplot = plt.imshow(abs_img2, cmap='gray')
    plt.show()
