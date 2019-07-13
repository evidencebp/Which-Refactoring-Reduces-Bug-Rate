
"""
This file contain a python implementation of the corrective commit linguistic model
and the English linguistic model.
While the model used in the research was implementer in a BigQuery implementation,
the python implementation is valuable.
First, it enable to structure the model and export it for BigQuery.
Other than that, it enable running the model on test and other examples.
Running it on the train set iteratively enabled rapid evaluation of the model.

BigQuery uses the re2 engine for regular expressions, since it is fast.
This prevented us from using lookaheads and lookbehinds, which are not supported.



"""

import re

# TODO - circumvents, repair
# Positive
bug_terms = ['(choose|take|set|use)\\s*(the|a)?\\s*correct', # correct as adjective
             "(not|isn't|doesn't)\\s+work(s|ing)?",
             'bad initialization',
             'buffer overflow',
             'bug(s|z)?',
             'bugfix(es)?',
             'correct\\s*(a|the|some|few|this)', # make sure that correct serves as a verb
             'correct(ed|ion|ly|s)?',
             'dangling pointer',
             'deadlock',
             'defect',
             'double free',
             'error',
             'fail(ed|s)?',
             'failure(s)?',
             'fault(s)?',
             'faulty initialization',
             'fix(ed|es)?',
             'fixin(s)?',
             'fixing(s)?',
             'fixup(s)?',
             'flaw(s)?',
             'hang',
             'heap overflow',
             'incorrect(ly)?',
             'memory leak',
             'missing\s(default value|initialization|switch case)',
             'mistake(s|n|nly)?',
             'null pointer',
             'overrun',
             'problem(?:s)?',
             'race condition',
             'resource leak',
             'revert',
             'segmentation fault',
             'workaround',
             'wrong(nly)?',
             'trouble(?:s)?']

# Valid_fix_objects
valid_fix_object = ['#',
                    '(camel|snake|kebab|flat|lower|upper)\\s*case',
                    'code review',
                    'coding style',
                    'comment(s)?',
                    'cosmetic',
                    'cr(s)?(-)?',
                    'documentation',
                    'format(s|ing)?',
                    'help',
                    'remark(s)?',
                    'space(s)?',
                    'style|styling',
                    'typo(s)?',
                    'warning(s)?',
                    'whitespace(s)?']

valid_terms = [
    'error check(ing)?',
    'error handling',
    'error message(s)?',
    'error report(s|ing)?',
    'exception handling',
    'fixed point']

# Negation
negation_terms = ["aren't", "didn't" ,"don't", "doesn't", "isn't", 'lack', "n't", 'never', 'no', 'nobody', 'none', 'not', 'nothing'
    , "weren't", 'without', "won't"]

# term_seperator = "(\s|\.|\?|\!|\[|\]|\)|\:|^|$|\,|\'|\"|\n|/)"
term_seperator = "(?:^|$|[^a-z_])"

def build_valid_find_regex():
    fix_re = 'fix(ed|s|es|ing)?'
    prefix = term_seperator + fix_re + '[\s\S]{1,40}' + "(" + "|".join(valid_fix_object) + ")" + term_seperator
    suffix = "(" + "|".join \
        (valid_fix_object) + ")" + term_seperator + '[\s\S]{1,40}' + term_seperator + fix_re + term_seperator

    other_valid_re = "(%s)" % "|".join(valid_terms)

    return "((%s)|(%s)|(%s))" % (prefix, suffix, other_valid_re)

def build_bug_fix_regex():
    bug_fix_re = "%s(%s)%s" % (term_seperator, "|".join(bug_terms), term_seperator)

    return bug_fix_re


def build_negeted_bug_fix_regex():
    bug_fix_re = build_bug_fix_regex()
    negation_re = '%s(%s)%s' % (term_seperator ,"|".join(negation_terms)
                                , term_seperator)

    return "%s[\s\S]{0,20}%s" % (negation_re, bug_fix_re)



def is_fix(commit_text):


    text = commit_text.lower()

    fix_num = len(re.findall(build_bug_fix_regex(), text))
    valid_num = len(re.findall(build_valid_find_regex(), text))
    negated_num = len(re.findall(build_negeted_bug_fix_regex(), text))

    return (fix_num - valid_num - negated_num) > 0


software_goals = ['abstraction', 'coherence', 'cohesion', 'complexity', 'correctness', 'coupling', 'dependability'
    , 'duplication', 'efficiency', 'extensibility', 'flexibility' ,'maintainability', 'naming', 'performance', 'portability', 'quality'
    , 'readability', 'reliability', 're(?:-| )?use' ,'re(?:-| )?usability', 'security', 'simplicity', 'testability', 'testable', 're(?:-| )?usable'
    , 'readable', 'portable', 'maintainable', 'flexible', 'efficient', 'encapsulation'
                  ]

software_goals_modification = [
    'better','improv(?:e|es|ed|ing)', 'increas(?:e|es|ed|ing)', 'reduc(?:e|es|ed|ing)', 'worse', 'make', 'more', 'less'
]

software_terms = ['algorithm(?:s)?', 'assertion(?:s)?', 'assignment(?:s)?', 'class(?:es)?', 'code', 'collection(?:s)?'
    , 'conditional(?:s)?', 'constant(?:s)?', 'constructor(?:s)?', 'control'
    , 'delegate', 'delegation'
    , 'design pattern(?:s)?', 'error(?:-| )?code(?:s)?', 'exception(?:s)?', 'field(?:s)?', 'flag(?:s)?', 'function(?:s)?', 'getter(?:s)?'
    , 'guard clause(?:s)?', 'hierarch(?:y|ies)', 'implementation(?:s)?', 'inheritance', 'inline'
    , 'interface(?:s)?', 'internal', 'macro(?:s)?'
    , 'magic number(?:s)?', 'member(?:s)?', 'method(?:s)?', 'modifier(?:s)?', 'null object(?:s)?', 'object(?:s)?', 'parameter(?:s)?'
    , 'patch(?:es)?',  'pointer(?:s)?', 'polymorphism', 'quer(?:y|ies)',  'reference(?:s)?'
    , 'ref(?:s)?'
    , 'return type', 'setter(?:s)?', 'static', 'structure(?:s)?', 'sub(?:-| )?class(?:es)?', 'super(?:-| )?class(?:es)?', '(?:sub)?(?:-| )?system(?:s)?'
    , 'template(?:s)?', 'type(?:s)?'
    , 'uninline'
    #, 'value(?:s)?'
    , 'variable(?:s)?', 'handler', 'plugin'
    #, '(?:in)?validation'
    #, 'input', 'output'
    , 'unit(?:s)?'
    , 'contravariant', 'covariant'
                  # , 'link(?:s)?'
    ,
                  'action(?:s)?'
                  # , 'event(?:s)?'
    , 'queue(?:s)?', 'stack(?:s)?'
    #, 'change(?:\s)?log'
    , 'driver(?:s)?'
    #, 'hook(?:s)?'
    #, 'target(?:s)?'
    , 'storage', 'tool(?:s)?', 'module(?:s)?', 'log(?:s)?', 'setting(?:s)?'
    #, '(?:index|indexes|indices)'
    , 'fall(?: |-)back(?:s)?', 'memory', 'param(?:s)?', 'volatile', 'file(?:s)?'
    , 'generic(?:s)?'
    #, 'test(?:s)?'
    , 'initialization(?:s)?', 'public', 'protected', 'private' ,'framework', 'singelton', 'declaration(?:s)?'
    , 'init' , 'destructor(?:s)?', 'instances(?:s)?', 'primitive(?:s)?'
    #, 'middle man'
    #, 'hierarchy'
                  ]

