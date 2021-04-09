#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from scipy import stats

# __Nominal__: Protocol_type(2), Service(3), Flag(4)
# 
# __Binary__: Land(7), logged_in(12), root_shell(14), su_attempted(15), is_host_login(21),, is_guest_login(22)
# 
# __Numeric__: Duration(1), src_bytes(5), dst_bytes(6), wrong_fragment(8), urgent(9), hot(10), num_failed_logins(11), num_compromised(13), num_root(16), num_file_creations(17),num_shells(18), num_access_files(19), num_outbound_cmds(20), count(23), srv_count(24), error_rate(25),srv_serror_rate(26), rerror_rate(27),srv_rerror_rate(28), same_srv_rate(29),diff_srv_rate(30),srv_diff_host_rate(31), dst_host_count(32), dst_host_srv_count(33), dst_host_same_srv_rate(34),dst_host_diff_srv_rate(35), dst_host_same_src_port_rate(36), dst_host_srv_diff_host_rate(37),dst_host_serror_rate(38), dst_host_srv_serror_rate(39), dst_host_rerror_rate(40),dst_host_srv_rerror_rate(41)

def feature_selection(df, columns = None):
    nominal = df[[ "protocol_type", "service", "flag"]]
    binary = df[["logged_in", "root_shell", "is_guest_login"]]
    numeric = df[df.columns.difference(list(binary.columns) + list(nominal.columns) + ['attack', "attacks_class"])]
    numeric = numeric[numeric.columns.difference(["num_outbound_cmds", "land","is_host_login"])]
    target = df.attacks_class
    if columns:
        nominal = nominal[nominal.columns.intersection(columns)]
        binary = binary[binary.columns.intersection(columns)]
        numeric = numeric[numeric.columns.intersection(columns)]
    return nominal, binary, numeric, target

def structure(nominal, binary, numeric, target):
    return pd.concat([pd.get_dummies(pd.concat([nominal,binary,numeric], axis= 1)), target], axis = 1)

def prep(df, columns = None):
    nominal, binary, numeric, target = feature_selection(df, columns)
    return structure(nominal, binary, numeric, target)

if __name__ == "__main__":
    df = pd.read_csv("../data/Train.csv")
    attacks = {
    'dos': ['back', 'land', 'neptune', 
            'pod', 'smurf', 'teardrop', 
            'apache2', 'udpstorm', 'processtable', 
            'worm'],
    'probe': ['satan', 'ipsweep', 'nmap', 
              'portsweep', 'mscan', 'saint'],
    'r2l': ['guess_passwd', 'ftp_write', 'imap',
            'phf', 'multihop', 'warezmaster',
            'warezclient', 'spy', 'xlock',
            'xsnoop', 'snmpguess', 'snmpgetattack',
            'httptunnel', 'sendmail', 'named'],
    'u2r': ['buffer_overflow', 'loadmodule', 'rootkit', 
            'perl', 'sqlattack', 'xterm', 'ps']
    }

    df["attacks_class"] = np.nan
    for each_attack_type in attacks.keys():
        df.loc[df[df.attack.isin(attacks[each_attack_type])].index, "attacks_class"] = each_attack_type
    
    df.attacks_class.fillna('normal', inplace = True)

    nominal, binary, numeric, target = feature_selection(df)
    _ = pd.concat([nominal, binary], axis= 1)
    _ = _.apply(lambda x: stats.chi2_contingency(pd.crosstab(x, target))[0:2])
    print("categorical variable\n", _)
    _ = numeric.apply(
        lambda x:
        tuple(map(lambda x: round(x, 2), stats.f_oneway(*[numeric.loc[target.isin([each_attack]), x.name] for each_attack in attacks.keys()])))
    )
    print("\n\ncontinous variable\n", _)