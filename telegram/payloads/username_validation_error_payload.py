def username_validation_error_payload(tg_id, message, text):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": f"{message}\n\n{text}",
    }
