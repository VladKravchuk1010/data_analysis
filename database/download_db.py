import kagglehub

# Download latest version
path = kagglehub.dataset_download("iamsouravbanerjee/world-population-dataset")

print("Path to dataset files:", path)