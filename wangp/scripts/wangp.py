#!/usr/bin/env python3
"""
Wan2GP CLI - AI agent interface for Wan2GP image/video generation.

Usage:
    wangp.py detect
    wangp.py list [--family F] [--type T] [--available]
    wangp.py defaults <model_type>
    wangp.py schema <model_type>
    wangp.py generate --model <type> --prompt "..." [--resolution R] [--steps N] [--seed N] [--frames N] [--image PATH] [--negative TEXT] [--output-dir DIR] [--guidance-scale F] [--batch-size N]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def find_wan2gp_root() -> Path | None:
    """Discover the most mature Wan2GP installation across all drives."""
    candidates = _collect_wan2gp_candidates()
    if not candidates:
        return None

    # Score each candidate and return the best
    scored = []
    for p in candidates:
        score = _score_wan2gp_install(p)
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def _collect_wan2gp_candidates() -> list[Path]:
    """Find all Wan2GP app directories across the system."""
    found = set()
    candidates = []

    def _add(p: Path):
        try:
            resolved = p.resolve()
            if resolved not in found and (resolved / "shared" / "api.py").exists():
                found.add(resolved)
                candidates.append(resolved)
        except (OSError, PermissionError):
            pass

    # 1. Explicit env var
    env_root = os.environ.get("WAN2GP_ROOT")
    if env_root:
        p = Path(env_root)
        _add(p)
        _add(p / "app")

    # 2. Script ancestor walk
    script_dir = Path(__file__).resolve().parent
    for ancestor in [script_dir, *script_dir.parents]:
        _add(ancestor / "app")

    # 3. Pinokio home env
    pinokio_home = os.environ.get("PINOKIO_HOME")
    if pinokio_home:
        _add(Path(pinokio_home) / "api" / "wan.git" / "app")
        _add(Path(pinokio_home) / "api" / "wan2gp" / "app")

    # 4. Default Pinokio location
    _add(Path.home() / ".pinokio" / "api" / "wan.git" / "app")
    _add(Path.home() / ".pinokio" / "api" / "wan2gp" / "app")

    # 5. Scan all mount points / drives for Pinokio-style installs
    _scan_mount_points(candidates, found)

    # 6. Common manual install locations
    for base in [Path.home(), Path("/opt"), Path("/usr/local")]:
        _add(base / "Wan2GP" / "app")
        _add(base / "wan2gp" / "app")
        _add(base / "Wan2GP")
        _add(base / "wan2gp")

    return candidates


def _scan_mount_points(candidates: list[Path], found: set):
    """Scan mounted drives for Pinokio api directories."""
    import subprocess as _sp

    # Get mount points
    mounts = set()
    try:
        r = _sp.run(["mount"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[1] == "on":
                    mount = parts[2]
                    if mount.startswith("/") and mount not in ("/", "/proc", "/sys", "/dev", "/run"):
                        mounts.add(Path(mount))
    except Exception:
        pass

    # Also check common drive locations
    for d in ["/data", "/mnt", "/media", "/home", "/opt", "/srv"]:
        p = Path(d)
        if p.exists():
            mounts.add(p)

    # Check user's home on each mount
    home_name = Path.home().name
    for mount in mounts:
        # Pinokio api dirs on this mount
        for pattern in [
            mount / "pinokio" / "api" / "wan.git" / "app",
            mount / "pinokio" / "api" / "wan2gp" / "app",
            mount / ".pinokio" / "api" / "wan.git" / "app",
            mount / ".pinokio" / "api" / "wan2gp" / "app",
            mount / home_name / ".pinokio" / "api" / "wan.git" / "app",
            mount / home_name / ".pinokio" / "api" / "wan2gp" / "app",
            mount / home_name / "Wan2GP" / "app",
            mount / home_name / "wan2gp" / "app",
        ]:
            try:
                resolved = pattern.resolve()
                if resolved not in found and (resolved / "shared" / "api.py").exists():
                    found.add(resolved)
                    candidates.append(resolved)
            except (OSError, PermissionError):
                pass


def _score_wan2gp_install(app_dir: Path) -> int:
    """Score a Wan2GP installation by maturity. Higher = more mature."""
    score = 0
    parent = app_dir.parent

    # Has working Python venv
    for venv in ["env", "venv", ".venv"]:
        venv_python = app_dir / venv / "bin" / "python"
        if venv_python.exists():
            score += 50
            break

    # Has wgp_config.json (has been configured/used)
    if (app_dir / "wgp_config.json").exists():
        score += 20

    # Has downloaded models (checkpoints)
    ckpt_dir = parent / "checkpoints"
    if ckpt_dir.exists():
        model_count = sum(1 for _ in ckpt_dir.rglob("*.safetensors"))
        score += min(model_count * 5, 100)  # up to 100 points for models

    # Has outputs (has been actively used)
    output_dir = app_dir / "outputs"
    if output_dir.exists():
        file_count = sum(1 for _ in output_dir.iterdir() if _.is_file())
        score += min(file_count * 2, 50)  # up to 50 points for outputs

    # Version check
    wgp_file = app_dir / "wgp.py"
    if wgp_file.exists():
        try:
            content = wgp_file.read_text()
            import re
            m = re.search(r'WanGP_version\s*=\s*"([^"]+)"', content)
            if m:
                version = m.group(1)
                # Parse version as float for comparison
                try:
                    score += int(float(version) * 10)
                except ValueError:
                    pass
        except Exception:
            pass

    # Is a git repo (can be updated)
    if (parent / ".git").exists():
        score += 10

    return score


def find_wan2gp_python(wan2gp_root: Path) -> str | None:
    """Find the Python executable in Wan2GP's venv."""
    candidates = [
        wan2gp_root / "env" / "bin" / "python",
        wan2gp_root / "venv" / "bin" / "python",
        wan2gp_root / ".venv" / "bin" / "python",
        wan2gp_root / "env" / "Scripts" / "python.exe",
        wan2gp_root / "venv" / "Scripts" / "python.exe",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def _in_wan2gp_env() -> bool:
    """Check if we're already running in Wan2GP's Python env (has diffusers)."""
    try:
        import diffusers  # noqa: F401
        return True
    except ImportError:
        return False


def ensure_wan2gp_on_path(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def detect_hardware(wan2gp_root: Path) -> dict:
    """Detect hardware and recommend settings."""
    ensure_wan2gp_on_path(wan2gp_root)

    import setup

    gpu_name, vendor = setup.get_gpu_info()
    profile_key = setup.get_profile_key(gpu_name, vendor)
    ram_gb, vram_gb = setup.get_system_specs()

    has_high_ram = ram_gb > 60
    has_mid_ram = ram_gb > 30
    has_huge_vram = vram_gb > 22
    has_high_vram = vram_gb > 11

    if has_high_ram and has_huge_vram:
        profile = 1
    elif has_high_ram:
        profile = 2
    elif has_mid_ram and has_huge_vram:
        profile = 3
    elif has_mid_ram and has_high_vram:
        profile = 4
    else:
        profile = 5

    if "50" in profile_key or "40" in profile_key or "30" in profile_key:
        attention = "sage2"
    elif "20" in profile_key:
        attention = "sage"
    else:
        attention = "sdpa"

    suitable = []
    if vram_gb >= 24:
        suitable = ["14B bf16", "22B int8", "all image models", "all architectures"]
    elif vram_gb >= 16:
        suitable = ["14B int8", "7B bf16", "most image models"]
    elif vram_gb >= 12:
        suitable = ["7B int8", "1.3B bf16", "GGUF models", "small image models"]
    elif vram_gb >= 8:
        suitable = ["1.3B int8", "GGUF Q4", "small image models"]
    else:
        suitable = ["GGUF Q4 only", "smallest models only"]

    return {
        "wan2gp_root": str(wan2gp_root),
        "gpu": gpu_name,
        "vendor": vendor,
        "profile_key": profile_key,
        "ram_gb": round(ram_gb, 1),
        "vram_gb": round(vram_gb, 1),
        "platform": sys.platform,
        "profile": profile,
        "attention": attention,
        "suitable_for": suitable,
    }


def cmd_detect(args, wan2gp_root: Path) -> None:
    result = detect_hardware(wan2gp_root)
    wgp_python = find_wan2gp_python(wan2gp_root)
    result["python"] = wgp_python
    result["python_env_ok"] = _in_wan2gp_env()

    version_info = get_wan2gp_version(wan2gp_root)
    result["wan2gp_version"] = version_info.get("version")
    result["wan2gp_update_available"] = version_info.get("update_available", False)
    result["wan2gp_latest_version"] = version_info.get("latest_version")

    # Show all found installations
    all_candidates = _collect_wan2gp_candidates()
    if len(all_candidates) > 1:
        installs = []
        for p in all_candidates:
            score = _score_wan2gp_install(p)
            ver = get_wan2gp_version(p).get("version", "unknown")
            installs.append({"path": str(p), "version": ver, "score": score, "selected": p == wan2gp_root})
        installs.sort(key=lambda x: x["score"], reverse=True)
        result["all_installations"] = installs

    print(json.dumps(result, indent=2))


def get_wan2gp_version(wan2gp_root: Path) -> dict:
    """Check Wan2GP version and if an update is available."""
    info = {"version": None, "update_available": False, "latest_version": None}

    # Get current version from wgp.py
    wgp_file = wan2gp_root / "wgp.py"
    if wgp_file.exists():
        try:
            content = wgp_file.read_text()
            import re
            m = re.search(r'WanGP_version\s*=\s*"([^"]+)"', content)
            if m:
                info["version"] = m.group(1)
        except Exception:
            pass

    # Check for git updates
    git_dir = wan2gp_root.parent / ".git"
    if git_dir.exists():
        try:
            # Fetch latest
            r = subprocess.run(
                ["git", "fetch", "--quiet"],
                cwd=str(wan2gp_root.parent),
                capture_output=True, timeout=15
            )
            if r.returncode == 0:
                # Compare local vs remote
                local = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=str(wan2gp_root.parent),
                    capture_output=True, text=True, timeout=5
                )
                remote = subprocess.run(
                    ["git", "rev-parse", "origin/main"],
                    cwd=str(wan2gp_root.parent),
                    capture_output=True, text=True, timeout=5
                )
                if local.returncode == 0 and remote.returncode == 0:
                    if local.stdout.strip() != remote.stdout.strip():
                        info["update_available"] = True
                        # Get latest version from remote wgp.py
                        try:
                            remote_content = subprocess.run(
                                ["git", "show", "origin/main:app/wgp.py"],
                                cwd=str(wan2gp_root.parent),
                                capture_output=True, text=True, timeout=5
                            )
                            if remote_content.returncode == 0:
                                import re
                                m = re.search(r'WanGP_version\s*=\s*"([^"]+)"', remote_content.stdout)
                                if m:
                                    info["latest_version"] = m.group(1)
                        except Exception:
                            pass
        except Exception:
            pass

    return info


def cmd_update(wan2gp_root: Path) -> None:
    """Pull latest Wan2GP updates via git."""
    repo_dir = wan2gp_root.parent
    git_dir = repo_dir / ".git"

    if not git_dir.exists():
        print(json.dumps({"error": "Not a git repository. Update manually or reinstall via Pinokio."}))
        return

    print("Checking for Wan2GP updates...", file=sys.stderr)

    # Fetch
    r = subprocess.run(["git", "fetch"], cwd=str(repo_dir), capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        print(json.dumps({"error": f"git fetch failed: {r.stderr.strip()}"}))
        return

    # Check diff
    local = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo_dir), capture_output=True, text=True, timeout=5)
    remote = subprocess.run(["git", "rev-parse", "origin/main"], cwd=str(repo_dir), capture_output=True, text=True, timeout=5)

    if local.stdout.strip() == remote.stdout.strip():
        print(json.dumps({"status": "up_to_date", "message": "Wan2GP is already up to date."}))
        return

    # Pull
    print("Updating Wan2GP...", file=sys.stderr)
    r = subprocess.run(["git", "pull"], cwd=str(repo_dir), capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        print(json.dumps({"status": "updated", "message": "Wan2GP updated successfully.", "output": r.stdout.strip()}))
    else:
        print(json.dumps({"error": f"git pull failed: {r.stderr.strip()}"}))


def cmd_list(args, wan2gp_root: Path) -> None:
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        from shared.api import init
        session = init(root=wan2gp_root, console_output=False)
    finally:
        sys.stdout = old_stdout

    filters = {}
    if args.family:
        filters["family"] = args.family
    if args.type:
        filters["model_type"] = args.type

    models = session.list_model_metadata(include_availability=args.available, **filters)
    print(json.dumps(models, indent=2))


def cmd_defaults(args, wan2gp_root: Path) -> None:
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        from shared.api import init
        session = init(root=wan2gp_root, console_output=False)
    finally:
        sys.stdout = old_stdout

    try:
        settings = session.get_default_settings(args.model_type)
        print(json.dumps(settings, indent=2))
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def cmd_schema(args, wan2gp_root: Path) -> None:
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        from shared.api import init
        session = init(root=wan2gp_root, console_output=False)
    finally:
        sys.stdout = old_stdout

    schema = session.get_model_schema(args.model_type)
    if schema is None:
        print(json.dumps({"error": f"Unknown model_type: {args.model_type}"}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(schema, indent=2))


def cmd_generate(args, wan2gp_root: Path) -> None:
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        from shared.api import init

        cli_args = []
        if args.attention:
            cli_args.extend(["--attention", args.attention])
        if args.profile:
            cli_args.extend(["--profile", str(args.profile)])

        session = init(root=wan2gp_root, cli_args=cli_args, console_output=False)
    finally:
        sys.stdout = old_stdout

    try:
        defaults = session.get_default_settings(args.model)
    except ValueError:
        print(json.dumps({"error": f"Unknown model: {args.model}. Use 'list' to see available models."}), file=sys.stderr)
        sys.exit(1)

    settings = defaults.copy()
    settings["model_type"] = args.model
    settings["prompt"] = args.prompt

    if args.resolution:
        settings["resolution"] = args.resolution
    if args.steps:
        settings["num_inference_steps"] = args.steps
    if args.seed is not None:
        settings["seed"] = args.seed
    if args.frames:
        settings["video_length"] = args.frames
    if args.image:
        settings["image_start"] = str(Path(args.image).resolve())
    if args.negative:
        settings["negative_prompt"] = args.negative
    if args.guidance_scale:
        settings["guidance_scale"] = args.guidance_scale
    if args.batch_size:
        settings["batch_size"] = args.batch_size
    if args.output_dir:
        settings["_api"] = {"output_dir": str(Path(args.output_dir).resolve())}

    if args.upscale:
        settings["spatial_upsampling"] = args.upscale

    if args.return_media:
        settings.setdefault("_api", {})["return_media"] = True

    import sys as _sys
    print("Starting generation...", file=_sys.stderr)
    print(f"  Model: {args.model}", file=_sys.stderr)
    print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}", file=_sys.stderr)

    job = session.submit_task(settings)

    for event in job.events.iter(timeout=0.5):
        if event.kind == "progress":
            d = event.data
            step_info = ""
            if d.current_step is not None and d.total_steps is not None:
                step_info = f" [{d.current_step}/{d.total_steps}]"
            print(f"  [{d.phase}] {d.status}{step_info}", file=_sys.stderr)
        elif event.kind == "completed":
            break

    result = job.result(timeout=300)

    output = {
        "success": result.success,
        "generated_files": list(result.generated_files),
        "total_tasks": result.total_tasks,
        "successful_tasks": result.successful_tasks,
        "failed_tasks": result.failed_tasks,
    }

    if result.errors:
        output["errors"] = [{"message": str(e), "stage": e.stage} for e in result.errors]

    print(json.dumps(output, indent=2))

    if args.show and result.success and result.generated_files:
        for f in result.generated_files:
            display_result = display_image(f)
            if not display_result.get("ok"):
                print(json.dumps({"display": display_result}), file=sys.stderr)

    if not result.success:
        sys.exit(1)


def display_image(path: str) -> dict:
    """Display an image using the best available method. Returns status dict."""
    import subprocess as _sp
    from pathlib import Path as _Path

    p = _Path(path)
    if not p.exists():
        return {"ok": False, "error": f"File not found: {path}", "method": None}

    ext = p.suffix.lower()
    is_video = ext in (".mp4", ".webm", ".mkv", ".avi", ".mov")
    is_image = ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff")

    if not is_image and not is_video:
        return {"ok": False, "error": f"Unsupported format: {ext}", "method": None}

    # Method 1: Try viu (fast Rust terminal image viewer)
    try:
        r = _sp.run(["viu", str(p)], capture_output=True, timeout=10)
        if r.returncode == 0:
            return {"ok": True, "method": "viu", "path": str(p)}
    except (FileNotFoundError, _sp.TimeoutExpired):
        pass

    # Method 2: Try chafa (versatile terminal image viewer)
    try:
        r = _sp.run(["chafa", "--size=80x40", str(p)], capture_output=True, timeout=10)
        if r.returncode == 0:
            # chafa outputs to stdout, print it
            sys.stdout.write(r.stdout.decode("utf-8", errors="replace"))
            return {"ok": True, "method": "chafa", "path": str(p)}
    except (FileNotFoundError, _sp.TimeoutExpired):
        pass

    # Method 3: Try timg
    try:
        r = _sp.run(["timg", str(p)], capture_output=True, timeout=10)
        if r.returncode == 0:
            sys.stdout.write(r.stdout.decode("utf-8", errors="replace"))
            return {"ok": True, "method": "timg", "path": str(p)}
    except (FileNotFoundError, _sp.TimeoutExpired):
        pass

    # Method 4: iTerm2 inline image protocol
    if os.environ.get("TERM_PROGRAM") == "iTerm.app":
        import base64
        data = p.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        # iTerm2 inline image escape sequence
        sys.stdout.write(f"\033]1337;File=name={p.name};size={len(data)};inline=1:{b64}\a\n")
        sys.stdout.flush()
        return {"ok": True, "method": "iterm2-inline", "path": str(p)}

    # Method 5: Kitty graphics protocol
    if os.environ.get("KITTY_WINDOW_ID"):
        import base64
        data = p.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        # Chunk the data for Kitty protocol (max 4096 bytes per chunk)
        chunk_size = 4096
        chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]
        for i, chunk in enumerate(chunks):
            m = 1 if i < len(chunks) - 1 else 0  # m=0 for last chunk
            sys.stdout.write(f"\033_Ga=T,f=100,m={m};{chunk}\033\\")
        sys.stdout.write("\n")
        sys.stdout.flush()
        return {"ok": True, "method": "kitty-inline", "path": str(p)}

    # Method 6: Sixel (many terminals support this)
    try:
        r = _sp.run(["img2sixel", str(p)], capture_output=True, timeout=10)
        if r.returncode == 0:
            sys.stdout.buffer.write(r.stdout)
            sys.stdout.flush()
            return {"ok": True, "method": "sixel", "path": str(p)}
    except (FileNotFoundError, _sp.TimeoutExpired):
        pass

    # Method 7: PIL show (opens in default OS image viewer)
    try:
        from PIL import Image
        img = Image.open(str(p))
        img.show()
        return {"ok": True, "method": "pil-show", "path": str(p), "note": "Opened in default image viewer"}
    except Exception as e:
        return {"ok": False, "error": str(e), "method": None}


