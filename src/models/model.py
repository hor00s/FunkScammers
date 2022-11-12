import sqlite3 as sqlite
from typing import Any
from sqlite3 import (
    Connection,
)


class ConnectionManager:
    def __init__(self, name: str) -> None:
        self.name = name
        self._connection = sqlite.connect(self.name)

    def __enter__(self) -> Connection:
        return self._connection

    def __exit__(self, *args: Any) -> None:
        self._connection.commit()
        self._connection.close()


class Model:
    def __init__(self, name: str, **table: str) -> None:
        """Initialize a database with it's values
        Example:
        ```
            # id is assigned automatically
            Model('my_db', user='TEXT', age='INTEGER')
        ```

        :param name: Name of the databse
        :type name: str
        """
        self.name = name
        self.table = table
        self.table['id'] = 'INTEGER PRIMARY KEY'

        # Format the `table` into a string, is it should be in the query
        # Example: table = {name='TEXT' age='INTEGER'} would translate to:
        # name TEXT, age INTEGER
        self.table_vals = ' '.join(
            f"{n} {t}," for (n, t) in table.items()
        )[:-1]

    def _execute(self, query: str, fetch: bool = False) -> Any:
        """Execute a query

        :param query: SQL Query
        :type query: str
        :param fetch: Choose wheather the data from the query needs to be
                      returned, defaults to False
        :type fetch: bool, optional
        :return: The result of the query if `fetch=True` else None
        :rtype: Any
        """
        with ConnectionManager(self.name) as cur:
            data = cur.execute(query)
            if fetch:
                return data.fetchall()
            return None

    def create_table(self) -> None:
        """Create a table based on the `self.table` (**table) kwargs
        provided upon initialization
        """
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.name} (
            {self.table_vals}
        )
        """
        self._execute(query)

    def insert(self, **values: str) -> None:
        """Insert new values into the table
        (can accept arbitary number of values
        for a new inserion and leave the rest
        NULL as long as the table allows it)
        """
        cols = ','.join(map(str, values.keys()))
        vals = ','.join(
            f"'{i}'" if not isinstance(i, int)
            else str(i) for i in list(values.values())
        )

        query = f"""
        INSERT INTO {self.name} ({cols}) VALUES (
            {vals}
        )
        """
        self._execute(query)

    def fetch_all(self) -> Any:
        """Fetch all the data from the table

        :return: All the saved data
        :rtype: Any
        """
        query = f"SELECT * FROM {self.name}"
        return self._execute(query, fetch=True)

    def filter_row(self, data: Any, col: str | None = None) -> Any:
        """If `col` is provided, this function will filter out a certain
        colummn out of a row
        ```
            data = [(name, age, id)]
            self._filter_last('name') -> name
        ```

        :param data: The data returned from a quert
        :type data: Any
        :param col: A certain column out of the data, defaults to None
        :type col: str | None, optional
        :return: All the data or the selected column
        :rtype: Any
        """
        enum_table = {row: num for (num, row) in enumerate(self.table)}
        if col is not None:
            return data[0][enum_table[col]]
        return data

    def fetch_last(self, col: str | None = None) -> Any:
        """Fetch the last insertion based on id

        :param col: A certain column if needed, defaults to None
        :type col: str | None, optional
        :return: All the data or the selected column
        :rtype: Any
        """
        query = f"""
        SELECT * FROM {self.name}
        WHERE id = (SELECT MAX(id)  FROM {self.name})
        """
        data = self._execute(query, fetch=True)
        return self.filter_row(data, col)

    def edit(self, set: str, where: str) -> None:
        """Edit a row based on a condition

        :param set: Which column to set
        :type set: str
        :param where: Condition
        :type where: str
        """
        query = f"""
        UPDATE {self.name}
        SET
            {set}
        WHERE
            {where}
        """
        self._execute(query)
