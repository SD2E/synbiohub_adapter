from synbiohub_adapter.cache_query import wrap_query_fn, db_dir
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
import unittest
import os

catchable_exception = False
uncatchable_exception = False

def reset_flags():
    global catchable_exception, uncatchable_exception
    catchable_exception = False
    uncatchable_exception = False

def set_catchable():
    global catchable_exception, uncatchable_exception
    catchable_exception = True
    uncatchable_exception = False

def set_uncatchable():
    global catchable_exception, uncatchable_exception
    catchable_exception = False
    uncatchable_exception = True

def query_result(*args):
    return " -- ".join((str(x) for x in args))

class UncatchableException(Exception): pass

def query(*args):
    global catchable_exception, uncatchable_exception
    if catchable_exception:
        raise QueryBadFormed()
    elif uncatchable_exception:
        raise UncatchableException()
    
    return query_result(*args)

db_file_path = os.path.join(db_dir, 'testing_fallback_cache.db')
cached_query = wrap_query_fn(query, db_file_path=db_file_path)

class TestFallbackCache(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(db_file_path)
        except FileNotFoundError:
            pass
            
    def test_normal_success(self):
        # Normal query works when no exceptions occur
        reset_flags()
        q_key = ('normal', 'success')
        self.assertEqual(query(q_key), query_result(q_key))

    def test_normal_catchable_fail(self):
        # Normal query fails when catchable exception occurs
        set_catchable()
        q_key = ('normal', 'catchable', 'fail')
        with self.assertRaises(QueryBadFormed):
            query(q_key)

    def test_normal_uncatchable_fail(self):
        # Normal query fails when uncatchable exception occurs
        set_uncatchable()
        q_key = ('normal', 'uncatchable', 'fail')
        with self.assertRaises(UncatchableException):
            query(q_key)

    def test_cache_catchable_success(self):
        # Cache works when catchable exception occurs and result is cached
        reset_flags()
        q_key = ('cache', 'catchable', 'success')
        # Get the result in the cache
        self.assertEqual(cached_query(q_key), query_result(q_key))
        
        set_catchable()
        self.assertEqual(cached_query(q_key), query_result(q_key))
        
    def test_cache_uncatchable_fail(self):
        # Cache fails when uncatchable exception occurs and result is cached
        reset_flags()
        q_key = ('cache', 'uncatchable', 'fail')
        # Get the result in the cache
        self.assertEqual(cached_query(q_key), query_result(q_key))
        
        set_uncatchable()
        with self.assertRaises(UncatchableException):
            cached_query(q_key)

    def test_cache_catchable_fail(self):
        # Cache fails when catchable exception occurs and result is not cached
        # Should raise orignal catchable error
        reset_flags()
        q_key = ('cache', 'catchable', 'fail')
        # Don't get the result in the cache
        #self.assertEqual(cached_query(q_key), query_result(q_key))
        
        set_catchable()
        with self.assertRaises(QueryBadFormed):
            cached_query(q_key)


if __name__ == '__main__':
    unittest.main()
