INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "placed": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        },
    },
    "required": ["approved", "delivered", "placed"],
    "additionalProperties": False
}
