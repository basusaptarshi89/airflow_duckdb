-- read csv file in duckdb
-- Ref: https://duckdb.org/docs/data/csv/overview

CREATE TABLE netflix 
AS 
SELECT * 
  FROM 
read_csv(
    '{{ csv_file_path }}',
    delim = ',',
    header = true,
    ignore_errors = true,
    dateformat = "%B %-d, %Y",
    columns = {
        'show_id': 'VARCHAR',
        'type': 'VARCHAR',
        'title': 'VARCHAR',
        'director': 'VARCHAR',
        'cast': 'VARCHAR',
        'country': 'VARCHAR',
        'date_added': 'DATE',
        'release_year': 'INTEGER',
        'rating': 'VARCHAR',
        'duration': 'VARCHAR',
        'listed_in': 'VARCHAR',
        'description': 'VARCHAR'
    }
);
