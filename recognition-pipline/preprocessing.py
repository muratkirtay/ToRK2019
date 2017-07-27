import numpy as np
import cv2
import os
import scipy.io as sio

# Eliminate the incompatibility between different open cv versions
cv2.CV_LOAD_IMAGE_GRAYSCALE = 0



def binarize_images(num_of_objects=50, vect_size, data_path, icub_bin_path):
    """
    Extract the content of the .mat file.
    :param num_of_objects: number of object 
    :param vect_size:      size of vectorized images (32,32)
    :param data_path:      where images located
    :param icub_bin_path:  where binarized image vectors located
    :return: save the binarized images in vector form 
    """

	content = np.zeros((number_of_images-1, vect_size), dtype=np.uint8)

    # object loop
    for ii in range(1, num_of_objects+1):
        if ii < 10:
            directory = data_path + "object00" + str(ii)
        else:
            directory = data_path + "object0" + str(ii)
        # image loop
        for i in range(1, number_of_images):
            imgpath = directory+'/'+"00"+str(i) + ".png"

            gimage = cv2.imread(imgpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            roimg = gimage[100:450, 50:460] # verified by rectangle
            bin_img = cv2.adaptiveThreshold(roimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 351, -10)

            rimage = cv2.resize(bin_img, resize)
            nonz = rimage.nonzero()
            rimage[nonz] = 1
            img_vect = np.reshape(rimage, vect_size)
            content[i-1, :] = img_vect

        sio.savemat(icub_bin_path + 'obj' + str(ii) + '.mat', mdict={'obj' + str(ii): content})
        content = np.zeros((number_of_images-1, vect_size), dtype=np.uint8)


def extract_folder_names(path):
    """ 
    Extract file names as a list form the data path directory
    :param path: where the folders located
    :return: the name of the folders in a tuple
    """
    directories = []
    for dname, sdir, fnames in os.walk(path):
        directories.append(dname)

    return directories 

def extract_category_images(file_names, num_of_imgs):
    """ Extract all images form directory list and combine them according to
        their category.
    """

    imgnames_list = []
    for i in xrange(0, len(file_names), num_of_imgs):
        imgnames_list.append(file_names[i:i + num_of_imgs])

    return imgnames_list


def display_images(path, name_list, num_of_imgs):
    """ Display images in the image name list.
        TODO: Since os.walk produce a list in not in order.
        That should be reconsidered for later process.
    """
    resize_dims = (300, 300)

    for i in range(len(name_list)):
        for j in range(num_of_imgs):
            showimg = cv2.imread(path + name_list[i][j])
            imgtitle = "Class id" + str(i) + name_list[i][j]
            cv2.imshow(imgtitle, cv2.resize(showimg, resize_dims))
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def resize_patterns(ppath, rpath, resize_wh):
    ''' Resize a given pattern (to default20x20) and save it to 
        a predefined directory
    '''

    width, height = resize_wh[0], resize_wh[1]
    for dname, sdir, fnames in os.walk(ppath):
        for pname in fnames:
            npname = os.path.join(ppath, pname)
            npimg = cv2.imread(npname,0)
            resized_pattern = cv2.resize(npimg, resize_wh)

            cv2.imwrite(os.path.join(rpath, pname), resized_pattern)

