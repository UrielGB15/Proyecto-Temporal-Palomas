# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 18:35:44 2017

@author: Uriel
"""

import pandas as pd
import os



def caterpillar(file_name,array):
	"""
	Function that reads file 'file_name' and
	returns data contained in 'array' as a dict.
	(Should work for any MED file.)
	"""
	archive=open(file_name)
	found=False
	block=[]
	array_name=array+':'
	for line in archive:
		if line.startswith('Subject:'):
			subject=line.split()[1]
		if line.startswith('Experiment:'):
			experiment=line.split()[1]
		if line.startswith('Group:'):
			group=line.split()[1]
		if line.startswith('Box:'):
			box=line.split()[1]
		if line.startswith('Start Date:'):
			date=line.split()[2]
		if line.startswith('MSN:'):
			msn=line.split()[1]
		if line.startswith('Start Time:'):
			start_time=line.split()[2]
		if line.startswith('End Time:'):
			end_time=line.split()[2]
		if found:
			if len(line.split())==1:
				break
			block.append(line.split()[1:len(line.split())])
		else:
			if line.startswith(array_name):
				found=True

	before_point=[]
	after_point=[]
	for d1 in range(len(block)):
		for d2 in range(len(block[d1])):
			before_point.append(block[d1][d2].split('.')[0])
			after_point.append(block[d1][d2].split('.')[1])
	output={'raw_block':block,
		'before_point':before_point,
		'after_point':after_point,
		'experiment_name':experiment,
		'experiment_program':msn,
		'subject':subject,
		'box':box,
		'date':date,
		'session_start':start_time,
		'session_end':end_time}

	return output



#%%
def hatter(file_name,array):
    """
    Function that extracts certain array from certain
    MED file and returns it in a pandas dataframe
    """
    extraction=caterpillar(file_name,array)
    base={'before_point':extraction['before_point'],
        'after_point':extraction['after_point'],
        'subject':extraction['subject'],
        'box':extraction['box'],
        'date':extraction['date'],
        'session_start':extraction['session_start'],
        'session_end':extraction['session_end'],
        #'condition':extraction['condition'],
        'experiment_name':extraction['experiment_name'],
        'experiment_program':extraction['experiment_program']}
    data_frame=pd.DataFrame(base)
    data_frame=data_frame.loc[(data_frame['after_point']!='000')]
    data_frame['data_file']=file_name
    return data_frame


#%%
def concurrent_extractor(file):
    ht=hatter(file,'A')
    rt=ht.loc[:,['box',
            'data_file',
            'date',
            'session_start',
            'session_end']]
    rt['bird']=ht.subject
    rt['session']=file.split('_')[1]
    rt['med_notation_file']=ht.experiment_program
    rt['event_key']=ht.after_point
    rt['time_sec_100']=ht.before_point
    rt['event']=ht.after_point
    rt['session_time_sec']=ht.before_point.astype('float')/100
    rt.event.loc[rt.event_key=='010']='session_start'
    rt.event.loc[rt.event_key=='020']='session_end'
    rt.event.loc[rt.event_key=='091']='Res_Ref_IF10' #Respuestas Reforzadas
    rt.event.loc[rt.event_key=='092']='Res_Ref_IF14'
    rt.event.loc[rt.event_key=='093']='Res_Ref_IF19'
    rt.event.loc[rt.event_key=='094']='Res_Ref_IF27'
    rt.event.loc[rt.event_key=='095']='Res_Ref_IF38'
    rt.event.loc[rt.event_key=='111']='Res_TCB_10' #Respuestas tecla blanca encendida
    rt.event.loc[rt.event_key=='112']='Res_TCB_14'
    rt.event.loc[rt.event_key=='113']='Res_TCB_19'
    rt.event.loc[rt.event_key=='114']='Res_TCB_27'
    rt.event.loc[rt.event_key=='115']='Res_TCB_38'
    rt.event.loc[rt.event_key=='121']='Res_TDR_10' #Respuestas tecla roja encendida
    rt.event.loc[rt.event_key=='122']='Res_TDR_14'
    rt.event.loc[rt.event_key=='123']='Res_TDR_19'
    rt.event.loc[rt.event_key=='124']='Res_TDR_27'
    rt.event.loc[rt.event_key=='125']='Res_TDR_38'
    rt.event.loc[rt.event_key=='071']='Res_TDOFF_10' #Respuestas a apagada derecha cuando TCB
    rt.event.loc[rt.event_key=='072']='Res_TDOFF_14'
    rt.event.loc[rt.event_key=='073']='Res_TDOFF_19'
    rt.event.loc[rt.event_key=='074']='Res_TDOFF_27'
    rt.event.loc[rt.event_key=='075']='Res_TDOFF_38'
    rt.event.loc[rt.event_key=='061']='Res_TIOFF_10' #Respuestas a apagada izquierda cuando TCB
    rt.event.loc[rt.event_key=='062']='Res_TIOFF_14'
    rt.event.loc[rt.event_key=='063']='Res_TIOFF_19'
    rt.event.loc[rt.event_key=='064']='Res_TIOFF_27'
    rt.event.loc[rt.event_key=='065']='Res_TIOFF_38'
    rt.event.loc[rt.event_key=='211']='Res_TCOFF_10' #Respuestas a apagada central cuando TDR
    rt.event.loc[rt.event_key=='212']='Res_TCOFF_14'
    rt.event.loc[rt.event_key=='213']='Res_TCOFF_19'
    rt.event.loc[rt.event_key=='214']='Res_TCOFF_27'
    rt.event.loc[rt.event_key=='215']='Res_TCOFF_38'
    rt.event.loc[rt.event_key=='221']='Res_TIOFF_10' #Respuestas a apagada izquierda cuando TDR
    rt.event.loc[rt.event_key=='222']='Res_TIOFF_14'
    rt.event.loc[rt.event_key=='223']='Res_TIOFF_19'
    rt.event.loc[rt.event_key=='224']='Res_TIOFF_27'
    rt.event.loc[rt.event_key=='225']='Res_TIOFF_38'
    rt.event.loc[rt.event_key=='411']='ResBlackO_TD' #Respuestas en BLACKOUTS
    rt.event.loc[rt.event_key=='412']='ResBlackO_TC' 
    rt.event.loc[rt.event_key=='413']='ResBlackO_TI' 
    rt.event.loc[rt.event_key=='611']='LCB_ON_10' #TECLA BLANCA ON-OFF
    rt.event.loc[rt.event_key=='612']='LCB_ON_14' 
    rt.event.loc[rt.event_key=='613']='LCB_ON_19' 
    rt.event.loc[rt.event_key=='614']='LCB_ON_27' 
    rt.event.loc[rt.event_key=='615']='LCB_ON_38'
    rt.event.loc[rt.event_key=='621']='LCB_OFF_10' 
    rt.event.loc[rt.event_key=='622']='LCB_OFF_14' 
    rt.event.loc[rt.event_key=='623']='LCB_OFF_19' 
    rt.event.loc[rt.event_key=='624']='LCB_OFF_27'
    rt.event.loc[rt.event_key=='625']='LCB_OFF_38'  
    rt.event.loc[rt.event_key=='711']='LDR_ON_10' #TECLA ROJA IF ON-OFF
    rt.event.loc[rt.event_key=='712']='LDR_ON_14' 
    rt.event.loc[rt.event_key=='713']='LDR_ON_19' 
    rt.event.loc[rt.event_key=='714']='LDR_ON_27' 
    rt.event.loc[rt.event_key=='715']='LDR_ON_38'
    rt.event.loc[rt.event_key=='721']='LDR_OFF_10' 
    rt.event.loc[rt.event_key=='722']='LDR_OFF_14' 
    rt.event.loc[rt.event_key=='723']='LDR_OFF_19' 
    rt.event.loc[rt.event_key=='724']='LDR_OFF_27'
    rt.event.loc[rt.event_key=='725']='LDR_OFF_38'  
    rt.event.loc[rt.event_key=='901']='Reforzador_ON'  #COMEDERO ON-OFF
    rt.event.loc[rt.event_key=='902']='Reforzador_OFF'  
    rt.event.loc[rt.event_key=='910']='LG_ON' #LUZ GENERAL ON-OFF
    rt.event.loc[rt.event_key=='920']='LG_OFF' #LUZ GENERAL ON-OFF
    rt.event.loc[rt.event_key=='005']='LD_OFF_FINS' #TERMINANDO SESION
    rt.event.loc[rt.event_key=='006']='LC_OFF_FINS'
    rt.event.loc[rt.event_key=='007']='LG_OFF_FINS'
    rt.event.loc[rt.event_key=='811']='LDRP_ON_10' #TECLA ROJA PEAK ON-OFF
    rt.event.loc[rt.event_key=='812']='LDRP_ON_14' 
    rt.event.loc[rt.event_key=='813']='LDRP_ON_19' 
    rt.event.loc[rt.event_key=='814']='LDRP_ON_27' 
    rt.event.loc[rt.event_key=='815']='LDRP_ON_38'
    rt.event.loc[rt.event_key=='821']='LDRP_OFF_10' 
    rt.event.loc[rt.event_key=='822']='LDRP_OFF_14' 
    rt.event.loc[rt.event_key=='823']='LDRP_OFF_19' 
    rt.event.loc[rt.event_key=='824']='LDRP_OFF_27'
    rt.event.loc[rt.event_key=='825']='LDRP_OFF_38'  
    rt.event.loc[rt.event_key=='131']='Res_TDRP_10' #Respuestas tecla roja encendida
    rt.event.loc[rt.event_key=='132']='Res_TDRP_14'
    rt.event.loc[rt.event_key=='133']='Res_TDRP_19'
    rt.event.loc[rt.event_key=='134']='Res_TDRP_27'
    rt.event.loc[rt.event_key=='135']='Res_TDRP_38'
    return rt


#%%
def concurrent_builder(output_archive):
	#os.chdir('/Users/arturobouzasriano2/Desktop/Uriel/Pigeons/Raw_MED_files')
	files=os.listdir('.')
	global_df=pd.DataFrame()
	for archive in range(len(files)):
		print(files[archive])
		#if files[archive]!='p736_s02_atsh':
		frames=[global_df,concurrent_extractor(files[archive])]
		global_df=pd.concat(frames)
	os.chdir('..')
	global_df.to_csv(output_archive)



#%%