refactor_entities = software_terms + ['(helper|utility|auxiliary) function(?:s)?']


# Well, we need them...
unnedded_terms = ['unnecessary', 'unneeded', 'unused', '(?:not|never|no longer) used'
    #, 'old'
    , 'no longer needed', 'redundant', 'useless', 'duplicate(?:d)?', 'deprecated', 'obsolete(?:d)?', 'commented']


modification_activity = [
                            #'chang(?:e|esed|ing)'
 'clean(?:ing|s|ed)?'
#,
                            'clean(?:ing)?(?:-| )?up(?:s)?'
    , 'combin(?:e|es|ed|ing)',
           'compos(?:e|es|ed|ing)','de(?:-| )?compos(?:e|es|ed|ing)', 'convert(?:ed|s|ing)?'
                            #, 'creat(?:e|es|ed|ing)'
                            , 'dead'
#, 'delet(?:e|es|ed|ing)'
                            , 'deprecat(?:e|es|ed|ing)'
                            , 'drop(?:ed|s|ing)?', 'duplicat(?:e|es|ed|ing)', 'extract(?:ed|s|ing)?'
           # Goals modification only?
                            ,'improv(?:e|es|ed|ing)', 'increas(?:e|es|ed|ing)'
                            #, 'instead'
                            #, 'kill(?:ed|s|ing)?'
                            , '(?:make|makes|made|making)'
                            , 'mov(?:e|es|ed|ing)'
           # , 'provid(?:e|es|ed|ing)'
                            , 'rebuil(?:d|ds|ding|t)'
                            , 'replac(?:e|es|ed|ing)', 'redundant', 're(?:-|)?organiz(?:e|es|ed|ing)'
    , 're(?:-|)?structur(?:e|es|ed|ing)','separat(?:e|e s|ed|ing)'
                            , 'split(?:s|ing)?', 'subsitut(?:e|es|ed|ing)', 'tid(?:y|ying|ied)'
, 'short(:?en|er|ing|s)?', 'polish(?:ed|es|ing)?', '(?:get|got|getting) rid', 'encapsulate'
                            , 'hide(?:e|es|ed|ing)', 'un(?:-| )?hid(?:e|es|ed|ing)'
                            , 'parameteriz(?:e|es|ed|ing)'
                            , 'substitut(?:e|es|ed|ing)'
                            #, 'introduc(?:e|es|ed|ing)'
                        , ] + unnedded_terms

feedbak_terms = [ 'py(?:-| )?lint', 'lint', 'review comments(?:s)?', 'code review', 'cr', 'pep8'
                  ]
feedback_action = ['fix(?:ed|s|es|ing)?', 'fix(?:-| )?up(?:s)?', 'resolv(?:e|ed|es|ing)', 'correct(?:ed|s|es|ing)?']

perfective_header_action = [
    #'polish(?:ed|es|ing)?'
    #, 'clean(?:ing|s|ed)?(?:-| )?up(?:s)?'
     'clean(?:ing|s|ed)?(?:-| )?up(?:s)?'
    , 'cleaner'
    , 'deprecat(?:e|es|ed|ing)'
    , 'extract(?:ed|s|ing)?',
    're(?:-|)?organiz(?:e|es|ed|ing)', 're(?:-|)?structur(?:e|es|ed|ing)', 'tid(?:y|ying|ied) up'
    , 'improv(?:e|ed|es|ing|ement|ements)' , 're(?:-|)?organiz(?:e|es|ed|ing)', 're(?:-|)?structur(?:e|es|ed|ing)'
    , '(helper|utility|auxiliary) function(?:s)?'
    , '(?:move|moved|moves|moving) to'
    , 'separat(?:e|es|ed|ing)'
    , 'split(?:s|ing)?', '->'
    #, '(private|public|protected|static)'
]

# TODO - rewrited, move into/out???, deduplicate, remove legacy, redo, PR, feedback

# TODO - clean , style, prettier, "->", refine, "Removed commented code", "More startup improvements.", recode
# ""Remove another old function", "improved redis error message", utility functions, never used
# Checkstyle


# TODO - perfective, not refactor - ident, spacing, tabs, "tabs -> spaces", cosmetic, ""*** empty log message ***"
# examples ""DOC: remove mention of TimeSeries in docs"

# TODO - add "resolving review comments"
# TODO - lint, pylint
refactor_context = [ 'clean(ing)?(-| )?up(s)?'
    ,'call(?:s|ed|ing)?[\s\S]{1,50}instead'
    , 'collaps(?:e|es|ed|ing)', 'consolidat(e|es|ed|ing)'
    , 'decompos(?:e|es|ed|ing)'
    , 'drop(?:ed|s|ing)?( back)', 'encapsulat(e|es|ed|ing)'
    , 'gereneliz(?:e|es|ed|ing)'
                    # , 'inline'
                    # , 'no longer needed', 'not used', 'obsolete(d)?'
    , 'optimiz(?:e|es|ed|ing|ation|ations)'
    , 'pull(?:ed|s|ing)? (up|down)', 're(?:-)?(?:write|wrote)', 're(?:-| )?factor(?:ed|s|ing|ings)?'
    , 're(-)?implement(ed|s|ing)?'
    , 'renam(?:e|es|ed|ing|ings)', 'better nam(?:e|es|ing)','re(?:-)?organiz(e|es|ed|ing)', 're(?:-)?organization'
    , 're(?:-)?work(ed|s|ing|ings)?'
    , 'reorg' , 'simplif(y|es|ied|ying|ication)', 'suppress(es|ed|ing)? warning(?:s)?'
    , 'unif(?:y|ies|ied|ing)', 'uninline'
    , 'beef(?:ed|s|ing)? up', 'refactor(?:ing)?(?:s)?', 'code improvement(?:s)?'
    #, '(?:^|^[\s\S]{0,25}%s)(?:%s)%s[\s\S]{0,25}$' % (term_seperator, "|".join(perfective_header_action), term_seperator)
    , 'revis(?:e|es|ed|ing)'
    , 're(?:-)?construct(?:s|ed|ing)?'
    , 're(?:-)?(?:write|write|wrote|writing)'
    , 're(?:-)?cod(?:e|ed|es|ing)'
    , 'factor(?:ed|s|ing)? out'
    , 're(?:-| )?packag(?:e|es|ed|ing)'
    #, 'code review'
    #, 'collapse'
    #, "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(feedback_action
    #                                                                                      , just_before=True)
    #                                                                 , term_seperator
    #                                                                 , term_seperator
    #                                                                 , term_seperator
    #                                                                 , "|".join(feedbak_terms)
    #                                                                 , term_seperator)
                    # ,'us(e|es|ed|ing)[\s\S]{1,50}(instead)'
                    # , '(instead)[\s\S]{1,50}us(e|es|ed|ing)'
                    ]
