"""CLI entry point for securityme."""

import sys
from curate import curate_europe, curate_spain, generate_audio_briefing
from build import build


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    if cmd == "europe":
        curate_europe()
    elif cmd == "spain":
        curate_spain()
    elif cmd == "audio":
        import json, pathlib
        DATA = pathlib.Path(__file__).parent / "data"
        eu = json.loads((DATA / "europe.json").read_text()) if (DATA / "europe.json").exists() else {}
        es = json.loads((DATA / "spain.json").read_text()) if (DATA / "spain.json").exists() else {}
        generate_audio_briefing(eu, es)
    elif cmd == "build":
        build()
    elif cmd == "all":
        print("=== Curating Europe ===")
        eu = curate_europe()
        print("\n=== Curating Spain ===")
        es = curate_spain()
        print("\n=== Generating audio ===")
        generate_audio_briefing(eu, es)
        print("\n=== Building static site ===")
        build()
    else:
        print(f"Usage: python run.py [europe|spain|audio|build|all]")
        sys.exit(1)


if __name__ == "__main__":
    main()
