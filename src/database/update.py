import psycopg2
from database.access import connection
from logger.config import logger
from database.access import connection

def execute_update(query, params=None, fetchone=True):
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

def update_crawl_status(status, crawl_uuid):
        query = """
            UPDATE events.crawls
            SET status = %s
            WHERE crawl_uuid = %s
            RETURNING status;
        """
        updated_status = execute_update(query, (status, crawl_uuid))
        return updated_status[0] if updated_status else None

def update_crawl_user_agent(user_agent_id, crawl_uuid):
    query = """
        UPDATE events.crawls
        SET user_agent_id = %s, status = 'processing'
        WHERE crawl_uuid = %s;
    """
    try:
        execute_update(query, (user_agent_id, crawl_uuid))
        return True
    except:
        return False

def update_crawl_complete(crawl_uuid, new_urls, updated_urls):
    query = """
        UPDATE events.crawls
        SET new_urls = %s,
            updated_urls = %s,
            status = 'completed',
            ended_at = NOW()
        WHERE crawl_uuid = %s;
    """
    try:
        execute_update(query, (new_urls, updated_urls, crawl_uuid))
        logger.info(f'Crawl {crawl_uuid} completed successfully')
        return True
    except:
        logger.error(f'Failed to complete crawl {crawl_uuid}')
        return False
