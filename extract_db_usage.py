#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project : IPRO Revisi Header Laporan Trading Term
"""
extract_db_usage.py

Extract database objects (tables, views, stored procedures, custom Oracle
functions) used by an ASP.NET MVC controller and the data-layer classes it
calls, then emit a Markdown file with the same structure as TransaksiCMO.md.

This script is intentionally kept modular so it can grow with new patterns
found in the codebase (EDMX entity usage, LINQ/EF calls, raw SQL, stored
procedure calls, custom function calls, subqueries, EXISTS, etc.).

Usage:
    python extract_db_usage.py \
        --controller "D:/.../MasterMainSupplierController.cs" \
        --output "D:/.../MasterMainSupplier.md" \
        --name "Master Main Supplier" \
        --url "/Transaction/MasterMainSupplier"

The database schema defaults to MCGDATA unless an explicit schema prefix is
found in the SQL text.
"""

import argparse
from collections import deque
from dataclasses import dataclass, field
import os
import re
import sys
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SCHEMA = "MCGDATA"
DATA_LAYER_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMMD.Data")

# project : IPRO Revisi Header Laporan Trading Term
# Oracle built-in functions that must NOT be listed as custom calls.
ORACLE_BUILTINS = {
    "abs", "add_months", "ascii", "avg", "cast", "ceil", "chr", "coalesce",
    "concat", "count", "current_date", "current_timestamp", "decode",
    "dense_rank", "dual", "exp", "extract", "floor", "greatest", "instr", "lag", "lead",
    "last_day", "least", "length", "lengthb", "listagg", "lpad", "ltrim", "lower", "max", "min", "mod",
    "months_between", "nvl", "nvl2", "rank", "regexp_like", "regexp_replace",
    "regexp_substr", "replace", "round", "row_number", "rpad", "rtrim",
    "sign", "soundex", "sqrt", "stddev", "substr", "sum", "sysdate", "systimestamp",
    "to_char", "to_date", "to_number", "translate", "trim", "trunc", "upper",
    "variance",
}

# Oracle namespaces and package prefixes whose members are built-in calls.
ORACLE_BUILTIN_NAMESPACE_NAMES = {"standard", "sys"}
ORACLE_BUILTIN_PACKAGE_PREFIXES = (
    "apex_",
    "dbms_",
    "htf",
    "htp",
    "owa_",
    "utl_",
)
# end project : IPRO Revisi Header Laporan Trading Term

# C# runtime method names that look like function calls in raw text but are not
# Oracle calls. These are used when a regex runs over raw C# rather than SQL.
CSHARP_METHOD_NOISE = {
    "parse", "tostring", "tolower", "toupper", "format", "contains", "count",
    "firstordefault", "split", "replace", "substring", "getstring", "getdecimal",
    "getint32", "getdatetime", "isdbnull", "equals", "orderby", "orderbydescending",
    "thenby", "thenbydescending", "distinct", "tolist", "skip", "take", "where",
    "select", "any", "first", "add", "clear", "trim", "execute", "executenonquery",
    "executereader", "executescalar", "open", "close", "addwithvalue", "add",
}

# Oracle built-in objects that must NOT be listed as tables/views.
ORACLE_BUILTIN_OBJECTS = {
    "dual", "sys", "system", "dba_users", "user_tables", "all_tables",
    "user_objects", "all_objects",
}

# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def strip_csharp_comments(text):
    """Remove C# comments while preserving string literals.

    Handles // line comments and /* */ block comments. Keeps SQL fragments that
    contain '--' or '/*' inside a string literal.
    """
    out = []
    i = 0
    n = len(text)
    state = "code"
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        nxt2 = text[i + 2] if i + 2 < n else ""
        if state == "code":
            if ch == '"':
                state = "string"
                out.append(ch)
                i += 1
                continue
            if ch == "@" and nxt == '"':
                state = "verbatim"
                out.append(ch)
                out.append(nxt)
                i += 2
                continue
            if ch == "@" and nxt == "$" and nxt2 == '"':
                state = "verbatim"
                out.append(ch)
                out.append(nxt)
                out.append(nxt2)
                i += 3
                continue
            if ch == "/" and nxt == "/":
                state = "line_comment"
                i += 2
                continue
            if ch == "/" and nxt == "*":
                state = "block_comment"
                i += 2
                continue
            out.append(ch)
            i += 1
            continue
        if state == "string":
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue
        if state == "verbatim":
            out.append(ch)
            if ch == '"' and nxt == '"':
                out.append(nxt)
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue
        if state == "line_comment":
            if ch == "\n":
                state = "code"
                out.append(ch)
            i += 1
            continue
        if state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "code"
                i += 2
                continue
            i += 1
            continue
    return "".join(out)


# project : IPRO Revisi Header Laporan Trading Term
def mask_csharp_non_code(text):
    """Blank C# comments and literals while preserving source positions.

    Call-graph matching must inspect executable identifiers only. Comments and
    string/character literals are replaced with spaces, while newlines remain
    intact so diagnostics and future source locations stay meaningful.
    """
    source = strip_csharp_comments(text)
    out = list(source)
    i = 0
    n = len(source)
    state = "code"

    def blank(index):
        if out[index] not in ("\n", "\r"):
            out[index] = " "

    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        nxt2 = source[i + 2] if i + 2 < n else ""

        if state == "code":
            if ch == "$" and nxt == "@" and nxt2 == '"':
                blank(i)
                blank(i + 1)
                blank(i + 2)
                state = "verbatim"
                i += 3
                continue
            if ch == "@" and nxt == '"':
                blank(i)
                blank(i + 1)
                state = "verbatim"
                i += 2
                continue
            if ch == "@" and nxt == "$" and nxt2 == '"':
                blank(i)
                blank(i + 1)
                blank(i + 2)
                state = "verbatim"
                i += 3
                continue
            if ch == '"':
                blank(i)
                state = "string"
                i += 1
                continue
            if ch == "'":
                blank(i)
                state = "char"
                i += 1
                continue
            i += 1
            continue

        if state == "string":
            blank(i)
            if ch == "\\" and i + 1 < n:
                blank(i + 1)
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue

        if state == "verbatim":
            blank(i)
            if ch == '"' and nxt == '"':
                blank(i + 1)
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue

        if state == "char":
            blank(i)
            if ch == "\\" and i + 1 < n:
                blank(i + 1)
                i += 2
                continue
            if ch == "'":
                state = "code"
            i += 1

    return "".join(out)
# end project : IPRO Revisi Header Laporan Trading Term


def walk_cs_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d.lower() not in ("bin", "obj", "node_modules")
        ]
        for filename in filenames:
            lowered = filename.lower()
            if lowered.endswith(".cs") and not lowered.endswith(".designer.cs"):
                yield os.path.join(dirpath, filename)


def normalize_name(name):
    """Strip schema prefixes, aliases, quotes, and normalize to uppercase."""
    name = name.strip()
    if not name:
        return ""
    # Keep only the part after the last dot if it looks like schema.object.
    if "." in name:
        name = name.split(".")[-1]
    # Remove quoting and trailing punctuation.
    name = name.strip("`\"'[];,")
    return name.upper()