# https://refactoring.guru/refactoring/techniques

# TODO - change [\s\S] with . ?
removal = [ 'add(?:s|ed|ing)?[\s\S]{1,50}helper(?:s)?'
    ,  'us(?:e|es|ed|ing)[\s\S]{1,50}instead'
    #,  'us(?:e|es|ed|ing)[\s\S]{1,25}\(\)[\s\S]{1,25}instead'
    ,  'split(?:s|ing)?[\s\S]{1,50}into'
    ,  'break(?:s|ing)?[\s\S]{1,50}into'
    ,  'separat(?:e|e s|ed|ing)[\s\S]{1,50}into'
    #,  'replac(?:e|es|ed|ing)?[\s\S]{1,50}with'
    ,  'replac(?:e|es|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    , 'remov(?:e|es|ed|ing)[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    #, '(?:this|that|is)[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'kill(?:s|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'drop(?:s|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
    ,  'mov(?:e|es|ed|ing)?[\s\S]{1,50}(?:%s)' % "|".join(unnedded_terms)
            ]

documentation_entities = [
    'change(?: |-)?log',
    'comment(s)?',
    'copy(?: |-)?right(?:s)?',
    'doc(?:s)?',
    'documentation',
    'explanation(?:s)?',
    'man(?: |-)?page(?:s)?',
    'manual',
    'note(?:s)?',
    'readme(?:.md)?',
    'translation(?:s)?',
    'java(?: |-)?doc(?:s)?',
    'java(?: |-)?documentation',
    'example(?:s)?',
    'diagram(?:s)?',
    'guide(?:s)?',
    'icon(?:s)?',
    'doc(?: |-)?string(?:s)?',
    'tutorials(?:s)?',
    'help',
    'man',
    'doc(?: |-)?string(?:s)?',
    'desc',
    'copy(?: |-)?right(?:s)?',
    'explanation(?:s)?'

]

prefective_entities = documentation_entities +[
    'indentation(?:s)?'
    , 'style'
    , 'todo(s)?'
    , 'typo(s)?'
    , 'verbosity']

adaptive_context = [
    '(?:un)?hid(?:e|es|den)', 'add(?:s|ed|ing)?', 'allow(?:s|ed|ing)?'
    , 'buil(?:t|ds|ing)', 'calibirat(?:e|es|ed|ing)'
    , 'configure'
    , 'creat(?:e|es|ing)' #   O created
    , 'deferr(?:ed|s|ing)?'
    , 'disabl(?:e|es|ed|ing)'
    , 'enhanc(?:e|es|ed|ing)', 'extend(?:s|ed|ing)?', 'form(?:ed|s|ing)?'
    , 'implement(?:ed|s|ing)?', 'import(?:s|ed|ing)?', 'introduc(?:e|es|ed|ing)'
    , 'port(?:s|ed|ing)?'
    , 'provid(?:e|es|ed|ing)'
    , 'report(?:s|ed|ing)?'
    , 'support(s|ed|ing)?'
    , 'updat(?:e|es|ed|ing)'
    , 'upgrad(?:e|es|ed|ing)'

    # , 'mov(e|es|ed|ing)'
    # , 'print(s|ed|ing)?'


]


#

# 'build', , 'mark(s|ed|ing)?', 'mov(e|es|ed|ing)', 'us(e|es|ed|ing)'
adaptive_context_old = [
    'allow(?:s|ed|ing)?'
    , 'add(?:s|ed|ing)?'
    ,' build'
    # , 'mark(s|ed|ing)?', 'mov(e|es|ed|ing)', 'us(e|es|ed|ing)'
    ,' (?:make|makes|made|making)'
    ,' (?:un)?hid(e|es|den)'
    , 'allow(?:s|ed|ing)?'
    , 'buil(?:t|ds|ing)'
    , 'calibirat(?:e|es|ed|ing)'
    , 'chang(?:e|es|ed|ing)'
    , 'complet(?:e|es|ed|ing)'
    , 'configure'
    # , 'creat(e|es|ed|ing)'
    , 'creat(?:e|es|ing)'  # NO created
    , 'deferr(?:ed|s|ing)?'
    , 'disabl(?:e|es|ed|ing)'
    , 'enabl(?:e|es|ed|ing)'
    , 'enhanc(?:e|es|ed|ing)', 'extend(?:s|ed|ing)?', 'form(?:ed|s|ing)?'
    , '(get|got|getting)'
    # , 'handl(e|es|ed|ing)'
    , '\simplement(ed|s|ing)?'
    , 'import(s|ed|ing)?', 'introduc(e|es|ed|ing)'
    , 'new'
    , 'port(s|ed|ing)?'
    , 'preserv(?:e|es|ing)'
    , 'print(s|ed|ing)?'
    , 'provid(e|es|ed|ing)'
    , 'quirk(s|ed|ing)?'
    , '(rm|remov(e|es|ed|ing))'
    , 'report(s|ed|ing)?'
    , 're(-)?buil(d|ds|t|ding)'
    , 're(-)?calibirat(e|es|ed|ing)'
    , '(set|sets|setting)'
    , 'switch(es|ed|ing)?'
    , 'support(s|ed|ing)?'
    # , 'us(e|es|ed|ing)'
    , 'updat(e|es|ed|ing)'
    , 'upgrad(e|es|ed|ing)'
]

adaptive_entities = ['ability', 'configuration', 'conversion', 'debug', 'new', 'possibility', 'support'
    , 'test(s)?', 'tweak(s)?', 'mode', 'option']


def match(commit_text, regex):
    text = commit_text.lower()

    return len(re.findall(regex, text))


def build_sepereted_term(term_list , just_before =False):
    if just_before:
        sep = "%s(%s)" % (term_seperator, "|".join(term_list))
    else:
        sep = "%s(%s)%s" % (term_seperator, "|".join(term_list), term_seperator)
    return sep


def build_refactor_regex():
    header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)%s' % (term_seperator
                                                       , "|".join(perfective_header_action)
                                                       , term_seperator)

    activity_regerx = "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(modification_activity
                                                                                          , just_before=True)
                                                                     , term_seperator
                                                                     , term_seperator
                                                                     , term_seperator
                                                                     , "|".join(refactor_entities)
                                                                     , term_seperator)
    return "(%s)|(%s)|(%s)" % (build_sepereted_term(refactor_context)
                          , activity_regerx
                          , header_regex)


def build_refactor_goals_regex():
    goals_regerx = "(?:(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)%s)" % (build_sepereted_term(software_goals_modification
                                                                                       , just_before=True)
                                                                  , term_seperator
                                                                  , term_seperator
                                                                  , term_seperator
                                                                  , "|".join(software_goals)
                                                                  , term_seperator)
    return goals_regerx


