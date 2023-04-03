import psycopg2
from database.access import connection
from logger.config import logger

def execute_insert(query, params=None, fetchone=True):
    logger.debug(f"🗄️✏️ Executing query: {query}")
    logger.debug(f"🗄️✏️ Query parameters: {params}")

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
    logger.debug("🗄️✏️ Database connection opened")

    # Create a cursor
    cur = conn.conn.cursor()

    try:
        # Execute the query
        cur.execute(query, params)
        conn.conn.commit()
        logger.info("🗄️✏️ Query executed and committed")

        # Fetch the results if requested
        result = None
        if fetchone:
            result = cur.fetchone() if cur.rowcount > 0 else None
        else:
            result = cur.fetchall()
            logger.debug(f'🗄️✏️ Fetched results: {result}')
    except Exception as e:
        logger.error(f"🗄️✏️ Error executing insert query: {e}")
        result = None

    # Close the cursor and connection
    cur.close()
    conn.close()
    logger.debug("🗄️✏️ Cursor and connection closed")

    return result


def record_new_crawl(actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url):
    logger.info(f"🗄️✏️ Recording new crawl: {crawl_uuid}")
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
        RETURNING crawl_uuid
        """
    result = execute_insert(query, (actor_id, started_by, crawl_uuid, crawl_type, domain_id, start_url))
    logger.debug(f'🗄️✏️ Record New Crawl Output: {result} ')
    if result[0] == crawl_uuid:
        logger.debug(f'🗄️✏️ Crawl {crawl_uuid} created... ')
        return True
    else:
        logger.error(f'🗄️✏️ Record New Crawl had an issue with: {crawl_uuid} ')
        return False


def record_crawled_url(url, crawl_uuid, source_url):
    logger.info(f"🗄️✏️ Recording crawled URL: {url}")
    query = """
        INSERT INTO results.urls (url,
            crawl_uuid,
            discovery_crawl_uuid,
            source_url,
            discovery_source_url,
            last_crawled_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        ON CONFLICT (url) DO UPDATE SET last_crawled_at = NOW()
        RETURNING CASE WHEN xmax = 0 THEN 'add' ELSE 'update' END;
    """
    try:
        result = execute_insert(query, (url, crawl_uuid, crawl_uuid, source_url, source_url))
        action = result[0] if result else None
        logger.info(f'🗄️✏️ URL Recorded: {url}')
        return action
    except:
        logger.error(f'🗄️✏️ Unable to record URL: {url}')
        return None

