import shelve
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound, EndPointInternalError
import appdirs
import os
import errno

# Not sure if complete list of exceptions that can be thrown
# When query goes bad
_catch_exceptions = (
    QueryBadFormed, EndPointNotFound, EndPointInternalError
)

db_dir = appdirs.user_cache_dir(appname='synbiohub_adapter')
db_file = os.path.join(db_dir, 'queries.db')

try:
    os.makedirs(db_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        # Directory does not exists, something else went wrong
        raise
    else:
        # Directory already exists, ignore error
        pass
    

def wrap_query_fn(fn, db_file_path=None):
    if db_file_path is None:
        db_file_path = db_file

    def wrapped_fn(*args):
        # Just join the args into one string as the query key
        q_key = ", ".join((str(x) for x in args))

        try:
            raise QueryBadFormed()
            result = fn(*args)
            # Run the query function then cache the results
            with shelve.open(db_file_path) as db:
                db[q_key] = result
        except _catch_exceptions as e:

            # Query failed, try to load the results from the cache
            import sys
            sys.stderr.write('Query failed, using fallback cache: {}\n'.format(e))

            try:
                with shelve.open(db_file_path) as db:
                    result = db[q_key]
            except Exception:
                # If fail to get cached value, re-raise the original exception instead.
                raise e

        return result

    return wrapped_fn
