

EElbrain two-stage model (v.0.26) 

# two-stage
# Two-stage test. Stage 1: fit a regression model to the data for each subject. Stage 2: test coefficients from stage 1 against 0 across subjects.

# stage 1 : str
# Stage 1 model specification. Coding for categorial predictors uses 0/1 dummy coding.
# vars : dict (optional)
# Add new variables for the stage 1 model. This is useful for specifying coding schemes based on categorial variables. Each entry specifies a variable with the following schema: {name: definition}. definition can be either a string that is evaluated in the events-Dataset, or a (source_name, {value: code})-tuple (see example below). source_name can also be an interaction, in which case cells are joined with spaces ("f1_cell f2_cell").
# model : str (optional)
# This parameter can be supplied to perform stage 1 tests on condition averages. If model is not specified, the stage1 model is fit on single trial data.
# Example: The first example assumes 2 categorical variables present in events, ‘a’ with values ‘a1’ and ‘a2’, and ‘b’ with values ‘b1’ and ‘b2’. These are recoded into 0/1 codes. The second test definition ('a_x_time' uses the “index” variable which is always present and specifies the chronological index of the event within subject as an integer count and can be used to test for change over time. Due to the numeric nature of these variables interactions can be computed by multiplication:

# tests = {'word_basic': {'kind': 'two-stage',
#                         'vars': {'wordlength': 'word.label_length()'},
#                         'stage 1': 'wordlength'},
#          'a_x_b': {'kind': 'two-stage',
#                    'vars': {'a_num': ('a', {'a1': 0, 'a2': 1}),
#                             'b_num': ('b', {'b1': 0, 'b2': 1})},
#                    'stage 1': "a_num + b_num + a_num * b_num + index + a_num * index"},
#          'a_x_time': {'kind': 'two-stage',
#                       'vars': {'a_num': ('a', {'a1': 0, 'a2': 1})},
#                       'stage 1': "a_num + index + a_num * index"},
#          'ab_linear': {'kind': 'two-stage',
#                        'vars': {'ab': ('a%b', {'a1 b1': 0, 'a1 b2': 1, 'a2 b1': 1, 'a2 b2': 2})},
#                        'stage 1': "ab"},
#         }


def _src_to_label_tc(ds, func):
        src = ds.pop('src')
        out = {}
        for label in src.source.parc.cells:
            if label.startswith('unknown-'):
                continue
            label_ds = ds.copy()
            label_ds['label_tc'] = getattr(src, func)(source=label)
            out[label] = label_ds
        return out


raw2 <- gather(raw, key="testtype", value = "testsentence", atest:etest)



parc = mne.read_labels_from_annot(subject='fsaverage', parc = 'PALS_B12_Brodmann', hemi='both', subjects_dir = '/Users/songhee/Documents/academic/research/VerbSpec/experiment/mri')