def cmd_show(args, _wan2gp_root=None) -> None:
    result = display_image(args.path)
    print(json.dumps(result, indent=2))


def cmd_upscale(args, wan2gp_root: Path) -> None:
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        from shared.api import init
        session = init(root=wan2gp_root, console_output=False)
    finally:
        sys.stdout = old_stdout

    source = str(Path(args.path).resolve())
    print(f"Upscaling {source}...", file=sys.stderr)
    print(f"  Method: {args.method}", file=sys.stderr)

    kwargs = {"spatial_upsampling": args.method}
    if args.output_dir:
        kwargs["output_dir"] = str(Path(args.output_dir).resolve())

    job = session.submit_media_postprocessing(source, **kwargs)

    for event in job.events.iter(timeout=0.5):
        if event.kind == "progress":
            d = event.data
            print(f"  [{d.phase}] {d.status}", file=sys.stderr)
        elif event.kind == "completed":
            break

    result = job.result(timeout=300)

    output = {
        "success": result.success,
        "generated_files": list(result.generated_files),
        "total_tasks": result.total_tasks,
        "successful_tasks": result.successful_tasks,
        "failed_tasks": result.failed_tasks,
    }

    if result.errors:
        output["errors"] = [{"message": str(e), "stage": e.stage} for e in result.errors]

    print(json.dumps(output, indent=2))

    if args.show and result.success and result.generated_files:
        for f in result.generated_files:
            display_result = display_image(f)
            if not display_result.get("ok"):
                print(json.dumps({"display": display_result}), file=sys.stderr)

    if not result.success:
        sys.exit(1)


