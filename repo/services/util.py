import statistics
from typing import List

from repo.data.general import Statistics


def get_statistics(data: List[int]) -> Statistics:
    if len(data) > 1:
        mean = statistics.fmean(data)
        standard_deviation = statistics.stdev(data)
    else:
        mean = data[0]
        standard_deviation = 0.0

    return Statistics(
        mean=mean,
        standard_deviation=standard_deviation,
    )
