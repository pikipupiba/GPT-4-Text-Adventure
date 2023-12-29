item_schema = {
    "Item_Schema": {
        "type": "array",
        "description": (
            "Items in the player's inventory. Be as succinct as possible. Only include"
            " items whose status has changed from the previous turn."
        ),
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the item"},
                "status": {
                    "type": "string",
                    "description": "The current status or condition of the item.",
                },
            },
        },
    },
}
