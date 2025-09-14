
import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}


def with_db_connection(func):
    """Decorator to handle opening and closing the database connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Look for 'query' in kwargs or positional args
        query = kwargs.get("query")
        if query is None and len(args) > 1:  # args[0] is conn, args[1] is query
            query = args[1]

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE STORE] Caching result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will hit DB and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
