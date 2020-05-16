
import numpy as np
import matplotlib.pyplot as plt

img = plt.imread("big_granite.png")
print(img.shape)

img2 = np.sum(img, axis=2)
plt.imshow(img2)
plt.show()
print(img2.shape)
print("mean", np.mean(img2))
print("var", np.var(img2))

# histogram = np.histogram(img2, bins=256)
# plt.plot(histogram[0])
# plt.show()


# new = np.random.rand(600, 800)
# new = np.random.exponential(scale=0.64, size=(600, 800))
# plt.imshow(new)
# plt.show()
# print("mean", np.mean(new))
# print("var", np.var(new))
#
# histogram2 = np.histogram(new, bins=256)
# plt.plot(histogram2[0])
# plt.show()





def chunks(img):
    height, width = img.shape
    res = []
    tilesize = 32
    # cnt = 100
    for i in range(int(height/tilesize) - 1):
        for j in range(int(height/tilesize) - 1):
            tile = img[i*tilesize:(i+1)*tilesize, j*tilesize:(j+1)*tilesize]
            res.append(tile)
            # plt.imsave(f"{cnt}_rock.png", tile, cmap='gray')
            # cnt += 1

    return res

def chunks_blownup(img):
    height, width = img.shape
    res = []
    tilesize = 16
    # cnt = 100
    for i in range(int(height/tilesize) - 1):
        for j in range(int(height/tilesize) - 1):
            tile = img[i*tilesize:(i+1)*tilesize, j*tilesize:(j+1)*tilesize]
            tile = np.kron(tile, np.ones((2,2)))
            res.append(tile)
            # plt.imsave(f"{cnt}_rock.png", tile, cmap='gray')
            # cnt += 1

    return res


# tiles = chunks(img2)


# img3 = plt.imread("sand.png")
# img3 = np.sum(img3, axis=2)
# tiles = chunks(img3)

tiles = chunks_blownup(img2)

cnt = 3000
for tile in sorted(tiles, key=lambda t: np.mean(t)):
    plt.imsave(f"{cnt}_rock_big.png", tile, cmap='gray')
    cnt += 1




