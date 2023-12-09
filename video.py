import cv2
import numpy as np
import random 
import sys

def string_to_binary(input_string):
    # convert each character to a binary string
    binary_string = ""
    for char in input_string:
        binary_string += format(ord(char), '08b')

    return binary_string

def getPixelValue(bit):
    if bit == '0':
        return 0
    else:
        return 255
    
def getBitValue(pixel):
    if pixel == 0:
        return '0'
    else:
        return '1'

def stringToVideo(string, videoFile):
    # convert string data to binary
    binaryData = string_to_binary(string)

    print(binaryData)
    
    # convert the binary data to pixels
    pixels = []
    for binary in binaryData:
        for bit in binary:
            pixels.append(getPixelValue(bit))

    print("pixels", pixels)

    # convert the pixels to a numpy array
    pixels = np.array(pixels)


    # create a video writer
    frame_width = 640
    frame_height = 480
    fps = 30  # Set the frame rate to 1 frame per second


    # reshape the array to a 2D array
    pixels = pixels.reshape((len(string), 8))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(videoFile, fourcc, fps, (frame_width, frame_height), isColor=True)

    print(pixels)
    print(pixels.shape)

    totalPixelsOnAFrame = frame_width * frame_height

    # write the pixels to the video
    for pixel in pixels:
        frame = np.zeros((frame_height, frame_width, 3), np.uint8)
        # for i in range(0, frame_height):
        for j in range(0, 8):
            #     height      ,  width   ,   color channel
            frame[:, j*80:(j+1)*80, random.randint(0,2)] = pixel[j]  # random color channels
        out.write(frame)

    # release the video writer
    out.release()


def videoToString(videoFile):
    # create a video capture
    cap = cv2.VideoCapture(videoFile)

    # read the video
    string = ""
    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        # get the pixels from the frame
        pixels = []
        for i in range(0, 8):
            pixels.append(frame[:, i*80:(i+1)*80].mean())

        # convert the pixels to binary
        binary = ""
        for pixel in pixels:
            binary += getBitValue(pixel)

        # convert the binary to a character
        string += chr(int(binary, 2))

    # release the video capture
    cap.release()

    return string

def readFromFile(filePath):
    with open(filePath, 'r') as f:
        data = f.read()

    return data

def writeToFile(filePath, data):
    with open(filePath, 'w') as f:
        f.write(data)

def getTotalFrames(videoFile):
    cap = cv2.VideoCapture(videoFile)
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

if __name__ == "__main__":
    # get 1st and 2nd command line arguments
    operation = sys.argv[1]
    videoFile = sys.argv[2]
    inputFile = sys.argv[3]

    if operation == "encode":
        # read the input file
        inputString = readFromFile(inputFile)

        # encode the string into a video
        stringToVideo(inputString, videoFile)

    elif operation == "decode":
        # decode the video into a string
        outputString = videoToString(videoFile)

        # write the string to a file
        writeToFile(inputFile, outputString)
