import numpy as np
from keras.preprocessing import image
test_image = image.load_img('D:/Shivani Chander/test.png', target_size = (150,150))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)



from keras.models import Sequential
from keras.layers import Dense, Activation


def build_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    #model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

    return model

model2 = build_model()
model2.load_weights('D:/Shivani Chander/Sangam 2K18/ListeninWeights.hdf5')


result = model2.predict(test_image)

train_generator.class_indices
if result[0][0] == 1:
    prediction = 'Depressed'
else:
    prediction = 'Undepressed'
    
print(prediction)