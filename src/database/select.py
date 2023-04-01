import psycopg2
from database.access import connection
from logger.config import logger
from database.access import connection
from config import SITEMAP_FREQUENCY
from datetime import datetime, timedelta

def execute_select(query, params=None, fetchone=True):
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

def next_sitemap_url():
    query = """
        SELECT url, domain_id
        FROM meta.sitemaps
        WHERE crawl_uuid = '' OR crawl_uuid IS NULL
        ORDER BY
          CASE WHEN crawl_uuid = '' OR crawl_uuid IS NULL
            THEN created_at
            ELSE (SELECT ended_at FROM events.crawls WHERE crawl_uuid = meta.sitemaps.crawl_uuid)
          END ASC
        LIMIT 1;
    """
    result = execute_select(query)
    if result:
        url, domain_id = result
        logger.info(f'Sitemap Selected for Domain {domain_id}: {url}')
        return url, domain_id
    else:
        logger.error('Unable to select sitemap')
        return None, None

def get_useragent():
        query = """
            SELECT user_agent, id as "user_agent_id"
            FROM meta.user_agents
            WHERE active=TRUE
            ORDER BY RANDOM()
            LIMIT 1;
        """
        result = execute_select(query)
        if result:
            user_agent, user_agent_id = result
            logger.info(f'Useragent Selected: {user_agent}')
            return user_agent, user_agent_id
        else:
            logger.error('No Useragent Returned')
            return None, None

def select_pending_sitemap_count():
        query = """
            SELECT count(*)
            FROM meta.sitemaps
            WHERE crawl_uuid is NULL OR events.crawls.ended_at < %s
        """
        # calculate the datetime value SITEMAP_FREQUENCY hours ago
        frequency = timedelta(hours=SITEMAP_FREQUENCY)
        past_time = datetime.utcnow() - frequency

        # Connect to the database
        conn = connection()
        conn.open()

        # Create a cursor
        cur = conn.conn.cursor()

        # Execute the query
        cur.execute(query, (past_time,))

        # Fetch the result
        count = cur.fetchone()[0]

        # Close the cursor and connection
        cur.close()
        conn.close()
        logger.info(f'{count} Sitemaps to Crawl  ')
        return count