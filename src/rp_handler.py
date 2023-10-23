import os


import runpod
from runpod.serverless.utils import rp_download, rp_upload, rp_cleanup
from runpod.serverless.utils.rp_validator import validate
from inference_main import main

def run(job):
    wav_url = main(job)
    return wav_url

runpod.serverless.start({"handler": run})