self.enc1 = nn.Conv2d(
    1, 16,
    kernel_size=3,
    padding=1
)

self.enc2 = nn.Conv2d(
    16, 32,
    kernel_size=3,
    padding=1
)

self.dec1 = nn.ConvTranspose2d(
    32, 16,
    kernel_size=2,
    stride=2
)

self.final = nn.Conv2d(
    16, 1,
    kernel_size=1
)

mask = torch.sigmoid(x)