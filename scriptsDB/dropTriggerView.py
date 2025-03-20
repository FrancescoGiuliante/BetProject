import psycopg2

DATABASE_SETTINGS = {
    'NAME': 'betproject',
    'USER': 'postgres',
    'PASSWORD': 'Gheddafi22',
    'HOST': 'localhost',
    'PORT': '5432',
}

def drop_triggers_and_functions():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_SETTINGS['NAME'],
            user=DATABASE_SETTINGS['USER'],
            password=DATABASE_SETTINGS['PASSWORD'],
            host=DATABASE_SETTINGS['HOST'],
            port=DATABASE_SETTINGS['PORT']
        )
        cursor = conn.cursor()

        drop_triggers = [
            "DROP TRIGGER IF EXISTS trg_reduce_user_credit_on_betslip ON bet_betslip;",
            "DROP TRIGGER IF EXISTS trg_update_bet_result_on_event_conclusion ON bet_event;",
            "DROP TRIGGER IF EXISTS trg_update_betslip_status_on_bet_update ON bet_bet;",
            "DROP TRIGGER IF EXISTS trg_add_user_credit_on_betslip_win ON bet_betslip;"
        ]

        for query in drop_triggers:
            cursor.execute(query)

        drop_functions = [
            "DROP FUNCTION IF EXISTS reduce_user_credit_on_betslip() CASCADE;",
            "DROP FUNCTION IF EXISTS update_bet_result_on_event_conclusion() CASCADE;",
            "DROP FUNCTION IF EXISTS update_betslip_status_on_bet_update() CASCADE;",
            "DROP FUNCTION IF EXISTS add_user_credit_on_betslip_win() CASCADE;"
        ]

        for query in drop_functions:
            cursor.execute(query)

        drop_views = [
            "DROP VIEW IF EXISTS betslip_details;",
            "DROP VIEW IF EXISTS event_bet_summary;"
        ]

        for query in drop_views:
            cursor.execute(query)

        conn.commit()

        print("Triggers, functions, and views dropped successfully!")

    except Exception as error:
        print(f"Error executing the queries: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    drop_triggers_and_functions()