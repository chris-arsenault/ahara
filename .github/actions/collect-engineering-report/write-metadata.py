import hashlib
import json
import os
from pathlib import Path


config_path = Path(os.environ["QLTY_CONFIG"])
metadata = {
    "qlty_version": "0.641.0",
    "analyzer_digest": os.environ["QLTY_DIGEST"],
    "config_digest": f"sha256:{hashlib.sha256(config_path.read_bytes()).hexdigest()}",
    "generated_config": os.environ["GENERATED_CONFIG"] == "true",
    "status": os.environ["QLTY_STATUS"],
    "started_at": os.environ["QLTY_STARTED_AT"],
}

output = Path(".ahara-ci-report/quality/metadata.json")
output.write_text(json.dumps(metadata, indent=2) + "\n")
