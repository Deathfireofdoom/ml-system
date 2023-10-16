from abc import ABC, abstractmethod
import pandas as pd
import os


class BaseDataSource(ABC):
    """
    Base class for data sources which can be used to load data from different sources.
    A data source can be a local file, a database, a remote file, etc.

    The get_dataframe method should return a pandas dataframe. Right now, the datasource is
    responsible for filtering the data based on the start_date and end_date. Also implementing
    time travel for reproducability.

    Notes
    -----
    Why did I put filtering in the data source?
    I put filtering in the data source to avoid reading the entire dataset into memory, for files like CSV this is not
    really applicable, since the data needs to be loaded into memory anyway. But if I implemented a database source
    then it would be beneficial to filter the data before loading it into memory.

    Why did I put time travel in the data source?
    I put time travel in the data source because the logic behind time travel may be significantly different for
    each data source. In the example below we just filter on "created_at", but on other data sources we may need to
    read from another location etc.
    """

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        pass


class LocalParquetDataSource(BaseDataSource):
    def __init__(
        self,
        file_path: str,
        start_date: str = None,
        end_date: str = None,
        interval_date_column: str = "effective_date",
        time_travel: bool = False,
        time_travel_date: str = None,
        time_travel_date_column: str = "created_at",
        convert_interval_date_to_epoch: bool = True,
        convert_time_travel_date_to_epoch: bool = False,
    ):
        if time_travel and not time_travel_date:
            raise ValueError(
                "time_travel_date must be specified if time_travel is True"
            )

        # Check if file exists - Failing early is better than failing late
        if not os.path.exists(file_path):
            raise ValueError(f"File {file_path} does not exist.")
        self.file_path = file_path
        self.start_date = start_date
        self.end_date = end_date
        self.interval_date_column = interval_date_column

        self.time_travel = time_travel
        self.time_travel_date = time_travel_date
        self.time_travel_date_column = time_travel_date_column

        # This is a last minute fix, didn't really look at the files.
        # A bit hacky, maybe correct, maybe not.
        self.convert_interval_date_to_epoch = convert_interval_date_to_epoch
        self.convert_time_travel_date_to_epoch = convert_time_travel_date_to_epoch

    def get_dataframe(self) -> pd.DataFrame:  # TODO remove dask
        # Load the data
        ddf = pd.read_parquet(self.file_path)

        # ddf[self.time_travel_date_column] = dd.to_datetime(ddf[self.time_travel_date_column])
        # ddf[self.interval_date_column] = dd.to_datetime(ddf[self.interval_date_column])

        # Filter the data
        if self.time_travel:
            self.time_travel_date = pd.to_datetime(self.time_travel_date)
            ddf = ddf.loc[ddf[self.time_travel_date_column] <= self.time_travel_date]

        if self.start_date:
            self.start_date = pd.to_datetime(self.start_date)
            ddf = ddf.loc[ddf.index >= self.start_date]

        if self.end_date:
            self.end_date = pd.to_datetime(self.end_date)
            ddf = ddf.loc[ddf.index <= self.end_date]

        # Convert to pandas dataframe
        # df = ddf.compute()
        df = ddf
        print(len(df))
        return df