def build_non_code_perfective_regex():

    non_perfective_entities = ['warning(?:s)?'
                               , 'format(?:ting)?'
                               , 'indentation(?:s)?'
                              ]
    # TODO - applied to perfective entities too here, which is a bug.
    modification_action = ['clean(?:-| )?up(?:s)?']
    non_perfective_context = [
                            'fix(?:es|ed|ing)?'
                            ,'(?:get|got|getting) rid'
                            , 'support(?:s|ed|ing)?'
                            ]
    modifiers = modification_activity + non_perfective_context
    activity_regerx = "((?:%s)(?:\s|%s[\s\S]{0,50}%s)(?:%s))" % (build_sepereted_term(modifiers, just_before=True)
                                                                                , term_seperator
                                                                                , term_seperator
                                                                                , "|".join(prefective_entities
                                                                                           + non_perfective_entities))
    doc_header_regex =  '(?:^|^[\s\S]{0,25}%s)(?:%s)[\s\S]{0,25}(?:%s)' % (term_seperator
                                                       , "|".join(perfective_header_action)
                                                       , build_sepereted_term(documentation_entities))


    no_prefective_action = "|".join([
        'convert(?:ed|s|ing)?(?:%s|%s[\s\S]{0,50}%s)support(?:s|ed|ing)?' % (
            term_seperator,term_seperator, term_seperator)
        , '(?:make|made|making|makes)(?:%s|%s[\s\S]{0,50}%s)work' % (term_seperator, term_seperator, term_seperator)
        , '(?:make|made|making|makes)(?:%s|%s[\s\S]{0,50}%s)sense' % (term_seperator, term_seperator, term_seperator)
        , 'improv(?:e|es|ed|ing) handling'
        , '(?:%s)(?:%s|%s[\s\S]{0,50}%s)(?:%s)' %(build_sepereted_term(non_perfective_entities,just_before=True)
                                                   ,term_seperator
                                                   , term_seperator
                                                   , term_seperator
                                                   , "|".join(modification_action)
                                                   )
        , doc_header_regex

    ])
    non_perfective_context = '(?:%s|%s)' % (no_prefective_action
                                         , activity_regerx)

    return non_perfective_context


# instead of
# make sure
# missed to create
# can be replaced, e9dee4fc76caaca231bf10728d4f82bc46581bc5
# no seperation for create eb1027b5e8c047059f68e7547188d08c7fde0b6f
# inline c9d4924dcf129512dadd22dcd6fe0046cbcded43
# can be optimized 197fc962fa8a3153dc058abfa2ae8c816d67ea04
# corrective trouble (use wordnet) b580f0706dc1dcded6d1a584c37a83dd1cb2ea2a
# not used 72894b26c24b1ea31c6dda4634cfde67e7dc3050


def built_is_refactor(commit_text):
    removal_re = build_sepereted_term(removal)

    return (match(commit_text, build_refactor_regex())
            + match(commit_text, removal_re)
            + match(commit_text, build_refactor_goals_regex())
            - match(commit_text, build_non_code_perfective_regex())
            - match(commit_text, build_non_positive_linguistic(build_refactor_regex()))
            - match(commit_text, build_non_positive_linguistic(build_sepereted_term(removal)))
            - match(commit_text, build_non_positive_linguistic(build_refactor_goals_regex()))
            ) > 0

def build_perfective_regex():
    non_code = build_sepereted_term (prefective_entities)

    perfective = "(%s)" %  non_code

    return perfective

adaptive_header_action = "|".join([
    'upgrad(?:e|es|ed|ing)',
    'configur(?:e|es|ed|ing)',
    '(?:keep|change)\s+(?:the\s+)?default',
    'new',
    # 'merg(?:e|es|ed|ing)',
    # '(?:make(?:s)?|made|making)',
    # 'merg(?:e|es|ed|ing)',
    'clear(?:s|ed|ing)?',
    # 'convert(?:s|ed|ing)?',
    # 'check(?:s|ed|ing)?',
    'add(?:s|ed|ing)?',
    # 'build',
    # 'buil(?:d|t|ds|ing)',
    '(?:im)?port(?:s|ed|ing)?',
    '(?:un)?hid(?:e|es|den)',
    'updat(?:e|es|ed|ing)',
    'disabl(?:e|es|ed|ing)',
    'enabl(?:e|es|ed|ing)',
    'quirk(?:s|ed|ing)?',
    'allow(?:s|ed|ing)?',
    'provid(e|es|ed|ing)',
    # 'remov(e|es|ed|ing)'

    ###
    # , 'build'
    # , 'mark(?:s|ed|ing)?'
    # , 'us(?:e|es|ed|ing)'
    # , '(?:make|made|making)'
    # , 'chang(?:e|es|ed|ing)'
    # , 'creat(?:e|es|ed|ing)'
    # , 'enabl(?:e|es|ed|ing)'
    # , 'handl(?:e|es|ed|ing)'
    'remov(?:e|es|ed|ing)'

])

file_scheme = '([a-z  -Z0-9_\*\.])+\.[a-zA-Z]{1,4}'

adaptive_actions = [  # 'revert(?:s|ed|ing)?',
    #'merg(?:e|es|ed|ing)[\s\S]{1,5}(pull request|pr|branch)',
    'add(?:s|ed|ing)?[\s\S]{1,50}(?:version|v\d|ver\d)',
    '(^|\s)implement(?:ed|s|ing)?\s',
    '(?:make(?:s)?|made|making)[\s\S]{1,50}consitent',
    'updat(?:e|es|ed|ing)[\s\S]{1,25}to[\s\S]{1,25}\d+.\d',
    'updat(?:e|es|ed|ing)\s+(to\s+)?\d+\.\d',
    '(?:add(s|ed|ing)?|delet(?:e|es|ed|ing)|updat(?:e|es|ed|ing))\s+' + file_scheme,
    # '(add(s|ed|ing)?|delet(e|es|ed|ing)|updat(e|es|ed|ing))\s+([A-Z0-9_]*)', # TODO - run without lower
    '(^|^[\s\S]{0,25}%s)(%s)%s' % (term_seperator, adaptive_header_action, term_seperator),
    # '^(?:version|v\d+\.\d|ver\d+\.\d)',
    '^\[(?:IMP|imp)\]',  # TODO - take care of upper/lower case
    'support(?:s|ed|ing)?\sfor\s',
    'show(?:es|ed|ing)?[\s\S]instead']


def build_adaptive_action_regex():

    return "(%s)" % ("|".join(
    adaptive_actions))




def build_adaptive_regex():

    adaptive_context_re = build_sepereted_term(adaptive_context, just_before=True)


    return "((%s)\s[\s\S]{0,50}(%s)%s)" % (adaptive_context_re
                            ,  "|".join(adaptive_entities + software_terms)
                            , term_seperator)


