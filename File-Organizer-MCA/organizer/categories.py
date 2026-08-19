FILE_CATEGORIES = {
    "Images": {".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg",".ico",".tiff",".heic"},
    "Documents": {".doc",".docx",".txt",".rtf",".odt",".md"},
    "PDFs": {".pdf"},
    "Videos": {".mp4",".mkv",".avi",".mov",".wmv",".flv",".webm",".m4v"},
    "Audio": {".mp3",".wav",".flac",".aac",".ogg",".m4a",".wma"},
    "Archives": {".zip",".rar",".7z",".tar",".gz",".bz2",".xz"},
    "Spreadsheets": {".xls",".xlsx",".csv",".ods"},
    "Presentations": {".ppt",".pptx",".odp"},
    "Code": {".py",".java",".c",".cpp",".h",".hpp",".cs",".go",".rs",".js",".ts",".php",".html",".css",".scss",".sql",".json",".xml",".yml",".yaml",".sh",".bat",".ps1"},
}

def get_category(file_path):
    ext = file_path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"
