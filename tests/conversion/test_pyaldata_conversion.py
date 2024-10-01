import os

import pandas as pd
import pytest
import scipy

from beneuro_data.config import _load_config
from beneuro_data.conversion.convert_nwb_to_pyaldata import convert_nwb_to_pyaldata


@pytest.mark.needs_experimental_data
@pytest.mark.processing
@pytest.mark.parametrize("session_name", ["M030_2024_04_12_09_40"])
def test_nwb_to_pyaldata(session_name):
    config = _load_config()
    local_session_path = config.get_local_session_path(session_name, "processed")

    nwbfiles = list(local_session_path.glob("*.nwb"))
    assert nwbfiles
    assert len(nwbfiles) == 1

    # delete existing NWB file
    for mat_file in local_session_path.glob("*.mat"):
        mat_file.unlink()

    nwbfile_path = nwbfiles[0].absolute()

    convert_nwb_to_pyaldata(nwbfile_path=nwbfile_path, verbose=False)
    mat = scipy.io.loadmat(
        local_session_path / f"{session_name}_pyaldata.mat", simplify_cells=True
    )

    real_keys = [k for k in mat.keys() if not (k.startswith("__") and k.endswith("__"))]
    td_name = real_keys[0]

    df = pd.DataFrame(mat[td_name])

    expected_columns = [
        "animal",
        "session",
        "trial_id",
        "trial_name",
        "trial_length",
        "bin_size",
        "idx_trial_start",
        "idx_trial_end",
        "values_before_camera_trigger",
        "idx_before_camera_trigger",
        "idx_motion",
        "idx_quiet_period_end",
        "values_Sol_direction",
        "idx_Sol_direction",
        "idx_quiet_period_start",
        "idx_session_timer",
        "motion_sensor_xy",
        "SSp_ul_chan_best",
        "SSp_ul_KSLabel",
        "SSp_ul_spikes",
        "SSp_m_chan_best",
        "SSp_m_KSLabel",
        "SSp_m_spikes",
        "MOp_chan_best",
        "MOp_KSLabel",
        "MOp_spikes",
        "ccg_chan_best",
        "ccg_KSLabel",
        "ccg_spikes",
        "ccb_chan_best",
        "ccb_KSLabel",
        "ccb_spikes",
        "scwm_chan_best",
        "scwm_KSLabel",
        "scwm_spikes",
        "CP_chan_best",
        "CP_KSLabel",
        "CP_spikes",
    ]

    # Assert that all expected columns are present
    # TODO: Add some more thorough checking on the data structure.

    assert set(expected_columns).issubset(
        df.columns
    ), f"Missing columns: {set(expected_columns) - set(df.columns)}"
    assert (df["bin_size"] == 0.01).all(), "Not all values in 'bin_size' are equal to 0.01"
