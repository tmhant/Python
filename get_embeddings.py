import numpy as np
import onnxruntime as rt
from sklearn.preprocessing import normalize

onnx_path = "model/arcfaceresnet100.onnx"
extractor = rt.InferenceSession(onnx_path)

t_aligned = np.transpose(aligned, (2, 0, 1))
inputs = t_aligned.astype(np.float32)
input_blob = np.expand_dims(inputs, axis=0)

first_input_name = extractor.get_inputs()[0].name
first_output_name = extractor.get_outputs()[0].name

predict = extractor.run([first_output_name], {first_input_name: input_blob})[0]
final_embedding = normalize(predict).flatten()
