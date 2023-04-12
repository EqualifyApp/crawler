import psycopg2
import json
import traceback
from database.access import connection
from utils.watch import logger
from psycopg2.pool import SimpleConnectionPool

# Set use_pooling to True to enable connection pooling
use_pooling = True

# Connection pool
pool = None

if use_pooling:
    conn_params = connection().get_connection_params()
    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **conn_params
    )



def connection_pooling():
    return pool.getconn()

def release_pooling(conn):
    pool.putconn(conn)



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

# # # # # # # # # #

    # Bulk Updates

    def execute_bulk_update(query, params_list):
        # Connect to the database
        if use_pooling:
            conn = connection_pooling()
        else:
            conn = connection()
            conn.open()

        # Create a cursor
        cur = conn.cursor()

        try:
            # Execute the query
            with conn:
                cur.executemany(query, params_list)
                logger.info("🗄️✏️🟢 Query executed and committed")
        except Exception as e:
            logger.error(f"🗄️✏️ Error executing bulk insert query: {e}\n{traceback.format_exc()}")

        # Close the cursor and connection
        cur.close()
        if use_pooling:
            release_pooling(conn)
        else:
            conn.close()



#########################################################
## Queries


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

def update_sitemap_status(sitemap_id, crawl_id):
   logger.debug(f'Updating Sitemap Status: {sitemap_id}...')
   query = """
      UPDATE targets.sitemaps
         SET status = 'completed'
            recent_crawl_id = %s
         WHERE id = %s
         RETURNING id;
   """
   try:
      result = execute_update(query, (sitemap_id,))
      logger.debug(f'Update: {sitemap_id} Updated')
      return True
   except:
      logger.error(f'🗄️🔧 Failed to update Sitemap {sitemap_id}')
      return False


