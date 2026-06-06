from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Iterable


ITEMSET_SEPARATOR = " | "
BASKET_ITEM_SEPARATOR = " ||| "


def ensure_project_root() -> None:
    """Allow scripts to run from either project root or src/."""
    current_dir = Path.cwd()
    if current_dir.name == "src":
        os.chdir(current_dir.parent)


def load_baskets(path: str | Path) -> list[tuple[str, tuple[str, ...]]]:
    baskets_path = Path(path)
    baskets: list[tuple[str, tuple[str, ...]]] = []

    with baskets_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required_columns = {"InvoiceNo", "Items"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                f"{baskets_path} must contain columns: {', '.join(sorted(required_columns))}"
            )

        for row in reader:
            invoice_no = str(row["InvoiceNo"]).strip()
            raw_items = (row["Items"] or "").strip()
            if not raw_items:
                continue

            if raw_items.startswith("["):
                parsed_items = json.loads(raw_items)
                items = tuple(sorted({str(item).strip() for item in parsed_items if str(item).strip()}))
            elif BASKET_ITEM_SEPARATOR in raw_items:
                items = tuple(
                    sorted(
                        {
                            item.strip()
                            for item in raw_items.split(BASKET_ITEM_SEPARATOR)
                            if item.strip()
                        }
                    )
                )
            elif "," in raw_items:
                raise ValueError(
                    f"{baskets_path} appears to use comma-separated baskets. "
                    "This is unsafe because product descriptions can contain commas. "
                    "Run src/preprocess_clean_data.py again to regenerate baskets.csv."
                )
            else:
                items = (raw_items,)

            if invoice_no and items:
                baskets.append((invoice_no, items))

    return baskets


def load_transactions(path: str | Path) -> list[tuple[str, tuple[str, ...]]]:
    transactions_path = Path(path)
    with transactions_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = set(reader.fieldnames or [])

        if {"InvoiceNo", "Items"}.issubset(fieldnames):
            return load_baskets(transactions_path)

        required_columns = {"InvoiceNo", "Description"}
        if not required_columns.issubset(fieldnames):
            raise ValueError(
                f"{transactions_path} must contain either InvoiceNo/Items or "
                "InvoiceNo/Description columns"
            )

        grouped_items: dict[str, set[str]] = defaultdict(set)
        for row in reader:
            invoice_no = str(row["InvoiceNo"]).strip()
            item = str(row["Description"]).strip()
            if invoice_no and item:
                grouped_items[invoice_no].add(item)

    return [
        (invoice_no, tuple(sorted(items)))
        for invoice_no, items in grouped_items.items()
        if items
    ]


def format_itemset(items: Iterable[str]) -> str:
    return ITEMSET_SEPARATOR.join(items)


def parse_itemset(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(ITEMSET_SEPARATOR) if item.strip())
