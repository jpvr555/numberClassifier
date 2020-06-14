import tensorflow as tf
import os

epochs = int(os.getenv('EPOCHS', 5))

# Download reshape and normalize data.
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_train, x_test = x_train / 255.0, x_test / 255.0

# Quick model taken from the Tensorflow examples.
model = tf.keras.models.Sequential([ 
    tf.keras.layers.Conv2D(28, kernel_size=(3,3), input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)

model.compile(optimizer='adam',
    loss=loss_fn,
    metrics=['accuracy'])

model.fit(x_train, y_train, epochs=epochs)

model.evaluate(x_test,  y_test, verbose=2)

model.save('./output/numberClassifier.h5')