def main(argv: list[str] | None = None) -> int:
    # Auto-detect Wan2GP venv and re-exec if needed
    if not _in_wan2gp_env():
        wan2gp_root = find_wan2gp_root()
        if wan2gp_root is not None:
            wgp_python = find_wan2gp_python(wan2gp_root)
            if wgp_python is not None and wgp_python != sys.executable:
                result = subprocess.run(
                    [wgp_python, str(Path(__file__).resolve())] + (argv or sys.argv[1:]),
                    capture_output=False,
                )
                raise SystemExit(result.returncode)

    parser = argparse.ArgumentParser(
        prog="wangp",
        description="Wan2GP CLI - Generate images and videos with local AI models",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("detect", help="Detect hardware and recommend settings")

    list_p = subparsers.add_parser("list", help="List available models")
    list_p.add_argument("--family", help="Filter by model family")
    list_p.add_argument("--type", help="Filter by model type")
    list_p.add_argument("--available", action="store_true", help="Include download availability")

    defaults_p = subparsers.add_parser("defaults", help="Get default settings for a model")
    defaults_p.add_argument("model_type", help="Model type identifier")

    schema_p = subparsers.add_parser("schema", help="Get full model schema")
    schema_p.add_argument("model_type", help="Model type identifier")

    gen_p = subparsers.add_parser("generate", help="Generate image or video")
    gen_p.add_argument("--model", required=True, help="Model type (e.g. flux, t2v, ltx2_22B_distilled)")
    gen_p.add_argument("--prompt", required=True, help="Generation prompt")
    gen_p.add_argument("--resolution", help="Output resolution (e.g. 1280x720)")
    gen_p.add_argument("--steps", type=int, help="Number of inference steps")
    gen_p.add_argument("--seed", type=int, default=-1, help="Random seed (-1 for random)")
    gen_p.add_argument("--frames", type=int, help="Video frame count (video models)")
    gen_p.add_argument("--image", help="Start image path (image-to-video/image-to-image)")
    gen_p.add_argument("--negative", help="Negative prompt")
    gen_p.add_argument("--guidance-scale", type=float, help="Guidance scale")
    gen_p.add_argument("--batch-size", type=int, help="Batch size")
    gen_p.add_argument("--output-dir", help="Output directory")
    gen_p.add_argument("--attention", help="Attention mode override (sdpa, sage, sage2, flash)")
    gen_p.add_argument("--profile", type=int, choices=[1, 2, 3, 4, 5], help="Performance profile override")
    gen_p.add_argument("--return-media", action="store_true", help="Return media in-memory")
    gen_p.add_argument("--show", action="store_true", help="Display image after generation")
    gen_p.add_argument("--upscale", help="Spatial upsampling method (e.g. lanczos2, flashvsr2, coz4, flux_pid4, vae2)")

    show_p = subparsers.add_parser("show", help="Display an image or video file")
    show_p.add_argument("path", help="Path to image/video file to display")

    upscale_p = subparsers.add_parser("upscale", help="Upscale an existing image or video")
    upscale_p.add_argument("path", help="Path to image or video to upscale")
    upscale_p.add_argument("--method", default="lanczos2", help="Upscaling method (default: lanczos2). Options: lanczos{2-4}, flashvsr{2-4}, coz{2,4,8,16}, flux_pid4, vae2")
    upscale_p.add_argument("--output-dir", help="Output directory")
    upscale_p.add_argument("--show", action="store_true", help="Display result after upscaling")

    subparsers.add_parser("update", help="Check for and apply Wan2GP updates")

    args = parser.parse_args(argv)

    if args.command == "detect":
        wan2gp_root = find_wan2gp_root()
        if wan2gp_root is None:
            print(json.dumps({
                "error": "Wan2GP not found",
                "help": "Set WAN2GP_ROOT env var to your Wan2GP app directory, or install Wan2GP via Pinokio.",
            }), file=sys.stderr)
            return 1
        cmd_detect(args, wan2gp_root)
        return 0

    if args.command == "show":
        cmd_show(args)
        return 0

    wan2gp_root = find_wan2gp_root()
    if wan2gp_root is None:
        print(json.dumps({
            "error": "Wan2GP not found",
            "help": "Set WAN2GP_ROOT env var to your Wan2GP app directory, or install Wan2GP via Pinokio.",
        }), file=sys.stderr)
        return 1

    ensure_wan2gp_on_path(wan2gp_root)

    if args.command == "list":
        cmd_list(args, wan2gp_root)
    elif args.command == "defaults":
        cmd_defaults(args, wan2gp_root)
    elif args.command == "schema":
        cmd_schema(args, wan2gp_root)
    elif args.command == "generate":
        cmd_generate(args, wan2gp_root)
    elif args.command == "upscale":
        cmd_upscale(args, wan2gp_root)
    elif args.command == "update":
        cmd_update(wan2gp_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
