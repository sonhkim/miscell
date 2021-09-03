
import numpy as np 
import pandas as pd

######## PART 1: EXPORT SINGLE TRIAL DATA
rois = ['Frankland-25', 'LATP', 'left_BA21', 'LAG']
#e.set(inv='fixed-3-dSPM')
e.set(inv='free-3-dSPM')

### 2-or-3 word trials data
# e.set(epoch='main_2_or_3_word_trials_decim')

# for r in rois: 
# 	for subject in e:
# 		ds_single = e.load_epochs_stc(subject=subject, parc=r, mask=True, morph=True, model='sub_specificity%subject')
# 		print (subject)
# 		print ('ds shape is', ds_single.shape)
# 		ds_single.index(name='index')
# 		ds_single['srcm_tc'] = ds_single['srcm'].mean(dims='source')
# 		print ('srcm_tc: ', ds_single['srcm_tc'])
# 		### in below, ds_single['srcm_tc'].x is a list of arrays, where each array is 401 timeseries
# 		if len(set([len(array) for array in ds_single['srcm_tc'].x])) != 1: 
# 			print (r, e, 'cases have different # of time points')
# 		timepointN =  list(set([len(array) for array in ds_single['srcm_tc'].x]))[0] #this should be 401 for current e
# 		if timepointN != 401:
# 			print (r, e, '# of time points is not 401')
# 		keys = ds_single.keys()
# 		keys.remove('interpolate_channels')
# 		keys.remove('i_start')
# 		keys.remove('SOA')
# 		keys.remove('srcm')
# 		keys.remove('srcm_tc')
# 		ds_single_backbone = ds_single[:, keys]
# 		rows = [] 
# 		for case in ds_single_backbone.itercases():
# 		    case_n = case['index']
# 		    for i in range(401):
# 		        casecopy = case.copy()
# 		        casecopy['t'] = int(i)
# 		        casecopy['srcm_at_t'] = ds_single['srcm_tc'].x[case_n][i]
# 		        rows.append(casecopy)
# 		        del casecopy
# 		if len(rows) != ds_single.shape[0]*timepointN:
# 			print (r,e, 'check row numbers')
# 		ds_single_extended = pd.DataFrame(rows)
# 		ds_single_extended.to_csv('singletrialexport_free/2_or_3_word_trials_subspecificity/%s/ds_single_%s.csv' %(r, subject), index_label='index')
# 		print (e, 'is finished')
# 		del ds_single, ds_single_extended, ds_single_backbone
# 	print ('========', r, 'is finished', '========')


## 3 word trials data
e.set(epoch='main_3_word_trials_decim')
for r in rois: 
	for subject in e:
		ds_single = e.load_epochs_stc(subject=subject, parc=r, mask=True, morph=True, model='sub_specificity%verb_specificity%object_specificity%subject')
		print (subject)
		print ('ds shape is', ds_single.shape)
		ds_single.index(name='index')
		ds_single['srcm_tc'] = ds_single['srcm'].mean(dims='source')
		print ('srcm_tc: ', ds_single['srcm_tc'])
		### in below, ds_single['srcm_tc'].x is a list of arrays, where each array is 401 timeseries
		if len(set([len(array) for array in ds_single['srcm_tc'].x])) != 1: 
			print (r, e, 'cases have different # of time points')
		timepointN =  list(set([len(array) for array in ds_single['srcm_tc'].x]))[0] #this should be 401 for current e
		if timepointN != 401:
			print (r, e, '# of time points is not 401')
		keys = ds_single.keys()
		keys.remove('interpolate_channels')
		keys.remove('i_start')
		keys.remove('SOA')
		keys.remove('srcm')
		keys.remove('srcm_tc')
		ds_single_backbone = ds_single[:, keys]
		rows = [] 
		for case in ds_single_backbone.itercases():
		    case_n = case['index']
		    for i in range(401):
		        casecopy = case.copy()
		        casecopy['t'] = int(i)
		        casecopy['srcm_at_t'] = ds_single['srcm_tc'].x[case_n][i]
		        rows.append(casecopy)
		        del casecopy
		if len(rows) != ds_single.shape[0]*timepointN:
			print (r,e, 'check row numbers')
		ds_single_extended = pd.DataFrame(rows)
		ds_single_extended.to_csv('singletrialexport_free/3_word_trials_full/%s/ds_single_3word_fullanova_%s.csv' %(r, subject), index_label='index')
		#print (e, 'is finished')
		del ds_single, ds_single_extended, ds_single_backbone
	print ('========', r, 'is finished', '========')






