

## Requirements

The Darknet framework is self-contained in the "darknet" folder and must be compiled before running the tests. To build Darknet please run the following command:

$ cd darknet && make

Other requirements:
1. Keras
2. Tensorflow
3. Numpy

## Download Models

The models should be downloaded before running the other script

$ bash get-networks.sh
```

## Running


Please run the script "run.sh".

It requires 3 arguments:
1. Output folder, please make sure this folder exists.
2. an output (CSV) file
3. The video file

$ bash run.sh ./tmp/output ./tmp/output/results.csv LPR.mp4
