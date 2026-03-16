#!/usr/bin/env python3
"""
Pollinations.ai Image Generation Script

Usage:
    python generate_image.py --prompt "a beautiful sunset" --model zimage --width 1024 --height 768
    POLLINATIONS_API_KEY=your_key python generate_image.py --prompt "cat"
    python generate_image.py --create-env --api-key YOUR_KEY
"""

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Optional

import requests


def find_env_file() -> Optional[Path]:
    home_env = Path.home() / ".env"
    if home_env.exists():
        return home_env
    return None


def load_api_key(env_path: Optional[Path]) -> Optional[str]:
    if not env_path:
        return None
    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("POLLINATIONS_API_KEY="):
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


def check_api_key() -> tuple[bool, Optional[str]]:
    env_path = find_env_file()
    if not env_path:
        return False, None
    api_key = load_api_key(env_path)
    if not api_key or len(api_key) < 10:
        return False, None
    return True, api_key


def write_api_key_to_env(api_key: str) -> Path:
    env_path = Path.home() / ".env"

    existing_lines: list[str] = []
    key_exists = False
    if env_path.exists():
        try:
            with open(env_path, "r") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("POLLINATIONS_API_KEY="):
                        existing_lines.append(f"POLLINATIONS_API_KEY={api_key}\n")
                        key_exists = True
                    else:
                        existing_lines.append(line)
        except Exception:
            existing_lines = []

    if not key_exists:
        existing_lines.append(f"POLLINATIONS_API_KEY={api_key}\n")

    with open(env_path, "w") as f:
        f.writelines(existing_lines)

    return env_path


def generate_image(
    prompt: str,
    model: str = "zimage",
    width: int = 1024,
    height: int = 768,
    api_key: Optional[str] = None,
    seed: int = -1,
    enhance: bool = False,
    negative_prompt: str = "worst quality, blurry",
    output_path: Optional[str] = None,
) -> dict:
    if not api_key:
        is_configured, api_key = check_api_key()
        if not is_configured:
            return {
                "success": False,
                "error": "API_KEY_NOT_CONFIGURED",
                "message": "POLLINATIONS_API_KEY 未配置. 请在 .env 文件中配置 API_KEY 或通过 --api-key 参数传入.",
            }

    base_url = "https://gen.pollinations.ai/image"
    encoded_prompt = urllib.parse.quote(prompt)

    params = {
        "model": model,
        "width": width,
        "height": height,
        "seed": seed,
        "enhance": str(enhance).lower(),
        "negative_prompt": negative_prompt,
        "key": api_key,
    }

    url = f"{base_url}/{encoded_prompt}"

    print(
        f"[pollinations] generating: prompt={prompt}, model={model}, size={width}x{height}"
    )

    try:
        response = requests.get(url, params=params, timeout=60, allow_redirects=True)

        if response.status_code == 401:
            return {
                "success": False,
                "error": "AUTH_FAILED",
                "message": "API 认证失败. 请检查 API_KEY 是否正确.",
            }

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"API_ERROR_{response.status_code}",
                "message": response.text[:200],
            }

        content_type = response.headers.get("content-type", "")
        if "image" in content_type:
            image_data = response.content
            if output_path:
                save_path = Path(output_path)
            else:
                import tempfile

                save_dir = Path(tempfile.gettempdir()) / "pollinations"
                save_dir.mkdir(parents=True, exist_ok=True)
                safe_prompt = "".join(
                    c for c in prompt[:20] if c.isalnum() or c in " -_"
                ).strip()
                save_path = (
                    save_dir / f"{safe_prompt}_{seed if seed > 0 else 'random'}.png"
                )

            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(image_data)

            return {
                "success": True,
                "image_url": str(save_path.absolute()),
                "saved_path": str(save_path),
                "prompt": prompt,
                "model": model,
                "width": width,
                "height": height,
            }
        else:
            if response.url:
                image_url = response.url
            else:
                content = response.text
                if "image_url" in content:
                    data = json.loads(content)
                    image_url = data.get("image_url", url)
                else:
                    image_url = url

            if "seed" not in image_url and "pollinations" in image_url:
                separator = "&" if "?" in image_url else "?"
                image_url = (
                    f"{image_url}{separator}seed={seed if seed > 0 else 'random'}"
                )

            return {
                "success": True,
                "image_url": image_url,
                "prompt": prompt,
                "model": model,
                "width": width,
                "height": height,
            }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "TIMEOUT", "message": "请求超时"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "NETWORK_ERROR", "message": str(e)[:100]}


def main():
    parser = argparse.ArgumentParser(
        description="Pollinations.ai 图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--prompt", "-p", help="图片描述")
    parser.add_argument(
        "--model",
        "-m",
        default="zimage",
        choices=[
            "zimage",
            "flux",
            "turbo",
            "gptimage",
            "seedream",
            "nanobanana",
            "nanobanana-pro",
        ],
    )
    parser.add_argument("--width", "-w", type=int, default=1024)
    parser.add_argument("--height", "-H", type=int, default=768)
    parser.add_argument("--seed", "-s", type=int, default=-1)
    parser.add_argument("--enhance", "-e", action="store_true")
    parser.add_argument("--api-key", help="API Key")
    parser.add_argument("--create-env", action="store_true", help="创建 .env 文件")

    args = parser.parse_args()

    if args.create_env:
        if not args.api_key:
            print("ERROR: --create-env 需要 --api-key 参数")
            sys.exit(1)
        env_path = write_api_key_to_env(args.api_key)
        print(f"DONE: .env updated at {env_path}")
        sys.exit(0)

    if not args.prompt:
        print("ERROR: --prompt is required")
        sys.exit(1)

    api_key = args.api_key

    result = generate_image(
        prompt=args.prompt,
        model=args.model,
        width=args.width,
        height=args.height,
        api_key=api_key,
        seed=args.seed,
        enhance=args.enhance,
    )

    if result["success"]:
        print(f"IMAGE_URL: {result['image_url']}")
        sys.exit(0)
    else:
        print(f"ERROR: {result['error']} - {result['message']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
