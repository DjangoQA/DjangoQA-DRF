def validation_error(tg_id, message, text):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": f"{message}\n\n{text}",
    }
