import getopt
import sys
import magic

import cv2


def encode(rgba_image, __message):
    message_iterator = iter(__message)
    size_x, size_y = get_image_info(rgba_image)
    __KEY = key_generator(size_x, size_y, len(__message))
    print("key is " + str(__KEY))

    try:
        for index_y, y in enumerate(rgba_image):
            for index_x, x in enumerate(y):
                if (index_y * size_x + index_x) % __KEY == 0:
                    x[3] = 0
                    for i in range(3):
                        x[i] = ord(" ")
                    for i in range(3):
                        x[i] = ord(next(message_iterator))
    except StopIteration as si:
        print("message hidden")
    return True


def decode(rgba_image):
    __KEY = -1
    size_x, size_y = get_image_info(rgba_image)
    for index_y, y in enumerate(rgba_image):
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
    for index_y, y in enumerate(rgba_image):
        for index_x, x in enumerate(y):
            if (index_y * size_x + index_x) % __KEY == 0:
                if x[3] == 0:
                    result += chr(x[0]) + chr(x[1]) + chr(x[2])
                else:
                    break
    print(result)
    return result


def key_generator(size_x, size_y, message_size):
    return int((size_x * size_y) / message_size)


def get_image_info(rgba_image):
    size_y = len(rgba_image)
    size_x = len(rgba_image[0])
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
        usage("parameters missing")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
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
        usage("input image is missing")
        sys.exit(2)
    is_clean, input_image = check_image(image_path)
    if mode == "encode":
        # is_clean, input_image = check_image(image_path)
        if not is_clean:
            print("the imported image may contain already a message or does not fit the algorithm")
            sys.exit(0)
        if output_path == "":
            usage("output path missing")
            sys.exit(2)
        rgba_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
        if encode(rgba_image, message):
            cv2.imwrite(output_path, rgba_image)
        else:
            print("encoding error")
            sys.exit(2)
    else:
        decode(input_image)


def usage(message=""):
    if message != "":
        print(message)
    encode_example = "Main.py -m <message> -i <inputfile> -o <outputfile>"
    decode_example = "Main.py -d -i <inputfile>"
    print("to encode:  >> " + encode_example + "\nor\n" + "to decode:  >> " + decode_example)


def check_image(image_path):
    x = magic.from_file(image_path)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if "JPEG" in x:
        print("jpeg detected")
        return True, image
    elif "PNG" in x:
        print("png detected")
        if len(image[0,0]) != 4:
            print("png alpha channel error")
            sys.exit(2)
        else:
            for y in image:
                for x in y:
                    if x[3] == 0:
                        break
                else:
                    continue
                break
            else:
                # print("input file is ok to hide a message")
                return True, image
            # print("input file is a not valid png to hide a message")
            return False, image
    print(x)


main()
