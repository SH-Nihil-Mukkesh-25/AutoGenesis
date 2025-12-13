# Autogenesis Backend

## Setup

1.  Create virtual environment:
    ```bash
    python -m venv venv
    ```
2.  Activate:
    -   Windows: `.\venv\Scripts\activate`
    -   Mac/Linux: `source venv/bin/activate`
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running

```bash
uvicorn api:app --reload
```
