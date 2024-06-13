USER_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "lat": {
            "type": "number"
        },
        "long": {
            "type": "number"
        }
    },
    "required": [
        "lat",
        "long"
    ]
}
