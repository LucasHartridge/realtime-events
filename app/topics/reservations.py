import json


class ReservationsTopic:
    # Replace with your topic Key and value Schema
    @staticmethod
    def key_schema():
        return json.dumps({
            "fields": [
                {
                "name": "organization_id",
                "type": "int"
                },
            ],
            "name": "record",
            "type": "record"
        })

    @staticmethod
    def value_schema():
        return json.dumps({
        "fields": [
            {
            "default": None,
            "name": "reservation_id",
            "type": [
                "null",
                "string"
            ]
            },
        ],
        "name": "record",
        "type": "record"
        })
