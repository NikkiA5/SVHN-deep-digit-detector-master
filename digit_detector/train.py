
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator

import numpy as np


def train_detector(X_train, X_test, Y_train, Y_test, nb_filters = 32, batch_size=128, nb_epoch=5, nb_classes=2, do_augment=False, save_file='models/detector_model.hdf5'):
    """ vgg-like deep convolutional network """
    
    np.random.seed(1337)  # for reproducibility
      
    # input image dimensions
    img_rows, img_cols = X_train.shape[1], X_train.shape[2]
    
    # size of pooling area for max pooling
    pool_size = (2, 2)
    # convolution kernel size
    kernel_size = (3, 3) 
    input_shape = (img_rows, img_cols, 1)


    model = Sequential()
    model.add(Convolution2D(filters=nb_filters, kernel_size=(3,3),
                            border_mode='valid',
                            input_shape=input_shape, name='covolution2d_1'))
    model.add(Activation('relu', name='activation_1'))
    model.add(Convolution2D(filters=nb_filters, kernel_size=(3,3), name='covolution2d_2'))
    model.add(Activation('relu', name='activation_2'))
    model.add(MaxPooling2D(pool_size=pool_size, name='maxpooling2d_1'))
    # (16, 8, 32)
     
    model.add(Convolution2D(filters=nb_filters*2, kernel_size=(3,3), name='covolution2d_3'))
    model.add(Activation('relu', name='activation_3'))
    model.add(Convolution2D(filters=nb_filters*2, kernel_size=(3,3), name='covolution2d_4'))
    model.add(Activation('relu', name='activation_4'))
    model.add(MaxPooling2D(pool_size=pool_size, name='maxpooling2d_2'))
    # (8, 4, 64) = (2048)
        
    model.add(Flatten(name='flatten_1'))
    model.add(Dense(1024, name='dense_1'))
    model.add(Activation('relu'), name='activation_5')
    model.add(Dropout(0.5, name='dropout_1'))
    model.add(Dense(nb_classes, name='dense_2'))
    model.add(Activation('softmax'), name='activation_6')
        
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    
    if do_augment:
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2)
        datagen.fit(X_train)
        model.fit_generator(datagen.flow(X_train, Y_train, batch_size=batch_size),
                            samples_per_epoch=len(X_train), nb_epoch=nb_epoch,
                            validation_data=(X_test, Y_test))
    else:
        model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
              verbose=1, validation_data=(X_test, Y_test))
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    model.save(save_file)  


