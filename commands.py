# from dataclasses import asdict
from sqlalchemy import text, true#, and_, or_
from sqlalchemy.orm.query import Query
from connection import session

import models
import tools
import sqlalchemy.sql.sqltypes

def hello(args)-> str:
    return "How can I help you?"

def bye(args)-> str:
    return "Good bye!"

def sql(args):
    results = session().execute(text(args.sql))
    return results

def create(args):
    table, result = __get_model_or_table(args.model[0])
    if table is not None:
        count = 0
        values = __parse_args_for_model(args.values, table, False)
        # if not hasattr(table, "name"):
        #     names = args.name[0].split()
        #     first_name  = names[0]  if len(names) > 0 else ""
        #     last_name   = names[-1] if len(names) > 1 else ""
        #     record = table(
        #                 first_name  = first_name,
        #                 last_name   = last_name,
        #                 group_id    = 0,
        #                 # id          = args.id if args.id > 0 else None
        #             )
        # else:
        for value in values:
            record = table(**(value))
            session().add(record)
        else:
            try:
                session().commit()
                count = len(values)
            except Exception as e:
                session().rollback()
                result = str(e)
            info = f"{count} record"
            info += "s created" if count > 1 else " created"
            info += f" with message:{result}" if result else ""
            return info
        return "None data specified."
    return result

def read(args):
    query, result = __get_query(args)
    if query is not None:
        # filters = text(args.filter) if args.filter else true()
        # result = session().query(table).filter(filters)
        headers = query.statement.columns.keys()
        results = tools.results(query, headers)
        tools.print_result(results, "keys")
        # sql =   "select * from " + table.name
        # sql +=  args.filter if args.filter else ""
        # results = session().execute(text(sql))
        # return results
        return
    return result

def update(args):
    query, result = __get_query(args)
    if query is not None:
        table, result = __get_model_or_table(args.model[0])
        values = __parse_args_for_model(args.values, table, False)
        count, result = __execute(query, Query.update, values[0], False)
        info = f"{count} record"
        info += "s updated" if count > 1 else " updated"
        info += f" with message:{result}" if result else ""
        return info
    return result

def delete(args):
    query, result = __get_query(args)
    if query is not None:
        count, result = __execute(query, Query.delete, False)
        info = f"{count} record"
        info += "s deleted" if count > 1 else " deleted"
        info += f" with message:{result}" if result else ""
        return info
    return result

def __execute(query, function, *args):
    count = 0
    result = None
    try:
        count = function(query, *args)
        session().commit()
    except Exception as e:
        session().rollback()
        result = str(e)
    return count, result

def __enclose_value(value):
    _value =    "'" if not value.startswith ("'") else ""
    _value +=   value
    _value +=   "'" if not value.endswith   ("'") else ""
    return _value

def __extend_mappings(values, value, enclose = True):
    for key, value in value.items():
        try:
            value = int(value)
        except ValueError as e:
            if enclose:
                value = __enclose_value(value)
        if key in values:
            if not isinstance(values[key], list):
                values[key] = [values[key]]
            values[key].append(value)
        else:
            values[key] = value

def __parse_args_for_model(datas, table, enclose = True):
    columns = table.__table__.columns if hasattr(table,"__table__") else table.columns
    return __parse_args(datas, columns, enclose)

def __parse_args(datas, columns, enclose = True):
    if datas is None:
        return []
    
    icolumn = 0
    scolumn = 0
    if columns:
        icolumns = [c for c in columns if type(c.type) == sqlalchemy.sql.sqltypes.Integer]
        scolumns = [c for c in columns if type(c.type) == sqlalchemy.sql.sqltypes.String]
    else:
        class Column():
            def __init__(self, key):
                self.key = key
        
        icolumns = [Column("id")]
        scolumns = [Column("name")]


    filters = []
    for value in datas:
        values = {}
        filters.append(values)

        icolumn = 0
        scolumn = 0
        _values = value.split(',')
        _values = list(map(lambda v: v.strip(), _values))
        _values = [v for v in _values if v]
        for value in _values:
            if '=' not in value:
                try:
                    _value = dict([(icolumns[icolumn].key, int(value))])
                    if icolumn < len(icolumns) - 1:
                        icolumn += 1
                    else:
                        icolumn = -1
                except ValueError as e:
                    if enclose:
                        _value = __enclose_value(value)
                    else:
                        _value = value
                    _value = dict([(scolumns[scolumn].key, _value)])
                    if scolumn < len(scolumns) - 1:
                        scolumn += 1
                    else:
                        scolumn = -1
            else:
                _value = {k.strip(): v.strip() for k, v in [value.split('=')]}
            __extend_mappings(values, _value, enclose)
    return filters

def __get_query(args):
    table, result = __get_model_or_table(args.model[0])
    if table is not None:
        _filters = __parse_args_for_model(args.filter, table)
        filters = ""
        orfilters = ""
        for group in _filters:
            if orfilters:
                orfilters += " OR ("
            andfilter = ""
            for k, v  in group.items():
                if andfilter:
                    andfilter += " AND "
                andfilter += k
                if isinstance(v, list) and len(v) > 1:
                    andfilter += " IN ("
                    subfilter = ""
                    for f in v:
                        if subfilter:
                            subfilter += ", "
                        subfilter += str(f)
                    andfilter += subfilter
                    andfilter += ")"
                else:
                    andfilter += " = "
                    andfilter += str(v)
            if orfilters:
                orfilters += andfilter
                orfilters += ")"
            else:
                orfilters += andfilter
        filters += orfilters
        filters = text(filters) if filters else true()
        query = session().query(table).filter(filters)
        return query, result
    return None, result

def __get_model_or_table(name: str):
    table   = None
    result  = None
    try:
        table = models.registry[name]
    except KeyError as e:
        try:
            table = models.metadata.tables[name]
        except KeyError as e:
            result = f"Model:'{e.args[0]}' not found."
    return table, result
