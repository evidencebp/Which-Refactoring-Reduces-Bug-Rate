import pandas as pd

DATA_PATH = '/Users/iamit/Documents/PhD/goto/data/'
CODE_PATH = '/Users/iamit/Documents/PhD/goto/code/'

execfile('/Users/iamit/journals/academy_relations/malware_redundency/confusion_matrix.py')
execfile(CODE_PATH + 'commit_type_model.py')

def evaluate_bq_results(labels_file):
    df = pd.read_csv(labels_file)
    l = df[df.Type.isin(['corrective', 'perfective', 'adaptive', 'multi'])]

    l['corrective_pred'] = l['bq_classification']


    l['is_refactor_pred'] = l.refactor_matches.map(lambda x: x > 0)

    l['adaptive_pred'] = l.adaptive_matches.map(lambda x: x > 0)
    linguistic_model_perfomance(l)

def evaluate_regex_results(labels_file):
    df = pd.read_csv(labels_file)
    df = classifiy_commits_df(df)
    linguistic_model_perfomance(df)

def linguistic_model_perfomance(df):
    print "l length ", len(df)

    bug_g = df.groupby(['corrective_pred', 'Is_Corrective'], as_index=False).agg({'commit' : 'count'})
    bug_cm = ConfusionMatrix(bug_g, classifier='corrective_pred', concept='Is_Corrective', count='commit')
    print "corrective commit performance"
    print bug_cm.summarize()


    refactor_g = df.groupby(['is_refactor_pred', 'Is_Refactor'], as_index=False).agg({'commit' : 'count'})
    refactor_cm = ConfusionMatrix(refactor_g,classifier='is_refactor_pred',concept='Is_Refactor',count='commit')
    print "refactor commit performance"
    print refactor_cm.summarize()

    adaptive_g = df.groupby(['adaptive_pred', 'Is_Adaptive'], as_index=False).agg({'commit' : 'count'})
    adaptive_cm = ConfusionMatrix(adaptive_g,classifier='adaptive_pred',concept='Is_Adaptive',count='commit')
    print "adaptive commit performance"
    print adaptive_cm.summarize()

def get_false_positives(df
                        , classifier
                        , concept):
    return df[(df[classifier] == True) & (df[concept] == False)]

def get_false_negatives(df
                        , classifier
                        , concept):
    return df[(df[classifier] == False) & (df[concept] == True)]


def main():
    print "test performance"
    print "***********************************"
    evaluate_regex_results(DATA_PATH + '/labels/commits_updated2.csv')
    #evaluate_bq_results(DATA_PATH + '/labels/commits_updated2.csv')
    print "stat performance"
    print "***********************************"
    evaluate_regex_results(DATA_PATH + '/labels/stas_labeling2.csv')
    print "train performance"
    print "***********************************"
    evaluate_regex_results(DATA_PATH + '/labels/train.csv')


