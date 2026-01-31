#!/usr/bin/env python3
"""
가상환경 초기화 및 패키지 검증
- .venv 없으면 생성
- 패키지 설치 여부 확인 후 누락된 것만 설치
- GOOGLE_API_KEY 설정 확인 및 .env 파일 생성
"""

import subprocess
import sys
import os
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
VENV_DIR = SKILL_DIR / ".venv"
ENV_FILE = SKILL_DIR / ".env"

REQUIRED_PACKAGES = {
    "PyYAML": "yaml",
    "google-genai": "google.genai",
    "pillow": "PIL",
}

OPTIONAL_PACKAGES = {
    "cairosvg": "cairosvg",
}


def get_venv_python():
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def create_venv():
    if VENV_DIR.exists():
        return True
    print(f"가상환경 생성 중: {VENV_DIR}")
    result = subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], capture_output=True)
    return result.returncode == 0


def is_package_installed(import_name: str) -> bool:
    python = get_venv_python()
    if not python.exists():
        return False
    result = subprocess.run([str(python), "-c", f"import {import_name}"], capture_output=True)
    return result.returncode == 0


def install_packages(packages: list):
    if not packages:
        return True
    python = get_venv_python()
    cmd = [str(python), "-m", "pip", "install", "--quiet"] + packages
    print(f"패키지 설치 중: {', '.join(packages)}")
    return subprocess.run(cmd, capture_output=True).returncode == 0


def setup_api_key():
    """GOOGLE_API_KEY 설정 확인 및 .env 파일 생성"""
    # 1. 환경변수 확인
    api_key = os.environ.get("GOOGLE_API_KEY")

    # 2. .env 파일에서 확인
    if not api_key and ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    # 3. 키가 없으면 입력 요청
    if not api_key:
        print("\n" + "=" * 50)
        print("GOOGLE_API_KEY가 설정되지 않았습니다.")
        print("Gemini API 키를 입력하세요 (https://aistudio.google.com/apikey)")
        print("=" * 50)
        api_key = input("GOOGLE_API_KEY: ").strip()

        if api_key:
            # .env 파일에 저장
            with open(ENV_FILE, "w") as f:
                f.write(f'GOOGLE_API_KEY="{api_key}"\n')
            print(f"API 키가 {ENV_FILE}에 저장되었습니다.")

            # .gitignore에 .env 추가
            gitignore = SKILL_DIR / ".gitignore"
            if gitignore.exists():
                content = gitignore.read_text()
                if ".env" not in content:
                    with open(gitignore, "a") as f:
                        f.write("\n.env\n")
            else:
                gitignore.write_text(".env\n.venv/\n__pycache__/\n")
        else:
            print("API 키가 입력되지 않았습니다. 나중에 설정하세요.")
            return False

    return True


def ensure_environment():
    print("=" * 50)
    print("search-blogging 스킬 환경 초기화")
    print("=" * 50)

    # Step 1: venv 생성
    if not create_venv():
        print("가상환경 생성 실패")
        return False

    # Step 2: 패키지 확인 및 설치
    missing = [pkg for pkg, imp in REQUIRED_PACKAGES.items() if not is_package_installed(imp)]

    if missing:
        if not install_packages(missing):
            return False
    else:
        print("모든 필수 패키지 설치됨")

    # Step 3: API 키 설정
    setup_api_key()

    print("\n환경 준비 완료!")
    print(f"Python: {get_venv_python()}")
    return True


if __name__ == "__main__":
    sys.exit(0 if ensure_environment() else 1)
