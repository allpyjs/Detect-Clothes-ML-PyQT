from transformers import AutoFeatureExtractor, SegformerForSemanticSegmentation
import cv2
import torch.nn as nn
import numpy as np
import random
extractor = AutoFeatureExtractor.from_pretrained("mattmdjaga/segformer_b2_clothes")
model = SegformerForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")

def process(src):
    image = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]
    inputs = extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits.cpu()
    upsampled_logits = nn.functional.interpolate(
        logits,
        size=(h, w),
        mode="bilinear",
        align_corners=False,
    )
    pred_seg = np.array(upsampled_logits.argmax(dim=1)[0]).astype("uint8")
    mask_vals = np.unique(pred_seg)
    for val in mask_vals:
        if 2<val:
            temp_mask = pred_seg.copy()
            temp_mask[np.where(temp_mask!=val)] = 0
            temp_mask[np.where(temp_mask==val)] = 255
            contours = cv2.findContours(temp_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
            cnt = max(contours, key = cv2.contourArea)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            for pt in cnt:
                cv2.circle(src, pt[0], 1, (r, g, b), -1)
    return src