def split_schema_and_name(name):
    name = name.strip().strip("`\"'[];,")
    if "." in name:
        schema, obj = name.split(".", 1)
        return schema.strip().upper(), obj.strip().upper()
    return DEFAULT_SCHEMA, name.upper()


# project : IPRO Revisi Header Laporan Trading Term
def split_dblink_name(name):
    """Return ``(object_name, dblink)`` from a normalized object label."""
    raw_name = str(name or "").strip().strip("`\"'[];,")
    if "@" not in raw_name:
        return raw_name, ""
    object_name, dblink = raw_name.rsplit("@", 1)
    if not object_name or not dblink:
        return raw_name, ""
    return object_name, dblink.strip("`\"'[];,").upper()
# end project : IPRO Revisi Header Laporan Trading Term


# project : IPRO Revisi Header Laporan Trading Term
@dataclass(frozen=True)
class SqlToken:
    kind: str
    value: str
    position: int
    depth: int


SQL_TOKEN_KEYWORDS = {
    "and", "as", "asc", "by", "case", "cross", "delete", "desc", "distinct",
    "else", "end", "exists", "from", "full", "group", "having", "in", "inner",
    "insert", "into", "join", "left", "like", "merge", "not", "null", "on",
    "or", "order", "outer", "select", "set", "then", "union", "update", "using",
    "values", "when", "where", "with", "between", "connect", "start", "prior",
    "matched", "returning",
}


def tokenize_sql(sql):
    """Tokenize the SQL subset needed by object/function extraction.

    Comments are discarded, quoted values are emitted as ``string`` tokens,
    quoted identifiers as ``quoted_identifier`` tokens, and every token keeps
    its parenthesis depth for nested-query scans.
    """
    tokens = []
    i = 0
    n = len(sql)
    depth = 0

    def append(kind, value, position, token_depth=None):
        tokens.append(
            SqlToken(kind, value, position, depth if token_depth is None else token_depth)
        )

    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""

        if ch.isspace():
            i += 1
            continue
        if ch == "-" and nxt == "-":
            i += 2
            while i < n and sql[i] not in "\r\n":
                i += 1
            continue
        if ch == "/" and nxt == "*":
            i += 2
            while i + 1 < n and sql[i:i + 2] != "*/":
                i += 1
            i += 2 if i + 1 < n else 0
            continue

        if ch == "'":
            start = i
            i += 1
            value = []
            while i < n:
                if sql[i] == "'" and i + 1 < n and sql[i + 1] == "'":
                    value.append("'")
                    i += 2
                    continue
                if sql[i] == "'":
                    i += 1
                    break
                value.append(sql[i])
                i += 1
            append("string", "".join(value), start)
            continue

        if ch in ('"', "`", "["):
            closing = "]" if ch == "[" else ch
            start = i
            i += 1
            value = []
            while i < n:
                if sql[i] == closing and i + 1 < n and sql[i + 1] == closing:
                    value.append(closing)
                    i += 2
                    continue
                if sql[i] == closing:
                    i += 1
                    break
                value.append(sql[i])
                i += 1
            append("quoted_identifier", "".join(value), start)
            continue

        if ch.isalpha() or ch in "_$#":
            start = i
            i += 1
            while i < n and (sql[i].isalnum() or sql[i] in "_$#"):
                i += 1
            value = sql[start:i]
            kind = "keyword" if value.lower() in SQL_TOKEN_KEYWORDS else "identifier"
            append(kind, value, start)
            continue

        if ch.isdigit():
            start = i
            i += 1
            while i < n and (sql[i].isalnum() or sql[i] in "._$#"):
                i += 1
            append("number", sql[start:i], start)
            continue

        token_depth = depth
        append("punctuation", ch, i, token_depth)
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        i += 1

    return tokens
# end project : IPRO Revisi Header Laporan Trading Term


# ---------------------------------------------------------------------------
# SQL extraction
# ---------------------------------------------------------------------------

# project : IPRO Revisi Header Laporan Trading Term
SQL_STATEMENT_STARTS = {
    "select", "insert", "update", "delete", "merge", "with",
}
# end project : IPRO Revisi Header Laporan Trading Term

# SQL words that must not be treated as custom functions or stored procedures.
SQL_FUNCTION_NOISE = {
    "select", "from", "where", "and", "or", "not", "in", "exists", "union",
    "union all", "insert", "into", "update", "delete", "values", "set", "on",
    "as", "by", "order", "group", "having", "case", "when", "then", "else",
    "end", "distinct", "top", "between", "like", "is", "null", "join",
    "inner", "left", "right", "outer", "full", "cross", "begin", "commit",
    "rollback", "transaction", "using", "for", "loop", "return", "declare",
    "begin", "if", "else", "end", "while", "break", "continue", "goto",
}


# project : IPRO Revisi Header Laporan Trading Term
def looks_like_sql(text):
    tokens = tokenize_sql(text)
    if not tokens:
        return False

    statement = tokens[0].value.lower()
    if statement not in SQL_STATEMENT_STARTS:
        return False
    if statement in {"insert", "merge"}:
        return len(tokens) > 1 and tokens[1].value.lower() == "into"
    if statement == "delete":
        return len(tokens) > 1 and tokens[1].value.lower() == "from"
    if statement == "update":
        return (
            len(tokens) > 2
            and _is_identifier_token(tokens[1])
            and any(token.value.lower() == "set" for token in tokens[2:])
        )
    return True
# end project : IPRO Revisi Header Laporan Trading Term


# project : IPRO Revisi Header Laporan Trading Term
def extract_csharp_string_literals(text, with_spans=False):
    """Yield C# string literals, optionally including source spans."""
    literals = []
    i = 0
    n = len(text)
    state = "code"
    current = []
    literal_start = None

    def start_literal(kind, index, start):
        nonlocal state, current, i, literal_start
        state = kind
        current = []
        i = index
        literal_start = start

    def finish_literal(end):
        value = "".join(current)
        if with_spans:
            literals.append((literal_start, end, value))
        else:
            literals.append(value)

    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        nxt2 = text[i + 2] if i + 2 < n else ""

        if state == "code":
            if ch == "/" and nxt == "/":
                i += 2
                while i < n and text[i] not in "\r\n":
                    i += 1
                continue
            if ch == "/" and nxt == "*":
                i += 2
                while i + 1 < n and text[i:i + 2] != "*/":
                    i += 1
                i += 2 if i + 1 < n else 0
                continue
            if ch == "$" and nxt == "@" and nxt2 == '"':
                start_literal("verbatim", i + 3, i)
                continue
            if ch == "@" and nxt == "$" and nxt2 == '"':
                start_literal("verbatim", i + 3, i)
                continue
            if ch == "@" and nxt == '"':
                start_literal("verbatim", i + 2, i)
                continue
            if ch == '$' and nxt == '"':
                start_literal("regular", i + 2, i)
                continue
            if ch == '"':
                start_literal("regular", i + 1, i)
                continue
            if ch == "'":
                state = "char"
                i += 1
                continue
            i += 1
            continue

        if state == "regular":
            if ch == "\\" and i + 1 < n:
                escaped = text[i + 1]
                escape_map = {
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                    "b": "\b",
                    "f": "\f",
                    "v": "\v",
                    "0": "\0",
                }
                current.append(escape_map.get(escaped, escaped))
                i += 2
                continue
            if ch == '"':
                finish_literal(i + 1)
                state = "code"
                i += 1
                continue
            current.append(ch)
            i += 1
            continue

        if state == "verbatim":
            if ch == '"' and nxt == '"':
                current.append('"')
                i += 2
                continue
            if ch == '"':
                finish_literal(i + 1)
                state = "code"
                i += 1
                continue
            current.append(ch)
            i += 1
            continue

        if state == "char":
            if ch == "\\" and i + 1 < n:
                i += 2
                continue
            if ch == "'":
                state = "code"
            i += 1

    for literal in literals:
        yield literal


