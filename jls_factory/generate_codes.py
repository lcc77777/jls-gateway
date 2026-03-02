import json
import csv
import random
import string
import os
import base64

# 获取脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = os.path.join(BASE_DIR, 'model_list.json')
INVENTORY_CSV = os.path.join(BASE_DIR, 'inventory_import.csv')
MODELS_CSV = os.path.join(BASE_DIR, 'models_import.csv')
QR_DIR = os.path.join(BASE_DIR, 'qr_codes')

# 替换为你的真实 GitHub Pages 地址
BASE_URL = "https://lcc77777.github.io/jls-gateway/index.html" 

def generate_random_id(length=8):
    """生成随机激活码后缀"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def to_base64(text):
    """将文本转为 Base64"""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def main():
    if not os.path.exists(MANIFEST_FILE):
        print(f"Error: {MANIFEST_FILE} not found.")
        return

    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        models = json.load(f)

    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR)

    inventory_rows = []
    models_rows = []
    
    # 尝试导入 qrcode 库
    try:
        import qrcode
        has_qrcode = True
    except ImportError:
        print("Warning: qrcode library not found. Run 'pip install qrcode[pil]' to generate images.")
        has_qrcode = False

    print("--- JLS Industrialization Suite v1.1 ---")

    # 1. 准备型号注册数据 (models_registry)
    for model in models:
        models_rows.append({
            "model_id": model['model_id'],
            "name": model['name'],
            "category": model['category'],
            "lisp_code": to_base64(model['lisp_code']),
            "initial_fuel": model.get('initial_fuel', 1000)
        })

        # 2. 为每个型号生成激活码 (logic_inventory)
        # 规范: JLS-[ShortCode]-[Random]
        # 示例: JLS-K01-ABCD-1234
        short_code_part = model['short_code'] # 如 JLS-K01
        
        count = model.get('quantity', 10)
        print(f"Producing {count} units for {model['name']} [{model['model_id']}]...")
        
        for _ in range(count):
            random_part = generate_random_id(8)
            code = f"{short_code_part}-{random_part[:4]}-{random_part[4:]}"
            
            inventory_rows.append({
                "id": code,
                "model_id": model['model_id'],
                "is_active": False,
                "user_id": ""
            })

            if has_qrcode:
                qr_url = f"{BASE_URL}?code={code}"
                img = qrcode.make(qr_url)
                img_name = f"{code}.png"
                img.save(os.path.join(QR_DIR, img_name))

    # 导出 Models CSV
    with open(MODELS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["model_id", "name", "category", "lisp_code", "initial_fuel"])
        writer.writeheader()
        writer.writerows(models_rows)

    # 导出 Inventory CSV
    with open(INVENTORY_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "model_id", "is_active", "user_id"])
        writer.writeheader()
        writer.writerows(inventory_rows)

    print(f"\n[ASSET_PIPELINE_COMPLETE]")
    print(f">> Registry: {MODELS_CSV}")
    print(f">> Inventory: {INVENTORY_CSV}")
    if has_qrcode:
        print(f">> QR Graphics: {len(inventory_rows)} files generated in {QR_DIR}/")

if __name__ == "__main__":
    main()