# ds_single_0053 = e.load_epochs_stc(subject='R0053', parc='LATP', mask=True, morph=True, model='sub_specificity%subject')
# ds_single_0053.index(name='index')
# ds_single_0053['srcm_tc'] = ds_single_0053['isrcm'].mean(dims='source')
# keys.remove('interpolate_channels')
# keys.remove('i_start')
# keys.remove('SOA')
# keys.remove('srcm')
# keys.remove('srcm_tc')
# ds_single_0053_backbone = ds_single_0053[:, keys]
# rows = [] 
# for case in ds_single_0053_backbone.itercases():
#     case_n = case['index']
#     for i in range(401):
#         casecopy = case.copy()
#         casecopy['t'] = int(i)
#         casecopy['srcm_at_t'] = ds_single_0053['srcm_tc'].x[case_n][i]
#         rows.append(casecopy)
#         del casecopy

# ds_single_0053_extended = pd.DataFrame(rows)
# ds_single_0053_extended.to_csv('singletrialexport/ds_single_0053.csv', index_label='index')



# ### 3-word trials data 
# e.set(epoch='main_3_word_trials_decim')











# e.set(epoch = 'main_2_or_3_word_trials_decim')
# e.set(group = 'official27')


# ds = e.load_epochs_stc(src_baseline=True, parc='PALS_B12_Brodmann')
# ds['src_latp'] = ds['src'].sub(source='Brodmann.38-lh')
# ds['in_c1'] = ds['src_latp'].mean(dims='source').mean(time=(0.313, 0.374))
# ds.save_txt('filename.txt')

# ## ANALYSIS 1: eheck whether evoked activity is the same as the sum of single trials (with one subject)
# e.set(epoch = 'main_2_or_3_word_trials_decim')

# ### replicate the results 
# e.make_report_rois('subject_anova', parc= 'LATP', pmin = 0.05, tstart = 0.7, tstop = 1.2, samples = 10000, group = 'official27', match = 'subject') 
# e.make_report_rois('subject_anova', parc= 'left_BA21', pmin = 0.05, tstart = 0.7, tstop = 1.2, samples = 10000, group = 'official27', match = 'subject')
# e.make_report_rois('subject_anova', parc= 'Frankland-25', pmin = 0.05, tstart = 0.7, tstop = 1.2, samples = 10000, group = 'official27', match = 'subject')
# e.make_report_rois('subject_anova', parc= 'LAG', pmin = 0.05, tstart = 0.7, tstop = 1.2, samples = 10000, group = 'official27', match = 'subject')


# ### run the same test manually and check if the report is replicated
# ds_test, res_test = e.load_test('subject_anova', tstart=0.7, tstop=1.2, pmin=0.05, parc='LATP', data='source.mean', return_data=True, make=True)
# res_test.res['LATP-lh'].clusters[1] ### the significant cluster
# ds_test_anova = testnd.anova(Y=ds_test['LATP-lh']['label_tc'], X='sub_specificity*subject', ds=ds_test['LATP-lh'], match='subject', samples=10000, pmin=0.05, tstart=0.7, tstop=1.2, mintime=0.01)
# ds_test_anova.clusters[1] ### same as the clusters in the html report

# ### export the ds['label_tc'] 
# # ds_test_x = ds_test['LATP-lh']['label_tc'].x
# # np.save('ds_test_label_tc', ds_test_x, allow_pickle=True, fix_imports=True)

# ### to plot epoch timecourse
# plot.UTSStat(Y=ds_test['LATP-lh']['label_tc'], X='sub_specificity', match='subject', ds=ds_test['LATP-lh'])

