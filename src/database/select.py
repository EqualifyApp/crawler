import psycopg2
from database.access import connection
from logger.config import logger
from database.access import connection
from config import SITEMAP_FREQUENCY
from datetime import datetime, timedelta
# Log Emoji: 🗄️🔍


def execute_select(query, params=None, fetchone=True):
    # Connect to the database
    conn = connection()
    conn.open()
    logger.debug("🗄️🔍 Database connection opened")

    # Create a cursor
    cur = conn.conn.cursor()

    # Execute the query
    cur.execute(query, params)
    # logger.debug(f"🗄️🔍 Executed select query: {query}")
    logger.debug(f"🗄️🔍 Query parameters: {params}")

    # Fetch the results if requested
    result = None
    if fetchone:
        result = cur.fetchone() if cur.rowcount > 0 else None
    else:
        result = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()
    logger.debug("🗄️🔍 Cursor and connection closed")

    return result


def next_sitemap_url():
    query = """
        WITH null_crawl AS (
            SELECT
                url AS "sitemap_url",
                id AS "sitemap_id",
                domain_id
            FROM targets.sitemaps
            WHERE recent_crawl_id IS NULL
            AND active_crawl is TRUE
            ORDER BY RANDOM()
            LIMIT 1
        ),
        random_row AS (
            SELECT
                url AS "sitemap_url",
                id AS "sitemap_id",
                domain_id
            FROM targets.sitemaps
            WHERE NOT EXISTS (SELECT 1 FROM null_crawl) AND
                  (current_timestamp - updated_at) > INTERVAL '24 hours'
                  AND active_crawl is TRUE
            ORDER BY RANDOM()
            LIMIT 1
        )
        SELECT * FROM null_crawl
        UNION ALL
        SELECT * FROM random_row
        LIMIT 1;
    """
    result = execute_select(query, ())
    if result:
        sitemap_url, sitemap_id, domain_id = result
        logger.info(f'🗄️🔍 Sitemap Selected for Domain {domain_id}: {sitemap_url}')
        return sitemap_url, sitemap_id, domain_id
    else:
        logger.error('🗄️🔍 Unable to select sitemap')
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
        logger.debug(f'🗄️🔍 User Agent result from query: {result}')
        if result:
            user_agent, user_agent_id = result
            logger.info(f'🗄️🔍 Useragent Selected: {user_agent}')
            return user_agent, user_agent_id
        else:
            logger.error('🗄️🔍 No Useragent Returned')
            return None, None



def select_pending_sitemap_count():
    query = """
        SELECT count(*)
        FROM meta.sitemaps
        LEFT JOIN events.crawls ON meta.sitemaps.crawl_uuid = events.crawls.crawl_uuid
        WHERE meta.sitemaps.crawl_uuid is NULL OR events.crawls.ended_at < %s;
    """
    # calculate the datetime value SITEMAP_FREQUENCY hours ago
    frequency = timedelta(hours=SITEMAP_FREQUENCY)
    past_time = datetime.utcnow() - frequency
    logger.debug(f'🗄️🔍 Executing query: {query}')
    logger.debug(f'🗄️🔍 Query parameters: {past_time}')
    result = execute_select(query, (past_time,))
    logger.info(f'{result} Sitemaps to Crawl')
    return result