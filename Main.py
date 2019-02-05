import getopt
import sys

import cv2


def encode(rgbaImage, __MESSAGE):
    messageIterator = iter(__MESSAGE)
    size_x, size_y = getImageInfo(rgbaImage)
    __KEY = keyGenerator(size_x, size_y, len(__MESSAGE))
    print("key is " + str(__KEY))

    try:
        for index_y, y in enumerate(rgbaImage):
            for index_x, x in enumerate(y):
                if (index_y * size_x + index_x) % __KEY == 0:
                    x[3] = 0
                    for i in range(3):
                        x[i] = ord(" ")
                    for i in range(3):
                        x[i] = ord(next(messageIterator))
    except StopIteration as si:
        print("message hidden")
    return True


def decode(rgbaImage):
    __KEY = -1
    size_x, size_y = getImageInfo(rgbaImage)
    for index_y, y in enumerate(rgbaImage):
        for index_x, x in enumerate(y):
            if index_y != 0 | index_x != 0:
                if x[3] == 0:
                    __KEY = index_y * size_x + index_x
                    break
        else:
            continue  # for termina  regolarmente
        break  # for termina con un break: ho trovato la chiave
    if __KEY < 0:
        print("invalid image")
        return -1
    else:
        print("key is " + str(__KEY))
    result = ""
    for index_y, y in enumerate(rgbaImage):
        for index_x, x in enumerate(y):
            if (index_y * size_x + index_x) % __KEY == 0:
                if x[3] == 0:
                    result += chr(x[0]) + chr(x[1]) + chr(x[2])
                else:
                    break
    print(result)
    return result


def keyGenerator(size_x, size_y, messageSize):
    return int((size_x * size_y) / messageSize)


def getImageInfo(rgbaImage):
    size_y = len(rgbaImage)
    size_x = len(rgbaImage[0])
    return size_x, size_y


def main():
    output_path = ""
    image_path = ""
    message = ""
    mode = "encode"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdm:i:o:", ["decode", "message=", "inputfile=", "outputfile="])
        if len(opts) == 0:
            raise getopt.GetoptError("No params")
    except getopt.GetoptError:
        print('Main.py -m <message> -i <inputfile> -o <outputfile>')
        print("or")
        print('Main.py -d -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Main.py -m <message> -i <inputfile> -o <outputfile>')
            return
        elif opt in ("-i", "ifile"):
            image_path = arg
        elif opt in ("-o", "ofile"):
            output_path = arg
        elif opt in ("-m", "message"):
            message = arg
        elif opt in ("-d", "decode"):
            mode = "decode"
    if image_path == "":
        print("input image is missing")
        sys.exit(2)

    input_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if mode == "encode":
        if output_path == "":
            print("output path missing")
            sys.exit(2)
        rgba_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
        if encode(rgba_image, message):
            cv2.imwrite(output_path, rgba_image)
        else:
            print("encoding error")
            sys.exit(2)
    else:
        decode(input_image)


# TODO make usage function
main()
