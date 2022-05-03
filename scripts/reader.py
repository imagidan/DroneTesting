from cuda_functions import *

class Reader:

    def __init__(self, labels_path="../lpr/us_lp_characters.txt", engine_path="../lpr/lpr_us_onnx_b16.engine"):
        trt_logger = trt.Logger(trt.Logger.WARNING)
        trt_runtime = trt.Runtime(trt_logger)
        trt_engine = load_engine(trt_runtime, engine_path)
        self.context = trt_engine.create_execution_context()
        self.buffers = allocate_buffers(trt_engine)
        label_text = open(labels_path, "r").readlines()
        self.labels = []
        for line in label_text:
            self.labels.append(line[0])

    def read(self, img):
        inputs, outputs, bindings, stream = self.buffers
        inputs[0].host = img
        input_shape = (1, 3, 48, 96)
        self.context.set_binding_shape(0, input_shape)
        outputs = do_inference(self.context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream)
        filtered_outputs = list(filter(lambda a: a != 35, outputs[0]))
        license_plate_chars = ""
        for ind in filtered_outputs:
            license_plate_chars += self.labels[ind]
        
        print(img.shape)
        print(len(self.labels))
    
        return license_plate_chars