# Semantic segmentation fcn_resnet101


## Pre-requisites

* Please follow the instructions for setting up Qualcomm Neural Processing SDK using the [link] (https://developer.qualcomm.com/sites/default/files/docs/snpe/setup.html) provided. 
- Install onnx v1.6.0. Installation instruction can be found [here](https://qdn-drekartst.qualcomm.com/hardware/qualcomm-innovators-development-kit/frameworks-qualcomm-neural-processing-sdk-for-ai)
- Install onnxsim ```pip install onnxsim``` and onnxruntime ```pip install onnxruntime```.
- Install OpenCV ```pip install cv2```
- Install mxnet ```pip install mxnet```


## How to get the model ? 

for ONNX model follow  attached notebook 

```
import os
dummy_input = torch.randn(1,3, 400, 400).type(torch.FloatTensor).to('cpu')
torch.onnx.export(model, dummy_input, "./models/fcn_resnet101.onnx",opset_version=11)

``` 
## Convert model to DLC

for fp32_DLC and FP16_DLC model follow  attached notebook  

```
snpe-onnx-to-dlc --input_network models/fcn_resnet101.onnx --output_path models/fcn_resnet101.dlc

```

## Quantization of DLC
for quantized INT8_DLC, INT16_DLC model follow  attached notebook  
```
cd input/
snpe-dlc-quantize --input_dlc ../models/fcn_resnet101.dlc --input_list input.txt  --axis_quant --output_dlc ../models/fcn_resnet101_quant.dlc  
```

## Accuracy Analysis
- To check results please run "[fcn_resnet101](fcn_resnet101.ipynb)".
- To run any jupyter notebook, run below command. It will generate few links on the screen, pick the link with your machine name on it (host-name) and paste it in any browser.
- Navigate to the notebook ".ipynb" file and simply click that file.
```python
jupyter notebook --no-browser --port=8080 --ip 0.0.0.0 --allow-root
```


###### *Snapdragon and Qualcomm Neural Processing SDK are products of Qualcomm Technologies, Inc. and/or its subsidiaries.*
