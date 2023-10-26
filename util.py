def is_video(filename):
    ext = filename.split(".")[-1]
    return ext in {
        "mp4",
        "gif",
        "webm",
        "mov",
        "avi",
        "mkv",
        "flv",
        "wmv",
        "m4v",
        "m4p",
        "m4b",
    }
