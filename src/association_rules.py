from __future__ import annotations

import argparse
import csv
from itertools import combinations
from pathlib import Path

from eclat import (
    DEFAULT_OUTPUT_PATH,
    DEFAULT_TRANSACTIONS_PATH,
    resolve_min_support_count,
)
from utils import ensure_project_root, format_itemset, load_transactions, parse_itemset


DEFAULT_RULES_PATH = Path("results/association_rules.csv")
DEFAULT_SUMMARY_PATH = Path("results/eclat_summary.md")


def load_frequent_itemsets(path: str | Path) -> list[dict[str, object]]:
    frequent_itemsets: list[dict[str, object]] = []

    with Path(path).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            itemset = parse_itemset(row["itemset"])
            if not itemset:
                continue
            frequent_itemsets.append(
                {
                    "itemset": itemset,
                    "itemset_size": int(row["itemset_size"]),
                    "support_count": int(row["support_count"]),
                    "support": float(row["support"]),
                }
            )

    return frequent_itemsets


def _non_empty_proper_subsets(itemset: tuple[str, ...]) -> list[tuple[str, ...]]:
    subsets: list[tuple[str, ...]] = []
    for size in range(1, len(itemset)):
        subsets.extend(combinations(itemset, size))
    return subsets


def generate_association_rules(
    frequent_itemsets: list[dict[str, object]],
    min_confidence: float = 0.5,
    min_lift: float = 1.0,
    transaction_count: int | None = None,
) -> list[dict[str, object]]:
    support_count_lookup = {
        tuple(row["itemset"]): int(row["support_count"]) for row in frequent_itemsets
    }
    if transaction_count:
        support_lookup = {
            itemset: support_count / transaction_count
            for itemset, support_count in support_count_lookup.items()
        }
    else:
        support_lookup = {
            tuple(row["itemset"]): float(row["support"]) for row in frequent_itemsets
        }
    rules: list[dict[str, object]] = []

    for row in frequent_itemsets:
        itemset = tuple(row["itemset"])
        if len(itemset) < 2:
            continue

        itemset_support_count = support_count_lookup[itemset]
        itemset_support = support_lookup[itemset]
        for antecedent in _non_empty_proper_subsets(itemset):
            consequent = tuple(item for item in itemset if item not in set(antecedent))
            antecedent_support = support_lookup.get(tuple(antecedent))
            consequent_support = support_lookup.get(consequent)
            if not antecedent_support or not consequent_support:
                continue

            if transaction_count:
                antecedent_support_count = support_count_lookup[tuple(antecedent)]
                confidence = itemset_support_count / antecedent_support_count
            else:
                confidence = itemset_support / antecedent_support
            lift = confidence / consequent_support
            if confidence < min_confidence or lift < min_lift:
                continue

            rules.append(
                {
                    "antecedent": tuple(antecedent),
                    "consequent": consequent,
                    "antecedent_size": len(antecedent),
                    "consequent_size": len(consequent),
                    "support_count": itemset_support_count,
                    "support": itemset_support,
                    "antecedent_support": antecedent_support,
                    "consequent_support": consequent_support,
                    "confidence": confidence,
                    "lift": lift,
                }
            )

    rules.sort(
        key=lambda row: (
            -float(row["lift"]),
            -float(row["confidence"]),
            -float(row["support"]),
            format_itemset(row["antecedent"]),
            format_itemset(row["consequent"]),
        )
    )
    return rules


def save_association_rules(
    rules: list[dict[str, object]],
    output_path: str | Path = DEFAULT_RULES_PATH,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "antecedent",
                "consequent",
                "antecedent_size",
                "consequent_size",
                "support_count",
                "support",
                "antecedent_support",
                "consequent_support",
                "confidence",
                "lift",
            ],
        )
        writer.writeheader()
        for rule in rules:
            writer.writerow(
                {
                    "antecedent": format_itemset(rule["antecedent"]),
                    "consequent": format_itemset(rule["consequent"]),
                    "antecedent_size": rule["antecedent_size"],
                    "consequent_size": rule["consequent_size"],
                    "support_count": rule["support_count"],
                    "support": f"{rule['support']:.6f}",
                    "antecedent_support": f"{rule['antecedent_support']:.6f}",
                    "consequent_support": f"{rule['consequent_support']:.6f}",
                    "confidence": f"{rule['confidence']:.6f}",
                    "lift": f"{rule['lift']:.6f}",
                }
            )


