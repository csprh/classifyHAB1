# HAB Deep Learning Classifications

This code is for generating classfication scores for HAB databases

There are two basic classification methods:

1. Extract features from each frame with a ConvNet, passing the sequence to an RNN, in a separate network
2. Extract features from each frame with a ConvNet and pass the sequence to an MLP

The code is based on a method of classifying videos(see full details on blog: https://medium.com/@harvitronix/five-video-classification-methods-implemented-in-keras-and-tensorflow-99cad29cc0b5)

## Requirements

This code requires you have Keras 2 and TensorFlow 1 or greater installed. Please see the `requirements.txt` file. To ensure you're up to date, run:

`pip install -r requirements.txt`

## Getting the data

The data is extracted using a MATLAB script and deposited into the CNNIms
directory (one jpg per time stamp).

## Extracting features

For the two models (`lstm` and `mlp`) features are firstly extracted from each jpg image using the 
`extract_features.py` script. 

## Training models

The CNN-only method (method #1 in the blog post) is run from `train_cnn.py`.

The rest of the models are run from `train.py`. There are configuration options you can set in that file to choose which model you want to run.

The models are all defined in `models.py`. Reference that file to see which models you are able to run in `train.py`.

Training logs are saved to CSV and also to TensorBoard files. To see progress while training, run `tensorboard --logdir=data/logs` from the project root folder.

## Demo/Using models

I have not yet implemented a demo where you can pass a video file to a model and get a prediction. Pull requests are welcome if you'd like to help out!

## TODO

- [ ] Add data augmentation to fight overfitting
- [x] Support multiple workers in the data generator for faster training
- [ ] Add a demo script
- [ ] Support other datasets
- [ ] Implement optical flow
- [ ] Implement more complex network architectures, like optical flow/CNN fusion

## UCF101 Citation

Khurram Soomro, Amir Roshan Zamir and Mubarak Shah, UCF101: A Dataset of 101 Human Action Classes From Videos in The Wild., CRCV-TR-12-01, November, 2012. 

