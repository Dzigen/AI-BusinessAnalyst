from .connectors  import \
    InMemoryKVConnector, DEFAULT_INMEMORYKV_CONFIG,\
    MixedKVConnector, DEFAULT_MIXEDKV_CONFIG,\
    RedisKVConnector, DEFAULT_REDISKV_CONFIG,\
    MongoKVConnector, DEFAULT_MONGOKV_CONFIG

DEFAULT_KVDB_CONFIGS = {
    'inmemory_kv': DEFAULT_INMEMORYKV_CONFIG,
    'redis': DEFAULT_REDISKV_CONFIG,
    'mongo': DEFAULT_MONGOKV_CONFIG,
    'mixed_kv': DEFAULT_MIXEDKV_CONFIG
}

AVAILABLE_KVDB_CONNECTORS = {
    'inmemory_kv': InMemoryKVConnector,
    'redis': RedisKVConnector,
    'mongo': MongoKVConnector,
    'mixed_kv': MixedKVConnector
}