# # print ("res_test.clusters: ", res_test.res['LATP-lh'].clusters, '\n')
# # print ("res_test.clusters[0]: ", res_test.res['LATP-lh'].clusters[0], '\n')
# # print ("ds_test[LATP-lh']['label_tc']: ", ds_test['LATP-lh']['label_tc'], '\n')

# ##### data from evoked activity 
# ds_evoked = e.load_evoked_stc(subject='official27', morph_ndvar=True, model='sub_specificity%subject')
# ds_evoked['srcm'] = set_parc(ds_evoked['srcm'], parc= 'PALS_B12_Brodmann')
# ds_evoked['label_tc_38'] = ds_evoked['srcm'].sub(source='Brodmann.38-lh').mean(dims='source')
# res_evoked_38 = testnd.anova(Y=ds_evoked['label_tc_38'], X='sub_specificity*subject', ds=ds_evoked, match='subject', samples=10000, pmin=0.05, tstart=0.7, tstop=1.2, mintime=0.01),
# testnd.anova(Y=ds_evoked['label_tc_38'], X='sub_specificity*subject', ds=ds_evoked['LATP-lh'], match='subject', samples=10000, pmin=0.05, tstart=0.7, tstop=1.2, mintime=0.01)
# res_evoked_38.clusters[1] ## the result is same as in the report
# np.save('ds_evoked_label_tc', ds_evoked['label_tc_38'].x, allow_pickle=True, fix_imports=True)

# ##### data from evoked activity for R0053
# # ds_evoked_0053 = e.load_evoked_stc(subject='R0053', morph_ndvar=True, model='sub_specificity%subject')
# # ds_evoked_0053['srcm'] = set_parc(ds_evoked_0053['srcm'], parc = 'PALS_B12_Brodmann')
# # ds_evoked_0053['label_tc_38'] = ds_evoked_0053['srcm'].sub(source='Brodmann.38-lh').mean(dims='source')

# ds_evoked_0053= e.load_evoked_stc(subject='R0053', parc= 'LATP', mask=True, morph_ndvar=True, model='sub_specificity%subject')
# ds_evoked_0053['label_tc_latp'] = ds_evoked_0053['srcm'].mean(dims='source')
# ds_evoked_0053['at915']=ds_evoked_0053['label_tc_latp'].sub(time=(0.915, 0.916)).mean(dims='time')

# ##### data from single trials for R0053 
# ds_single_0053 = e.load_epochs_stc(subject='R0053', parc='LATP', mask=True, morph=True, model='sub_specificity%subject')
# ds_single_0053['label_tc_latp'] = ds_single_0053['srcm'].mean(dims='source')
# ds_single_0053['at915'] = ds_single_0053['label_tc_latp'].sub(time=(0.915, 0.916)).mean(dims='time')


# ds_single_0053_nomorph = e.load_epochs_stc(subject='R0053', parc='LATP', mask=True, model='sub_specificity%subject')
# ds_single_0053_nomorph['label_tc_38'] = ds_single_0053_nomorph['srcm'].mean(dims='source')
# ds_single_0053_nomorph['at915']=ds_single_0053_nomorph['label_tc_38'].sub(time=(0.915, 0.916)).mean(dims='time')



# ####
# ds_evoked_baseline = e.load_evoked_stc(subject='official27', src_baseline=True, morph_ndvar=True, model='sub_specificity%subject')
# ds_evoked_baseline['label_tc_38'] = ds_evoked_baseline['srcm'].sub(source='Brodmann.38-lh').mean(dims='source')


# #### print out dSPM value of R0053 
# ds_single_0053 = e.load_epochs_stc(subject='R0053', parc='LATP', morph=True, mask=True)
# ds_single_0053['913914'] = ds_single_0053['label_tc_38'].sub(time=(0.913, 0.914)).mean(dims='time')
# filename = 'export_to_R/' + epoch + '/' + epoch + '_latp_at_verb' + '_313_374_' + sub + '.txt'
# ds.save_txt(filename)
# del ds








