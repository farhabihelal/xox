#! /bin/env bash
uv sync

. .venv/bin/activate

cd xox_rs

maturin develop

cd ..

uv run xox/xox_gui.py