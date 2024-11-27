from datetime import datetime, timezone

def response(http_status_code: int, status_code: str, message: str, result: dict) -> dict:
    return {
        "statusCode": status_code,
        "responseDatetime": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "result": result
    }