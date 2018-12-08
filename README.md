
This is a Face Recognition API is based on [Dlib](http://dlib.net)[1].
It consists on a client-server recognition pipeline, storing the face descriptors and its attributes on a database.

The client side reads a single face image from webcam, using:
'''
 python3 fakeTotem.py
'''
and makes a request to the server, which can be a new register insertion or
a face matching.

The server side gets a [Request](https://github.com/luanps/faceRecognitionAPI/blob/7b87e39677601c9d9fb6d522b0b5e5080964fc7d/request.py#L7) JSON and make a face identification query on the database.


The demo_2d.py, demo_3d.py and demo_onclick.py scripts are used for local test.

Note that this code won't work without the database, which is not
publicly available.


The model has been trained on a dataset with 3 million faces
[3,4]. Accuracy achieved on Labeled Faces in the Wild (LFW)[2] dataset: 99.38%
More details about Dlib face analisys pipeline can be obtained
[here](https://github.com/davisking/dlib-models).

**Basic Requirements:**

- python3
- dlib
- numpy
- cv2 (opencv)
- python3-tk
- Pillow
- _pickle
- skimage

**Download Dlib trained models from:**

- [Face alignment](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2)
- [Face descriptor](http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2)
and rename to model1.dat(face descriptor) and model2.dat(face aligment)

**References:**

[1] http://dlib.net/

[2] HUANG, Gary B. et al. Labeled faces in the wild: A database for studying
face recognition in unconstrained environments. Technical Report 07-49,
     University of Massachusetts, Amherst, 2007.

[3] H.-W. Ng, S. Winkler. A data-driven approach to cleaning large face
datasets. Proc. IEEE International Conference on Image Processing (ICIP),
  Paris, France, Oct. 27-30, 2014 

[4] O. M. Parkhi, A. Vedaldi, A. Zisserman Deep Face Recognition British
Machine Vision Conference, 2015.