modals = ['can', 'could', 'ha(?:ve|s|d)', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']

def build_non_adaptive_context():

    non_adaptive_header_action = "|".join([
                                'transla(?:tion|et|eted|ets|ting)'
                                ,  'readme(?:.md)?'
                              ])

    non_adaptive_header ='^[\s\S]{0,50}(%s)' % non_adaptive_header_action

    entities = documentation_entities + ['bug',
                'helper',
                'miss(?:ing|ed)',
                'to(?: |-)?do(?:s)?',
                'warning(?:s)?'
                ]

    adaptive_actions = ['remov(?:e|es|ed|ing)']
    non_adaptive_entities = documentation_entities + software_terms + unnedded_terms + [file_scheme]


    return '(%s)' % "|".join(['(?:%s)\s[\s\S]{0,50}(?:%s)' % (build_sepereted_term(adaptive_context, just_before=True)
                                                            , "|".join(entities))
                     , non_adaptive_header
                     , '(?:%s)\s[\s\S]{0,50}(?:%s)' % (build_sepereted_term(adaptive_actions, just_before=True)
                                                            , "|".join(non_adaptive_entities))
                     ])





def build_non_positive_linguistic(positive_re):

    non_actionable_context = ['for(?:get|gets|got|geting)'
        , 'allow(s|ed|ing)?']


    return '(?:%s)' % "|".join([
        '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(modals, just_before=True)
                                      ,  positive_re)
        , '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(negation_terms, just_before=True)
                                        ,  positive_re)
        , '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(non_actionable_context, just_before=True)
                                        ,  positive_re)
        , '(?:%s)[\s\S]{0,10}(?:%s)' % (build_sepereted_term(documentation_entities, just_before=True)
                                        ,positive_re)
    ])


def build_non_adaptive_linguistic():

    return build_non_positive_linguistic(build_adaptive_regex())

def is_adaptive(text):

    return (match(text, build_adaptive_regex())
            + match(text, build_adaptive_action_regex())
            - match(text, build_non_adaptive_context())
            - match(text, build_non_adaptive_linguistic()))

def classifiy_commits_df(df):
    df['corrective_pred'] = df.message.map(lambda x: is_fix(x))
    df['is_refactor_pred'] = df.message.map(lambda x: built_is_refactor(x))
    df['perfective_pred'] = df.message.map(lambda x: (match(x, build_perfective_regex())) +
                                                     (match(x, build_refactor_regex())) > 0)
    df['adaptive_pred'] = df.message.map(lambda x: is_adaptive(x) > 0)

    return df


def regex_to_big_query(re):
    # Take care of encoding
    re = re.replace("\\", "\\\\").replace("'","\\'")
    # No need for grouping
    re = re.replace("(?:", "(")
    str = "(" + "LENGTH(REGEXP_REPLACE(lower(message),"  + "'%s', '@'))"   % re + "-" \
        + "LENGTH(REGEXP_REPLACE(lower(message),"  + "'%s', ''))"  % re + ")"

    return str


def adaptive_to_bq():


    print "# Adaptive"
    print "# Adaptive :build_adaptive_regex()"
    print ","
    print regex_to_big_query(build_adaptive_regex())
    print "#Adaptive :build_adaptive_action_regex()"
    print "+"
    print regex_to_big_query(build_adaptive_action_regex())
    print "# Adaptive :build_non_adaptive_context()"
    print "-"
    print regex_to_big_query(build_non_adaptive_context())
    print "# Adaptive :build_non_adaptive_linguistic()"
    print "-"
    print regex_to_big_query(build_non_adaptive_linguistic())




def refactor_to_bq():

    # TODO - add build_refator_goals_regex and negation
    print "# Refactor"
    print "# Refactor :build_refactor_regex()"
    print ","
    print regex_to_big_query(build_refactor_regex())
    print "# Refactor :build_sepereted_term(removal)"
    print "+"
    print regex_to_big_query(build_sepereted_term(removal))

    print "# Refactor :build_refactor_goals_regex()"
    print "+"
    print regex_to_big_query(build_refactor_goals_regex())


    print "# Refactor :build_non_code_perfective_regex()"
    print "-"
    print regex_to_big_query(build_non_code_perfective_regex())
    print "# Refactor :build_non_positive_linguistic(build_refactor_regex())"
    print "-"
    print regex_to_big_query(build_non_positive_linguistic(build_refactor_regex()))


    print "# Refactor :build_non_positive_linguistic(build_sepereted_term(removal))"
    print "-"
    print regex_to_big_query(build_non_positive_linguistic(build_sepereted_term(removal)))


    print "# Refactor :build_non_positive_linguistic(build_refactor_goals_regex())"
    print "-"
    print regex_to_big_query(build_non_positive_linguistic(build_refactor_goals_regex()))


English_terms = ['about', 'all', 'also', 'and', 'because', 'but', 'can', 'come', 'could', 'day', 'even', 'find'
    , 'first', 'for', 'from', 'get', 'give', 'have', 'her', 'here', 'him', 'his', 'how', 'into', 'its', 'just', 'know'
    , 'like', 'look', 'make', 'man', 'many', 'more', 'new', 'not', 'now', 'one', 'only', 'other', 'our', 'out'
    , 'people', 'say', 'see', 'she', 'some', 'take', 'tell', 'than', 'that', 'the', 'their', 'them', 'then', 'there'
    , 'these', 'they', 'thing', 'think', 'this', 'those', 'time', 'two', 'use', 'very', 'want', 'way', 'well', 'what'
    , 'when', 'which', 'who', 'will', 'with', 'would', 'year', 'you', 'your']

def build_English_regex():
    Eng_re = "%s(%s)%s" % (term_seperator
                               , "|".join(English_terms)
                               , term_seperator)

    return Eng_re

def is_English(commit_text):
    text = commit_text.lower()

    English_num = len(re.findall(build_English_regex(), text))

    return English_num > 0



observed =[# False positives
    'ef04a29737dd08352fdf6431d119ca636d664efe'
    , 'aeb4f20a02b4c984c48995ad54f40caf5ffa0705'
    , '4f066173f  8deb8874f41917e5d26ea2e0c46e3b'
    , '5f29805a4f4627e766f862ff9f10c14f5f314359'
    , '0ad6d37d17a9cc4012720a2d5c35945d458514e8'
    , '6c39d116ba308ccf9007773a090ca6d20eb68459' # a qoute example
    , '733fe62640bc88bc49f02c217c754d05c3337de4'
    , 'c7c6b1fe9f942c1a30585ec2210a09dfff238506'
    , '709de13f0c532fe9c468c094aff069a725ed57fe'
    , 'cbbc49877d44408c4d0decf77c3c141732bbc679'
    , 'e6e898cfea5f35d64f850277e7fa295c386cf953'
    , '62b08a0959a3bc7b4afdc97bb6f051f5cba8c4ce'
    , 'ee20a98314e52a6675e94d1a07ca205ffdf09a72'
    , '00c5ec287ab3c8e1cac343f6e1155bad4cbb23ce'
    , '051031143544ff196d94927be8f384864fbca6a4'
    , '932f0549f872cde022eed200910ee3291b1d3c69'
    , 'b040b44c3  c251882da8488a5f038435a531312c'
    , 'f8c07de6beac55c3273cbd679bfa67555ef14ef5'
    , '9be7efdc163b8d9c2b27aa12581f42d4cade94d1'
    , '952fccac50350481742425cac0c80f36ba8b83f2' # remove refs
    # , '32780cd1350e651e68bdf33b7f5b009d21d5b794' allows to create
    , '40be0c28b33ff0821594a3fa7126354dfe6eccd1'  # too long negation
    , '654d09f9c52c1374cd8408e3aa9f42c1330bb1b5'
    , 'aa7a6c5f9c554417ce7a34076ae21289d0c8a5d1'
    , '0ee1d714c285aabaadf7495bf5820114ad0959b1'
    , '1dcc336b02bff3d38f173feac55a2b6c25a5fb54'
    , '02b1bae5e1c0f810168037be0134685085e95e88'
    , 'b164935b38d64557a32892e7aa45e213e9d11ea8'
    , '2f3c78a2358fb127b017fce8e92c34b9b8d0259e'
    , 'c976bc82339437e840f7dbf0b8c89c09d3fcd75e'


    # False negative
    , '17d2cc25f04462fd5d835318f02fb5492576ab4b'
    , '04f1b6cdfe2743cbfda68d221d2faa0e5ac13f6c'
    , 'd2eecb03936878ec574ade5532fa83df7d75dde7'
    , '1c10070a55a38ad8489df8afd52c9a3ffd46bbb5'
    , 'f39d1b9792881ce4eb982ec8cc65258bf95674b5'
    , '968a5763fb7247feb0e69573a2975a7a0c094267'
    , '63427530fa7a78b42a19f47fb0c12b303c0666ca'
    , '4b9bc014bf4c65e1da86fbc9721f04e2763feca9'
    , 'f32f986f6e134f85a9f0c5ed66d98439d86e7cc4'
    , '4da456168f41499369bef5ebb33d5966cd9cbb8c'
    , 'c2d7051ed1727e6a7b0debe448b5f6ba915e246b'
    , '683d5fb526d7706794d671c6190b139c91ff753b'
    , '1ac4594d88f63ba1557cc1a30ec1f915ca55b7cb'
    , 'fae255253b393d5e4f0d77d5afa103bfc8b47a97'
    , '0df4604ed09873c46ddb3232a3efc5a2798854cb'
    , 'b625883f24d018c989173aeb727f6de954fb154d'
    , 'd0a0a08a1fdf07a222ac1d972a74bc923c569c84'
    , 'dac4ccfb64bcdd5b4c248ccc22903d67486573cd'
    , '902d21d5313ba08cccadc9fceee2df3cf34e84eb'
    , '897f17a65389a26509bd0c79a981  d1c9ea8ea6f'
]


