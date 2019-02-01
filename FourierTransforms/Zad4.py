# Zadanie 4.
# Zaproponuj metodę rozpoznawania tekstu pisanego w plikach graficznych (tzw.
# OCR). Wykorzystaj metodę z zadania 3 lub inny klasyfikator (uwaga: niemile widziane
# rozwiązania typu black-box i [niemal]jednolinijkowe)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.signal as s


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def runFourth():
    img = mpimg.imread("myRGB.JPG")
    print(img.shape)
    imgInGray = rgb2gray(img)
    print(imgInGray.shape)

    a = mpimg.imread("myB.JPG")
    print(a.shape)
    aInGray = rgb2gray(a)
    ah, aw = aInGray.shape

    plt.imshow(aInGray, cmap='gray')
    plt.show()
    plt.imshow(imgInGray, cmap='gray')
    plt.show()

    # orbracamy o 180 stopni
    aInGray = np.rot90(aInGray, 2)

    m1 = [[-1, 0, 1],
          [-1, 0, 1],
          [-1, 0, 1]]
    m2 = [[-1, -1, -1],
          [0, 0, 0],
          [1, 1, 1]]

    imgInGray = s.convolve2d(imgInGray, np.divide(m1, 3), mode='same') + s.convolve2d(imgInGray, np.divide(m2, 3),
                                                                                      mode='same')
    aInGray = s.convolve2d(aInGray, np.divide(m1, 3), mode='same') + s.convolve2d(aInGray, np.divide(m2, 3),
                                                                                  mode='same')

    convolution = s.convolve2d(imgInGray, aInGray, mode='valid')

    cw, ch = np.unravel_index(convolution.argmin(), convolution.shape)
    print(cw, ch, convolution[cw, ch])

    plt.imshow(convolution, cmap='gray')
    plt.show()

    w, k = convolution.shape
    indexes = []

    for r in range(0, w):
        for c in range(0, k):
            if convolution[r, c] < -8400000:
                indexes.append((r, c))
    print(indexes, len(indexes))

    for r, c in indexes:
        # gorna i dolna czesc ramki
        for i in range(c, c + aw + 1):
            if r + ah >= w or c + aw + 1 >= k:
                continue
            imgInGray[r, i] = 255
            imgInGray[r + ah, i] = 255

        # prawa i lewa czesc ramki
        for j in range(r, r + ah + 1):
            if r + ah + 1 >= w or c + aw >= k:
                continue
            imgInGray[j, c] = 255
            imgInGray[j, c + aw] = 255

    mpimg.imsave("result.JPG", imgInGray)
    # litery w dolnych wierszach moga nie byc zaznaczone z uwagi iz ramka moglabhy wyjsc poza indeks listy
    return "xDDD"
