import psycopg2
from database.access import connection
from logger.config import logger
from database.access import connection

# Log Emoji: 🗄️🔧

def execute_update(query, params=None, fetchone=True):
   # logger.debug(f'🗄️🔧 Executing query: {query}'')
   # logger.debug(f'🗄️🔧 Query parameters: {params}... ')

    # Connect to the database
    conn = connection()
    conn.open()
    logger.debug(f'🗄️🔧 Database connection opened')

    # Create a cursor
    cur = conn.conn.cursor()

    try:
        # Execute the query
        cur.execute(query, params)
        conn.conn.commit()
        logger.info(f'🗄️🔧 Query executed and committed')

        # Fetch the results if requested
        result = None
        if fetchone:
            result = cur.fetchone() or ()  # return an empty tuple if None is returned
        else:
            result = cur.fetchall() or []  # return an empty list if None is returned
            logger.debug(f'🗄️🔧 Fetched results: {result}')
    except Exception as e:
        logger.error(f'🗄️🔧 Error executing update query: {e}')
        result = None

    # Close the cursor and connection
    cur.close()
    conn.close()
    logger.debug(f'🗄️🔧 Cursor and connection closed')

    return result



def update_crawl_status(status, crawl_uuid):
    logger.info(f'🗄️🔧 Updating crawl status for {crawl_uuid} to {status}')
    query = """
        UPDATE events.crawls
        SET status = %s
        WHERE crawl_uuid = %s
        RETURNING status;
    """
    updated_status = execute_update(query, (status, crawl_uuid))
    logger.debug(f'🗄️🔧 Crawl status updated to {updated_status[0]}')
    return updated_status[0] if updated_status else None

def update_crawl_user_agent(user_agent_id, crawl_uuid):
    logger.info(f'🗄️🔧 Updating crawl {crawl_uuid} user agent to {user_agent_id}')
    query = """
        UPDATE events.crawls
        SET user_agent_id = %s, status = 'processing'
        WHERE crawl_uuid = %s;
    """
    try:
        execute_update(query, (user_agent_id, crawl_uuid))
        logger.debug(f'🗄️🔧 Crawl user agent updated to {user_agent_id}')
        return True
    except:
        logger.error(f'🗄️🔧 Failed to update crawl {crawl_uuid} user agent')
        return False


def update_crawl_complete(crawl_uuid):
    logger.info(f'🗄️🔧 Updating crawl {crawl_uuid} as completed')
    query = """
        UPDATE events.crawls
        SET status = 'completed',
            ended_at = NOW()
        WHERE crawl_uuid = %s;
    """
    try:
        execute_update(query, (crawl_uuid))
        logger.debug(f'🗄️🔧 Crawl {crawl_uuid} completed successfully')
        return True
    except:
        logger.error(f'🗄️🔧 Failed to complete crawl {crawl_uuid}')
        return False