adaptive_observed = ['5f29805a4f4627e766f862ff9f  0c14f5f314359'
    , '330e3f95b30d9616edd6df7646473179c159c00d'
    , '364f5c4d7a8e8289058dafe3b9e6fe9f7cee5566'  # should not add
    , '2ed6603c038104e0e9834827080f490ae21ff1ba'  # might recheck
    , '66c63b84b23d39ce191a18833b5a769370114ec9'
    , '797a796a13df6b84a4791e57306737059b5b2384'
    , 'f32f986f6  134f85a9f0c5ed66d98439d86e7cc4'
    , 'd9e5d6183715e691b37afd3785c311d05cd1338d'
    , '0ee1d714c285aabaadf7495bf5820114ad0959b1'
    , 'c868595d5686e97183bc1ad8  502835d81d7a457'  # port as noun
    , '95f4efb2d78661065aaf0be  7f5bf00e4d2aea1d'
    , 'e2a1b9ee2335c35e0e34c88a024481b194b3c9cc'
    , '7d76b911d722632224eb6f16342043c7ba61d861'  # merge a fix
    , 'cbe9ee00cea58d1f77b172fe22a51080e90877f2'  # merge with clean up
    , '5677c38e376a9d3525d94f4a89e7dcc387cda98f'
    , 'b9bd9ae3f  3e8a917ff3e374a1f5599fc72fceb0'
    , 'a4a87d9916b2cfd7a3feed2ac708f85c8bdd83fc'
    , 'bca268565fd18f0b36ab8fff6e1623d8dffae2b1'
    , '1fef891761ddcbd7e57ec3961a0fb748003222ac'  # merge , also few of the above
    , 'df2f5e721ed36e21da27e1f415c71ba0e20f31b5'
    , 'd39c3b895  76427c5083a936e00f3f5b7f0fc1b3'
    , 'ef71b1b87521ff93ed77b3e8f3e  49afb392761c'
    , '75464d585cac944e3cffb4401663e4c1185b7cb5'
    , '35ec7aa29833de350f51922736aefe22ebf76c4d'  # class not clear
    , 'd6ba06b8b9a947a8385769f4586  1d3c97410226'  # indirect speech
    , 'ee20a98314e52a6675e94d1a07ca205ffdf09a72'
    , '54f2d7361da09f3fc2b5407f93ad3b86df951577'
    , '352d4657b23fbd329efccc396000a549e0150907'  # merge
    , '3fa37deb1a287e100c7db5b4f964784fd664bee9'
    , '2dc27f01ec3990d79fc97386459191fc3da2b02f'
    , 'b7783b691  bd5dd12d19150334de9c32d9cbfcad'
    , '9cd9d65ba40aef21342bcdf0ea35d20c9a75be07'
    , '4d85b471593d03e141f9160a58574b9204363267'
    , '2320f2373326269f1  961b7ffc114cd5f20b88e5'  # merge
    , '902d21d5313ba08cccadc9fceee2df3cf34e84eb'
    , 'ad1f8bf073e1c1996bb37b669352e3d7b1eb2b1f'
    , '9b641251aee1a804169a17fe4236a50188894994'  # port
    , '8bf29b0eb3ba38c8cf55e60976f124672cda7ab2'
    , 'c1e6098b23bb46e2b488fe9a26f831f867157483'
    , '051031143544ff196d94927be8f384864fbca6a4'
    , 'e36c455c2f5fee08fed395e94c7ab156cd159360'
    , '04f1b6cdfe2743cbfda68d221d2faa0e5ac13f6c'
    , '522b6a22722e4897aa3958eb4c5559bd3fc15433'
    , '21641e3fb1c2e53b3a0acf68e6f62f1f82f61445'
    , '744a82b004b0a08d55f579daa55e32d963353edc'
    , 'c427d27452b41378e305af80db5757da048dd38e'

                     # false negatives
    , 'ff49d86aedc3afbed5c109d60d2b6c02230cb5d4'
    , '12bc99d38606f86a94d6e553982321b6379e7d81'
    , '7a779490b9ea250e0b69e25fed4afc5e71fbb46c'
    , 'c2aba006aa376a6c76007e81f09fe3cf59e421f6'
    , '4836bb7988cf33bdf009cad92bc6953c31749938'
    , '42d7f7e884fcce78301ca88da3434f0fcbf3fee5'
    , '36286e23141e8a088b6881893626dfc8aff062d3'
    , '42f8eb7a1087442e9710ce75b355c0f28aadbf96'
    , 'ab372621723767fcf483dddc82b71f38441e18fd'
    , 'd632a2c35af16328f3f176bd3d86393108c38509'
    , '4ec133d125e8ccae185fc82118f0c302abbefa97'
    , 'f229d0451306508a8a16af337deef01b5d66b6d7'
    , '118052d81597eff3eb636d242eacdd0437dabdd6'
    , '2e7cbd43089318cf8cead76c6c35b55c390dae82'
    , '6e91f527cd0644530894ee3bfb06d209d3c8c54a'
    , 'dac4696a4b4f6823efda32f92dbc236a918c376f'
    , 'f46898017  fa6293917a8b59bfec71c6616e06c9'
    , 'b3ff4d8796f472e839831e81317de3680c62ccd3'
    , 'c106646d32451fcb0dd79ffc6774263f59d59084'
    , 'c5d28fb297efaa97c4b90e36f9dff3066e7f2778'  # Might reconsider
    , 'c4ded8d9771c8e8d5d7a202d58af9c70591dd675'
    , 'a26bf12afb608eb5a96192eaee35fc08ffbf85aa'
    , 'ebf905d8368d9ed132a2c86e4b1e213886d57bf6'
    , '9378f064aef207ddc6efaac02314b996941936e1'
    , '31f6a29a5  c0c9aa5c6e13abe0b00b81bb3c9601'
    , 'a870d62726721785c34fa73d852bd35e5d1b295b'
    , 'e04a4a411446ee214cc9837cca33517fa89cd0cb'
    , '8aea4d44e3a016437b594b773e1f  bc5f8ff3798'  # rearrang buttons
    , '6a486b7e09a5af285581864ee6b9e857b617ee64'
    , 'cc9b2757f7dadfc486e8e3fb3f94  b36dbb7fd2d'
    , '0f881d612071f2a90465f8fd4ffc943080271049'  # use X by default
    , '6c2626bba1c9901c864477bee15898d5ba868ab5'
    , '8db80b6  5a46194731a40fffc7290b280974bb85'  # new API version moved to master
    , '7ec676bb3dd6cba4b56fccb2d5aae08e66086b4e'  # CONST name
    , '33cc7df065b136a7c6d7f0f1bdb9615990d1a062'  # no synt  ctic evidence
    , 'b0a2d06f28a2e3409ff96d936140fce8940a7855'  # when ... should
    , '41f4451c203d2f964acbcd32  c0b6e678062fe43'
    , '5f8f718ae1e1a6b4e16e67e9e67aff1864419f2e'  # Do not check
    , 'abe1c3638ccf8b68536  fb52b111f6ad46d1cf71'
    , 'ad46c54868078440b4538fa263a5fd2f124b5  a57'  # unclear
    , 'c08a3c5d52aa616ffa1edb017c81309  4f030a5d'
    , '64d269d12b5ea72c53cb37e806a3a08709336  ca'  # remove fallbaks
    , '08def7cdf5ee57bc80ff14990799  195dd9e982f'  # v3
    , 'e58f173c788cf4e793b0ba241a358adad  941119'  # use
    , '8c48412f59d2ae51857516d8173a260f673c81  f'  # handle
    , '952fccac50350481742425cac0c80f36ba8b83  2'  # remove
    , '037dbf85d60daf43582d94140ef6eb29df37  c4b'  # complete
    , '45fda7d2fdcb10d09fd5498491212be6ffcf91e1'  #   emove
    , '4b221f0313f0f7f1f7aa0a1fd16ad400840def26'  # make
    , '0d00e37c23dce23cad5b98f82ae711675f324810'  #  not and then add
    , '9d9f5b44ed5271e85d1ea9b9e675d20914e621  3'  # use
    , 'f1088d471f8d846e817eb4d673212d18d9820c61'  # remove
    , '24c232d8e911ef6189e02da411dc2b72cb03bfcf'  # switch hook
    , '1d3840ac7704c5c04631f371f90559fa5e44d778'  # merge pull req  est
    , 'f14ca90e4c966f4d4eb70aee54c9a45fe864ba4f'  # uncertain
    , '  9575dad59de382dd1f1ddcaa6de38d9844691fe'  # set in header
    , 'd0ac70  deabf25afa6d2fc1503195c632c45355d'  # no syntactic evidence
    , 'be  4c2bb4731b0e6223a496eed615b816ac879ec'  # implement in header
    , '  848bef0382af53a7c9568bbc6757db97c53a0e3'  # replace in header  , '72679f287e2fbd672de1da5463dcfd71e7cc857e'  # imporve in header
    , '9dcbd061a54  bf61f67c33db2d4dd85f014838e6'  # new in header
    , '6532b14a5ede937fd36  5ea0c588c8edc1be1c57'  # skip becuase we can't create
    , '335abcad8611eecabcfc801ed3d8dd2fc413a74b'  # remove in header (rm)
    , '26216e3e15ed8257e582966989f5da3bdbdfa135'  # switch
    , '91121d9cfdeea84cdc837c  2f041dae735f5131c'  # remove
    , '852ee16a914fb3ada2f81e  22677c04defc2f15f'
    , '782b877c8073a9ef307ad6638ee472b8336b2b85'
    , '9e495a2603334f9c8fcc6802300c22fc8a0eae02'  # remove
    , '2f3c78a2358fb127b017fce8e92c34b9b8d0259e'  # rebuild index
    , '39fd33933b020  e4b6254743f2cede07c5ad4c52'
    , '59758f44592b0930e83b190cf0206e59d616c983'
    , 'b040b44c35c251882da8488a5f038435a531312c'
    , '33b8eb53b0bdaf40f81e133d5b0234b83e0415a1'  # version in header
    , 'a4efb20eedc3fe90d6524d62468352c5a25b7585'
    , '4559154a58fdb  8939dda8f1691a2aecf9154166'
    , 'a31ff707a27b3ed4a1c082c131194995efbbce4b'
    , 'e8a1a4ce69d0180fc4e9ce924872d373688132dc'
    , 'aa9348563c88b984d9c42c41aa5d227145c8ac4b'  # make determisitc in header
    , 'ba20a1645795106165db7b03a7fa61cd4  46b242'
    , '32432cc770eb49a612d37d89fee2e98fb0ba6422'  # convert in header
    , 'ab1b32bb96022ecfbb34af15a5e63a8b8da39536'
    , '413202e7d66a7388d6e786a87fb66890e64569b7'  # merged in header
    , '7d226b12df414df3214745100c1bbec8e3d7768b'
    , 'cbbc49877d44408c4d0decf77c3c141732bbc679'
    , '40be0c28b33ff0821594a3fa7126354dfe6eccd1'
    , 'c7c6b1fe9f942c1a30585ec2210a09dfff238506'
    , 'a8a45a4afc615926a705eee482c27ef166f2f9ec'
                     ]

