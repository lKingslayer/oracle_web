
from logging import root
import sys
import torch
import torchvision.models as models
from torchvision.transforms import transforms
from PIL import Image
import json
from utils import preprocess, euclidean_dist, cosine_dist

class OCRModel:
    def __init__(self,
                 fc=torch.nn.Identity(),
                 checkpoint_path="../SimCLR-release/checkpoints/handa_best.pth.tar",
                 feat_path="../SimCLR-release/feats/predict_feats.pth",
                 paths_json="../SimCLR-release/feats/predict_paths.json",
                 device="cuda:0"):
        self.model = models.resnet50(pretrained=False)
        checkpoint = torch.load(checkpoint_path, "cpu")
        # self.model.fc = torch.nn.Linear(2048, checkpoint["state_dict"]["fc.weight"].shape[0])
        self.model.fc = torch.nn.Identity()
        self.model.load_state_dict(checkpoint["state_dict"], strict=False)
        self.model.to(device)
        self.model.eval()
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((128,128))])
        print(f"loading feature from {feat_path}")
        self.feats = torch.load(feat_path, map_location=device)
        print(self.feats.shape)
        self.pred_paths = json.load(open(paths_json, 'r'))
        self.device = device

    def classify(self, path):
        img = Image.open(path).convert("L")
        img = preprocess(img).convert("RGB")
        img.save(path)
        img = self.transform(img).to(self.device)
        target_feat = self.model(img.unsqueeze(0))
        dists = euclidean_dist(target_feat, self.feats).squeeze()
        _, indices = torch.sort(dists)
        result1 = [self.pred_paths[i] for i in indices.tolist()[:50]]
        dists = cosine_dist(target_feat, self.feats).squeeze()
        _, indices = torch.sort(dists)
        result2 = [self.pred_paths[i] for i in indices.tolist()[:50]]
        return result1, result2

config = json.load(open("config.json"))
root_dir = config["root_dir"]
model = OCRModel(checkpoint_path=root_dir+config["checkpoint"],
                 feat_path=root_dir+config["feat"],
                 paths_json=root_dir+config["paths"], device='cpu')

def classify(path):
    return model.classify(path)
