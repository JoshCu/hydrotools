import pytest
from hydrotools.metrics import metrics

import pandas as pd
from math import isclose
import numpy as np

contigency_table = {
    'true_positive': 1,
    'false_positive': 2,
    'false_negative': 3,
    'true_negative': 4
}

alt_contigency_table = {
    'TP': 1,
    'FP': 2,
    'FN': 3,
    'TN': 4
}

zero_contingency_table = {
    'true_positive': 0,
    'false_positive': 0,
    'false_negative': 0,
    'true_negative': 0
}

nan_contigency_table = {
    'true_positive': np.nan,
    'false_positive': np.nan,
    'false_negative': np.nan,
    'true_negative': np.nan
}

y_true = [1., 2., 3., 4.]
y_pred = [4., 3., 2., 1.]

def test_compute_contingency_table():
    obs = pd.Categorical([True, False, False, True, True, True,
        False, False, False, False])
    sim = pd.Categorical([True, True, True, False, False, False, 
        False, False, False, False])

    table = metrics.compute_contingency_table(obs, sim)

    assert table['true_positive'] == 1
    assert table['false_positive'] == 2
    assert table['false_negative'] == 3
    assert table['true_negative'] == 4

    alt_table = metrics.compute_contingency_table(obs, sim, 
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )

    assert alt_table['TP'] == 1
    assert alt_table['FP'] == 2
    assert alt_table['FN'] == 3
    assert alt_table['TN'] == 4

def test_probability_of_detection():
    POD = metrics.probability_of_detection(contigency_table)
    assert POD == (1/4)

    POD = metrics.probability_of_detection(alt_contigency_table,
        true_positive_key='TP',
        false_negative_key='FN'
        )
    assert POD == (1/4)

    with pytest.warns(RuntimeWarning):
        POD = metrics.probability_of_detection(zero_contingency_table)
        assert np.isnan(POD)

    POD = metrics.probability_of_detection(nan_contigency_table)
    assert np.isnan(POD)

def test_probability_of_false_detection():
    POFD = metrics.probability_of_false_detection(contigency_table)
    assert POFD == (2/6)

    POFD = metrics.probability_of_false_detection(alt_contigency_table,
        false_positive_key='FP',
        true_negative_key='TN'
        )
    assert POFD == (2/6)

    with pytest.warns(RuntimeWarning):
        POFD = metrics.probability_of_false_detection(zero_contingency_table)
        assert np.isnan(POFD)

    POFD = metrics.probability_of_false_detection(nan_contigency_table)
    assert np.isnan(POFD)

def test_probability_of_false_alarm():
    POFA = metrics.probability_of_false_alarm(contigency_table)
    assert POFA == (2/3)


    POFA = metrics.probability_of_false_alarm(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP'
        )
    assert POFA == (2/3)

    with pytest.warns(RuntimeWarning):
        POFA = metrics.probability_of_false_alarm(zero_contingency_table)
        assert np.isnan(POFA)

    POFA = metrics.probability_of_false_alarm(nan_contigency_table)
    assert np.isnan(POFA)

def test_threat_score():
    TS = metrics.threat_score(contigency_table)
    assert TS == (1/6)


    TS = metrics.threat_score(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN'
        )
    assert TS == (1/6)

    with pytest.warns(RuntimeWarning):
        TS = metrics.threat_score(zero_contingency_table)
        assert np.isnan(TS)

    TS = metrics.threat_score(nan_contigency_table)
    assert np.isnan(TS)

def test_frequency_bias():
    FBI = metrics.frequency_bias(contigency_table)
    assert FBI == (3/4)

    FBI = metrics.frequency_bias(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN'
        )
    assert FBI == (3/4)

    with pytest.warns(RuntimeWarning):
        FBI = metrics.frequency_bias(zero_contingency_table)
        assert np.isnan(FBI)

    FBI = metrics.frequency_bias(nan_contigency_table)
    assert np.isnan(FBI)

def test_percent_correct():
    PC = metrics.percent_correct(contigency_table)
    assert PC == (5/10)

    PC = metrics.percent_correct(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert PC == (5/10)

    with pytest.warns(RuntimeWarning):
        PC = metrics.percent_correct(zero_contingency_table)
        assert np.isnan(PC)

    PC = metrics.percent_correct(nan_contigency_table)
    assert np.isnan(PC)

def test_base_chance():
    a_r = metrics.base_chance(contigency_table)
    assert a_r == (12/10)

    a_r = metrics.base_chance(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert a_r == (12/10)

    with pytest.warns(RuntimeWarning):
        a_r = metrics.base_chance(zero_contingency_table)
        assert np.isnan(a_r)

    a_r = metrics.base_chance(nan_contigency_table)
    assert np.isnan(a_r)

def test_equitable_threat_score():
    ETS = metrics.equitable_threat_score(contigency_table)
    assert isclose(ETS, (-0.2/4.8), abs_tol=0.000001)

    ETS = metrics.equitable_threat_score(alt_contigency_table,
        true_positive_key='TP',
        false_positive_key='FP',
        false_negative_key='FN',
        true_negative_key='TN'
        )
    assert isclose(ETS, (-0.2/4.8), abs_tol=0.000001)

    with pytest.warns(RuntimeWarning):
        ETS = metrics.equitable_threat_score(zero_contingency_table)
        assert np.isnan(ETS)

    ETS = metrics.equitable_threat_score(nan_contigency_table)
    assert np.isnan(ETS)

def test_mean_squared_error():
    MSE = metrics.mean_squared_error(y_true, y_pred)
    assert MSE == 5.0

    RMSE = metrics.mean_squared_error(y_true, y_pred, root=True)
    assert RMSE == np.sqrt(5.0)

def test_nash_sutcliffe_efficiency():
    NSE = metrics.nash_sutcliffe_efficiency(y_true, y_pred)
    assert NSE == -3.0
    
    NNSE = metrics.nash_sutcliffe_efficiency(y_true, y_pred, 
        normalized=True)
    assert NNSE == 0.2
    
    NSEL = metrics.nash_sutcliffe_efficiency(np.exp(y_true), 
        np.exp(y_pred), log=True)
    assert NSEL == -3.0
    
    NNSEL = metrics.nash_sutcliffe_efficiency(np.exp(y_true), 
        np.exp(y_pred), log=True, normalized=True)
    assert NNSEL == 0.2