def _is_csharp_string_concatenation(source):
    """Return true when two literals belong to one ``+`` expression."""
    if re.fullmatch(r"\s*\+\s*", source, flags=re.DOTALL):
        return True
    return bool(
        re.fullmatch(
            r"\s*\+\s*[^;{}]*?\s*\+\s*",
            source,
            flags=re.DOTALL,
        )
    )


def extract_sql_literals(text):
    """Yield SQL-looking C# string expressions without duplicate matches."""
    csharp_fragment = re.compile(
        r'^(?:var|return|using|foreach|catch|throw|try|finally)\b'
        r'|\b(?:if|for|while)\s*\(|\.Where\s*\(|\.ForEach\s*\(',
        flags=re.IGNORECASE,
    )

    literals = list(extract_csharp_string_literals(text, with_spans=True))
    consumed = set()
    for index, (start, end, literal) in enumerate(literals):
        if index in consumed:
            continue

        fragments = [literal]
        last_end = end
        next_index = index + 1
        while next_index < len(literals):
            next_start, next_end, next_literal = literals[next_index]
            if not _is_csharp_string_concatenation(text[last_end:next_start]):
                break
            fragments.append(next_literal)
            consumed.add(next_index)
            last_end = next_end
            next_index += 1

        candidate = "".join(fragments)
        if not csharp_fragment.search(candidate.strip()) and looks_like_sql(candidate):
            yield candidate
# end project : IPRO Revisi Header Laporan Trading Term


# project : IPRO Revisi Header Laporan Trading Term
def _is_identifier_token(token):
    return token.kind in ("identifier", "quoted_identifier")


def _normalize_sql_identifier(value):
    return value.strip().strip("`\"'[];, ").upper()


def _read_qualified_identifier(tokens, start):
    """Read ``schema.object[@dblink]`` from a token position."""
    if start >= len(tokens) or not _is_identifier_token(tokens[start]):
        return None, start

    parts = [tokens[start].value]
    index = start + 1
    while (
        index + 1 < len(tokens)
        and tokens[index].kind == "punctuation"
        and tokens[index].value == "."
        and _is_identifier_token(tokens[index + 1])
    ):
        parts.append(tokens[index + 1].value)
        index += 2

    if len(parts) == 1:
        schema = DEFAULT_SCHEMA
        name = _normalize_sql_identifier(parts[0])
        qualified = False
    else:
        schema = _normalize_sql_identifier(parts[-2])
        name = _normalize_sql_identifier(parts[-1])
        qualified = True

    if (
        index + 1 < len(tokens)
        and tokens[index].value == "@"
        and _is_identifier_token(tokens[index + 1])
    ):
        dblink = _normalize_sql_identifier(tokens[index + 1].value)
        name = f"{name}@{dblink}"
        index += 2
    return (schema, name, qualified), index


def _matching_parenthesis(tokens, start):
    if start >= len(tokens) or tokens[start].value != "(":
        return start
    opening_depth = tokens[start].depth
    for index in range(start + 1, len(tokens)):
        token = tokens[index]
        if token.value == ")" and token.depth == opening_depth + 1:
            return index
    return len(tokens) - 1


def _extract_cte_definitions(sql_or_tokens):
    """Return ``(name, body_start, body_end)`` token ranges for CTEs."""
    tokens = tokenize_sql(sql_or_tokens) if isinstance(sql_or_tokens, str) else sql_or_tokens
    definitions = []

    for with_index, token in enumerate(tokens):
        if token.value.lower() != "with":
            continue
        base_depth = token.depth
        index = with_index + 1
        if index < len(tokens) and tokens[index].value.lower() == "recursive":
            index += 1

        while index < len(tokens):
            if tokens[index].depth != base_depth or not _is_identifier_token(tokens[index]):
                break
            cte_name = _normalize_sql_identifier(tokens[index].value)
            index += 1

            if index < len(tokens) and tokens[index].value == "(":
                index = _matching_parenthesis(tokens, index) + 1
            if index >= len(tokens) or tokens[index].value.lower() != "as":
                break
            index += 1
            if index >= len(tokens) or tokens[index].value != "(":
                break

            opening = index
            closing = _matching_parenthesis(tokens, opening)
            definitions.append((cte_name, opening + 1, closing))
            index = closing + 1
            if (
                index < len(tokens)
                and tokens[index].value == ","
                and tokens[index].depth == base_depth
            ):
                index += 1
                continue
            break

    return definitions


def extract_cte_names(sql_or_tokens):
    """Return logical CTE names declared by one or more WITH clauses."""
    return {name for name, _start, _end in _extract_cte_definitions(sql_or_tokens)}


def _add_sql_object(found, schema, name):
    object_name, _dblink = split_dblink_name(name)
    lowered = object_name.lower() if object_name else ""
    if not name or lowered in ORACLE_BUILTIN_OBJECTS or lowered in ORACLE_BUILTINS:
        return
    found.setdefault(name, set()).add(schema)


def _iter_source_identifiers(tokens, keyword_index):
    index = keyword_index + 1
    if index >= len(tokens) or tokens[index].value == "(":
        return

    while index < len(tokens):
        parsed, next_index = _read_qualified_identifier(tokens, index)
        if parsed is None:
            return
        yield parsed
        index = next_index

        # Skip a source alias before checking for a comma-separated source.
        if index < len(tokens) and tokens[index].value.lower() == "as":
            index += 2
        elif index < len(tokens) and _is_identifier_token(tokens[index]):
            index += 1
        if index >= len(tokens) or tokens[index].value != ",":
            return
        index += 1
        if index >= len(tokens) or tokens[index].value == "(":
            return


def _add_source_after_keyword(tokens, keyword_index, cte_names, found):
    for schema, name, qualified in _iter_source_identifiers(tokens, keyword_index):
        if not (name in cte_names and not qualified):
            _add_sql_object(found, schema, name)


def _extract_sql_object_ops_tokens(tokens, cte_names=None):
    cte_names = set(cte_names or extract_cte_names(tokens))
    read = {}
    write = {}
    delete_target_from = set()

    for index, token in enumerate(tokens):
        lowered = token.value.lower()
        next_value = tokens[index + 1].value.lower() if index + 1 < len(tokens) else ""

        if lowered in ("insert", "merge") and next_value == "into":
            _add_source_after_keyword(tokens, index + 1, cte_names, write)
        elif lowered == "update":
            _add_source_after_keyword(tokens, index, cte_names, write)
        elif lowered == "delete" and next_value == "from":
            delete_target_from.add(index + 1)
            _add_source_after_keyword(tokens, index + 1, cte_names, write)

    for index, token in enumerate(tokens):
        if token.value.lower() not in ("from", "join", "using"):
            continue
        if index in delete_target_from:
            continue
        _add_source_after_keyword(tokens, index, cte_names, read)

    return read, write