def write_summary(
    frequent_itemsets: list[dict[str, object]],
    rules: list[dict[str, object]],
    metadata: dict[str, object],
    min_confidence: float,
    min_lift: float,
    output_path: str | Path = DEFAULT_SUMMARY_PATH,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    top_single = max(
        (row for row in frequent_itemsets if int(row["itemset_size"]) == 1),
        key=lambda row: int(row["support_count"]),
        default=None,
    )
    top_combo = max(
        (row for row in frequent_itemsets if int(row["itemset_size"]) >= 2),
        key=lambda row: int(row["support_count"]),
        default=None,
    )
    single_consequent_rules = [
        rule for rule in rules if int(rule["consequent_size"]) == 1
    ]
    top_rule = (single_consequent_rules or rules)[0] if rules else None
    strong_support_rule = max(rules, key=lambda row: float(row["support"]), default=None)

    lines = [
        "# Ket luan thuc nghiem ECLAT",
        "",
        "## Tham so chay",
        f"- So transaction: {metadata['transaction_count']}",
        f"- So item rieng biet: {metadata['unique_item_count']}",
        (
            f"- Min support: {metadata['min_support']} "
            f"({metadata['min_support_count']} transaction)"
        ),
        f"- Min confidence: {min_confidence}",
        f"- Min lift: {min_lift}",
        "",
        "## Ket qua chinh",
        f"- So frequent itemsets tim duoc: {len(frequent_itemsets)}",
        f"- So association rules thoa nguong: {len(rules)}",
    ]

    if top_single:
        lines.append(
            "- Item pho bien nhat: "
            f"{format_itemset(top_single['itemset'])} "
            f"(support = {float(top_single['support']):.2%}, "
            f"{top_single['support_count']} transaction)."
        )

    if top_combo:
        lines.append(
            "- Tap item di cung nhau pho bien nhat: "
            f"{format_itemset(top_combo['itemset'])} "
            f"(support = {float(top_combo['support']):.2%}, "
            f"{top_combo['support_count']} transaction)."
        )

    if top_rule:
        lines.append(
            "- Luat co lift cao nhat: "
            f"{format_itemset(top_rule['antecedent'])} -> "
            f"{format_itemset(top_rule['consequent'])} "
            f"(confidence = {float(top_rule['confidence']):.2%}, "
            f"lift = {float(top_rule['lift']):.2f})."
        )

    if strong_support_rule and strong_support_rule is not top_rule:
        lines.append(
            "- Luat co support lon nhat: "
            f"{format_itemset(strong_support_rule['antecedent'])} -> "
            f"{format_itemset(strong_support_rule['consequent'])} "
            f"(support = {float(strong_support_rule['support']):.2%}, "
            f"confidence = {float(strong_support_rule['confidence']):.2%}, "
            f"lift = {float(strong_support_rule['lift']):.2f})."
        )

    lines.extend(
        [
            "",
            "## Nhan xet",
        ]
    )

    if top_combo and top_rule:
        lines.append(
            "Ket qua cho thay cac san pham thuoc cung dong thiet ke hoac cung muc "
            "dich su dung co xu huong xuat hien chung trong gio hang. Cac luat co "
            "lift > 1 nghia la viec mua tien de lam tang xac suat mua ket qua so "
            "voi muc trung binh, nen co the dung de goi y ban kem, sap xep san "
            "pham gan nhau hoac tao combo khuyen nghi."
        )
        lines.append(
            "Khi ung dung, can doc dong thoi support va lift. Luat co lift cao cho "
            "thay moi lien he manh, nhung luat co support cao thuong dang tin hon "
            "vi xuat hien tren nhieu giao dich hon. Vi vay cac cap san pham nhu "
            "JUMBO BAG co the phu hop cho goi y pho bien, trong khi nhom REGENCY "
            "TEACUP phu hop hon cho combo theo bo suu tap."
        )
        lines.append(
            "Cac luat ket hop chi phan anh mau dong xuat hien trong du lieu, khong "
            "khang dinh quan he nhan qua giua cac san pham."
        )
    else:
        lines.append(
            "Voi nguong hien tai, ket qua chua tao duoc nhieu quan he manh. Co the "
            "giam min_support hoac min_confidence de quan sat them cac mau ket hop."
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate association rules from ECLAT frequent itemsets."
    )
    parser.add_argument(
        "--transactions",
        "--baskets",
        dest="transactions",
        default=str(DEFAULT_TRANSACTIONS_PATH),
        help="Path to transactions_cleaned.csv or baskets.csv",
    )
    parser.add_argument(
        "--frequent-itemsets",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Path to frequent itemsets CSV",
    )
    parser.add_argument(
        "--rules-output",
        default=str(DEFAULT_RULES_PATH),
        help="Path to save association rules CSV",
    )
    parser.add_argument(
        "--summary-output",
        default=str(DEFAULT_SUMMARY_PATH),
        help="Path to save a short result summary",
    )
    parser.add_argument(
        "--min-support",
        type=float,
        default=0.02,
        help="Minimum support used if frequent itemsets must be regenerated",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Minimum confidence threshold",
    )
    parser.add_argument(
        "--min-lift",
        type=float,
        default=1.0,
        help="Minimum lift threshold",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=None,
        help="Optional maximum itemset size used if frequent itemsets must be regenerated",
    )
    return parser.parse_args()


def main() -> None:
    ensure_project_root()
    args = parse_args()

    baskets = load_transactions(args.transactions)
    frequent_itemsets_path = Path(args.frequent_itemsets)

    if frequent_itemsets_path.exists():
        frequent_itemsets = load_frequent_itemsets(frequent_itemsets_path)
        unique_items = {item for _, items in baskets for item in items}
        metadata = {
            "transaction_count": len(baskets),
            "unique_item_count": len(unique_items),
            "min_support": args.min_support,
            "min_support_count": resolve_min_support_count(args.min_support, len(baskets)),
            "max_size": args.max_size,
            "frequent_itemset_count": len(frequent_itemsets),
        }
    else:
        from eclat import mine_frequent_itemsets

        frequent_itemsets, metadata = mine_frequent_itemsets(
            baskets=baskets,
            min_support=args.min_support,
            max_size=args.max_size,
        )

    rules = generate_association_rules(
        frequent_itemsets=frequent_itemsets,
        min_confidence=args.min_confidence,
        min_lift=args.min_lift,
        transaction_count=int(metadata["transaction_count"]),
    )
    save_association_rules(rules, args.rules_output)
    write_summary(
        frequent_itemsets=frequent_itemsets,
        rules=rules,
        metadata=metadata,
        min_confidence=args.min_confidence,
        min_lift=args.min_lift,
        output_path=args.summary_output,
    )

    print("Association rule generation completed.")
    print(f"Frequent itemsets: {len(frequent_itemsets)}")
    print(f"Rules: {len(rules)}")
    print(f"Saved rules to: {args.rules_output}")
    print(f"Saved summary to: {args.summary_output}")


if __name__ == "__main__":
    main()