In [30]: print parc
[<Label  |  fsaverage, u'???-lh', lh : 11710 vertices>, <Label  |  fsaverage, u'???-rh', rh : 12369 vertices>, <Label  |  fsaverage, u'????-rh', rh : 12369 vertices>, <Label  |  fsaverage, u'???????-rh', rh : 12369 vertices>, <Label  |  fsaverage, u'ASP_deeper-lh', lh : 401 vertices>, <Label  |  fsaverage, u'Brodmann.1-lh', lh : 3258 vertices>, <Label  |  fsaverage, u'Brodmann.1-rh', rh : 3067 vertices>, <Label  |  fsaverage, u'Brodmann.10-lh', lh : 3600 vertices>, <Label  |  fsaverage, u'Brodmann.10-rh', rh : 3473 vertices>, <Label  |  fsaverage, u'Brodmann.11-lh', lh : 4995 vertices>, <Label  |  fsaverage, u'Brodmann.11-rh', rh : 5659 vertices>, <Label  |  fsaverage, u'Brodmann.17-lh', lh : 3660 vertices>, <Label  |  fsaverage, u'Brodmann.17-rh', rh : 3161 vertices>, <Label  |  fsaverage, u'Brodmann.18-lh', lh : 6345 vertices>, <Label  |  fsaverage, u'Brodmann.18-rh', rh : 6173 vertices>, <Label  |  fsaverage, u'Brodmann.19-lh', lh : 9828 vertices>, <Label  |  fsaverage, u'Brodmann.19-rh', rh : 10294 vertices>, <Label  |  fsaverage, u'Brodmann.2-lh', lh : 6038 vertices>, <Label  |  fsaverage, u'Brodmann.2-rh', rh : 5384 vertices>, <Label  |  fsaverage, u'Brodmann.20-lh', lh : 4815 vertices>, <Label  |  fsaverage, u'Brodmann.20-rh', rh : 4400 vertices>, <Label  |  fsaverage, u'Brodmann.21-lh', lh : 2185 vertices>, <Label  |  fsaverage, u'Brodmann.21-rh', rh : 2681 vertices>, <Label  |  fsaverage, u'Brodmann.22-lh', lh : 8373 vertices>, <Label  |  fsaverage, u'Brodmann.22-rh', rh : 7959 vertices>, <Label  |  fsaverage, u'Brodmann.23-lh', lh : 1645 vertices>, <Label  |  fsaverage, u'Brodmann.23-rh', rh : 1875 vertices>, <Label  |  fsaverage, u'Brodmann.24-lh', lh : 4190 vertices>, <Label  |  fsaverage, u'Brodmann.24-rh', rh : 3953 vertices>, <Label  |  fsaverage, u'Brodmann.25-lh', lh : 574 vertices>, <Label  |  fsaverage, u'Brodmann.25-rh', rh : 657 vertices>, <Label  |  fsaverage, u'Brodmann.26-lh', lh : 109 vertices>, <Label  |  fsaverage, u'Brodmann.26-rh', rh : 120 vertices>, <Label  |  fsaverage, u'Brodmann.27-lh', lh : 409 vertices>, <Label  |  fsaverage, u'Brodmann.27-rh', rh : 442 vertices>, <Label  |  fsaverage, u'Brodmann.28-lh', lh : 965 vertices>, <Label  |  fsaverage, u'Brodmann.28-rh', rh : 693 vertices>, <Label  |  fsaverage, u'Brodmann.29-lh', lh : 145 vertices>, <Label  |  fsaverage, u'Brodmann.29-rh', rh : 202 vertices>, <Label  |  fsaverage, u'Brodmann.3-lh', lh : 2816 vertices>, <Label  |  fsaverage, u'Brodmann.3-rh', rh : 2667 vertices>, <Label  |  fsaverage, u'Brodmann.30-lh', lh : 469 vertices>, <Label  |  fsaverage, u'Brodmann.30-rh', rh : 621 vertices>, <Label  |  fsaverage, u'Brodmann.31-lh', lh : 2848 vertices>, <Label  |  fsaverage, u'Brodmann.31-rh', rh : 3378 vertices>, <Label  |  fsaverage, u'Brodmann.32-lh', lh : 2674 vertices>, <Label  |  fsaverage, u'Brodmann.32-rh', rh : 2775 vertices>, <Label  |  fsaverage, u'Brodmann.33-lh', lh : 401 vertices>, <Label  |  fsaverage, u'Brodmann.33-rh', rh : 2667 vertices>, <Label  |  fsaverage, u'Brodmann.35-lh', lh : 387 vertices>, <Label  |  fsaverage, u'Brodmann.35-rh', rh : 444 vertices>, <Label  |  fsaverage, u'Brodmann.36-lh', lh : 1364 vertices>, <Label  |  fsaverage, u'Brodmann.36-rh', rh : 1525 vertices>, <Label  |  fsaverage, u'Brodmann.37-lh', lh : 4338 vertices>, <Label  |  fsaverage, u'Brodmann.37-rh', rh : 5327 vertices>, <Label  |  fsaverage, u'Brodmann.38-lh', lh : 2438 vertices>, <Label  |  fsaverage, u'Brodmann.38-rh', rh : 2833 vertices>, <Label  |  fsaverage, u'Brodmann.39-lh', lh : 4498 vertices>, <Label  |  fsaverage, u'Brodmann.39-rh', rh : 4215 vertices>, <Label  |  fsaverage, u'Brodmann.4-lh', lh : 9423 vertices>, <Label  |  fsaverage, u'Brodmann.4-rh', rh : 8995 vertices>, <Label  |  fsaverage, u'Brodmann.40-lh', lh : 5430 vertices>, <Label  |  fsaverage, u'Brodmann.40-rh', rh : 4873 vertices>, <Label  |  fsaverage, u'Brodmann.41-lh', lh : 1409 vertices>, <Label  |  fsaverage, u'Brodmann.41-rh', rh : 1287 vertices>, <Label  |  fsaverage, u'Brodmann.42-lh', lh : 2268 vertices>, <Label  |  fsaverage, u'Brodmann.42-rh', rh : 1985 vertices>, <Label  |  fsaverage, u'Brodmann.43-lh', lh : 1424 vertices>, <Label  |  fsaverage, u'Brodmann.43-rh', rh : 1871 vertices>, <Label  |  fsaverage, u'Brodmann.44-lh', lh : 2262 vertices>, <Label  |  fsaverage, u'Brodmann.44-rh', rh : 2136 vertices>, <Label  |  fsaverage, u'Brodmann.45-lh', lh : 897 vertices>, <Label  |  fsaverage, u'Brodmann.45-rh', rh : 1302 vertices>, <Label  |  fsaverage, u'Brodmann.46-lh', lh : 2814 vertices>, <Label  |  fsaverage, u'Brodmann.46-rh', rh : 2848 vertices>, <Label  |  fsaverage, u'Brodmann.47-lh', lh : 676 vertices>, <Label  |  fsaverage, u'Brodmann.47-rh', rh : 723 vertices>, <Label  |  fsaverage, u'Brodmann.5-lh', lh : 2862 vertices>, <Label  |  fsaverage, u'Brodmann.5-rh', rh : 2727 vertices>, <Label  |  fsaverage, u'Brodmann.6-lh', lh : 8429 vertices>, <Label  |  fsaverage, u'Brodmann.6-rh', rh : 8265 vertices>, <Label  |  fsaverage, u'Brodmann.7-lh', lh : 10574 vertices>, <Label  |  fsaverage, u'Brodmann.7-rh', rh : 9186 vertices>, <Label  |  fsaverage, u'Brodmann.8-lh', lh : 3219 vertices>, <Label  |  fsaverage, u'Brodmann.8-rh', rh : 4060 vertices>, <Label  |  fsaverage, u'Brodmann.9-lh', lh : 4225 vertices>, <Label  |  fsaverage, u'Brodmann.9-rh', rh : 4778 vertices>, <Label  |  fsaverage, u'CON_deeper_than_WS_t_2-lh', lh : 401 vertices>, <Label  |  fsaverage, u'CON_deeper_than_WS_t_2_CaS_Left-lh', lh : 401 vertices>, 



########Regression analysis 

In [11]: for subject in e:
    ...:     ds = e.load_epochs_stc(vardef='freq_s_regression')
    ...:     src = ds['src']
    ...:     src = set_parc(src, 'PALS_B12_Brodmann')
    ...:     y = src.mean(source='left_BA22').sub(time = (1.5, 1.7))
    ...:     lm = testnd.LM(y, 'freq_s', ds, subject=subject)
    ...:     lms.append(lm)


For subject in e:
     ...:     ds = e.load_epochs_stc(vardef= 'verb_regression', parc = 'Frankland-25')
     ...:     src = ds['src']
     ...:     y = src.sub(time=(1.3, 1.8)).mean(source='lmSTC-lh')
     ...:     lm = testnd.LM(y, 'freq_v + Nmorph_v + len_v', ds, subject=subject)
     ...:     lms.append(lm)
     ...:     del ds, src, y


lms= []
for subject in e:
   ...:     ds = e.load_epochs_stc(vardef='freq_s_regression', parc = 'PALS_B12_Brodmann')
   ...:     src = ds['src']
   ...:     y = src.sub(time=(1.5, 1.7)).mean(source='Brodmann.22-lh')
   ...:     lm = testnd.LM(y, 'freq_s', ds, subject=subject)
   ...:     lms.append(lm)
   ...:     del ds, src, y

lmg = testnd.LMGroup(lms)
res = lmg.column_ttest('free_s', samples=1000, pmin=.05)

lms= []
for subject in e:
   ...:     ds = e.load_epochs_stc(vardef='freq_s_regression', parc = 'PALS_B12_Brodmann')
   ...:     src = ds['src']
   ...:     y = src.sub(time=(1.5, 1.7)).mean(source='Brodmann.22-lh')
   ...:     lm = testnd.LM(y, 'freq_s', ds, subject=subject)
   ...:     lms.append(lm)
   ...:     del ds, src, y

lmg = testnd.LMGroup(lms)
res = lmg.column_ttest('free_s', samples=1000, pmin=.05)


###########LMM analysis ##############
dss, ress = e.load_test()
ds = dss['LATP']
ds['cluster1'] = ds['label_tc'].mean(time=(tstart, tstop))
ds.save_txt()








