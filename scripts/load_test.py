"""Command line local synthetic load test."""
import argparse
import json
from app.loadlab import estimate, run_synthetic

def main():
    p = argparse.ArgumentParser(description="Synthetic financial ledger load benchmark")
    p.add_argument("--accounts", type=int, default=20)
    p.add_argument("--operations", type=int, default=100)
    p.add_argument("--tps", type=float, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--database", default="load_lab.db")
    p.add_argument("--execute", action="store_true", help="Write synthetic transactions locally")
    args = p.parse_args()
    result = (run_synthetic(args.accounts, args.operations, args.tps, args.seed,
                            args.database) if args.execute else
              estimate(args.accounts, args.operations, args.tps))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