stas_observed_fp = [
    '59d6a57f9a5e93146bcc83bcdb6f7c26ce644c51'
    , 'ad2358bba102bd4e9876028cf30341ec48aabe4f'
    , '1927f040774aa75d2dfe1d95fae9b43ee821361b'
    , '4405698ee99fe26d0ac9317a2df96096f2731a7b'
    , 'a62eecc95a164415d8f924e1c88e2d144282395d'
    , '98249507cff3e363ecb4c5f06f14f0bb96da1ad5'
    , 'f4cf5a7d4a1b3998632309288777275bc30517bb'
    , '9f923255878b7baefd89bc37af8fe3072f163322'
    , 'f0e9bf9f4ccaaa8e0b41f28f97fb7b6d15a88363'
    , '26d26d605e9887885afe78d943fbf152d965e44a'
    , 'eb1027b5e8c047059f68e7547188d08c7fde0b6f'
    , '5fee1b116bcd427168f1fafc7948c2e44520cc5c'
    , 'fe6e166c17990070a64c0b15d91b283a18c9dec5'
    , '04f1e7a41874bb93434c91c80544eda24afbb215'
    , '7206c04bb05a5ad7db4030aaf92b355b4c6538ff'
    , '1e49dcda27564e133e5528db215d8fb2d08130d0'
    , '7be3d247f90c23bbb11bc735276d51008243a7f6'
    , '64a2fde80a9f3  a71ac5c0e0b479c242bcecb561'
    , '14c657d448b6dd743806c4df2a321d58f4e0618e'
    , 'b40e657180d21655dc6d1ceed6c7726fe7c78071'
    , 'bfb2bf6246c48caaca6926e9cba6fae052242939' # instead - take care later
    , 'b580f0706dc1d  ded6d1a584c37a83dd1cb2ea2a'
    , '88a7e673b3ed7e07aa5cf31a1163697808a1f763'
    , '197fc962fa8a3153dc058abfa2ae8c816d67ea04'
    , 'ebe25c83d1f5f1202c56051  e8d58294b97ddf37'  # instead
    , '9a40de8e6c1974d4ae187b181055ecd4b1cc93da'
    , '66ae626f91e0b2bbfcf9b9059cb06b07883d9b0b'
    , '72894b26c24b1ea31c6dda4634cfde67e7dc3050' # not used
]

