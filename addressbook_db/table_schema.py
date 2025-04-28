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
                {"name": "id", "type": "INT", "constraint": ["AUTO_INCREMENT", "PRIMARY KEY"]},
                {"name": "address_book_id", "type": "INT", "constraint": ["NOT NULL"]},
                {"name": "first_name", "type": "VARCHAR(50)"},
                {"name": "last_name", "type": "VARCHAR(50)"},
                {"name": "email", "type": "VARCHAR(100)"},
                {"name": "phone", "type": "VARCHAR(50)"},
                {"name": "address", "type": "VARCHAR(255)"},
                {"name": "city", "type": "VARCHAR(50)"},
                {"name": "state", "type": "VARCHAR(50)"},
                {"name": "zip", "type": "VARCHAR(10)"},
                {"name": "is_valid", "type": "TINYINT(1)", "constraint": ["DEFAULT 0"]}  # Added the is_valid column here
            ],
            "foreign_keys": [
                "FOREIGN KEY (address_book_id) REFERENCES address_books(id) ON DELETE CASCADE"
            ]
        }
    }

    stored_procedure = {
        "sp_add_contact": """
            CREATE PROCEDURE sp_add_contact(
                IN address_book_id INT,
                IN first_name VARCHAR(50),
                IN last_name VARCHAR(50),
                IN email VARCHAR(100),
                IN phone VARCHAR(50),
                IN address VARCHAR(255),
                IN city VARCHAR(50),
                IN state VARCHAR(50),
                IN zip VARCHAR(10)
            )
            BEGIN
                INSERT INTO contacts (
                    address_book_id, first_name, last_name, email,
                    phone, address, city, state, zip, is_valid  -- Added is_valid field in insert
                ) VALUES (
                    address_book_id, first_name, last_name, email,
                    phone, address, city, state, zip, 0  -- Default value for is_valid
                );
            END
        """
    }
    trigger_scripts = {
    "before_insert_contacts": """
        CREATE TRIGGER before_insert_contacts
        BEFORE INSERT ON contacts
        FOR EACH ROW
        BEGIN
            DECLARE valid_email BOOLEAN;
            DECLARE valid_phone BOOLEAN;

            SET valid_email = CASE
                WHEN NEW.email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN 1 ELSE 0
            END;

            SET valid_phone = CASE
                WHEN CHAR_LENGTH(NEW.phone) BETWEEN 7 AND 15 THEN 1 ELSE 0
            END;

            IF valid_email = 1 AND valid_phone = 1 THEN
                SET NEW.is_valid = 1;
            ELSE
                SET NEW.is_valid = 0;
            END IF;
        END
    """
}


    @classmethod
    def get_procedure(cls, procedure_name: str) -> str:
        return cls.stored_procedure.get(procedure_name)
    
    @classmethod
    def get_trigger(cls, trigger_name: str) -> str:
        return cls.trigger_scripts.get(trigger_name)


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
