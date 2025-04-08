import os

structure = {
    "app": {
        "models": ["__init__.py", "user.py", "campaign.py", "transaction.py"],
        "routes": ["__init__.py", "auth_routes.py", "koc_routes.py", "campaign_routes.py"],
        "services": ["affiliate_service.py"],
        "templates": ["base.html", "dashboard.html"],
        "static": {
            "css": [],
            "js": [],
            "images": []
        },
        "forms": ["login_form.py"],
        "utils": ["email.py", "token.py"],
        "__init__.py": ""
    },
    ".": ["config.py", "run.py", "requirements.txt", "README.md"]
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, list):  # Create files in a folder
            os.makedirs(path, exist_ok=True)
            for file in content:
                open(os.path.join(path, file), "w").close()
        elif isinstance(content, dict):  # Nested folder
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, str):  # Single file in current directory
            open(os.path.join(base_path, name), "w").close()

if __name__ == "__main__":
    current_dir = os.getcwd()
    create_structure(current_dir, structure)
    print("✅ Cấu trúc thư mục Flask đã được tạo ngay trong thư mục hiện tại.")
