class TableSchema:
    table_schema = {
        "addressbook": {
            "table_name": "address_books",
            "columns": [
                {"name": "id",   "type": "INT", "constraint": ["AUTO_INCREMENT", "PRIMARY KEY"]},
                {"name": "name", "type": "VARCHAR(100)", "constraint": ["UNIQUE", "NOT NULL"]}
            ]
        },
        "contacts": {
            "table_name": "contacts",
            "columns": [
                {"name": "id",               "type": "INT", "constraint": ["AUTO_INCREMENT", "PRIMARY KEY"]},
                {"name": "address_book_id",  "type": "INT", "constraint": ["NOT NULL"]},
                {"name": "first_name",       "type": "VARCHAR(50)"},
                {"name": "last_name",        "type": "VARCHAR(50)"},
                {"name": "email",            "type": "VARCHAR(100)"},
                {"name": "phone",            "type": "VARCHAR(15)"},
                {"name": "address",          "type": "VARCHAR(255)"},
                {"name": "city",             "type": "VARCHAR(50)"},
                {"name": "state",            "type": "VARCHAR(50)"},
                {"name": "zip",              "type": "VARCHAR(10)"}
            ],
            "foreign_keys": [
                "FOREIGN KEY (address_book_id) REFERENCES address_books(id) ON DELETE CASCADE"
            ]
        }
    }

    @classmethod
    def get_table_name(cls, table_key: str) -> str:
        return cls.table_schema[table_key]["table_name"]

    @classmethod
    def get_columns(cls, table_key: str) -> list[str]:
        return [col["name"] for col in cls.table_schema[table_key]["columns"]]

    @classmethod
    def get_non_id_columns(cls, table_key: str) -> list[str]:
        return [col["name"] for col in cls.table_schema[table_key]["columns"] if col["name"] != "id"]

    @classmethod
    def get_create_statement(cls, table_key: str) -> str:
        schema = cls.table_schema[table_key]
        lines = []

        for col in schema["columns"]:
            constraint_str = " ".join(col.get("constraint", []))
            lines.append(f"{col['name']} {col['type']} {constraint_str}".strip())

        if "foreign_keys" in schema:
            lines.extend(schema["foreign_keys"])

        body = ",\n    ".join(lines)
        return f"CREATE TABLE IF NOT EXISTS {schema['table_name']} (\n    {body}\n);"