import psycopg2

DATABASE_SETTINGS = {
    'NAME': 'betproject',
    'USER': 'postgres',
    'PASSWORD': 'Gheddafi22',
    'HOST': 'localhost',
    'PORT': '5432',
}

def visualizza_view_trigger():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_SETTINGS['NAME'],
            user=DATABASE_SETTINGS['USER'],
            password=DATABASE_SETTINGS['PASSWORD'],
            host=DATABASE_SETTINGS['HOST'],
            port=DATABASE_SETTINGS['PORT']
        )
        cursor = conn.cursor()

        # Visualizza view e dettagli
        cursor.execute("SELECT table_name FROM information_schema.views WHERE table_schema = 'public';")
        views = cursor.fetchall()
        print("View presenti nel database:")
        for view_name in views:
            view_name = view_name[0]
            print(f"\nView: {view_name}")
            cursor.execute(
                "SELECT view_definition FROM information_schema.views WHERE table_name = %s AND table_schema = 'public';",
                (view_name,),
            )
            view_definition = cursor.fetchone()[0]
            print(f"  Definizione:\n{view_definition}")

        # Visualizza trigger e dettagli
        cursor.execute("SELECT trigger_name, event_object_table, action_timing, event_manipulation FROM information_schema.triggers WHERE trigger_schema = 'public';")
        triggers = cursor.fetchall()
        print("\nTrigger presenti nel database:")
        for trigger_info in triggers:
            trigger_name, table_name, action_timing, event_manipulation = trigger_info
            print(f"\n  Trigger: {trigger_name}")
            print(f"    Tabella: {table_name}")
            print(f"    Momento: {action_timing}")
            print(f"    Operazione: {event_manipulation}")
            cursor.execute(
                "SELECT action_statement FROM information_schema.triggers WHERE trigger_name = %s AND trigger_schema = 'public';",
                (trigger_name,),
            )
            action_statement = cursor.fetchone()[0]
            print(f"    Istruzione: {action_statement}")
            cursor.execute(f"SELECT pg_get_functiondef(t.tgfoid) FROM pg_trigger t WHERE t.tgname = '{trigger_name}';")
            function_code = cursor.fetchone()
            if function_code:
                print(f"    Funzione associata:\n{function_code[0]}")

        conn.close()

    except Exception as error:
        print(f"Errore durante la visualizzazione di view e trigger: {error}")

if __name__ == "__main__":
    visualizza_view_trigger()