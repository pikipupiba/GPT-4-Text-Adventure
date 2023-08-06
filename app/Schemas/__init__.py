import json
from . import stats_schema, combat_schema

stats_schema_string = json.dumps(stats_schema, separators=(',', ':'))
combat_schema_string = json.dumps(combat_schema, separators=(',', ':'))

schema_strings = {
    "Stats_Schema": stats_schema_string,
    "Combat_Schema": combat_schema_string,
}

__all__ = ['schema_strings', 'stats_schema', 'stats_schema_string', 'combat_schema', 'combat_schema_string']