import tabulate


"""Parse command line"""
def tokenize(string: str) -> list:
    separators  = " \t\n"
    delimiters  = "\'\""
    tokens      = []
    i = 0
    separator   = ' '
    delimiter   = ''
    token       = ""
    while i < len(string):
        char = string[i]

        if not token and char in delimiters:
            delimiter = char
            i += 1
            continue
        if delimiter:
            i += 1
            if char in delimiters:
                delimiter = ''
                if token:
                    tokens.append(token)
                    token = ""
                else:
                    delimiter = char
            else:
                token += char
            continue
    # if separator:
        i += 1
        if char in separators:
            # i += 1
            if token:
                tokens.append(token)
                token = ""
                # separator = ' '
            # else:
            #     separator = char
            continue
        else:
            # i += 1
            token += char

        # elif not separator and not delimiter and char in delimiters:
        #     i += 1
        #     delimiter = char
        #     continue
        # elif not delimiter:
        #     if char in separators:
        #         i += 1
        #         if token:
        #             tokens.append(token)
        #             token = ""
        #             separator = ''
        #         else:
        #             separator = char
        #         continue
        #     else:
        #         i += 1
        #         token += char
        # else:
        #     i += 1
        #     token += char
    if token:
        tokens.append(token)
        token = ""
    return tokens

def results(resultset, columns):
    results = []
    for record in resultset:
        row = {}
        for column in columns:
            row[column] = getattr(record, column)
        results.append(row)
    return results

def print_result(result, headers = []):
    if not isinstance(result,str):
        if not headers:
            headers =   [column["name"] for column in result.column_descriptions]   \
                            if hasattr(result, "column_descriptions")               \
                            else                                                    \
                        headers
            headers =   [column.name for column in result.cursor.description]       \
                            if hasattr(result, "cursor")                            \
                            else                                                    \
                        headers
        # if headers:
        tabulated = tabulate.tabulate(
            result,
            headers = headers,
            tablefmt= "grid",
            floatfmt= ".2f"
        )
        print(tabulated)
    else:
        print(result)