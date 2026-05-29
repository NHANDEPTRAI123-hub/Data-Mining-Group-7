from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from utils import ensure_project_root, format_itemset, load_transactions


DEFAULT_TRANSACTIONS_PATH = Path("data/processed/transactions_cleaned.csv")
DEFAULT_OUTPUT_PATH = Path("results/frequent_itemsets.csv")


def resolve_min_support_count(min_support: float, transaction_count: int) -> int:
    if transaction_count <= 0:
        raise ValueError("transaction_count must be greater than 0")
    if min_support <= 0:
        raise ValueError("min_support must be greater than 0")
    if min_support < 1:
        return max(1, math.ceil(transaction_count * min_support))
    return int(math.ceil(min_support))


def build_vertical_tidsets(
    baskets: Iterable[tuple[str, tuple[str, ...]]],
) -> tuple[dict[str, set[int]], int]:
    tidsets: dict[str, set[int]] = defaultdict(set)
    transaction_count = 0

    for transaction_id, (_, items) in enumerate(baskets):
        transaction_count += 1
        for item in items:
            tidsets[item].add(transaction_id)

    return dict(tidsets), transaction_count


def _eclat(
    prefix: tuple[str, ...],
    candidates: list[tuple[str, set[int]]],
    min_support_count: int,
    transaction_count: int,
    results: list[dict[str, object]],
    max_size: int | None,
) -> None:
    for index, (item, tidset) in enumerate(candidates):
        itemset = prefix + (item,)
        support_count = len(tidset)

        results.append(
            {
                "itemset": itemset,
                "itemset_size": len(itemset),
                "support_count": support_count,
                "support": support_count / transaction_count,
            }
        )

        if max_size is not None and len(itemset) >= max_size:
            continue

        suffix_candidates: list[tuple[str, set[int]]] = []
        for other_item, other_tidset in candidates[index + 1 :]:
            intersection = tidset.intersection(other_tidset)
            if len(intersection) >= min_support_count:
                suffix_candidates.append((other_item, intersection))

        if suffix_candidates:
            _eclat(
                itemset,
                suffix_candidates,
                min_support_count,
                transaction_count,
                results,
                max_size,
            )


def mine_frequent_itemsets(
    baskets: list[tuple[str, tuple[str, ...]]],
    min_support: float = 0.02,
    max_size: int | None = None,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    vertical_tidsets, transaction_count = build_vertical_tidsets(baskets)
    min_support_count = resolve_min_support_count(min_support, transaction_count)

    candidates = [
        (item, tidset)
        for item, tidset in vertical_tidsets.items()
        if len(tidset) >= min_support_count
    ]
    candidates.sort(key=lambda pair: (-len(pair[1]), pair[0]))

    results: list[dict[str, object]] = []
    _eclat(
        prefix=(),
        candidates=candidates,
        min_support_count=min_support_count,
        transaction_count=transaction_count,
        results=results,
        max_size=max_size,
    )

    results.sort(
        key=lambda row: (
            -int(row["support_count"]),
            -int(row["itemset_size"]),
            tuple(row["itemset"]),
        )
    )
    metadata = {
        "transaction_count": transaction_count,
        "unique_item_count": len(vertical_tidsets),
        "min_support": min_support,
        "min_support_count": min_support_count,
        "max_size": max_size,
        "frequent_itemset_count": len(results),
    }
    return results, metadata


def save_frequent_itemsets(
    frequent_itemsets: list[dict[str, object]],
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["itemset", "itemset_size", "support_count", "support"],
        )
        writer.writeheader()
        for row in frequent_itemsets:
            writer.writerow(
                {
                    "itemset": format_itemset(row["itemset"]),
                    "itemset_size": row["itemset_size"],
                    "support_count": row["support_count"],
                    "support": f"{row['support']:.6f}",
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mine frequent itemsets with the ECLAT algorithm."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_TRANSACTIONS_PATH),
        help="Path to transactions_cleaned.csv or baskets.csv",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Path to save frequent itemsets CSV",
    )
    parser.add_argument(
        "--min-support",
        type=float,
        default=0.02,
        help="Minimum support as a ratio, or an absolute count if >= 1",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=None,
        help="Optional maximum itemset size to mine",
    )
    return parser.parse_args()


def main() -> None:
    ensure_project_root()
    args = parse_args()

    baskets = load_transactions(args.input)
    frequent_itemsets, metadata = mine_frequent_itemsets(
        baskets=baskets,
        min_support=args.min_support,
        max_size=args.max_size,
    )
    save_frequent_itemsets(frequent_itemsets, args.output)

    print("ECLAT frequent itemset mining completed.")
    print(f"Transactions: {metadata['transaction_count']}")
    print(f"Unique items: {metadata['unique_item_count']}")
    print(
        "Minimum support: "
        f"{metadata['min_support']} ({metadata['min_support_count']} transactions)"
    )
    print(f"Frequent itemsets: {metadata['frequent_itemset_count']}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
