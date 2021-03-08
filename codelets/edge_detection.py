import cv2
from isaac import Codelet


class EdgeDetector(Codelet):
    def __init__(self):
        self.kernel_size = 3

    def start(self):
        # defining input
        self.input_image = self.isaac_proto_rx("ImageProto", "input_image")

        # defining output
        self.output_image = self.isaac_proto_tx("ImageProto", "output_image")

        # setting codelet to tick when input appears
        self.tick_on_message(self.input_image)

    def tick(self):
        # getting the input
        image_tensor = self.input_image.message.tensor

        # Performing edge detection:
        ## applying gaussian blur
        blurred = cv2.GaussianBlur(
            image_tensor,
            (self.kernel_size, self.kernel_size),
            sigmaX=0,
            sigmaY=0,
            borderType=cv2.BORDER_DEFAULT,
        )
        blurred = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)

        ## getting gradients
        gradient_x = cv2.Sobel(blurred, cv2.CV_16S, 1, 0, ksize=self.kernel_size)
        gradient_y = cv2.Sobel(blurred, cv2.CV_16S, 0, 1, ksize=self.kernel_size)

        abs_gradient_x = cv2.convertScaleAbs(gradient_x)
        abs_gradient_y = cv2.convertScaleAbs(gradient_y)

        ## getting resultant image
        res_image = cv2.addWeighted(abs_gradient_x, 0.5, abs_gradient_y, 0.5, 0)

        # Setting output of codelet
        ## initializing the output
        tx_builder = self.output_image.init()

        ## setting ImageProto properties (have a look at messages/image.capnp in the sdk)
        tx_builder.proto.elementType = "uint8"
        tx_builder.proto.rows = res_image.shape[0]
        tx_builder.proto.cols = res_image.shape[1]
        tx_builder.proto.channels = 1
        tx_builder.proto.dataBufferIndex = 0

        ## setting the resultant image as output
        tx_builder.buffers = [res_image]

        ## setting acquisition time
        tx_builder.acqtime = self.input_image.message.acqtime

        # sending the output
        self.output_image.publish()