def extract_sql_object_ops(sql):
    """Return ``(read, write)`` table maps from token-aware SQL scanning."""
    return _extract_sql_object_ops_tokens(tokenize_sql(sql))


# end project : IPRO Revisi Header Laporan Trading Term
# project : IPRO Revisi Header Laporan Trading Term
def _source_cte_references(tokens, cte_names):
    references = set()
    for index, token in enumerate(tokens):
        if token.value.lower() not in ("from", "join", "using"):
            continue
        for _schema, name, qualified in _iter_source_identifiers(tokens, index):
            if name in cte_names and not qualified:
                references.add(name)
    return references


def extract_cte_relations(sql):
    """Return logical CTE relations with physical reads and consumers."""
    tokens = tokenize_sql(sql)
    definitions = _extract_cte_definitions(tokens)
    relations = {
        name: CteRelation(name=name)
        for name, _start, _end in definitions
    }
    cte_names = set(relations)

    for name, body_start, body_end in definitions:
        body_tokens = tokens[body_start:body_end]
        reads, _writes = _extract_sql_object_ops_tokens(body_tokens, cte_names)
        relations[name].physical_reads = {
            PhysicalObject(
                schema=schema,
                name=normalize_name(split_dblink_name(object_name)[0]),
                dblink=split_dblink_name(object_name)[1],
            )
            for object_name, schemas in reads.items()
            for schema in schemas
        }
        dependencies = _source_cte_references(body_tokens, cte_names) - {name}
        relations[name].cte_dependencies = dependencies
        for dependency in dependencies:
            if dependency in relations:
                relations[dependency].consumers.add(name)

    if definitions:
        outer_tokens = tokens[definitions[-1][2] + 1:]
        for consumer in _source_cte_references(outer_tokens, cte_names):
            relations[consumer].consumers.add("OUTER_QUERY")

    return relations
# end project : IPRO Revisi Header Laporan Trading Term


# project : IPRO Revisi Header Laporan Trading Term
def extract_tables_from_sql(sql):
    """Return all physical objects from SQL, preserving schema identity."""
    read, write = extract_sql_object_ops(sql)
    found = {}
    for source in (read, write):
        for name, schemas in source.items():
            found.setdefault(name, set()).update(schemas)
    return found
# end project : IPRO Revisi Header Laporan Trading Term


def _starts_with_dml(sql):
    """True if the SQL string starts with a DML/query keyword.

    This keeps function extraction focused on actual SQL statements and avoids
    filenames or prose that happen to contain SQL-looking words.
    """
    tokens = tokenize_sql(sql)
    return bool(tokens and tokens[0].value.lower() in {
        "select", "insert", "update", "delete", "merge", "with"
    })


# project : IPRO Revisi Header Laporan Trading Term
def _is_old_style_outer_join_operand(tokens, index, parts):
    """Return true for a qualified column followed by the Oracle ``(+)`` marker."""
    if len(parts) < 2 or index + 3 >= len(tokens):
        return False
    return (
        tokens[index + 1].value == "("
        and tokens[index + 2].value == "+"
        and tokens[index + 3].value == ")"
    )


def _is_oracle_builtin_parts(parts):
    """Return true when a qualified name belongs to Oracle built-ins."""
    normalized = [str(part).strip().lower() for part in parts if str(part).strip()]
    if not normalized:
        return False
    if normalized[-1] in ORACLE_BUILTINS:
        return True
    return any(
        part in ORACLE_BUILTIN_NAMESPACE_NAMES
        or any(part.startswith(prefix) for prefix in ORACLE_BUILTIN_PACKAGE_PREFIXES)
        for part in normalized[:-1]
    )
# end project : IPRO Revisi Header Laporan Trading Term


def extract_functions_from_sql(sql):
    """Return qualified custom Oracle function calls found in SQL."""
    funcs = set()
    if not _starts_with_dml(sql):
        return funcs

    tokens = tokenize_sql(sql)
    for index, token in enumerate(tokens):
        if not _is_identifier_token(token):
            continue
        if index + 1 >= len(tokens) or tokens[index + 1].value != "(":
            continue
        parts = [token.value]
        start = index
        while (
            start >= 2
            and tokens[start - 1].kind == "punctuation"
            and tokens[start - 1].value == "."
            and _is_identifier_token(tokens[start - 2])
        ):
            parts.insert(0, tokens[start - 2].value)
            start -= 2

        if start > 0 and tokens[start - 1].value.lower() in {
            "from", "into", "join", "table", "update", "using",
        }:
            continue

        if _is_old_style_outer_join_operand(tokens, index, parts):
            continue

        name = ".".join(_normalize_sql_identifier(part) for part in parts)
        lowered = parts[-1].lower()
        if _is_oracle_builtin_parts(parts):
            continue
        if lowered in CSHARP_METHOD_NOISE:
            continue
        if lowered in SQL_FUNCTION_NOISE:
            continue
        funcs.add(name)
    return funcs


def _oracle_command_arguments(text):
    """Yield ``(argument, is_literal)`` for command constructors/assignments."""
    source = strip_csharp_comments(text)
    literal = re.compile(
        r'(?:\$?@|@?\$)?"(?:""|\\.|[^"\\])*"',
        flags=re.DOTALL,
    )

    prefixes = (
        (re.compile(r'new\s+OracleCommand\s*\(\s*', flags=re.IGNORECASE), ",)\r\n"),
        (re.compile(r'\.CommandText\s*=\s*', flags=re.IGNORECASE), ";\r\n"),
    )
    for prefix, delimiters in prefixes:
        for match in prefix.finditer(source):
            start = match.end()
            literal_match = literal.match(source, start)
            if literal_match:
                value = next(extract_csharp_string_literals(literal_match.group(0)), "")
                if re.match(r'\s*\+', source[literal_match.end():]):
                    yield source[start:literal_match.end()].strip(), False
                else:
                    yield value, True
                continue
            end = start
            while end < len(source) and source[end] not in delimiters:
                end += 1
            yield source[start:end].strip(), False


def _is_simple_procedure_name(name):
    name = name.strip()
    if not name or _starts_with_dml(name):
        return False
    if _is_oracle_builtin_parts(name.split(".")):
        return False
    if name.lower() in SQL_FUNCTION_NOISE:
        return False
    return bool(re.fullmatch(
        r'[A-Za-z_][A-Za-z0-9_$#]*(?:\.[A-Za-z_][A-Za-z0-9_$#]*)*',
        name,
    ))


def extract_procedures_from_text(text):
    """Return stored procedure names from literal command values."""
    procs = set()
    for name, is_literal in _oracle_command_arguments(text):
        if is_literal and _is_simple_procedure_name(name):
            procs.add(name.strip())
    return procs


def extract_dynamic_procedure_messages(text):
    """Return messages for OracleCommand values that cannot be resolved."""
    return [
        "OracleCommand procedure argument is dynamic: " + (argument or "<empty>")
        for argument, is_literal in _oracle_command_arguments(text)
        if not is_literal
    ]


