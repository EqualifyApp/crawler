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

# Normal Insert

def execute_insert(query, params=None, fetchone=True):
    # logger.debug(f"🗄️✏️ Executing query: {query}")
    # logger.debug(f"🗄️✏️ Query parameters: {params}")

    # Connect to the database
    if use_pooling:
        conn = connection_pooling()
    else:
        conn = connection()
        conn.open()
        logger.debug("🗄️✏️ Database connection opened")

    # Create a cursor
    cur = conn.cursor() # Removed conn.

    try:
        # Execute the query
        cur.execute(query, params)
        conn.commit()   # Removed conn.
        logger.debug("🗄️✏️🟢 Query executed and committed")

        # Fetch the results if requested
        result = None
        if fetchone:
            result = cur.fetchone() or () # return an empty tuple if None is returned
        else:
            result = cur.fetchall() or [] # return an empty list if None is returned
            logger.debug(f'🗄️✏️ Fetched results: {result}')
    except Exception as e:
        logger.error(f"🗄️✏️ Error executing insert query: {e}\n{traceback.format_exc()}")
        result = None

    # Close the cursor and connection
    cur.close()
    if use_pooling:
        release_pooling(conn)
    else:
        conn.close()
        logger.debug("🗄️✏️ Cursor and connection closed")

    return result
# # # # # # # # # #

# Bulk Inserts

def execute_bulk_insert(query, params_list):
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
            logger.debug("🗄️✏️🟢 Query executed and committed")
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

def record_new_url(discovered_url, source_url, crawl_id, sitemapped, domain_id):
    query = """
        INSERT INTO targets.urls (
            url,
            source_url,
            recent_crawl_id,
            sitemapped,
            domain_id
        )
        VALUES (
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (url) DO UPDATE SET recent_crawl_id = %s
        RETURNING url;
    """
    logger.debug(f'🗄️ ✏️ Recording new url: {discovered_url} ')
    execute_insert(query, (discovered_url, source_url, crawl_id, sitemapped, domain_id, crawl_id ))
    # TODO-if there is an error, logger.error that things broke

def record_new_urls(url_records):
    query = """
        INSERT INTO targets.urls (
            url,
            source_url,
            recent_crawl_id,
            sitemapped,
            domain_id
        )
        VALUES (
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (url) DO UPDATE SET recent_crawl_id = %s;
    """
    params_list = [(discovered_url, source_url, crawl_id, sitemapped, domain_id, crawl_id) for discovered_url, source_url, crawl_id, sitemapped, domain_id in url_records]
    execute_bulk_insert(query, params_list)
    # TODO-if there is an error, logger.error that things broke



def create_new_crawl(crawl_type, sitemap_id, agent, domain_id):
    query = """
        INSERT INTO events.crawls (
            crawl_type,
            sitemap_id,
            agent
        )
        VALUES (
            %s, %s, %s
        )
        RETURNING id as crawl_id;
        """
    logger.debug('🗄️ ✏️ Recording New Crawl')
    result = execute_insert(query, (crawl_type, sitemap_id, agent))
    if result:
        crawl_id = result
        logger.debug(f'🗄️🔍 Created new crawl: {crawl_id} ')
        return crawl_id
    else:
        logger.error('🗄️🔍 Unable create new crawl')
        return None


def create_new_crawl_html(crawl_type, url_id, agent):
        query = """
            INSERT INTO events.crawls (
                crawl_type,
                url_id,
                agent
            )
            VALUES (
                %s, %s, %s
            )
            RETURNING id as crawl_id;
            """
        logger.debug('🗄️ ✏️ Recording New Crawl')
        result = execute_insert(query, (crawl_type, url_id, agent))
        if result:
            crawl_id = result
            logger.debug(f'🗄️🔍 Created new crawl: {crawl_id} ')
            return crawl_id
        else:
            logger.error('🗄️🔍 Unable create new crawl')
            return None


# Record New URLs found during Rosevelt - HTML - Crawl
def record_new_crawled_htmls(new_urls):
    query = """
        INSERT INTO targets.urls (
            source_url_id,
            url,
            recent_crawl_id
        )
        VALUES (
            %s, %s, %s
        )
        ON CONFLICT (url) DO UPDATE SET recent_crawl_id = %s;
    """
    params_list = [(entry["source_url_id"], entry["url"], entry["crawl_id"], entry["crawl_id"]) for entry in new_urls]
    execute_bulk_insert(query, params_list)
    # TODO-if there is an error, logger.error that things broke
