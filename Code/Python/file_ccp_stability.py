"""

Weight Pearson methods are taken from
https://stackoverflow.com/questions/38641691/weighted-correlation-coefficient-with-pandas
"""

import numpy as np


DATA_PATH = '/Users/iamit/Documents/PhD/goto/data/'

def m(x, w):
    """Weighted Mean"""
    return np.sum(x * w) / np.sum(w)

def cov(x, y, w):
    """Weighted Covariance"""
    return np.sum(w * (x - m(x, w)) * (y - m(y, w))) / np.sum(w)

def corr(x, y, w):
    """Weighted Correlation"""
    return cov(x, y, w) / np.sqrt(cov(x, x, w) * cov(y, y, w))

def analyze_ccp_stability(ccp_file):
    st = pd.read_csv(ccp_file)
    corr(st.hit_rate_q1, st.hit_rate_q2, st.files)

    print "all files", "{:,}".format(st.files.sum())
    print "CCP Pearson correlation", "{0:0.2f}".format(corr(st.hit_rate_q1, st.hit_rate_q2, st.files))

    st['ccp_diff'] = st.hit_rate_q2 -  st.hit_rate_q1
    print "CCP difference mean", "{0:0.2f}".format(st.ccp_diff.mean())
    print "CCP difference std", "{0:0.2f}".format(st.ccp_diff.std())
    print "CCP difference 95th", "{0:0.2f}".format(st.ccp_diff.quantile(0.95))


    st['abs_diff'] = abs(st.hit_rate_q2 -  st.hit_rate_q1)
    print "CCP abs difference mean", "{0:0.2f}".format(st.abs_diff.mean())
    print "CCP abs difference std", "{0:0.2f}".format(st.abs_diff.std())
    print "CCP abs difference 95th", "{0:0.2f}".format(st.abs_diff.quantile(0.95))

    print "CCP improvement probability", "{0:0.2f}".format(1.0*st[st.hit_rate_q2 < st.hit_rate_q1].files.sum()
                                                           /st.files.sum())


analyze_ccp_stability(DATA_PATH +'file_ccp_stability_dist.csv')