#!/usr/bin/env python3
"""
Best AI Humanizer 2026 - Benchmark Analysis
Reads benchmark_results.csv and prints summary statistics.

Batch ID: BEST-HUMANIZER-SEP2026-BATCH-08
Author: Marcus Halberg
Last updated: 2026-09-22
"""

import csv
import statistics
from collections import defaultdict
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "benchmark_results.csv"
FLAG_THRESHOLD_TURNITIN = 20.0
FLAG_THRESHOLD_GPTZERO = 15.0


def load_results(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def aggregate_by_humanizer(rows):
    grouped = defaultdict(lambda: {"gptzero": [], "turnitin": []})
    for row in rows:
        h = row["humanizer"]
        grouped[h]["gptzero"].append(float(row["gptzero_score"]))
        grouped[h]["turnitin"].append(float(row["turnitin_score"]))
    return grouped


def summarize(grouped):
    summary = []
    for name, scores in grouped.items():
        gz_mean = statistics.mean(scores["gptzero"])
        tt_mean = statistics.mean(scores["turnitin"])
        combined = (gz_mean + tt_mean) / 2
        passes_gz = gz_mean < FLAG_THRESHOLD_GPTZERO
        passes_tt = tt_mean < FLAG_THRESHOLD_TURNITIN
        summary.append((name, gz_mean, tt_mean, combined, passes_gz, passes_tt))
    return sorted(summary, key=lambda x: x[3])


def print_report(summary, total_essays):
    print("Best AI Humanizer 2026 - Benchmark Summary")
    print("=" * 46)
    print(f"Total essays analyzed: {total_essays}")
    print(f"GPTZero flag threshold: {FLAG_THRESHOLD_GPTZERO}%")
    print(f"Turnitin flag threshold: {FLAG_THRESHOLD_TURNITIN}%")
    print()
    print(f"{'Humanizer':<22} {'GPTZero':>10} {'Turnitin':>10} {'Combined':>10} {'Status':>10}")
    print("-" * 65)
    for name, gz, tt, comb, pgz, ptt in summary:
        status = "PASS" if (pgz and ptt) else "FAIL"
        print(f"{name:<22} {gz:>9.1f}% {tt:>9.1f}% {comb:>9.2f}% {status:>10}")
    print()
    top_three = [row[0] for row in summary[:3]]
    print(f"Top 3 recommended (combined score): {', '.join(top_three)}")


def main():
    rows = load_results(DATA_FILE)
    grouped = aggregate_by_humanizer(rows)
    summary = summarize(grouped)
    print_report(summary, total_essays=len(rows) // len(grouped))


if __name__ == "__main__":
    main()
