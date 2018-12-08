
This is a client-server Face Recognition API, able to maintain multiple data from different companies 
in the same database.
The face descriptor network were obtained from [Dlib](http://dlib.net)[1].
The server uses Flask microframework, and MySQL is used as a database.

Once the server ```server.py```  
is online, it waits  a JSON post [with this attributes](https://github.com/luanps/faceRecognitionAPI/blob/49ebd3387ef947a9ba6987a31f553b1885be8cc5/client.py#L14-L40), and parses it to the ```recognition.py``` main function.

The recognition function is responsible for making queries on the database, returning a JSON with error/success codes.

The client side can POST a JSON directly to the server.
Alternatively, we made a client script for easily understanding. In this example,
 a face image is obtained from the webcam, using:
```
 python3 fakeTotem.py
```

The demo_2d.py, demo_3d.py and demo_onclick.py scripts are used for local tests.

Note that the code in this repository  won't work without the database, which is not
publicly available.


The model has been trained on a dataset with 3 million faces
[3,4]. Accuracy achieved on Labeled Faces in the Wild (LFW)[2] dataset: 99.38%
More details about Dlib face analisys pipeline can be obtained
[here](https://github.com/davisking/dlib-models).


The requirements are listed  on requirements.txt

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


