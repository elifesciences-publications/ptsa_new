import numpy as np
from scipy.signal import resample

from ptsa.data.timeseries import TimeSeries
from ptsa.data.filters import BaseFilter
import traits.api


class ResampleFilter(BaseFilter):
    """Upsample or downsample a time series to a new sample rate.

    .. versionchanged:: 2.0

        Parameter "time_series" was renamed to "timeseries". Parameter
        "time_axis_index" was removed; the time axis is assumed to be named
        "time"

    Keyword Arguments
    -----------------
    timeseries
        TimeSeries object
    resamplerate: float
        new sampling frequency
    round_to_original_timepoints: bool
        Flag indicating if timepoints from original time axis
        should be reused after proper rounding. Defaults to False
    time_axis: str
        Name of the time axis.

    """

    resamplerate = traits.api.CFloat
    round_to_original_timepoints = traits.api.Bool

    def __init__(self, timeseries, resamplerate,
                 round_to_original_timepoints=False, time_axis_name='time'):
        super(ResampleFilter, self).__init__(timeseries=timeseries)
        self.resamplerate = resamplerate
        self.round_to_original_timepoints = round_to_original_timepoints
        self.time_axis_name = time_axis_name

    def filter(self):
        """resamples time series

        Returns
        -------
        resampled: TimeSeries
            resampled time series with sampling frequency set to resamplerate

        """
        samplerate = float(self.timeseries['samplerate'])

        self.time_axis_index = self.timeseries.get_axis_num(
            self.time_axis_name)

        time_axis = self.timeseries.coords[
            self.timeseries.dims[self.time_axis_index]]

        time_axis_length = len(time_axis)
        new_length = int(np.round(
            time_axis_length*self.resamplerate/samplerate))

        try:
            # time axis can be recarray with one of the arrays being time
            time_axis_data = time_axis.data[self.time_axis_name]
        except (KeyError, IndexError) as excp:
            # if we get here then most likely time axis is ndarray of floats
            time_axis_data = time_axis.data

        time_idx_array = np.arange(len(time_axis))

        if self.round_to_original_timepoints:
            filtered_array, new_time_idx_array = resample(
                self.timeseries.data, new_length, t=time_idx_array,
                axis=self.time_axis_index)

            # print new_time_axis

            new_time_idx_array = np.rint(new_time_idx_array).astype(np.int)

            new_time_axis = time_axis[new_time_idx_array]

        else:
            filtered_array, new_time_axis = \
                resample(self.timeseries.data,
                         new_length,
                         t=time_axis_data,
                         axis=self.time_axis_index)

        coords = {}
        for i, dim_name in enumerate(self.timeseries.dims):
            if i != self.time_axis_index:
                coords[dim_name] = self.timeseries.coords[dim_name].copy()
            else:
                coords[dim_name] = new_time_axis
        coords['samplerate'] = self.resamplerate

        filtered_timeseries = TimeSeries(filtered_array, coords=coords,
                                         dims=self.timeseries.dims)
        return filtered_timeseries
