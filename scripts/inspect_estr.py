from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.ecb import fetch_recent_estr


def main() -> None:
    observations = fetch_recent_estr(limit=5)
    latest = observations[-1]

    print("ECB €STR benchmark")
    print()
    print(f"Reference date: {latest.reference_date}")
    print(f"Rate:           {latest.rate_pct:.3f}%")
    print(f"Currency:       {latest.currency}")
    print(f"Source:         {latest.source}")


if __name__ == "__main__":
    main()