trt_logger = trt.Logger(trt.Logger.WARNING)
trt_engine_path = "../lpr/lpr_us_onnx_b16.engine"
trt_runtime = trt.Runtime(trt_logger)
trt_engine = load_engine(trt_runtime, trt_engine_path)
context = trt_engine.create_execution_context()

inputs, outputs, bindings, stream = allocate_buffers(trt_engine)

rgb2 = cv2.resize(rgb, (96, 48))

    np.copyto(inputs[0].host, rgb2.ravel())
    outputs = do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream)
    print(outputs)

        xError = detection.Center[0] - 640
        yError = detection.Center[1] - 360
        #print(xError)
        #print(yError)