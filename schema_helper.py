from sqlalchemy import create_engine, inspect, text


def build_relationship_graph(inspector, tables):
    relationships = []

    for table in tables:
        if "." in table:
            schema_name, table_name = table.split(".", 1)
            columns = inspector.get_columns(table_name, schema=schema_name)
        else:
            columns = inspector.get_columns(table)

        foreign_keys = []
        for column in columns:
            column_name = column["name"].lower()

            if column_name.endswith("_id"):
                possible_table = column_name.replace("_id", "")

                for target_table in tables:
                    target = target_table.lower()
                    if target == possible_table or target == possible_table + "s":
                        foreign_keys.append((column_name, target_table))

        if len(foreign_keys) >= 2:
            related_tables = [target for _, target in foreign_keys]
            relationships.append(
                f"{table} acts as a bridge table connecting "
                + " and ".join(related_tables)
            )
        else:
            for _, target in foreign_keys:
                relationships.append(f"{table} is related to {target}")

    return relationships


def load_metadata():
    from main_langchain import APP_DB_URL

    engine = create_engine(APP_DB_URL)
    connection = engine.connect()

    metadata = {}
    try:
        result = connection.execute(
            text(
                """
                SELECT
                    table_name,
                    column_name,
                    description
                FROM metadata_definitions
                """
            )
        )

        for row in result:
            table_name = row[0].lower()
            column_name = row[1].lower()
            description = row[2]

            if table_name not in metadata:
                metadata[table_name] = {}

            metadata[table_name][column_name] = description
    except Exception:
        pass

    connection.close()
    return metadata


def build_compact_schema(db_url):
    engine = create_engine(db_url)
    connection = engine.connect()
    inspector = inspect(engine)

    metadata = load_metadata()

    ignored_tables = [
        "spt_fallback_db",
        "spt_fallback_dev",
        "spt_fallback_usg",
        "spt_monitor",
        "MSreplication_options",
        "metadata_definitions",
    ]

    tables = []
    schemas = inspector.get_schema_names()

    for schema in schemas:
        if schema in ["sys", "INFORMATION_SCHEMA"]:
            continue

        schema_tables = inspector.get_table_names(schema=schema)
        for table in schema_tables:
            if table not in ignored_tables:
                tables.append(f"{schema}.{table}")

    schema_text = ""
    for table in tables:
        schema_text += f"\nTable: {table}\n"

        if "." in table:
            schema_name, table_name = table.split(".", 1)
            columns = inspector.get_columns(table_name, schema=schema_name)
        else:
            columns = inspector.get_columns(table)

        for column in columns:
            column_name = column["name"]
            column_type = str(column["type"])
            column_description = ""

            table_key = table.lower()
            column_key = column_name.lower()

            if table_key in metadata and column_key in metadata[table_key]:
                column_description = metadata[table_key][column_key]

            schema_text += f"- Column: {column_name}\n" f"  Type: {column_type}\n"

            if column_description:
                schema_text += f"  Meaning: {column_description}\n"

            schema_text += "\n"

    relationship_graph = build_relationship_graph(inspector, tables)

    schema_text += "\nRelationship Graph:\n"
    for relation in relationship_graph:
        schema_text += f"- {relation}\n"

    connection.close()
    return schema_text

