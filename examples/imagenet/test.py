# Copyright 2020 Lorna Authors. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Example
In this simple example, we load an image, pre-process it, and classify it with a pretrained GoogLeNet.
"""

import json

import torch
import torchvision.transforms as transforms
from PIL import Image
from googlenet import GoogLeNet

image_size = 224

# Open image
img = Image.open('panda.jpg')

# Preprocess image
tfms = transforms.Compose([transforms.Resize(image_size), transforms.CenterCrop(image_size),
                           transforms.ToTensor(),
                           transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), ])
img = tfms(img).unsqueeze(0)

# Load class names
labels_map = json.load(open('labels_map_1000.txt'))
labels_map = [labels_map[str(i)] for i in range(1000)]

# Classify with AlexNet
print("=> loading checkpoint 'googlenet'.")
model = GoogLeNet.from_pretrained('googlenet')
print("=> loaded checkpoint 'googlenet'.")
model.eval()
with torch.no_grad():
    logits = model(img)
preds = torch.topk(logits, k=5).indices.squeeze(0).tolist()

print('-----')
for idx in preds:
    label = labels_map[idx]
    prob = torch.softmax(logits, dim=1)[0, idx].item()
    print('{:<75} ({:.2f}%)'.format(label, prob * 100))
