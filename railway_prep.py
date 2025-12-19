import os
import re

print("🔍 Railway Discord Bot Auto-Prep Tool\n")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_FILE = "bot.py"
BOT_PATH = os.path.join(BASE_DIR, MAIN_FILE)

# Check bot file
if not os.path.exists(BOT_PATH):
    print("❌ bot.py not found in the same folder as railway_prep.py")
    exit()

print(f"✅ Bot file detected: {BOT_PATH}")

# Scan imports
imports = set()
with open(BOT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        match = re.match(r"(?:from|import)\s+([a-zA-Z0-9_]+)", line)
        if match:
            pkg = match.group(1)
            if pkg not in ["os", "sys", "asyncio", "time"]:
                imports.add(pkg)

# Write requirements.txt HERE
with open(os.path.join(BASE_DIR, "requirements.txt"), "w") as f:
    for pkg in sorted(imports):
        f.write(pkg + "\n")

print("✅ requirements.txt created")

# Write Procfile HERE
with open(os.path.join(BASE_DIR, "Procfile"), "w") as f:
    f.write("worker: python bot.py")

print("✅ Procfile created")

# .env example
if not os.path.exists(os.path.join(BASE_DIR, ".env.example")):
    with open(os.path.join(BASE_DIR, ".env.example"), "w") as f:
        f.write("DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE\n")
    print("✅ .env.example created")

print("\n🎉 Done!")
print("Commit this folder and deploy from Railway.")

