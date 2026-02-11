from train import train_dataset

if __name__ == "__main__":
    datasets = ['diabetes', 'heart']
    for ds in datasets:
        train_dataset(ds)
    print("\nAll models trained and saved successfully!")