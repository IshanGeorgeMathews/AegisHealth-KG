# AegisHealth-KG

An autonomous digital advocate that turns insurance claim denials into structured, legally grounded appeals.

## Quickstart

```bash
# Set up environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Run API
uvicorn src.aegis.api.main:app --reload
```
