import pandas as pd
import re

DATA_PATH = '/Users/iamit/Documents/PhD/goto/data/'
CODE_PATH = '/Users/iamit/Documents/PhD/goto/code/'

execfile('/Users/iamit/journals/academy_relations/malware_redundency/confusion_matrix.py')
execfile(CODE_PATH + 'compare_word_dist.py')
execfile(CODE_PATH + 'commit_type_model.py')


def evaluate_performance(agg
                         , name
                         , name_regex):
    agg[name] = agg.message.map(lambda x: len(re.findall(name_regex, x.lower())) > 0)
    cm = ConfusionMatrix(raw_df=agg
                         , classifier=name
                         , concept='improve_ccp'
                         , count='commit')
    return cm






performace = {
    'improve': {'regex': build_sepereted_term(['improv(?:e|es|ed|ing)','better'])}
    , 'rename': {'regex': build_sepereted_term(['renam(?:e|es|ed|ing|ings)', 'better nam(?:e|es|ing)'])}
    , 'rework': {'regex': build_sepereted_term(['re(?:-)?work(ed|s|ing|ings)?', 're(?:-)?(?:write|write|wrote|writing)'
    , 're(?:-)?cod(?:e|ed|es|ing)'])}
    , 'upgrade': {'regex': build_sepereted_term(['upgrad(?:e|es|ed|ing)'])}
    , 'refactor': {'regex': build_sepereted_term(['re(?:-| )?factor(?:ed|s|ing|ings)?'])}
    , 'se_constructs': {'regex': build_sepereted_term(['enum(s)?', 'names(?:-| )?pace(s)?'])}
    , 'simple': {'regex': build_sepereted_term(['simplif(y|es|ied|ying|ication)', 'simplicity' ])}
    , 'reuse': {'regex': build_sepereted_term(['re(?:-| )?use' ,'re(?:-| )?usability'])}
    , 'spelling': {'regex': build_sepereted_term(['typo(s)?', 'spelling', 'mis(?:-| )?sspell(ed|ing)?'])} # might be wrong since not in refactor regex
    , 'whitespace_wars': {'regex': build_sepereted_term(['space(s)?', 'white(?:-| )?space(s)?', 'tab(s)?'])}
    , 'todo': {'regex': build_sepereted_term(['to(?: |-)?do(?:s)?'])}
    , 'style': {'regex': build_sepereted_term(['style|styling'])}
    , 'optimization': {'regex': build_sepereted_term(['optimiz(?:e|es|ed|ing|ation|ations)', 'efficient'])}
    , 'clean': {'regex': build_sepereted_term(['clean(?:ing|s|ed)'
    , 'cleaner'])}
    , 'unneeded': {'regex': build_sepereted_term(unnedded_terms)}
    , 'feedback': {'regex': build_sepereted_term(feedbak_terms)}
    , 'reorgnize': {'regex': build_sepereted_term(['re(?:-|)?organiz(?:e|es|ed|ing)'
                                                      , 're(?:-|)?structur(?:e|es|ed|ing)'
                                                      , 'compos(?:e|es|ed|ing)'
                                                      ,'de(?:-| )?compos(?:e|es|ed|ing)'
                                                      , 'combin(?:e|es|ed|ing)'
                                                      , 're(?:-|)?arrang(?:e|es|ed|ing)'
                                                      , 're(?:-| )?packag(?:e|es|ed|ing)'])}
    , 'software_goals': {'regex':build_refactor_goals_regex()}
}

if __name__ == "__main__":
    messages = pd.read_csv(DATA_PATH + 'clean_commits_with_messages_2018.csv')
    agg = agg_by_message(messages)
    agg['improve_ccp'] = agg.ccp_diff.map(lambda x: x < 0)

    for i in performace.keys():
        cm = evaluate_performance(agg, i, performace[i]['regex'])
        performace[i]['confusion_matrix'] = cm.summarize()