def extract_dynamic_sql_messages(text):
    """Return messages for SQL-looking literals concatenated with variables."""
    source = strip_csharp_comments(text)
    literal = r'(?:\$?@|@?\$)?"(?:""|\\.|[^"\\])*"'
    messages = []
    patterns = (
        re.compile(literal + r'\s*\+\s*[A-Za-z_]\w*', flags=re.DOTALL),
        re.compile(r'[A-Za-z_]\w*\s*\+\s*' + literal, flags=re.DOTALL),
    )
    for pattern in patterns:
        for match in pattern.finditer(source):
            literal_text = next(extract_csharp_string_literals(match.group(0)), "")
            if looks_like_sql(literal_text):
                messages.append(
                    "SQL literal is concatenated with a dynamic value: " + literal_text
                )
    return sorted(set(messages))


def extract_table_ops_from_text(text):
    """Return (read_tables, write_tables) from raw SQL literals in text."""
    read = {}
    write = {}

    for sql in extract_sql_literals(text):
        sql_read, sql_write = extract_sql_object_ops(sql)
        for name, schemas in sql_read.items():
            read.setdefault(name, set()).update(schemas)
        for name, schemas in sql_write.items():
            write.setdefault(name, set()).update(schemas)

    return read, write


# project : IPRO Revisi Header Laporan Trading Term
def extract_ef_entity_usage(text):
    """Return entity names used for EF reads and writes."""
    source = strip_csharp_comments(text)
    code = mask_csharp_non_code(text)
    reads = set(re.findall(
        r'CurrentDataContext\.CurrentContext\.([A-Za-z_]\w*)',
        code,
    ))
    writes = set(re.findall(
        r'\.(?:InsertSave|UpdateSave|Delete)\s*<\s*([A-Za-z_]\w*)\s*>',
        code,
        flags=re.IGNORECASE,
    ))
    writes.update(re.findall(
        r'CurrentDataContext\.CurrentContext\.(?:AddObject)\s*\(\s*["\']([A-Za-z_]\w*)["\']',
        source,
        flags=re.IGNORECASE,
    ))
    writes.update(re.findall(
        r'CurrentDataContext\.CurrentContext\.([A-Za-z_]\w*)\s*\.(?:Add|Remove|Attach)\s*\(',
        code,
        flags=re.IGNORECASE,
    ))
    return reads, writes
# end project : IPRO Revisi Header Laporan Trading Term


# ---------------------------------------------------------------------------
# EDMX mapping
# ---------------------------------------------------------------------------

# project : IPRO Revisi Header Laporan Trading Term
def _xml_local_name(value):
    return value.rsplit("}", 1)[-1].split(":")[-1]


def _xml_attribute(element, name):
    if name in element.attrib:
        return element.attrib[name]
    expected = name.lower()
    for key, value in element.attrib.items():
        if _xml_local_name(key).lower() == expected:
            return value
    return ""


def _xml_namespaced_attribute(element, name):
    expected = name.lower()
    for key, value in element.attrib.items():
        if key.startswith("{") and _xml_local_name(key).lower() == expected:
            return value
    return ""


def _is_store_entity_type(entity_type):
    lowered = entity_type.lower()
    return ".store." in lowered or lowered.startswith("store.")


def _parse_edmx_entity_map(edmx_path, diagnostics=None):
    """Return conceptual entity -> ``(physical_schema, physical_name)``."""
    mapping = {}
    text = read_file(edmx_path)
    if not text:
        if diagnostics is not None and os.path.exists(edmx_path):
            diagnostics.append(Diagnostic(
                "EDMX_UNREADABLE",
                "EDMX input cannot be read: " + edmx_path,
                "error",
            ))
        return mapping

    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        if diagnostics is not None:
            diagnostics.append(Diagnostic(
                "EDMX_INVALID",
                "EDMX input is not valid XML: " + edmx_path,
                "error",
            ))
        return mapping

    for element in root.iter():
        if _xml_local_name(element.tag).lower() != "entityset":
            continue
        entity_type = _xml_attribute(element, "EntityType")
        if not _is_store_entity_type(entity_type):
            continue
        entity_name = _xml_attribute(element, "Name")
        physical_name = _xml_namespaced_attribute(element, "Name") or entity_name
        schema = (
            _xml_namespaced_attribute(element, "Schema")
            or _xml_attribute(element, "Schema")
            or DEFAULT_SCHEMA
        )
        normalized_name = normalize_name(entity_name)
        if normalized_name:
            mapping[normalized_name] = (
                schema.strip().upper(),
                normalize_name(physical_name) or normalized_name,
            )

    return mapping


def parse_edmx_entity_map(edmx_path, diagnostics=None):
    return _parse_edmx_entity_map(edmx_path, diagnostics)


def parse_edmx_schema_map(edmx_path, diagnostics=None):
    """Map conceptual entity names to their store schema.

    Returns a dict like {"T_CABANG": "MCGDATA", ...}. The richer
    ``parse_edmx_entity_map`` API additionally preserves physical store names.
    """
    return {
        entity: schema_and_name[0]
        for entity, schema_and_name in _parse_edmx_entity_map(edmx_path, diagnostics).items()
    }
# end project : IPRO Revisi Header Laporan Trading Term


# ---------------------------------------------------------------------------
# C# method extraction
# ---------------------------------------------------------------------------

# project : IPRO Revisi Header Laporan Trading Term
METHOD_SIGNATURE = re.compile(
    r'(?:(?:public|private|protected|internal)\s+)+'
    r'(?:static\s+)?'
    r'(?P<return_type>[\w<>,\[\]\.\s?]+?)\s+'
    r'(?P<name>[A-Za-z_]\w*)\s*'
    r'\((?P<parameters>[^()]*)\)\s*'
    r'\{'
)
# end project : IPRO Revisi Header Laporan Trading Term


def find_matching_brace(text, start):
    """Given text with '{' at start, return index after the matching '}'."""
    depth = 0
    state = "code"
    i = start
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        nxt2 = text[i + 2] if i + 2 < len(text) else ""
        if state == "line_comment":
            if ch == "\n":
                state = "code"
            i += 1
            continue
        if state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "code"
                i += 2
                continue
            i += 1
            continue
        if state == "string":
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue
        if state == "verbatim_string":
            if ch == '"' and nxt == '"':
                i += 2
                continue
            if ch == '"':
                state = "code"
            i += 1
            continue
        if state == "char":
            if ch == "\\":
                i += 2
                continue
            if ch == "'":
                state = "code"
            i += 1
            continue
        if ch == "/" and nxt == "/":
            state = "line_comment"
            i += 2
            continue
        if ch == "/" and nxt == "*":
            state = "block_comment"
            i += 2
            continue
        if ch == "@" and nxt == '"':
            state = "verbatim_string"
            i += 2
            continue
        if ch == "@" and nxt == "$" and nxt2 == '"':
            state = "verbatim_string"
            i += 3
            continue
        if ch == '"':
            state = "string"
            i += 1
            continue
        if ch == "'":
            state = "char"
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def extract_method_bodies(text):
    """Extract static method bodies keyed by method name.

    Returns a dict: method_name -> list of method body strings.
    """
    methods = {}
    for definition in extract_method_definitions(text):
        methods.setdefault(definition.name, []).append(definition.body)
    return methods


# project : IPRO Revisi Header Laporan Trading Term
@dataclass(frozen=True)
class MethodDefinition:
    name: str
    body: str
    start: int
    end: int
    return_type: str = ""
