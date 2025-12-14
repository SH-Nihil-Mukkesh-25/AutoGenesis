import os

print(f"CWD: {os.getcwd()}")
if os.path.exists(".env"):
    print(f".env exists, size {os.path.getsize('.env')}")
    try:
        with open(".env", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                clean = line.strip()
                if not clean or clean.startswith("#"):
                    continue
                if "=" in clean:
                    key, val = clean.split("=", 1)
                    val_preview = val[:4] + "..." if len(val) > 4 else val
                    print(f"Line {i+1}: {key} = {val_preview}")
                else:
                    print(f"Line {i+1}: [BAD FORMAT] {clean}")
    except Exception as e:
        print(f"Error reading .env: {e}")
else:
    print(".env NOT FOUND in " + os.getcwd())
