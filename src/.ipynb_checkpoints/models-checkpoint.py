from sklearn.ensemble import (RandomForestClassifier, 
                             AdaBoostClassifier, 
                             ExtraTreesClassifier, 
                             GradientBoostingClassifier, 
                             VotingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler


weight = {
    "normal"   :0.534582,
    "dos"      :0.364580,
    "probe"    :0.092526,
    "r2l"      :0.007904,
    "u2r"      :0.000408
}


MODELS = [
    RandomForestClassifier(n_jobs= -1, verbose=0, oob_score=True, class_weight= weight),
    Pipeline([('PCA', PCA(n_components= 50)), ('RandomForestClassifier', RandomForestClassifier(n_jobs= -1, verbose=0, oob_score=True, class_weight= weight))]),
    Pipeline([('Standard Scaler', StandardScaler()), ('RandomForestClassifier', RandomForestClassifier(n_jobs= -1, verbose=0, oob_score=True, class_weight= weight))]),
    LogisticRegression(n_jobs= -1, verbose=0, class_weight= weight)
]