# end project : IPRO Revisi Header Laporan Trading Term


# project : IPRO Revisi Header Laporan Trading Term
def extract_method_definitions(text):
    source = strip_csharp_comments(text)
    masked = mask_csharp_non_code(text)
    definitions = []
    for match in METHOD_SIGNATURE.finditer(masked):
        brace = masked.find("{", match.start())
        if brace < 0:
            continue
        end = find_matching_brace(source, brace)
        definitions.append(
            MethodDefinition(
                match.group("name"),
                source[brace:end],
                match.start(),
                end,
                match.group("return_type").strip(),
            )
        )
    return definitions
# end project : IPRO Revisi Header Laporan Trading Term


# ---------------------------------------------------------------------------
# Entity / data-layer indexing
# ---------------------------------------------------------------------------

CLASS_DECLARATION = re.compile(r'\bclass\s+([A-Za-z_]\w*)\b')


@dataclass(frozen=True)
class ClassSpan:
    name: str
    start: int
    end: int


def extract_class_spans(text):
    source = strip_csharp_comments(text)
    masked = mask_csharp_non_code(text)
    spans = []
    for match in CLASS_DECLARATION.finditer(masked):
        brace = masked.find("{", match.end())
        if brace < 0:
            continue
        end = find_matching_brace(source, brace)
        spans.append(ClassSpan(match.group(1), match.start(), end))
    return spans


# project : IPRO Revisi Header Laporan Trading Term
def index_data_layer(root, include_metadata=False):
    """Index data-layer C# files by class name.

    Returns (class_files, class_methods).

    class_files:   class_name -> set(file_paths)
    class_methods: class_name -> { method_name -> list(bodies) }
    """
    class_files = {}
    class_methods = {}
    class_method_definitions = {}

    for path in walk_cs_files(root):
        text = strip_csharp_comments(read_file(path))
        if not text:
            continue
        classes = extract_class_spans(text)
        methods = extract_method_definitions(text)

        for cls in classes:
            class_files.setdefault(cls.name, set()).add(path)
            class_methods.setdefault(cls.name, {})
            class_method_definitions.setdefault(cls.name, {})

        for method in methods:
            containers = [
                cls for cls in classes
                if cls.start <= method.start and method.end <= cls.end
            ]
            if not containers:
                continue
            owner = min(containers, key=lambda cls: cls.end - cls.start)
            class_methods[owner.name].setdefault(method.name, []).append(method.body)
            class_method_definitions[owner.name].setdefault(method.name, []).append(method)

    if include_metadata:
        return class_files, class_methods, class_method_definitions
    return class_files, class_methods
# end project : IPRO Revisi Header Laporan Trading Term


# ---------------------------------------------------------------------------
# Static data-layer method call extraction from controller text
# ---------------------------------------------------------------------------

STATIC_CALL = re.compile(r'\b([A-Za-z_]\w*)\s*\.\s*([A-Za-z_]\w*)\s*\(')


# project : IPRO Revisi Header Laporan Trading Term
def _known_data_layer_type(type_text, class_files):
    candidates = re.findall(r'[A-Za-z_]\w*', type_text or "")
    known = {candidate for candidate in candidates if candidate in class_files}
    return next(iter(known)) if len(known) == 1 else None


def build_method_return_types(class_method_definitions, class_files):
    """Return unambiguous data-layer return types by class and method."""
    return_types = {}
    for class_name, methods in class_method_definitions.items():
        for method_name, definitions in methods.items():
            known = set()
            for definition in definitions:
                data_layer_type = _known_data_layer_type(
                    definition.return_type,
                    class_files,
                )
                if data_layer_type:
                    known.add(data_layer_type)
            if len(known) == 1:
                return_types.setdefault(class_name, {})[method_name] = next(iter(known))
    return return_types


VARIABLE_ASSIGNMENT = re.compile(
    r'\b(?:(?P<declared_type>[A-Za-z_]\w*)\s+)?'
    r'(?P<variable>[A-Za-z_]\w*)\s*=\s*(?P<value>[^;\r\n]+)'
)


def infer_instance_receiver_types(
    text,
    class_files,
    method_return_types=None,
    current_class=None,
):
    """Infer local receiver types conservatively from source assignments."""
    receiver_types = {}
    if current_class in class_files:
        receiver_types["this"] = current_class

    method_return_types = method_return_types or {}
    masked = mask_csharp_non_code(text)
    for match in VARIABLE_ASSIGNMENT.finditer(masked):
        declared_type = match.group("declared_type")
        variable = match.group("variable")
        value = match.group("value")
        inferred = _known_data_layer_type(declared_type, class_files)

        if not inferred:
            new_match = re.match(r'\s*new\s+([A-Za-z_]\w*)\b', value)
            if new_match:
                inferred = _known_data_layer_type(new_match.group(1), class_files)

        if not inferred:
            static_match = re.match(
                r'\s*([A-Za-z_]\w*)\s*\.\s*([A-Za-z_]\w*)\s*\(',
                value,
            )
            if static_match:
                called_class = static_match.group(1)
                called_method = static_match.group(2)
                if called_class in class_files:
                    inferred = method_return_types.get(called_class, {}).get(
                        called_method
                    )

        if inferred:
            receiver_types[variable] = inferred

    return receiver_types


INSTANCE_CALL = re.compile(
    r'\b(?P<receiver>this|[A-Za-z_]\w*)\s*\.\s*'
    r'(?P<method>[A-Za-z_]\w*)\s*\('
)
INSTANCE_WRITE_METHOD_NAMES = frozenset(
    {
        "delete",
        "deleted",
        "insert",
        "inserted",
        "save",
        "saved",
        "update",
        "updated",
    }
)


def extract_instance_data_layer_calls(
    text,
    class_files,
    method_return_types=None,
    current_class=None,
    diagnostics=None,
):
    """Return proven instance data-layer calls and report write-like misses."""
    receiver_types = infer_instance_receiver_types(
        text,
        class_files,
        method_return_types=method_return_types,
        current_class=current_class,
    )
    calls = set()
    masked = mask_csharp_non_code(text)
    for match in INSTANCE_CALL.finditer(masked):
        receiver = match.group("receiver")
        method = match.group("method")
        class_name = receiver_types.get(receiver)
        if class_name in class_files:
            calls.add((class_name, method))
        elif (
            diagnostics is not None
            and not receiver[:1].isupper()
            and method.lower() in INSTANCE_WRITE_METHOD_NAMES
        ):
            diagnostics.add_diagnostic(
                "UNRESOLVED_INSTANCE_RECEIVER",
                "Instance data-layer receiver cannot be proven: {}.{}".format(
                    receiver,
                    method,
                ),
            )
    return calls
# end project : IPRO Revisi Header Laporan Trading Term


def extract_data_layer_calls(text, class_files):
    """Return list of (class_name, method_name) for known data-layer classes."""
    calls = set()
    masked = mask_csharp_non_code(text)
    for m in STATIC_CALL.finditer(masked):
        cls = m.group(1)
        method = m.group(2)
        if cls in class_files:
            calls.add((cls, method))
    return calls


# ---------------------------------------------------------------------------
# Analyzer
# ---------------------------------------------------------------------------