stas_observed_fn = [
    '0531b8bff5c14d9504beefb4ad47f473e3a22932'
    , '12954a69895db8e60522c72557b93c53973dc436'
    , '387c765e345c46a74a403aa2b8e3b7c634864087'
    , '959b0d84b4ee762461d47324cd2d4d00a3e49c0f'
    , 'ac26e42d1e85d  ac0b7bfa50c3ca3e5298493dd4'
    , 'ff642734febd8c5df95b67d5537c6f571a3c3aa2'
    , '45e4ec9000f8fbca1a5f04c68c1b516388f02a8f'
    , '7181fa35a35a4aa8e2f1bf8d2db39fa87a81e69d' # any char encoding problem
    , '8bf446f012faddf7762db07ed85199f05c58d6bf'
    , 'f1ac1054e3fc59f52237fb83da52c53dffe71de3'
    , '821b8e890f817  2bd070a6280c5255d8352d4a56'
    , 'a2ac32d1d9827f6edf7b72cf47fdbf9023e78ba9'
    , 'aa6d81a239cf699410b26517abba69a650b5ba42'
    , '663d9f43b0f5b49088102781ae8ce7123932e97b' # passive - method eliminated
    , '887139648d2e693bb50f286810231150bf1fba9f'
    , '575b48a63e55b5216bf78ecf48621ac8f9f80729'
    , '08d6538b3f9f611065682d08190747a7a93181fd'
    , 'd056c0b062311cc1e90ad134076fb13bcfe3ccf4'
    , '6ac389cf8a8d445d7689e672f1b9e8dd23f37419'
    , '296212eab186b860fd9494db9ed238b341fc2975'
    , 'ece368462243d7b4721029e31a261b450e026296'
    , '982eebf70ff4aebfc200c6373511f1ce0e8667ed'
    , '3d6253c27fbba7cb88626eead38ec18449ffd7bf'
    , 'ae6a2d38200dfe98755abfedf645621fe21ecf00'
    , '55ff4ae941e12c170a5e49801e599827e6461e27'
    , '041af28166c270b29b51f5f42fb3269c2dbe1159'
    , 'c4030850a057ed3cd8aedce4ea49147cd10a1798'
    , '6b3cef06538b2ba3ad1a67b8f0a67473b5596812'
    , '61b7b2defd9eccd914bde6b94c9fa978579eb4b3'
    , '5ed43d241a1786f41c97af3fc31de3a6f7d1f3ef'
    , 'e7950dccc0c4df38e172acbd99071e50397fc492'
    , '359a2756e623e605aaf29a1f3c7181666fae775c'
    , '77f1f5cd336bbd3c7b9d548a4916084bc1e56dc3'
    , '165c8954c94ca67d75ecd7fcbc7f1d3da41f5473'
    , '319b1c8ad41b769ff4bc5d8cb2d2eb9e3f5e9569'
    , '62f5e2a99d4f5c8bebf2b7ad581cae83ac437d0b'
    , 'ecea6e2615d9c1990e40613d5332e1f2d674a5b5'
    , '5bd0f4b011f861f866121b22a0fdb3c000bc5e01'
    , '8b9fdf23e2196dce9c956ba9088dd9b3146be60c'
    , '6858749cfd27f2975ce560e84b29e95d16eb88d2'
    , '6c0386029b4620e622f6d62939567f88238a21a2'
    , '21ee77a4383f5c970e8c73967d38615f5bfb48af'
    , '4145b9f00c83828c55ade3b509a7dce1ab621101'
    , '610115b44e10e5046b62a7dfad06dde18e0f83e7'
    , '55149154710b8bd1825442c308fb9b4b76054a63'
    , 'cfbc081dfdc76590d3f1e11b72caa1e30cf9134b'
    , 'a5b30fd0743195dd2d80dcec2c5e131d8bbc62ef'
    , 'ff7d4eebd8ebbf011656313dca8c6ee1a598c2aa'
    , 'c059f5382365930c7b87ff1dbaab0eae5452808a'
    , '595cdf05e962299c19c34bbfb370316636d074f2'
    , '2d7af3e17d5c33f79890cc7993b37da1b7d60fc9'
    , 'a2f8902b3a8569a1ebb4b4c87fab5a412cf4d389'
    , 'd89b18613f26094eee45d664cc2a8e5fc9fcba16'
    , 'caf2af077a3a6454cef39678564391c4abaf8eeb'
    , '610fa618aae58af50c12ee8d0c29d12b7460fd8a'
    , 'b27e240fdbf9ad91690ae596c21f511808377582'
    , '2a52decbbc8391f97ae443bb63032048ce2ae6c3'
    , '84f6d17c7bae1fbe1437ca0f62be476e012dbe8c' # due to negatives??
    , 'b0f0d2f28988eeffff9f6f6bd211c77565cc2704'
    , '4c73a29f99f0b9d2232b466972a55197758684db'
]


fp1 = [
    '5f29805a4f4627e766f862ff9f10c14f5f314359'
    , '6c39d116ba308ccf9007773a090ca6d20eb68459'
    , '952fccac50350481742425cac0c80f36ba8b83f2'
    , 'f9aa28adfc6a4b01268ebb6d88566cca8627905f'
    , '4f066173fe8deb8874f41917e5d26ea2e0c46e3b'
    , '90736e20e3805dd1ffff60e4750495944956cd44'
    , '4555227211ae867d8f8ec9eb5182273f58b648c0'
    , '932f0549f872cde022eed200910ee3291b1d3c69'
    , 'ef04a29737dd08352fdf6431d119ca636d664efe'
]

fp2 = [
    '6c39d116ba308ccf9007773a090ca6d20eb68459'
    , '952fccac50350481742425cac0c80f36ba8b83f2'
    , 'f9aa28adfc6a4b01268ebb6d88566cca8627905f'
    , '4f066173fe8deb8874f41917e5d26ea2e0c46e3b'
    , '4555227211ae867d8f8ec9eb5182273f58b648c0'
    , '932f0549f872cde022eed200910ee3291b1d3c69'
    , 'ef04a29737dd08352fdf6431d119ca636d664efe'
]




