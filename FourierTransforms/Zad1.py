# Zadanie 1. Korzystając z DFT w 2D dokonaj transformacji dowolnego zaszumionego zdjęcia
# (lenna, ławica ryb, printscreen tej instrukcji) do domeny częstotliwościowej. Wykonaj
# odpowiedni zabieg w celu odszumienia obrazu, a następnie wylicz IDFT - powróć do domeny
# "czasowej".


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def runFirst(k):  # k to czestotliwosci wycinane
    # wczytujemy szare zdjecie jako tablice
    img = mpimg.imread("myGray.jpg")
    # czytamy sobie ich rozmiar
    h, w = img.shape
    print(h, w)
    fft = np.fft.fft2(img)
    print(fft.shape)
    for i in range(h - k, h):  # wiersz
        for j in range(0, k):  # kolumna
            fft[i, j] = 0
    # zerujemy
    for i in range(w - k, w):  # kolumna
        for j in range(0, k):  # wiersz
            fft[i, j] = 0

    # teraz fourier w druga strone
    img2 = np.fft.ifft2(fft)
    abs_img2 = np.abs(img2)
    imgplot = plt.imshow(img, cmap='gray')
    plt.show()
    imgplot = plt.imshow(abs_img2, cmap='gray')
    plt.show()