# project : IPRO Revisi Header Laporan Trading Term
@dataclass(frozen=True)
class PhysicalObject:
    schema: str
    name: str
    kind: str = "unknown"
    dblink: str = ""

    def __post_init__(self):
        object.__setattr__(self, "dblink", str(self.dblink or "").strip().upper())

    @property
    def label(self):
        suffix = f"@{self.dblink}" if self.dblink else ""
        return f"{self.schema}.{self.name}{suffix}"


@dataclass(frozen=True)
class DatabaseCall:
    schema: str
    name: str
    kind: str = "unknown"

    @property
    def label(self):
        return f"{self.schema}.{self.name}"


@dataclass
class CteRelation:
    name: str
    physical_reads: set = field(default_factory=set)
    cte_dependencies: set = field(default_factory=set)
    consumers: set = field(default_factory=set)


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    severity: str = "warning"


class DbUsage:
    def __init__(self, schema_map):
        self.schema_map = {}
        self.entity_map = {}
        for entity, schema in schema_map.items():
            normalized_entity = normalize_name(entity)
            if not normalized_entity or not schema:
                continue
            if isinstance(schema, dict):
                schema_name = schema.get("schema", DEFAULT_SCHEMA)
                physical_name = schema.get("name", normalized_entity)
            elif isinstance(schema, (tuple, list)) and len(schema) >= 2:
                schema_name, physical_name = schema[0], schema[1]
            else:
                schema_name, physical_name = schema, normalized_entity
            self.schema_map[normalized_entity] = str(schema_name).strip().upper()
            self.entity_map[normalized_entity] = (
                self.schema_map[normalized_entity],
                normalize_name(physical_name) or normalized_entity,
            )
        self.read = set()
        self.write = set()
        self.calls = set()
        self.ctes = {}
        self.diagnostics = []
        self._diagnostic_keys = set()

    @staticmethod
    def _schema(schema):
        return (schema or DEFAULT_SCHEMA).strip().upper()

    def add_read(self, name, schema=DEFAULT_SCHEMA, kind="unknown"):
        if name:
            object_name, dblink = split_dblink_name(name)
            normalized = normalize_name(object_name)
            if normalized:
                self.read.add(
                    PhysicalObject(self._schema(schema), normalized, kind, dblink)
                )

    def add_write(self, name, schema=DEFAULT_SCHEMA, kind="unknown"):
        if name:
            object_name, dblink = split_dblink_name(name)
            normalized = normalize_name(object_name)
            if normalized:
                self.write.add(
                    PhysicalObject(self._schema(schema), normalized, kind, dblink)
                )

    def add_call(self, name, schema=DEFAULT_SCHEMA, kind="unknown"):
        if name:
            raw_name = str(name).strip().strip("`\"'[];,")
            call_schema = self._schema(schema)
            parts = [
                _normalize_sql_identifier(part)
                for part in raw_name.split(".")
                if _normalize_sql_identifier(part)
            ]
            if len(parts) > 1 and call_schema == DEFAULT_SCHEMA:
                call_schema = parts[0]
                normalized = ".".join(parts[1:])
            else:
                normalized = ".".join(parts)
            if normalized:
                self.calls.add(DatabaseCall(call_schema, normalized, kind))

    def add_table_dict(self, schemas_by_name, is_write):
        for name, schemas in schemas_by_name.items():
            for schema in schemas:
                if is_write:
                    self.add_write(name, schema)
                else:
                    self.add_read(name, schema)

    def add_entity(self, entity, is_write=False):
        name = normalize_name(entity)
        if not name:
            return
        if name not in self.entity_map:
            self.add_diagnostic(
                "EDMX_MAPPING_MISSING",
                "Entity has no EDMX physical mapping: " + name,
            )
        schema, physical_name = self.entity_map.get(
            name,
            (self.schema_map.get(name, DEFAULT_SCHEMA), name),
        )
        if is_write:
            self.add_write(physical_name, schema)
        else:
            self.add_read(physical_name, schema)

    def add_cte(self, name, physical_reads=None, cte_dependencies=None, consumers=None):
        normalized = normalize_name(name)
        if not normalized:
            return
        relation = self.ctes.setdefault(normalized, CteRelation(normalized))
        for physical_read in physical_reads or set():
            if isinstance(physical_read, PhysicalObject):
                relation.physical_reads.add(physical_read)
            elif isinstance(physical_read, (tuple, list)) and len(physical_read) >= 2:
                object_name, dblink = split_dblink_name(physical_read[1])
                physical_name = normalize_name(object_name)
                if not physical_name:
                    continue
                relation.physical_reads.add(
                    PhysicalObject(
                        self._schema(physical_read[0]),
                        physical_name,
                        physical_read[2] if len(physical_read) > 2 else "unknown",
                        dblink,
                    )
                )
        relation.cte_dependencies.update(
            normalize_name(dependency)
            for dependency in (cte_dependencies or set())
            if normalize_name(dependency)
        )
        relation.consumers.update(
            normalize_name(consumer)
            for consumer in (consumers or set())
            if normalize_name(consumer)
        )

    def add_diagnostic(self, code, message, severity="warning"):
        key = (code, message, severity)
        if key not in self._diagnostic_keys:
            self._diagnostic_keys.add(key)
            self.diagnostics.append(Diagnostic(code, message, severity))

    def add_raw_text(self, text):
        sql_literals = list(extract_sql_literals(text))
        read = {}
        write = {}
        for sql in sql_literals:
            sql_read, sql_write = extract_sql_object_ops(sql)
            for name, schemas in sql_read.items():
                read.setdefault(name, set()).update(schemas)
            for name, schemas in sql_write.items():
                write.setdefault(name, set()).update(schemas)
        self.add_table_dict(read, False)
        self.add_table_dict(write, True)
        for sql in sql_literals:
            for relation in extract_cte_relations(sql).values():
                self.add_cte(
                    relation.name,
                    physical_reads=relation.physical_reads,
                    cte_dependencies=relation.cte_dependencies,
                    consumers=relation.consumers,
                )
        ef_reads, ef_writes = extract_ef_entity_usage(text)
        for entity in ef_reads:
            self.add_entity(entity, is_write=False)
        for entity in ef_writes:
            self.add_entity(entity, is_write=True)
        for proc in extract_procedures_from_text(text):
            self.add_call(proc)
        functions = set()
        for sql in sql_literals:
            functions.update(extract_functions_from_sql(sql))
        for func in functions:
            self.add_call(func)
        for message in extract_dynamic_procedure_messages(text):
            self.add_diagnostic("DYNAMIC_PROCEDURE", message)
        for message in extract_dynamic_sql_messages(text):
            self.add_diagnostic("DYNAMIC_SQL", message)

    def add_method_bodies(self, bodies):
        for body in bodies:
            self.add_raw_text(body)


