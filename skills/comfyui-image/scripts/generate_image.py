#!/usr/bin/env python3
"""
ComfyUI Image Generation Script

Usage:
    python generate_image.py --prompt "a beautiful sunset"
    python generate_image.py --host http://127.0.0.1:8188 --prompt "cat"
    python generate_image.py --create-env --host http://127.0.0.1:8188
"""

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional

import requests


def find_env_file() -> Optional[Path]:
    """Find .env file - check home directory only."""
    # Only check home directory
    home_env = Path.home() / ".env"
    if home_env.exists():
        return home_env
    return None


def load_comfyui_host(env_path: Optional[Path]) -> Optional[str]:
    if not env_path:
        return None
    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("COMFYUI_HOST="):
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


def check_comfyui_config() -> tuple[bool, Optional[str]]:
    env_path = find_env_file()
    if not env_path:
        return False, None
    host = load_comfyui_host(env_path)
    if not host or len(host) < 10:
        return False, None
    return True, host


def write_host_to_env(host: str) -> Path:
    """Write COMFYUI_HOST to .env file in home directory."""
    env_path = Path.home() / ".env"

    existing_lines: list[str] = []
    key_exists = False
    if env_path.exists():
        try:
            with open(env_path, "r") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("COMFYUI_HOST="):
                        existing_lines.append(f"COMFYUI_HOST={host}\n")
                        key_exists = True
                    else:
                        existing_lines.append(line)
        except Exception:
            existing_lines = []

    if not key_exists:
        existing_lines.append(f"COMFYUI_HOST={host}\n")

    with open(env_path, "w") as f:
        f.writelines(existing_lines)

    return env_path


def find_workflow_file(workflow_name: str | None) -> Path:
    """Find workflow JSON file."""
    script_dir = Path(__file__).parent.parent
    references_dir = script_dir / "references"

    if workflow_name:
        # Custom workflow path
        if Path(workflow_name).exists():
            return Path(workflow_name)
        # Check in references folder
        custom_path = references_dir / workflow_name
        if custom_path.exists():
            return custom_path
        # Try with .json extension
        custom_path = references_dir / f"{workflow_name}.json"
        if custom_path.exists():
            return custom_path

    # Default workflow
    default_workflow = references_dir / "zimage.json"
    if default_workflow.exists():
        return default_workflow

    raise FileNotFoundError(
        f"Workflow file not found: {workflow_name or 'zimage.json'}"
    )


def load_workflow(workflow_path: Path) -> dict:
    """Load workflow JSON from file."""
    with open(workflow_path, "r", encoding="utf-8") as f:
        return json.load(f)


def update_workflow(
    workflow: dict,
    prompt: str,
    width: int,
    height: int,
) -> dict:
    """Update workflow with user prompt and dimensions."""
    # Find the prompt node (CLIPTextEncode, node 6 for positive)
    # Find the empty latent node (node 5) for dimensions

    # Update positive prompt (node 6)
    if "6" in workflow and "inputs" in workflow["6"]:
        workflow["6"]["inputs"]["text"] = prompt

    # Update dimensions in EmptyLatentImage (node 5)
    if "5" in workflow and "inputs" in workflow["5"]:
        workflow["5"]["inputs"]["width"] = width
        workflow["5"]["inputs"]["height"] = height

    return workflow


def queue_prompt(host: str, workflow: dict) -> str | None:
    """Send workflow to ComfyUI /prompt endpoint. Returns prompt_id."""
    url = f"{host.rstrip('/')}/prompt"

    # ComfyUI expects: {"prompt": workflow_json}
    payload = {"prompt": workflow}

    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result.get("prompt_id")
        else:
            print(
                f"ERROR: Failed to queue prompt: {response.status_code} - {response.text[:200]}",
                file=sys.stderr,
            )
            return None
    except requests.exceptions.ConnectionError:
        print(
            "ERROR: CONNECTION_FAILED - Cannot connect to ComfyUI server. Please check if server is running.",
            file=sys.stderr,
        )
        return None
    except requests.exceptions.Timeout:
        print("ERROR: TIMEOUT - Request timed out", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: NETWORK_ERROR - {str(e)[:100]}", file=sys.stderr)
        return None


def get_prompt_status(host: str, prompt_id: str) -> dict | None:
    """Get prompt execution status."""
    url = f"{host.rstrip('/')}/prompt/{prompt_id}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def get_history(host: str, prompt_id: str) -> dict | None:
    """Get prompt execution history."""
    url = f"{host.rstrip('/')}/history/{prompt_id}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def download_image(
    host: str, filename: str, subfolder: str = "", image_type: str = "output"
) -> bytes | None:
    """Download image from ComfyUI."""
    params = {"filename": filename}
    if subfolder:
        params["subfolder"] = subfolder
    if image_type:
        params["type"] = image_type

    try:
        response = requests.get(f"{host.rstrip('/')}/view", params=params, timeout=60)
        if response.status_code == 200:
            return response.content
        return None
    except Exception:
        return None


