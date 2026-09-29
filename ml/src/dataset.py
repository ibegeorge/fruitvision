from datasets import load_dataset
from torchvision import transforms
from torch.utils.data import DataLoader

image_transform = transforms.Compose(
    [
        transforms.Lambda(
            lambda img: img.convert("RGB")
        ),
        transforms.Resize(
            (224,224)
        ),
        transforms.ToTensor(),
    ]
)

def transform(example):

    example["image"] = [
        image_transform(image)
        for image in example["image"]
    ]

    return example

def get_dataloaders():

    dataset = load_dataset(
        "VinayHajare/Fruits-30"
    )

    dataset = dataset["train"].train_test_split(
        test_size=0.2,
        seed=42
    )
    dataset["train"].set_transform(transform)
    dataset["test"].set_transform(transform)

    train_loader = DataLoader(
        dataset["train"],
        batch_size=32,
        shuffle=True,
    )
    test_loader = DataLoader(
        dataset["test"],
        batch_size=32,
        shuffle=False,
    )

    return train_loader, test_loader

if __name__ == "__main__":

    train_loader, test_loader = get_dataloaders()
    batch = next(iter(train_loader))
    images = batch["image"]
    labels = batch["label"]

    print("Images:", images.shape)
    print("Labels:", labels.shape)