import json

with open("backup.json", "r", encoding="utf-8") as f:
    data = json.load(f)

clean = []

skip_models = {
    "accounts.userprofile",
}

for obj in data:
    model = obj.get("model", "")
    if model.startswith("accounts.") and model not in skip_models:
        clean.append(obj)

with open("accounts_only_v2.json", "w", encoding="utf-8") as f:
    json.dump(clean, f, indent=2)

print("Saved", len(clean), "objects")