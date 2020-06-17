from PIL import Image
import numpy as np
import cv2
import sys



class HeartMonitor(object):


    def __init__(self):
        self.i = 0

        # Webcam Parameters
        self.realWidth = 320
        self.realHeight = 240
        self.videoWidth = 160
        self.videoHeight = 120
        self.videoChannels = 3
        self.videoFrameRate = 15

        # Color Magnification Parameters
        self.levels = 3
        self.alpha = 170
        self.minFrequency = 1.0
        self.maxFrequency = 2.0
        self.bufferSize = 150
        self.bufferIndex = 0

        # Output Display Parameters
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.loadingTextLocation = (20, 30)
        self.bpmTextLocation = (self.videoWidth//2 + 5, 30)
        self.fontScale = 1
        self.fontColor = (255, 255, 255)
        self.lineType = 2
        self.boxColor = (0, 255, 0)
        self.boxWeight = 3

        # Bandpass Filter for Specified Frequencies
        self.frequencies = (1.0*self.videoFrameRate) * np.arange(self.bufferSize) / (1.0*self.bufferSize)
        self.mask = (self.frequencies >= self.minFrequency) & (self.frequencies <= self.maxFrequency)

        # Heart Rate Calculation Variables
        self.bpmCalculationFrequency = 15
        self.bpmBufferIndex = 0
        self.bpmBufferSize = 10
        self.bpmBuffer = np.zeros((self.bpmBufferSize))

        # Initialize Gaussian Pyramid
        self.firstFrame = np.zeros((self.videoHeight, self.videoWidth, self.videoChannels))
        self.firstGauss = self.buildGauss(self.firstFrame, self.levels+1)[self.levels]
        self.videoGauss = np.zeros(
                (self.bufferSize, self.firstGauss.shape[0], self.firstGauss.shape[1], self.videoChannels))
        self.fourierTransformAvg = np.zeros((self.bufferSize))

    def apply_makeup(self, pil_image):
        big_frame = np.array(pil_image)
        frame = cv2.resize(big_frame, (self.realWidth, self.realHeight), interpolation = cv2.INTER_AREA)
        detectionFrame = frame[self.videoHeight//2:self.realHeight -
                           self.videoHeight//2, self.videoWidth//2:self.realWidth-self.videoWidth//2, :]
        self.videoGauss[self.bufferIndex] = self.buildGauss(detectionFrame, self.levels+1)[self.levels]
        fourierTransform = np.fft.fft(self.videoGauss, axis=0)

        # Bandpass Filter
        fourierTransform[self.mask == False] = 0

        # Grab a Pulse
        if self.bufferIndex % self.bpmCalculationFrequency == 0:
            self.i += 1
            for buf in range(self.bufferSize):
                self.fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
            hz = self.frequencies[np.argmax(self.fourierTransformAvg)]
            bpm = 60.0 * hz
            self.bpmBuffer[self.bpmBufferIndex] = bpm
            self.bpmBufferIndex = (self.bpmBufferIndex + 1) % self.bpmBufferSize

        # Amplify
        filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
        filtered = filtered * self.alpha

        # Reconstruct Resulting Frame
        filteredFrame = self.reconstructFrame(filtered, self.bufferIndex, self.levels)
        outputFrame = detectionFrame + filteredFrame
        outputFrame = cv2.convertScaleAbs(outputFrame)

        self.bufferIndex = (self.bufferIndex + 1) % self.bufferSize

        frame[self.videoHeight//2:self.realHeight-self.videoHeight//2,
            self.videoWidth//2:self.realWidth-self.videoWidth//2, :] = outputFrame
        cv2.rectangle(frame, (self.videoWidth//2, self.videoHeight//2), (self.realWidth -
                                                            self.videoWidth//2, self.realHeight-self.videoHeight//2), self.boxColor, self.boxWeight)
        if self.i > self.bpmBufferSize:
            cv2.putText(frame, "BPM: %d" % self.bpmBuffer.mean(),
                        self.bpmTextLocation, self.font, self.fontScale, self.fontColor, self.lineType)
        else:
            cv2.putText(frame, "Calculating BPM...", self.loadingTextLocation,
                        self.font, self.fontScale, self.fontColor, self.lineType)
        return Image.fromarray(np.uint8(frame))

    def buildGauss(self, frame, levels):
            pyramid = [frame]
            for level in range(levels):
                frame = cv2.pyrDown(frame)
                pyramid.append(frame)
            return pyramid


    def reconstructFrame(self, pyramid, index, levels):
            filteredFrame = pyramid[index]
            for level in range(levels):
                filteredFrame = cv2.pyrUp(filteredFrame)
            filteredFrame = filteredFrame[:self.videoHeight, :self.videoWidth]
            return filteredFrame
