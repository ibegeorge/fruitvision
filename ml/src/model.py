import torch
from torch import nn


class FruitClassifier(nn.Module):
    """
    Convolutional neural network for fruit image classification.

    Args:
        num_classes:
            Number of fruit categories the model predicts.
    """
    def __init__(self, num_classes: int):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(
                in_channels=3,
                out_channels=16,
                kernel_size=3,
                padding=1,
                stride=1,
            ),
            nn.ReLU(),

            nn.MaxPool2d(
                kernel_size=2,
                stride=2,
            ),
        )

        self.flatten = nn.Flatten()

        self.classifier = nn.Sequential(
            nn.Linear(
                16 * 112 * 112,
                128,
            ),
            nn.ReLU(),

            nn.Linear(
                128,
                num_classes,
            ),
        )

    def forward(self, x):

        x = self.features(x)
        x = self.flatten(x)
        x = self.classifier(x)

        return x


if __name__ == "__main__":

    model = FruitClassifier(
        num_classes=4
    )

    image = torch.rand(
        1,
        3,
        224,
        224,
    )

    output = model(image)

    print("Input shape:", image.shape)
    print("Output shape:", output.shape)