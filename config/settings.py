# config/settings.py
PATHS = {
    "raw_data": "/path/to/raw_data.tsv",
    "result_db": "/path/to/result.db",
    "filtered_db": "/path/to/filtered_result.db",
    "final_csv": "/path/to/final_result.csv",
}

EMAIL_CONFIG = {
    "smtp_server": "smtp.example.com",
    "sender": "workflow@example.com",
    "recipients": ["user@example.com"],
}
