# Zadanie 3.
# Korzystając z algorytmu szybkiego liczenia konwolucji 2D (wykorzystującego DFT)
# zaproponuj metodę wyszukiwania wzorca na obrazie.
#
# Porównaj wyniki z dowolnym innym
# prostym podejściem znajdywania wzorca (np. korelacja).

# Korelacja w przestrzeni
# częstotliwości
# Korelacja dwóch obrazów również może
# być wydajnie przeprowadzona w przestrzeni
# częstotliwości. Jest ona ponownie
# równoważna mnożeniu transforat z
# dodatkową rotacją szukanego wzorca.

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random

import scipy.signal as s


def runThird():
    img = mpimg.imread("myGray.jpg")
    h, w = img.shape
    # we take only squere 20 image
    oryginalPartOfImage = []
    partOfImage = []
    sizeOfTemplate = 40
    darkenedPixels = 600
    for i in range(80, 80 + sizeOfTemplate):
        oryginalPartOfImage.append([])
        partOfImage.append([])
        for j in range(120, 120 + sizeOfTemplate):
            oryginalPartOfImage[i - 80].append(img[i, j])
            partOfImage[i - 80].append(img[i, j])
    # wyczerniamy 600 pixeli
    for i in range(0, darkenedPixels):
        rand1 = random.randrange(0, 40)
        rand2 = random.randrange(0, 40)
        # print(rand1,rand2)
        partOfImage[rand1][rand2] = 0

    # print(partOfImage)
    template = np.array(partOfImage)
    # print(template)
    template = np.rot90(template, 2)  # obrot o 180 stopni

    # working matrixes
    m1 = [[-1, 0, 1],
          [-1, 0, 1],
          [-1, 0, 1]]
    m2 = [[-1, -1, -1],
          [0, 0, 0],
          [1, 1, 1]]

    imagegd = s.convolve2d(img, np.divide(m1, 3), mode='same') + s.convolve2d(img, np.divide(m2, 3), mode='same')
    templategd = s.convolve2d(template, np.divide(m1, 3), mode='same') + s.convolve2d(template, np.divide(m2, 3),
                                                                                      mode='same')
    convolution = s.convolve2d(imagegd, templategd, mode='valid')
    # print(convolution)

    cw, ch = np.unravel_index(convolution.argmin(), convolution.shape)
    print("Indexes found: ", ch, ",", cw)
    copyImg = img.copy()
    # we want to mark it on our whole image
    for i in range(cw, cw + sizeOfTemplate):
        copyImg[i, ch] = 255
        copyImg[i, ch + sizeOfTemplate] = 255
    for i in range(ch, ch + sizeOfTemplate):
        copyImg[cw, i] = 255
        copyImg[cw + sizeOfTemplate, i] = 255

    # # pokazujemy nasz obrazek czesciowy
    imgplot = plt.imshow(oryginalPartOfImage, cmap='gray')
    plt.show()
    imgplot = plt.imshow(partOfImage, cmap='gray')
    plt.show()
    imgplot = plt.imshow(template, cmap='gray')
    plt.show()
    imgplot = plt.imshow(img, cmap='gray')
    plt.show()
    imgplot = plt.imshow(copyImg, cmap='gray')
    plt.show()
