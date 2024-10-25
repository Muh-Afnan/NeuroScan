import tensorflow as tf

# # Function to normalize images
# def normalize_image(image):
#     # Convert pixel values from 0-255 to 0-1 by dividing by 255
#     image = tf.cast(image, tf.float32) / 255.0
#     return image

# # Example usage with TensorFlow dataset
# def preprocess_dataset(dataset):
#     dataset = dataset.map(lambda x, y: (normalize_image(x), y))
#     return dataset

# # Load a dataset (for example, from files)
# # This is just a placeholder example, replace with actual dataset loading code
# (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# # Convert images to TensorFlow dataset format
# train_dataset = tf.data.Dataset.from_tensor_slices((train_images, train_labels))

# # Normalize the dataset images
# train_dataset = preprocess_dataset(train_dataset)

# # Batch and prefetch the dataset for performance optimization
# train_dataset = train_dataset.batch(32).prefetch(tf.data.AUTOTUNE)

image = tf.io.read_file("D:/CV2/images/volume_1.jpg")
image = tf.image.decode_image(image, channels=3)  # Decode the image (RGB)
