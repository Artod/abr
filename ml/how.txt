docker run --gpus all -it --rm -v "C:\Users\garto\OneDrive\Documents\GitHub\abr\ml:/tf/notebooks" -p 8888:8888 tensorflow/tensorflow:latest-gpu-jupyter
	
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))