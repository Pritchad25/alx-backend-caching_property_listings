from django.core.cache import cache
from properties.models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at'))
        cache.set('all_properties', properties, timeout=3600)  # Cache for 1 hour
    return properties

def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 4)
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {str(e)}")
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0
        }
