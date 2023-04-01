import psycopg2
from database.access import connection
from logger.config import logger
from database.access import connection

def execute_insert(query, params=None, fetchone=True):
    """
    Execute a query on the database and return the result.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to pass to the query. Defaults to None.
        fetchone (bool, optional): Whether to fetch only the first row of results. Defaults to True.

    Returns:
        Any: The result of the query.
    """
    # Connect to the database
    conn = connection()
    conn.open()

    # Create a cursor
    cur = conn.conn.cursor()

    # Execute the query
    cur.execute(query, params)

    # Fetch the results if requested
    result = None
    if fetchone:
        result = cur.fetchone()[0] if cur.rowcount > 0 else None
    else:
        result = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return result

def record_new_crawl(actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url):
    query = """
        INSERT INTO events.crawls (
            actor_id,
            status,
            started_by,
            crawl_uuid,
            crawl_type,
            domain_id,
            start_url
        )
        VALUES (
            %s, 'new', %s,
            %s, %s, %s, %s
        )
        """
    try:
        execute_insert(query, (actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url))
        return True
    except:
        return False



def record_crawled_url(url, crawl_uuid, source_url):
    query = """
        INSERT INTO results.urls (url,
            crawl_uuid,
            discovery_crawl_uuid,
            source_url,
            discovery_source_url,
            last_crawled_at,
            first_source_url)
        VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        ON CONFLICT (url) DO UPDATE SET last_crawled_at = NOW()
        RETURNING CASE WHEN xmax = 0 THEN 'add' ELSE 'update' END;
    """
    try:
        result = execute_insert(query, (url, crawl_uuid, crawl_uuid, source_url, source_url, source_url))
        action = result[0] if result else None
        logger.info(f'URL Recorded: {url}')
        return action
    except:
        logger.error(f'Unable to record URL: {url}')
        return None

