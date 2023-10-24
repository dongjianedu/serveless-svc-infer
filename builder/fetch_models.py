from huggingface_hub import hf_hub_download
import joblib

REPO_ID = "deejac/zhanyin"
FILENAME = "model"
hf_hub_download(repo_id=REPO_ID, filename=FILENAME,local_dir="./",repo_type="model")

FILENAME = "G_125600.pth"
hf_hub_download(repo_id=REPO_ID, filename=FILENAME,local_dir="./",repo_type="model")

FILENAME = "checkpoint_best_legacy_500.pt"
hf_hub_download(repo_id=REPO_ID, filename=FILENAME,local_dir="./",repo_type="model")

FILENAME = "rmvpe.pt"
hf_hub_download(repo_id=REPO_ID, filename=FILENAME,local_dir="./",repo_type="model")



