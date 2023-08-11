import json
from .stats_schema import stats_schema
from .combat_schema import combat_schema

from .day_schema import day_schema
from .item_schema import item_schema
from .relationship_schema import relationship_schema

stats_schema_string = json.dumps(stats_schema, separators=(',', ':'))
combat_schema_string = json.dumps(combat_schema, separators=(',', ':'))
day_schema_string = json.dumps(day_schema, separators=(',', ':'))
item_schema_string = json.dumps(item_schema, separators=(',', ':'))
relationship_schema_string = json.dumps(relationship_schema, separators=(',', ':'))

schema_strings = {
    "Stats_Schema": stats_schema_string,
    "Combat_Schema": combat_schema_string,
    "Day_Schema": day_schema_string,
    "Item_Schema": item_schema_string,
    "Relationship_Schema": relationship_schema_string,
}

__all__ = ['schema_strings', 'stats_schema', 'stats_schema_string', 'combat_schema', 'combat_schema_string', 'day_schema', 'day_schema_string', 'item_schema', 'item_schema_string', 'relationship_schema', 'relationship_schema_string']