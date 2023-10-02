from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, MaxAbsScaler
from sklearn.metrics import accuracy_score
from sklearn import tree
from aif360.datasets import AdultDataset, GermanDataset, CompasDataset, BankDataset
from aif360.datasets import MEPSDataset19
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.metrics import ClassificationMetric
from aif360.algorithms.preprocessing.optim_preproc_helpers.data_preproc_functions import load_preproc_data_adult, load_preproc_data_compas, load_preproc_data_german
from aif360.algorithms.preprocessing.optim_preproc_helpers.distortion_functions\
            import get_distortion_adult, get_distortion_german, get_distortion_compas
# protected in {sex,race,age}
def get_data(dataset_used, protected,preprocessed = False):
    if dataset_used == "adult":
        if protected == "sex":
            privileged_groups = [{'sex': 1}]
            unprivileged_groups = [{'sex': 0}]
            dataset_orig = load_preproc_data_adult(['sex'])
        else:
            privileged_groups = [{'race': 1}]
            unprivileged_groups = [{'race': 0}]
            dataset_orig = load_preproc_data_adult(['race'])
            
        optim_options = {
            "distortion_fun": get_distortion_adult,
            "epsilon": 0.05,
            "clist": [0.99, 1.99, 2.99],
            "dlist": [.1, 0.05, 0]
        }
        if not preprocessed:
            dataset_orig = AdultDataset()
    elif dataset_used == "german":
        if protected == "sex":
            privileged_groups = [{'sex': 1}]
            unprivileged_groups = [{'sex': 0}]
            dataset_orig = load_preproc_data_german(['sex'])
            optim_options = {
                "distortion_fun": get_distortion_german,
                "epsilon": 0.05,
                "clist": [0.99, 1.99, 2.99],
                "dlist": [.1, 0.05, 0]
            }
        
        else:
            privileged_groups = [{'age': 1}]
            unprivileged_groups = [{'age': 0}]
            dataset_orig = load_preproc_data_german(['age'])
            optim_options = {
                "distortion_fun": get_distortion_german,
                "epsilon": 0.1,
                "clist": [0.99, 1.99, 2.99],
                "dlist": [.1, 0.05, 0]
            }    
        if not preprocessed:
            dataset_orig = GermanDataset()
    elif dataset_used == "compas":
        if protected == "sex":
            privileged_groups = [{'sex': 1}]
            unprivileged_groups = [{'sex': 0}]
            dataset_orig = load_preproc_data_compas(['sex'])
        else:
            privileged_groups = [{'race': 1}]
            unprivileged_groups = [{'race': 0}]
            dataset_orig = load_preproc_data_compas(['race'])
            
        optim_options = {
            "distortion_fun": get_distortion_compas,
            "epsilon": 0.05,
            "clist": [0.99, 1.99, 2.99],
            "dlist": [.1, 0.05, 0]
        }
        if not preprocessed:
            dataset_orig = CompasDataset()
    elif dataset_used == "bank":
        privileged_groups = [{'age': 1}]  
        unprivileged_groups = [{'age': 0}]
        dataset_orig = BankDataset()
        #dataset_orig.features[:,0] =  dataset_orig.features[:,0]>=25
        optim_options = None
    elif dataset_used == "meps19":
        privileged_groups = [{'RACE': 1}]  
        unprivileged_groups = [{'RACE': 0}]
        dataset_orig = MEPSDataset19()
        optim_options = None
    return dataset_orig, privileged_groups,unprivileged_groups,optim_options

def write_to_file(fname,content):
    f = open(fname, "a")
    f.write(content)
    f.write("\n")
    f.close()


def get_metrics(clf,test,test_pred,unprivileged_groups,privileged_groups):
    pred = clf.predict(test.features).reshape(-1,1)
    #dataset_orig_test_pred = test.copy(deepcopy=True)
    test_pred.labels = pred
    class_metric = ClassificationMetric(test, test_pred,
                         unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
    stat = abs(class_metric.statistical_parity_difference())
    aod = abs(class_metric.average_abs_odds_difference())
    eod = abs(class_metric.equal_opportunity_difference())
    acc = class_metric.accuracy()
    return acc,stat,aod,eod