def wait_for_completion(host: str, prompt_id: str, timeout: int = 120) -> bool:
    """Wait for prompt to complete execution."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Use /history endpoint to check status (more reliable for completed prompts)
        history = get_history(host, prompt_id)
        if history and prompt_id in history:
            prompt_data = history[prompt_id]
            status_info = prompt_data.get("status", {})
            if status_info.get("completed"):
                return True
            if status_info.get("err_msg"):
                print(
                    f"ERROR: Execution failed: {status_info.get('err_msg')}",
                    file=sys.stderr,
                )
                return False

        time.sleep(1)

    print("ERROR: TIMEOUT - Image generation timed out", file=sys.stderr)
    return False


def generate_image(
    prompt: str,
    width: int = 1024,
    height: int = 768,
    host: Optional[str] = None,
    workflow_name: str | None = None,
    output_path: Optional[str] = None,
) -> dict:
    # Check host configuration
    if not host:
        is_configured, host = check_comfyui_config()
        if not is_configured:
            return {
                "success": False,
                "error": "COMFYUI_NOT_CONFIGURED",
                "message": "COMFYUI_HOST 未配置. 请在 .env 文件中配置服务器地址或通过 --host 参数传入.",
            }

    # Load and update workflow
    try:
        workflow_path = find_workflow_file(workflow_name)
        workflow = load_workflow(workflow_path)
        workflow = update_workflow(workflow, prompt, width, height)
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": "WORKFLOW_ERROR",
            "message": str(e),
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": "WORKFLOW_ERROR",
            "message": f"Invalid JSON: {e}",
        }

    assert host is not None, "host should be validated above"
    comfyui_host = host

    print(
        f"[comfyui] generating: prompt={prompt}, size={width}x{height}, host={comfyui_host}"
    )

    # Queue the prompt
    prompt_id = queue_prompt(comfyui_host, workflow)
    if not prompt_id:
        return {
            "success": False,
            "error": "WORKFLOW_ERROR",
            "message": "Failed to queue prompt",
        }

    # Wait for completion
    if not wait_for_completion(comfyui_host, prompt_id):
        return {
            "success": False,
            "error": "EXECUTION_FAILED",
            "message": "Workflow execution failed or timed out",
        }

    # Get output images
    history = get_history(comfyui_host, prompt_id)
    if not history or prompt_id not in history:
        return {
            "success": False,
            "error": "EXECUTION_FAILED",
            "message": "Failed to get execution history",
        }

    prompt_history = history[prompt_id]
    outputs = prompt_history.get("outputs", {})

    # Find images from output nodes (PreviewImage node 15, SaveImage, etc.)
    image_list: list[dict] = []
    for node_id, node_data in outputs.items():
        if isinstance(node_data, dict):
            images = node_data.get("images")
            if images and isinstance(images, list):
                for img in images:
                    if isinstance(img, dict) and "filename" in img:
                        image_list.append(
                            {
                                "filename": img["filename"],
                                "subfolder": img.get("subfolder", ""),
                                "type": img.get("type", "output"),
                            }
                        )

    if not image_list:
        return {
            "success": False,
            "error": "EXECUTION_FAILED",
            "message": "No output images found",
        }

    # Download and save images
    saved_paths: list[str] = []

    if output_path:
        save_dir = Path(output_path)
    else:
        import tempfile

        save_dir = Path(tempfile.gettempdir()) / "comfyui"

    save_dir.mkdir(parents=True, exist_ok=True)

    for img_info in image_list:
        filename = img_info["filename"]
        subfolder = img_info.get("subfolder", "")
        image_type = img_info.get("type", "output")

        image_data = download_image(comfyui_host, filename, subfolder, image_type)
        if image_data:
            # Determine file extension
            ext = Path(filename).suffix or ".png"
            # Use original filename or create new one
            save_path = save_dir / filename
            # If file exists, add timestamp
            if save_path.exists():
                import datetime

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                stem = Path(filename).stem
                save_path = save_dir / f"{stem}_{timestamp}{ext}"

            with open(save_path, "wb") as f:
                f.write(image_data)
            saved_paths.append(str(save_path.absolute()))

    if not saved_paths:
        return {
            "success": False,
            "error": "EXECUTION_FAILED",
            "message": "Failed to download output images",
        }

    return {
        "success": True,
        "saved_paths": saved_paths,
        "prompt": prompt,
        "width": width,
        "height": height,
    }


def main():
    parser = argparse.ArgumentParser(
        description="ComfyUI 图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--prompt", "-p", help="图片描述")
    parser.add_argument(
        "--width", "-w", type=int, default=1024, help="图片宽度 (默认: 1024)"
    )
    parser.add_argument(
        "--height", "-H", type=int, default=768, help="图片高度 (默认: 768)"
    )
    parser.add_argument(
        "--host", help="ComfyUI 服务器地址 (例如 http://127.0.0.1:8188)"
    )
    parser.add_argument("--workflow", "-wf", help="工作流文件名 (默认: zimage.json)")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--create-env", action="store_true", help="创建 .env 文件")
    parser.add_argument(
        "--timeout", "-t", type=int, default=120, help="生成超时时间 (默认: 120秒)"
    )

    args = parser.parse_args()

    if args.create_env:
        if not args.host:
            print("ERROR: --create-env 需要 --host 参数", file=sys.stderr)
            sys.exit(1)
        env_path = write_host_to_env(args.host)
        print(f"DONE: .env updated at {env_path}")
        print(f"COMFYUI_HOST={args.host}")
        sys.exit(0)

    if not args.prompt:
        print("ERROR: --prompt is required", file=sys.stderr)
        sys.exit(1)

    result = generate_image(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        host=args.host,
        workflow_name=args.workflow,
        output_path=args.output,
    )

    if result["success"]:
        for i, path in enumerate(result["saved_paths"]):
            if len(result["saved_paths"]) > 1:
                print(f"SAVED_PATH_{i + 1}: {path}")
            else:
                print(f"SAVED_PATH: {path}")
        sys.exit(0)
    else:
        print(f"ERROR: {result['error']} - {result['message']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
