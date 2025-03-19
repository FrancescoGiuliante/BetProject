import psycopg2

DATABASE_SETTINGS = {
    'NAME': 'betproject',
    'USER': 'postgres',
    'PASSWORD': 'Gheddafi22',
    'HOST': 'localhost',
    'PORT': '5432',
}

def create_triggers_and_functions():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_SETTINGS['NAME'],
            user=DATABASE_SETTINGS['USER'],
            password=DATABASE_SETTINGS['PASSWORD'],
            host=DATABASE_SETTINGS['HOST'],
            port=DATABASE_SETTINGS['PORT']
        )
        cursor = conn.cursor()

        sql_queries = [
            # Funzione per ridurre il credito dell'utente all'inserimento di una betslip
            """
            CREATE OR REPLACE FUNCTION reduce_user_credit_on_betslip() 
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE bet_user
                SET credit = credit - NEW.stake
                WHERE id = NEW.user_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,
            # Trigger che attiva la funzione reduce_user_credit_on_betslip dopo l'inserimento di una betslip
            """
            CREATE TRIGGER trg_reduce_user_credit_on_betslip
            AFTER INSERT
            ON bet_betslip
            FOR EACH ROW
            EXECUTE FUNCTION reduce_user_credit_on_betslip();
            """,
            # Funzione per aggiornare il risultato delle bet (won/lost) quando viene concluso un evento
            """
            CREATE OR REPLACE FUNCTION update_bet_result_on_event_conclusion()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE bet_bet
                SET status = CASE
                    WHEN NEW.result = bet_bet.result THEN 'won'
                    ELSE 'lost'
                END
                WHERE event_id = NEW.id;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,
            # Trigger che attiva la funzione update_bet_result_on_event_conclusion dopo l'aggiornamento di un evento
            """
            CREATE TRIGGER trg_update_bet_result_on_event_conclusion
            AFTER UPDATE ON bet_event
            FOR EACH ROW
            WHEN (OLD.result = '?' AND NEW.result <> '?')
            EXECUTE FUNCTION update_bet_result_on_event_conclusion();
            """,
            # Vista che mostra i dettagli delle betslip con informazioni sugli utenti, le bet e gli eventi
            """
            CREATE OR REPLACE VIEW betslip_details AS 
            SELECT 
                bs.id AS betslip_id,
                bs.user_id,
                u.name AS user_name,
                u.lastname AS user_lastname,
                bs.stake AS betslip_stake,
                bs.potential_win,
                bs.status AS betslip_status,
                b.id AS bet_id,
                b.event_id,
                e.team_home,
                e.team_away,
                e.date AS event_date,
                b.result AS bet_result,
                b.stake AS bet_stake,
                b.status AS bet_status
            FROM 
                bet_betslip bs
            JOIN 
                bet_user u ON bs.user_id = u.id
            LEFT JOIN
                bet_betslip_bets bb ON bs.id = bb.betslip_id
            LEFT JOIN
                bet_bet b ON bb.bet_id = b.id
            LEFT JOIN
                bet_event e ON b.event_id = e.id;
            """,
            # Vista che riassume le bet per evento, mostrando il numero totale di bet e la puntata totale
            """
            CREATE OR REPLACE VIEW event_bet_summary AS
            SELECT
                e.id AS event_id,
                e.team_home, 
                e.team_away, 
                e.date AS event_date,
                COUNT(b.id) AS total_bets,
                SUM(b.stake) AS total_stake
            FROM
                bet_event e
            LEFT JOIN 
                bet_bet b ON e.id = b.event_id
            GROUP BY
                e.id;
            """,
            # Funzione per aggiornare lo stato delle betslip
            """
            CREATE OR REPLACE FUNCTION update_betslip_status_on_bet_update()
            RETURNS TRIGGER AS $$
            DECLARE
                betslip_id_var INTEGER;
                all_bets_won BOOLEAN;
            BEGIN
                FOR betslip_id_var IN (SELECT betslip_id FROM bet_betslip_bets WHERE bet_id = NEW.id) LOOP
                    IF NEW.status = 'lost' THEN
                        UPDATE bet_betslip SET status = 'lost' WHERE id = betslip_id_var;
                    ELSE 
                        SELECT bool_and(status = 'won') INTO all_bets_won
                        FROM bet_bet
                        WHERE id IN (SELECT bet_id FROM bet_betslip_bets WHERE betslip_id = betslip_id_var);

                        IF all_bets_won THEN
                            UPDATE bet_betslip SET status = 'won' WHERE id = betslip_id_var;
                        END IF;
                    END IF;
                END LOOP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,
            # Trigger che attiva la funzione update_betslip_status_on_bet_update dopo l'aggiornamento di una bet
            """
            CREATE TRIGGER trg_update_betslip_status_on_bet_update
            AFTER UPDATE OF status ON bet_bet
            FOR EACH ROW
            WHEN (OLD.status IS DISTINCT FROM NEW.status)
            EXECUTE FUNCTION update_betslip_status_on_bet_update();
            """,
            # Funzione per aggiungere credito all'utente quando una betslip è vinta
            """
            CREATE OR REPLACE FUNCTION add_user_credit_on_betslip_win()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.status = 'won' THEN
                    UPDATE bet_user
                    SET credit = credit + NEW.potential_win
                    WHERE id = NEW.user_id;
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,
            # Trigger che attiva la funzione quando lo stato di una betslip diventa 'won'
            """
            CREATE TRIGGER trg_add_user_credit_on_betslip_win
            AFTER UPDATE OF status ON bet_betslip
            FOR EACH ROW
            WHEN (OLD.status IS DISTINCT FROM NEW.status AND NEW.status = 'won')
            EXECUTE FUNCTION add_user_credit_on_betslip_win();
            """
        ]

        for query in sql_queries:
            cursor.execute(query)

        conn.commit()

        print("Triggers and functions created successfully!")

    except Exception as error:
        print(f"Error executing the queries: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_triggers_and_functions()