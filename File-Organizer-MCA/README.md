# File Organizer

A Python desktop application that automatically organizes files into category folders.

## Features
- Tkinter GUI
- Detects and reuses existing category folders
- Creates missing folders only when needed
- Images, Documents, PDFs, Videos, Audio, Archives, Spreadsheets, Presentations and Code
- Unknown types go to `Others`
- Duplicate names are handled safely
- Preview mode
- Recursive scanning option
- Undo last organization operation
- Local operation history
- No third-party dependencies

## Run

```bash
python main.py
```

## Project Structure

```text
File-Organizer/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── organizer/
    ├── __init__.py
    ├── categories.py
    ├── models.py
    ├── scanner.py
    ├── history.py
    └── service.py
```
