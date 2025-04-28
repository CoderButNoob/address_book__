from table_schema import TableSchema
from db_connection import connect

def ensure_schema():
    conn = connect()
    cursor = conn.cursor()

    print("Creating Tables...")
    for table_key in TableSchema.table_schema.keys():
        query = TableSchema.get_create_statement(table_key)
        print(f"Creating: {TableSchema.get_table_name(table_key)}")
        cursor.execute(query)

    print("Creating Stored Procedures...")
    for proc in TableSchema.stored_procedure.keys():
        try:
            cursor.execute(f"DROP PROCEDURE IF EXISTS {proc}")
            proc_query = TableSchema.get_procedure(proc)
            if proc_query:
                cursor.execute(proc_query)
                print(f"Created Procedure {proc}")
        except Exception as e:
            print(f"Error creating procedure {proc}: {e}")
    
    print("Creating Triggers...")
    for trig_name in TableSchema.trigger_scripts.keys():
        try:
            cursor.execute(f"DROP TRIGGER IF EXISTS {trig_name}")
            trigger_query = TableSchema.get_trigger(trig_name)
            if trigger_query:
                cursor.execute(trigger_query)
                print(f"Created Trigger {trig_name}")
        except Exception as e:
            print(f"Error creating trigger {trig_name}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