def analyze_controller(controller_path, data_root, schema_map):
    text = strip_csharp_comments(read_file(controller_path))
    if not text:
        raise RuntimeError("Cannot read controller: " + controller_path)

    # project : IPRO Revisi Header Laporan Trading Term
    class_files, class_methods, class_method_definitions = index_data_layer(
        data_root,
        include_metadata=True,
    )
    method_return_types = build_method_return_types(
        class_method_definitions,
        class_files,
    )
    # end project : IPRO Revisi Header Laporan Trading Term
    usage = DbUsage(schema_map)

    # 1. Raw SQL + procedures + custom functions directly in the controller.
    usage.add_raw_text(text)

    # 2. Resolve every data-layer static method the controller calls.
    # project : IPRO Revisi Header Laporan Trading Term
    calls = extract_data_layer_calls(text, class_files)
    for controller_method in extract_method_definitions(text):
        calls.update(
            extract_instance_data_layer_calls(
                controller_method.body,
                class_files,
                method_return_types=method_return_types,
                diagnostics=usage,
            )
        )
    # end project : IPRO Revisi Header Laporan Trading Term
    visited = set()
    queue = deque(calls)

    while queue:
        cls, method = queue.popleft()
        key = (cls, method)
        if key in visited:
            continue
        visited.add(key)

        bodies = class_methods.get(cls, {}).get(method, [])
        if not bodies:
            usage.add_diagnostic(
                "UNRESOLVED_METHOD",
                "Data-layer method cannot be resolved: {}.{}".format(cls, method),
            )
            continue

        for body in bodies:
            usage.add_method_bodies([body])

            # Follow chained data-layer calls inside this method body.
            # project : IPRO Revisi Header Laporan Trading Term
            nested_calls = extract_data_layer_calls(body, class_files)
            nested_calls.update(
                extract_instance_data_layer_calls(
                    body,
                    class_files,
                    method_return_types=method_return_types,
                    current_class=cls,
                    diagnostics=usage,
                )
            )
            # end project : IPRO Revisi Header Laporan Trading Term
            for nested_cls, nested_method in nested_calls:
                nested_key = (nested_cls, nested_method)
                if nested_key not in visited:
                    queue.append(nested_key)

    return usage, class_files, class_methods


# end project : IPRO Revisi Header Laporan Trading Term
# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

# project : IPRO Revisi Header Laporan Trading Term
def sorted_objects(obj_map):
    if isinstance(obj_map, dict):
        objects = {
            PhysicalObject(
                schema,
                normalize_name(split_dblink_name(name)[0]),
                dblink=split_dblink_name(name)[1],
            )
            for name, schemas in obj_map.items()
            for schema in schemas
        }
    else:
        objects = obj_map
    return sorted({obj.label for obj in objects})


def render_markdown(usage, name, url, id_value):
    lines = []
    lines.append("---")
    lines.append(f"id: {id_value}")
    lines.append(f"name: {name}")
    lines.append("group: IMMD")
    lines.append(f"url: {url}")
    lines.append("---")
    lines.append("")
    lines.append("# Direct Read")
    lines.append("")
    for obj in sorted_objects(usage.read):
        lines.append(f"- {obj}")
    lines.append("")
    lines.append("# Direct Write")
    lines.append("")
    for obj in sorted_objects(usage.write):
        lines.append(f"- {obj}")
    lines.append("")
    lines.append("# Calls")
    lines.append("")
    for obj in sorted_objects(usage.calls):
        lines.append(f"- {obj}")
    lines.append("")

    if usage.ctes:
        lines.append("# CTE / Logical Relations")
        lines.append("")
        for cte_name in sorted(usage.ctes):
            relation = usage.ctes[cte_name]
            lines.append(f"- {relation.name}")
            reads = sorted_objects(relation.physical_reads)
            if reads:
                lines.append(f"  - Reads: {', '.join(reads)}")
            dependencies = sorted(relation.cte_dependencies)
            if dependencies:
                lines.append(f"  - Depends on: {', '.join(dependencies)}")
            consumers = sorted(relation.consumers)
            if consumers:
                lines.append(f"  - Consumers: {', '.join(consumers)}")
        lines.append("")

    if usage.diagnostics:
        lines.append("# Analysis Notes")
        lines.append("")
        for diagnostic in sorted(
            usage.diagnostics,
            key=lambda item: (item.severity, item.code, item.message),
        ):
            lines.append(
                f"- [{diagnostic.severity}] {diagnostic.code}: {diagnostic.message}"
            )
        lines.append("")
    return "\n".join(lines) + "\n"
# end project : IPRO Revisi Header Laporan Trading Term


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

# project : IPRO Revisi Header Laporan Trading Term
def validate_input_paths(controller_path, data_root, edmx_path):
    diagnostics = []
    if not os.path.isfile(controller_path):
        diagnostics.append(Diagnostic(
            "INPUT_MISSING",
            "Controller input does not exist: " + controller_path,
            "error",
        ))
    if not os.path.isdir(data_root):
        diagnostics.append(Diagnostic(
            "INPUT_MISSING",
            "Data-root input does not exist: " + data_root,
            "error",
        ))
    if not os.path.isfile(edmx_path):
        diagnostics.append(Diagnostic(
            "INPUT_MISSING",
            "EDMX input does not exist: " + edmx_path,
            "error",
        ))
    return diagnostics
# end project : IPRO Revisi Header Laporan Trading Term


def main(argv=None):
    parser = argparse.ArgumentParser(description="Extract DB usage from an ASP.NET MVC controller.")
    parser.add_argument("--controller", required=True, help="Path to the controller .cs file.")
    parser.add_argument("--output", required=True, help="Path to the output .md file.")
    parser.add_argument("--name", default="Master Main Supplier", help="Human-readable name.")
    parser.add_argument("--url", default="/Transaction/MasterMainSupplier", help="Route URL.")
    parser.add_argument("--id", default="MasterMainSupplier", help="Frontmatter id.")
    parser.add_argument("--data-root", default=DATA_LAYER_ROOT, help="Root of the data layer.")
    parser.add_argument("--edmx", default=os.path.join(DATA_LAYER_ROOT, "DbModel.edmx"),
                        help="Path to the EDMX file.")
    parser.add_argument("--strict", action="store_true",
                        help="Fail when a required input cannot be read.")
    args = parser.parse_args(argv)

    diagnostics = validate_input_paths(args.controller, args.data_root, args.edmx)
    schema_map = parse_edmx_entity_map(args.edmx, diagnostics)
    if args.strict and diagnostics:
        for diagnostic in diagnostics:
            print(
                f"[{diagnostic.severity}] {diagnostic.code}: {diagnostic.message}",
                file=sys.stderr,
            )
        return 2

    if os.path.isfile(args.controller):
        try:
            usage, _, _ = analyze_controller(args.controller, args.data_root, schema_map)
        except RuntimeError as error:
            usage = DbUsage(schema_map)
            diagnostics.append(Diagnostic("CONTROLLER_UNREADABLE", str(error), "error"))
    else:
        usage = DbUsage(schema_map)

    for diagnostic in diagnostics:
        usage.add_diagnostic(diagnostic.code, diagnostic.message, diagnostic.severity)

    markdown = render_markdown(usage, args.name, args.url, args.id)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Wrote {args.output}")
    print(f"  Direct Read : {len(usage.read)} objects")
    print(f"  Direct Write: {len(usage.write)} objects")
    print(f"  Calls       : {len(usage.calls)} objects")
    for diagnostic in usage.diagnostics:
        print(
            f"[{diagnostic.severity}] {diagnostic.code}: {diagnostic.message}",
            file=sys.stderr,
        )
    if args.strict and any(diagnostic.severity == "error" for diagnostic in usage.diagnostics):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
# end project : IPRO Revisi Header Laporan Trading Term
