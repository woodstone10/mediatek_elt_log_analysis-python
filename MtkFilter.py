###########################################################################################
#
# MtkFilter.py
#
# About this software:
# This is sample code for MediaTek automated parsing tool 
# Automated extraction 4G/5G radio condition and throughput value from MediaTek logs (*.muxz/*.elg) using ELT application
# Plot its values on graph and save as figure
# More features can be added in this manner and it will be updated
#
# How to use it:
# Step.1 copy and paste onto log folder
# Step.2 run this python file (Python installation pre-required)
#
# Pre-install required:
# 1. Python 3.7 (ELT 64bits) or 2.7 (ELT 32bits)
# 2. MACE, if you installed ELT on your PC, please find Automation\MACE2\Mace2Python in your ELT folder, then run install.py
# 3. Install Python matplotlib (type "pip install matplotlib" in command window)
# 
# MTK.xml:
# If you open MtkFilter.txt with Notepad++,
# load MTK.xml on Notepad++ and select language as MTK
# It will help easy to see MTK log with color legend
#
#
# Created by Jonggil Nam
# https://www.linkedin.com/in/jonggil-nam-6099a162/ | https://github.com/woodstone10 | woodstone10@gmail.com | +82-10-8709-6299 
###########################################################################################

from __future__ import print_function
from re import search
import sys
import mace
import json
import glob
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    #opt = sys.argv[1]
    #if opt=='5G':
    #	NR_supported=1
    #	print("Selected 5G chipset")
    #else:
    #	NR_supported=0
    #	print("Selected 4G chipset")


    f = open("MtkFilter.txt", "w")

    NR_MEAS_TIME, NR_RSRP0, NR_RSRP1, NR_RSRQ0, NR_RSRQ1, NR_SINR0, NR_SINR1 = [],[],[],[],[],[],[]
    NR_DCI_TIME, NR_DL_MCS1, NR_DL_MCS2, NR_DL_RB = [],[],[],[]
    NR_PDSCH_TPUT_TIME, NR_PDSCH_TPUT0, NR_PDSCH_TPUT1, NR_PDSCH_TPUT = [],[],[],[]
    LTE_MEAS_TIME, LTE_RSRP0, LTE_RSRP1, LTE_RSRQ0, LTE_RSRQ1, LTE_SINR0, LTE_SINR1 = [],[],[],[],[],[],[]
    LTE_DCI_TIME, LTE_DL_MCS1, LTE_DL_MCS2, LTE_DL_RB = [],[],[],[]
    LTE_PDSCH_TPUT_TIME, LTE_PDSCH_TPUT0, LTE_PDSCH_TPUT1, LTE_PDSCH_TPUT = [],[],[],[]
    EL1_STATUS_TIME, EL1_DL_CC_COUNT, EL1_UL_CC_COUNT = [],[],[]
    EL1_0_BAND, EL1_0_PCI, EL1_0_EARFCN = [],[],[]
    EL1_1_BAND, EL1_1_PCI, EL1_1_EARFCN = [],[],[]
    EL1_2_BAND, EL1_2_PCI, EL1_2_EARFCN = [],[],[]
    EL1_3_BAND, EL1_3_PCI, EL1_3_EARFCN = [],[],[]
    EL1_0_DL_BW, EL1_0_UL_BW = [],[]
    EL1_1_DL_BW, EL1_1_UL_BW = [],[]
    EL1_2_DL_BW, EL1_2_UL_BW = [],[]
    EL1_3_DL_BW, EL1_3_UL_BW = [],[]
    EL1_0_DL_TPUT, EL1_0_UL_TPUT = [],[]
    EL1_1_DL_TPUT, EL1_1_UL_TPUT = [],[]
    EL1_2_DL_TPUT, EL1_2_UL_TPUT = [],[]
    EL1_3_DL_TPUT, EL1_3_UL_TPUT = [],[]
    EL1_0_RSRP0, EL1_0_RSRP1, EL1_0_SINR0, EL1_0_SINR1, EL1_0_CQI0, EL1_0_CQI1, EL1_0_MCS, EL1_0_MCS0, EL1_0_MCS1, EL1_0_BLER, EL1_0_BLER0, EL1_0_BLER1, EL1_0_GRANT, EL1_0_ULMCS, EL1_0_ULRB, EL1_0_ULBLER, EL1_0_ULMOD = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    EL1_1_RSRP0, EL1_1_RSRP1, EL1_1_SINR0, EL1_1_SINR1, EL1_1_CQI0, EL1_1_CQI1, EL1_1_MCS, EL1_1_MCS0, EL1_1_MCS1, EL1_1_BLER, EL1_1_BLER0, EL1_1_BLER1, EL1_1_GRANT, EL1_1_ULMCS, EL1_1_ULRB, EL1_1_ULBLER, EL1_1_ULMOD = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    EL1_2_RSRP0, EL1_2_RSRP1, EL1_2_SINR0, EL1_2_SINR1, EL1_2_CQI0, EL1_2_CQI1, EL1_2_MCS, EL1_2_MCS0, EL1_2_MCS1, EL1_2_BLER, EL1_2_BLER0, EL1_2_BLER1, EL1_2_GRANT, EL1_2_ULMCS, EL1_2_ULRB, EL1_2_ULBLER, EL1_2_ULMOD = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    EL1_3_RSRP0, EL1_3_RSRP1, EL1_3_SINR0, EL1_3_SINR1, EL1_3_CQI0, EL1_3_CQI1, EL1_3_MCS, EL1_3_MCS0, EL1_3_MCS1, EL1_3_BLER, EL1_3_BLER0, EL1_3_BLER1, EL1_3_GRANT, EL1_3_ULMCS, EL1_3_ULRB, EL1_3_ULBLER, EL1_3_ULMOD = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    EL1_0_PRACH_PWR, EL1_0_PUCCH_PWR, EL1_0_PUSCH_PWR, EL1_0_SRS_PWR, EL1_0_TOT_PWR = [],[],[],[],[]
    EL1_1_PRACH_PWR, EL1_1_PUCCH_PWR, EL1_1_PUSCH_PWR, EL1_1_SRS_PWR, EL1_1_TOT_PWR = [],[],[],[],[]
    EL1_0_PHR, EL1_0_RETX_RATE, EL1_0_PCMAX = [],[],[]
    EL1_1_PHR, EL1_1_RETX_RATE, EL1_1_PCMAX = [],[],[]
    #LTE_PDSCH_TPUT_0_TIME, LTE_PDSCH_TPUT_0, LTE_PDSCH_TPUT_1_TIME, LTE_PDSCH_TPUT_1 = [],[],[],[]
    LTE_MAC_TPUT_TIME, LTE_MAC_TPUT, LTE_RLC_TPUT_TIME, LTE_RLC_TPUT, LTE_PDCP_TPUT_TIME, LTE_PDCP_TPUT, LTE_IP_TPUT_TIME, LTE_IP_TPUT = [],[],[],[],[],[],[],[]
    LTE_UL_MAC_TPUT_TIME, LTE_UL_MAC_TPUT, LTE_UL_RLC_TPUT_TIME, LTE_UL_RLC_TPUT, LTE_UL_PDCP_TPUT_TIME, LTE_UL_PDCP_TPUT, LTE_UL_IP_TPUT_TIME, LTE_UL_IP_TPUT = [],[],[],[],[],[],[],[]

    for files in ("*.muxz","*.elg","*.muxz.tmp"):
    	for fin in glob.glob(files):
    		print(fin)
    		logfile = mace.open_log_file(fin)
    		f.write("File: "+str(fin)+" ==================================================================================================================== \n")

    		try:
    			itemset = mace.create_itemset(logfile)
    			info = json.loads(logfile.platform_info)
    			sw = info["MtkSW"]
    			if sw.find("NR")>-1: NR_supported=1
    			else: NR_supported=0
    			print("-MtkSW:",sw)
    			print("-NR:",NR_supported,"(0:No NR parsing, 1:NR parsing)")

    			itemset.subscribe_ota()
    			itemset.subscribe_sys()
    			#--itemset.subscribe_raw_string()
    			itemset.subscribe_ps("Timer","CEL_DI","CELLJ","ERRC","ERLCDL","EMAC","EMM REG","EMM COMMON","AvailPLMN","MRM","COM","RLF","RCM","CHM","CREJ","CAP","PHB")
    			itemset.subscribe_icd("EL1_Serving_Cell_Measurement","EL1_RACH_Information")
    			itemset.subscribe_icd("EL1_MIMO_PDSCH_Throughput0","EL1_MIMO_PDSCH_Throughput1","EL2_MAC_Throughput_DL","EL2_RLC_Throughput_DL","EL2_PDCP_Throughput_DL","EL2_IP_Throughput_DL")
    			try: itemset.subscribe_icd("EL1_MIMO_PUSCH_Throughput0","EL1_MIMO_PUSCH_Throughput1")
    			except: pass
    			itemset.subscribe_icd("EL2_MAC_Throughput_UL","EL2_RLC_Throughput_UL","EL2_PDCP_Throughput_UL","EL2_IP_Throughput_UL")
    			try: itemset.subscribe_icd("EL1_PUSCH_Report")
    			except: pass
    			itemset.subscribe_primitive("_SEARCH_","_SCAN_","FOUND_IND")
    			itemset.subscribe_primitive("RLF_IND","OOS_IND")
    			itemset.subscribe_primitive("RELEASE_IND","REJECT_IND","REG_STATE_IND")
    			#--itemset.subscribe_primitive("_REQ","_CNF","_TIMER","_EXPR",)
    			itemset.subscribe_primitive("MSG_ID_EM_EL1_STATUS_IND")
    			itemset.subscribe_primitive("MSG_ID_EM_RAC_INFO_IND")
    			itemset.subscribe_primitive("MSG_ID_ERRC_MOB_CEL_SI_MEAS_IND")
    			itemset.subscribe_primitive("MSG_ID_ERRC_SYS_CEL_BCCH_RCVD_IND")
    			itemset.subscribe_primitive("MSG_ID_ERRC_MOB_CEL_RESEL_IND")
    			itemset.subscribe_primitive("MSG_ID_EMM_ERRC_CELLSELECT_IND")
    			itemset.subscribe_primitive("MSG_ID_EMM_ERRC_ESTABLISH_REQ","MSG_ID_EMM_ERRC_ESTABLISH_CNF")
    			itemset.subscribe_primitive("MSG_ID_ESMREG_PDN_CONN_EST_REQ","MSG_ID_ESMREG_PDN_CONN_EST_REJ")
    			itemset.subscribe_primitive("MSG_ID_VDM_ATP_CMD_DIAL_IND","MSG_ID_VDM_ATP_CMD_DIAL_RSP")
    			if NR_supported == 1:
    				itemset.subscribe_ps("CJUDGE","CJDG","ETCM","NL1MPC","NCONFIG","MRS_NRAS","SCG","VGMM_TRACE_TIMER_START","VGMM_TRACE_TIMER_STOP","VGMM_TRACE_TIMER_EXPIRY")
    				itemset.subscribe_icd("NL1_Serving_Cell_Measurement","NL1_DCI_Information","NL1_MIMO_PDSCH_Throughput","NL1_RACH_Information","NL2_PDCP_Throughput_DL","NL2_PDCP_Throughput_UL")
    				itemset.subscribe_primitive("PROBLEM_IND")
    				itemset.subscribe_primitive("MSG_ID_ERRC_NL1_SFTD_REQ","MSG_ID_ERRC_NL1_SFTD_CNF","MSG_ID_ERRC_NL1_SFTD_IND","MSG_ID_ERRC_NL1_SFTD_RSP")
    				itemset.subscribe_primitive("MSG_ID_ERRC_NRRC_MEAS_REPORT_IND")
    				itemset.subscribe_primitive("MSG_ID_NMAC_NL1_CA_IND")
    				itemset.subscribe_primitive("MSG_ID_NRRC_MAIN_CONFIG_ICD_INFO_IND")
    				itemset.subscribe_primitive("MSG_ID_NRRC_MAIN_SCG_IE_CHECK_CNF")
    				itemset.subscribe_primitive("MSG_ID_NRRC_NL1_RANDOM_ACCESS_REQ")
    				itemset.subscribe_primitive("MSG_ID_NRRC_NL1_CELL_INFO_IND")
    				itemset.subscribe_primitive("MSG_ID_NRRC_IDLE_CONFIG_CONFIG_REQ")
    				itemset.subscribe_primitive("MSG_ID_NRRC_NL1_PAGING_IND")
    				#--itemset.subscribe_primitive("MSG_ID_NRRC_IDLE_SI_COLLECT_SI_CNF")
    				itemset.subscribe_primitive("MSG_ID_NRRC_MAIN_IDLE_RESELECTION_NEEDED_IND","MSG_ID_NRRC_MAIN_IDLE_RESELECTION_REQ","MSG_ID_NRRC_MAIN_IDLE_RESELECTION_CNF")
    				itemset.subscribe_primitive("MSG_ID_NRRC_NCONN_MEAS_CONFIG_REQ","MSG_ID_NRRC_NCONN_MEAS_CONFIG_CNF")
    				#--itemset.subscribe_primitive("MSG_ID_NL1CSM_NL1MOB_SSB_INTRA_MEAS_RESULT_NTF","MSG_ID_NL1CSM_NL1MOB_SSB_INTER_MEAS_RESULT_NTF")
    				itemset.subscribe_primitive("MSG_ID_VGMM_NRRC_ESTABLISH_REQ","MSG_ID_VGMM_NRRC_ESTABLISH_CNF")
    				itemset.subscribe_primitive("MSG_ID_RAC_VGMM_NW_FEATURE_SUPPORT_IND")
    				itemset.subscribe_primitive("MSG_ID_VGSM_ESM_CONTEXT_TRANSFER_REQ_NTF")
    				itemset.subscribe_primitive("MSG_ID_EMM_ERRC_LOCAL_RELEASE_TRIGGER_IND") #AFR
    				itemset.subscribe_primitive("BACKGROUND_BAND_LEARNING") #BBL
    				itemset.subscribe_primitive("MSG_ID_IWLAN_L4BNW_ATTACHED_RAT_IND") #IWLAN
    				itemset.subscribe_primitive("MSG_ID_NAS_SV_ANY_RAT_CHANGE_START_IND","MSG_ID_NAS_SV_ANY_RAT_CHANGE_FINISH_IND")
    				itemset.subscribe_primitive("MSG_ID_SMIC_ACTIVE_SM_CHANGE_START_IND","MSG_ID_SMIC_ACTIVE_SM_CHANGE_FINISH_IND")

    			#print("-Total line:",len(itemset)) #debug message
    			for i in range(len(itemset)):
    				print(itemset[i].index, itemset[i].message) #debug message
    				if i%1000==0: print('#', end='') #print in progress
    				if i == len(itemset)-1: print("\n-Last item:", itemset[i].index, itemset[i].message) #print last line to check to run script

					#exception handling for "Decoded Fail"
    				if search("ICD_RECORD",itemset[i].message):
    					try: json.loads(itemset[i].icd_data)
    					except: continue
    				elif search("MSG_ID_",itemset[i].message):
    					try: itemset[i].prim
    					except: continue

					#ota
    				if search("NAS_MESSAGE_CONTAINER",itemset[i].message): s=1 #skip this due to no information included

    				elif search("NW->|MS->",itemset[i].message):
    					if search("5G|VGSM|NR_",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t5GOTA: "+ str(itemset[i].message) +"\n")
    					elif search("ESM|EMM|ERRC_|EARFCN",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t4GOTA: "+ str(itemset[i].message) +"\n")
    					else: f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\tOTA: "+ str(itemset[i].message) +"\n")

    				#icd
    				#NR
    				elif search("NL1_Serving_Cell_Measurement",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "PCI="+str(json.loads(itemset[i].icd_data)['PCI'])
    					+" "+ "Carrier type="+str(json.loads(itemset[i].icd_data)['Carrier type'])
    					+" "+ "Band="+str(json.loads(itemset[i].icd_data)['Band'])
    					+" "+ "NARFCN="+str(json.loads(itemset[i].icd_data)['NARFCN'])
    					+"\t"+ "RSRP RX0="+str(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRP RX0'])
    					+" "+ "RSRP RX1="+str(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRP RX1'])
    					+"\t"+ "RSRQ RX0="+str(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRQ RX0'])
    					+" "+ "RSRQ RX1="+str(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRQ RX1'])
    					+"\t"+ "SINR RX0="+str(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['SINR RX0'])
    					+" "+ "SINR RX1="+str(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['SINR RX1'])
    					+"\n")
    					NR_MEAS_TIME.append(itemset[i].device_time) #itemset[i].timestamp.strftime('%H:%M:%S:%f')[:-3])
    					NR_RSRP0.append(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRP RX0'])
    					NR_RSRP1.append(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRP RX1'])
    					NR_RSRQ0.append(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRQ RX0'])
    					NR_RSRQ1.append(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['RSRQ RX1'])
    					NR_SINR0.append(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['SINR RX0'])
    					NR_SINR1.append(json.loads(itemset[i].icd_data)['Serving Cell SSS Measurement Records'][0]['SINR RX1'])
    				elif search("NL1_DCI_Information",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "Carrier Index="+str(json.loads(itemset[i].icd_data)['Carrier Index'])
    					+"\t"+ "DL MCS1="+str(json.loads(itemset[i].icd_data)['DCI Info'][0]['DL DCI Info']['MCS index 1'])
    					+" "+ "MCS2="+str(json.loads(itemset[i].icd_data)['DCI Info'][0]['DL DCI Info']['MCS index 2'])
    					+" "+ "MCS1="+str(json.loads(itemset[i].icd_data)['DCI Info'][1]['DL DCI Info']['MCS index 1'])
    					+" "+ "MCS2="+str(json.loads(itemset[i].icd_data)['DCI Info'][1]['DL DCI Info']['MCS index 2'])
    					+" "+ "MCS1="+str(json.loads(itemset[i].icd_data)['DCI Info'][2]['DL DCI Info']['MCS index 1'])
    					+" "+ "MCS2="+str(json.loads(itemset[i].icd_data)['DCI Info'][2]['DL DCI Info']['MCS index 2'])
    					+" "+ "MCS1="+str(json.loads(itemset[i].icd_data)['DCI Info'][3]['DL DCI Info']['MCS index 1'])
    					+" "+ "MCS2="+str(json.loads(itemset[i].icd_data)['DCI Info'][3]['DL DCI Info']['MCS index 2'])
    					+" "+ "MCS1="+str(json.loads(itemset[i].icd_data)['DCI Info'][4]['DL DCI Info']['MCS index 1'])
    					+" "+ "MCS2="+str(json.loads(itemset[i].icd_data)['DCI Info'][4]['DL DCI Info']['MCS index 2'])
    					#...
    					+"\t"+ "DL RB="+str(json.loads(itemset[i].icd_data)['DCI Info'][0]['DL DCI Info']['NUM RB'])
    					+" "+ "RB="+str(json.loads(itemset[i].icd_data)['DCI Info'][1]['DL DCI Info']['NUM RB'])
    					+" "+ "RB="+str(json.loads(itemset[i].icd_data)['DCI Info'][2]['DL DCI Info']['NUM RB'])
    					+" "+ "RB="+str(json.loads(itemset[i].icd_data)['DCI Info'][3]['DL DCI Info']['NUM RB'])
    					+" "+ "RB="+str(json.loads(itemset[i].icd_data)['DCI Info'][4]['DL DCI Info']['NUM RB'])
    					#...
    					+"\n")
    					mcs1=[]
    					mcs1.append(json.loads(itemset[i].icd_data)['DCI Info'][0]['DL DCI Info']['MCS index 1'])
    					mcs1.append(json.loads(itemset[i].icd_data)['DCI Info'][1]['DL DCI Info']['MCS index 1'])
    					mcs1.append(json.loads(itemset[i].icd_data)['DCI Info'][2]['DL DCI Info']['MCS index 1'])
    					mcs1.append(json.loads(itemset[i].icd_data)['DCI Info'][3]['DL DCI Info']['MCS index 1'])
    					mcs1.append(json.loads(itemset[i].icd_data)['DCI Info'][4]['DL DCI Info']['MCS index 1'])
    					mcs2=[]
    					mcs2.append(json.loads(itemset[i].icd_data)['DCI Info'][0]['DL DCI Info']['MCS index 2'])
    					mcs2.append(json.loads(itemset[i].icd_data)['DCI Info'][1]['DL DCI Info']['MCS index 2'])
    					mcs2.append(json.loads(itemset[i].icd_data)['DCI Info'][2]['DL DCI Info']['MCS index 2'])
    					mcs2.append(json.loads(itemset[i].icd_data)['DCI Info'][3]['DL DCI Info']['MCS index 2'])
    					mcs2.append(json.loads(itemset[i].icd_data)['DCI Info'][4]['DL DCI Info']['MCS index 2'])
    					rb=[]
    					rb.append(json.loads(itemset[i].icd_data)['DCI Info'][0]['DL DCI Info']['NUM RB'])
    					rb.append(json.loads(itemset[i].icd_data)['DCI Info'][1]['DL DCI Info']['NUM RB'])
    					rb.append(json.loads(itemset[i].icd_data)['DCI Info'][2]['DL DCI Info']['NUM RB'])
    					rb.append(json.loads(itemset[i].icd_data)['DCI Info'][3]['DL DCI Info']['NUM RB'])
    					rb.append(json.loads(itemset[i].icd_data)['DCI Info'][4]['DL DCI Info']['NUM RB'])
    					NR_DCI_TIME.append(itemset[i].device_time)
    					NR_DL_MCS1.append(max(mcs1))
    					NR_DL_MCS2.append(max(mcs2))
    					NR_DL_RB.append(max(rb))
    				elif search("NL1_MIMO_PDSCH_Throughput",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "Carrier Index="+str(json.loads(itemset[i].icd_data)['Carrier Index'])
    					+" "+ "DL BLER="+str(json.loads(itemset[i].icd_data)['DL BLER'])
    					+"\t"+ "MIMO PDSCH Throughput0="+str(json.loads(itemset[i].icd_data)['MIMO PDSCH Throughput0'])
    					+" "+ "MIMO PDSCH Throughput1="+str(json.loads(itemset[i].icd_data)['MIMO PDSCH Throughput1'])
    					+" "+ "Peak Throughput="+str(json.loads(itemset[i].icd_data)['Peak Throughput'])
    					+"\t"+ "Avg DL Num Rb="+str(json.loads(itemset[i].icd_data)['DL Grant Abnormal']['Avg DL Num Rb'])
    					+"\t"+ "Avg DL Mcs="+str(json.loads(itemset[i].icd_data)['DL Grant Abnormal']['Avg DL Mcs'])
    					+"\n")
    					NR_PDSCH_TPUT_TIME.append(itemset[i].device_time) #itemset[i].timestamp.strftime('%H:%M:%S:%f')[:-3])
    					NR_PDSCH_TPUT0.append(json.loads(itemset[i].icd_data)['MIMO PDSCH Throughput0'])
    					NR_PDSCH_TPUT1.append(json.loads(itemset[i].icd_data)['MIMO PDSCH Throughput1'])
    					NR_PDSCH_TPUT.append(json.loads(itemset[i].icd_data)['Peak Throughput'])
    				elif search("NL1_RACH_Information",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "RA event="+str(json.loads(itemset[i].icd_data)['RA event'])
    					+" "+ "Prach Config="+str(json.loads(itemset[i].icd_data)['RACH_MSG1']['Prach Config'])
    					+" "+ "PRACH TX power="+str(json.loads(itemset[i].icd_data)['RACH_MSG1']['PRACH TX power'])
    					+"\t"+ "RNTI Type="+str(json.loads(itemset[i].icd_data)['RACH_MSG2']['RNTI Type'])
    					+" "+ "RNTI Value="+str(json.loads(itemset[i].icd_data)['RACH_MSG2']['RNTI Value'])
    					+"\t"+ "Msg3 Power="+str(json.loads(itemset[i].icd_data)['RACH_MSG3']['Msg3 Power'])
    					+"\t"+ "Msg4 valid="+str(json.loads(itemset[i].icd_data)['RACH_MSG4']['Msg4 valid'])
    					+"\n")
    				elif search("NL2_PDCP_Throughput_DL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "PDCP Throughput DL="+str(json.loads(itemset[i].icd_data)['PDCP Throughput DL'])
    					+"\n")
    				elif search("NL2_PDCP_Throughput_UL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "PDCP Throughput UL="+str(json.loads(itemset[i].icd_data)['PDCP Throughput UL'])
    					+"\n")

					#LTE
    				elif search("EL1_Serving_Cell_Measurement",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "PCI="+str(json.loads(itemset[i].icd_data)['PCI'])
    					+" "+ "Carrier type="+str(json.loads(itemset[i].icd_data)['Carrier type'])
    					+" "+ "EARFCN="+str(json.loads(itemset[i].icd_data)['EARFCN'])
    					+"\t"+ "RSRP RX0="+str(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRP RX0'])
    					+" "+ "RSRP RX1="+str(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRP RX1'])
    					+"\t"+ "RSRQ RX0="+str(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRQ RX0'])
    					+" "+ "RSRQ RX1="+str(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRQ RX1'])
    					+"\t"+ "SINR RX0="+str(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['SINR RX0'])
    					+" "+ "SINR RX1="+str(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['SINR RX1'])
    					+"\n")
    					LTE_MEAS_TIME.append(itemset[i].device_time) #itemset[i].timestamp.strftime('%H:%M:%S:%f')[:-3])
    					#print(type(itemset[i].device_time))
    					#print(type(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRP RX0']))
    					LTE_RSRP0.append(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRP RX0'])
    					LTE_RSRP1.append(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRP RX1'])
    					LTE_RSRQ0.append(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRQ RX0'])
    					LTE_RSRQ1.append(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['RSRQ RX1'])
    					LTE_SINR0.append(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['SINR RX0'])
    					LTE_SINR1.append(json.loads(itemset[i].icd_data)['Serving Cell Measurement Records'][0]['SINR RX1'])

    				elif search("EL2_MAC_Throughput_DL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "EMAC Throughput DL="+str(json.loads(itemset[i].icd_data)['EMAC Throughput DL'])
    					+"\n")
    					LTE_MAC_TPUT_TIME.append(itemset[i].device_time)
    					LTE_MAC_TPUT.append(json.loads(itemset[i].icd_data)['EMAC Throughput DL'])
    				elif search("EL2_RLC_Throughput_DL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "DL RB Rcv Bits="+str(json.loads(itemset[i].icd_data)['DL RB Rcv Bits'])
    					+"\n")
    					LTE_RLC_TPUT_TIME.append(itemset[i].device_time)
    					LTE_RLC_TPUT.append(json.loads(itemset[i].icd_data)['DL RB Rcv Bits'])
    				elif search("EL2_PDCP_Throughput_DL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "PDCP Throughput DL="+str(json.loads(itemset[i].icd_data)['PDCP Throughput DL'])
    					+"\n")
    					LTE_PDCP_TPUT_TIME.append(itemset[i].device_time)
    					LTE_PDCP_TPUT.append(json.loads(itemset[i].icd_data)['PDCP Throughput DL'])
    				elif search("EL2_IP_Throughput_DL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "IP Throughput DL="+str(json.loads(itemset[i].icd_data)['IP Throughput DL'])
    					+"\n")
    					LTE_IP_TPUT_TIME.append(itemset[i].device_time)
    					LTE_IP_TPUT.append(json.loads(itemset[i].icd_data)['IP Throughput DL'])

    				elif search("EL2_MAC_Throughput_UL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "EMAC Throughput UL="+str(json.loads(itemset[i].icd_data)['EMAC Throughput UL'])
    					+"\n")
    					LTE_UL_MAC_TPUT_TIME.append(itemset[i].device_time)
    					LTE_UL_MAC_TPUT.append(json.loads(itemset[i].icd_data)['EMAC Throughput UL'])
    				elif search("EL2_RLC_Throughput_UL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "DL RB Rcv Bits="+str(json.loads(itemset[i].icd_data)['UL RB Tx Bits'])
    					+"\n")
    					LTE_UL_RLC_TPUT_TIME.append(itemset[i].device_time)
    					LTE_UL_RLC_TPUT.append(json.loads(itemset[i].icd_data)['UL RB Tx Bits'])
    				elif search("EL2_PDCP_Throughput_UL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "PDCP Throughput UL="+str(json.loads(itemset[i].icd_data)['PDCP Throughput UL'])
    					+"\n")
    					LTE_UL_PDCP_TPUT_TIME.append(itemset[i].device_time)
    					LTE_UL_PDCP_TPUT.append(json.loads(itemset[i].icd_data)['PDCP Throughput UL'])
    				elif search("EL2_IP_Throughput_UL",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "IP Throughput UL="+str(json.loads(itemset[i].icd_data)['IP Throughput UL'])
    					+"\n")
    					LTE_UL_IP_TPUT_TIME.append(itemset[i].device_time)
    					LTE_UL_IP_TPUT.append(json.loads(itemset[i].icd_data)['IP Throughput UL'])


    				elif search("EL1_RACH_Information",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    		 			+"\t"+ "Prach Config="+str(json.loads(itemset[i].icd_data)['RACH_MSG1']['Prach Config'])
    					+" "+ "PRACH TX power="+str(json.loads(itemset[i].icd_data)['RACH_MSG1']['PRACH TX power'])
    					+"\t"+ "RNTI Type="+str(json.loads(itemset[i].icd_data)['RACH_MSG2']['RNTI Type'])
    					+" "+ "RNTI Value="+str(json.loads(itemset[i].icd_data)['RACH_MSG2']['RNTI Value'])
    					+"\t"+ "Msg3 valid="+str(json.loads(itemset[i].icd_data)['RACH_MSG3']['Msg3 valid'])
    					+"\t"+ "Msg4 valid="+str(json.loads(itemset[i].icd_data)['RACH_MSG4']['Msg4 valid'])
    					+"\n")


    				#primitive
    				elif search("event\(MSG_ID|received: MSG_ID",itemset[i].message): s=1 #skip this due to no information included

    				elif search("MSG_ID_EM_EL1_STATUS_IND",itemset[i].message):
    					#print(itemset[i].prim)
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "dl_cc_count="+str(itemset[i].prim.dl_cc_count)
    					+" "+ "ul_cc_count="+str(itemset[i].prim.ul_cc_count)

    					+"\t"+ "cell_info[0].band="+str(itemset[i].prim.cell_info[0].band)
    					+" "+ "ant_port="+str(itemset[i].prim.cell_info[0].ant_port)
    					+" "+ "dl_bw="+str(itemset[i].prim.cell_info[0].dl_bw)
    					+" "+ "ul_bw="+str(itemset[i].prim.cell_info[0].ul_bw)
    					+" "+ "pci="+str(itemset[i].prim.cell_info[0].pci)
    					+" "+ "earfcn="+str(itemset[i].prim.cell_info[0].earfcn)
    					+" "+ "dl_bw_rb="+str(itemset[i].prim.cell_info[0].dl_bw_rb)
    					+" "+ "ul_bw_rb="+str(itemset[i].prim.cell_info[0].ul_bw_rb)
    					+" "+ "dl_max_throughput="+str(itemset[i].prim.cell_info[0].dl_max_throughput)
    					+" "+ "ul_max_throughput="+str(itemset[i].prim.cell_info[0].ul_max_throughput)
						+"\t"+ "cell_info[1].band="+str(itemset[i].prim.cell_info[1].band)
						+" "+ "ant_port="+str(itemset[i].prim.cell_info[1].ant_port)
						+" "+ "dl_bw="+str(itemset[i].prim.cell_info[1].dl_bw)
						+" "+ "ul_bw="+str(itemset[i].prim.cell_info[1].ul_bw)
						+" "+ "pci="+str(itemset[i].prim.cell_info[1].pci)
						+" "+ "earfcn="+str(itemset[i].prim.cell_info[1].earfcn)
						+" "+ "dl_bw_rb="+str(itemset[i].prim.cell_info[1].dl_bw_rb)
						+" "+ "ul_bw_rb="+str(itemset[i].prim.cell_info[1].ul_bw_rb)
						+" "+ "dl_max_throughput="+str(itemset[i].prim.cell_info[1].dl_max_throughput)
						+" "+ "ul_max_throughput="+str(itemset[i].prim.cell_info[1].ul_max_throughput)
						+"\t"+ "cell_info[2].band="+str(itemset[i].prim.cell_info[2].band)
						+" "+ "ant_port="+str(itemset[i].prim.cell_info[2].ant_port)
						+" "+ "dl_bw="+str(itemset[i].prim.cell_info[2].dl_bw)
						+" "+ "ul_bw="+str(itemset[i].prim.cell_info[2].ul_bw)
						+" "+ "pci="+str(itemset[i].prim.cell_info[2].pci)
						+" "+ "earfcn="+str(itemset[i].prim.cell_info[2].earfcn)
						+" "+ "dl_bw_rb="+str(itemset[i].prim.cell_info[2].dl_bw_rb)
						+" "+ "ul_bw_rb="+str(itemset[i].prim.cell_info[2].ul_bw_rb)
						+" "+ "dl_max_throughput="+str(itemset[i].prim.cell_info[2].dl_max_throughput)
						+" "+ "ul_max_throughput="+str(itemset[i].prim.cell_info[2].ul_max_throughput)
						+"\t"+ "cell_info[3].band="+str(itemset[i].prim.cell_info[3].band)
						+" "+ "ant_port="+str(itemset[i].prim.cell_info[3].ant_port)
						+" "+ "dl_bw="+str(itemset[i].prim.cell_info[3].dl_bw)
						+" "+ "ul_bw="+str(itemset[i].prim.cell_info[3].ul_bw)
						+" "+ "pci="+str(itemset[i].prim.cell_info[3].pci)
						+" "+ "earfcn="+str(itemset[i].prim.cell_info[3].earfcn)
						+" "+ "dl_bw_rb="+str(itemset[i].prim.cell_info[3].dl_bw_rb)
						+" "+ "ul_bw_rb="+str(itemset[i].prim.cell_info[3].ul_bw_rb)
						+" "+ "dl_max_throughput="+str(itemset[i].prim.cell_info[3].dl_max_throughput)
						+" "+ "ul_max_throughput="+str(itemset[i].prim.cell_info[3].ul_max_throughput)
    					#+"\t"+ "dl_info[0].dl_rsrp[0]="+str(itemset[i].prim.dl_info[0].dl_rsrp.dl_rsrp[0])
    					#+"\t"+ "dl_info[0].dl_rsrp_avg[0]="+str(itemset[i].prim.dl_info[0].dl_rsrp_avg[0].__long__())
    					#+" "+ "dl_rsrp_avg[1]="+str(itemset[i].prim.dl_info[0].dl_rsrp_avg[1].__long__())
    					#+" "+ "dl_rsrp_avg[2]="+str(itemset[i].prim.dl_info[0].dl_rsrp_avg[2].__long__())
    					#+" "+ "dl_rsrp_avg[3]="+str(itemset[i].prim.dl_info[0].dl_rsrp_avg[3].__long__())
    					#+"\t"+ "dl_sinr_avg[0]="+str(itemset[i].prim.dl_info[0].dl_sinr_avg[0].__long__())
    					#+" "+ "dl_sinr_avg[1]="+str(itemset[i].prim.dl_info[0].dl_sinr_avg[1].__long__())
    					#+" "+ "dl_sinr_avg[2]="+str(itemset[i].prim.dl_info[0].dl_sinr_avg[2].__long__())
    					#+" "+ "dl_sinr_avg[3]="+str(itemset[i].prim.dl_info[0].dl_sinr_avg[3].__long__())
    					#+"\t"+ "tm="+str(itemset[i].prim.dl_info[0].tm)
    					#+"\t"+ "cqi_cw0="+str(itemset[i].prim.dl_info[0].cqi_cw0)
    					#+" "+ "cqi_cw1="+str(itemset[i].prim.dl_info[0].cqi_cw1)
    					#+"\t"+ "ri="+str(itemset[i].prim.dl_info[0].ri)
    					#+"\t"+ "mcs0="+str(itemset[i].prim.dl_info[0].dl_mcs0)
    					#+" "+ "mcs1="+str(itemset[i].prim.dl_info[0].dl_mcs1)
    					+"\n")

    					EL1_STATUS_TIME.append(itemset[i].device_time.__int__()) #itemset[i].timestamp.strftime('%H:%M:%S:%f')[:-3])
    					EL1_DL_CC_COUNT.append(itemset[i].prim.dl_cc_count.__int__())
    					EL1_UL_CC_COUNT.append(itemset[i].prim.ul_cc_count.__int__())
    					EL1_0_BAND.append(itemset[i].prim.cell_info[0].band.__int__())
    					EL1_1_BAND.append(itemset[i].prim.cell_info[1].band.__int__())
    					EL1_2_BAND.append(itemset[i].prim.cell_info[2].band.__int__())
    					EL1_3_BAND.append(itemset[i].prim.cell_info[3].band.__int__())
    					EL1_0_PCI.append(itemset[i].prim.cell_info[0].pci.__int__())
    					EL1_1_PCI.append(itemset[i].prim.cell_info[1].pci.__int__())
    					EL1_2_PCI.append(itemset[i].prim.cell_info[2].pci.__int__())
    					EL1_3_PCI.append(itemset[i].prim.cell_info[3].pci.__int__())
    					EL1_0_EARFCN.append(itemset[i].prim.cell_info[0].earfcn.__int__())
    					EL1_1_EARFCN.append(itemset[i].prim.cell_info[1].earfcn.__int__())
    					EL1_2_EARFCN.append(itemset[i].prim.cell_info[2].earfcn.__int__())
    					EL1_3_EARFCN.append(itemset[i].prim.cell_info[3].earfcn.__int__())

    					EL1_0_DL_BW.append(itemset[i].prim.cell_info[0].dl_bw.__int__())
    					EL1_1_DL_BW.append(itemset[i].prim.cell_info[1].dl_bw.__int__())
    					EL1_2_DL_BW.append(itemset[i].prim.cell_info[2].dl_bw.__int__())
    					EL1_3_DL_BW.append(itemset[i].prim.cell_info[3].dl_bw.__int__())
    					EL1_0_UL_BW.append(itemset[i].prim.cell_info[0].ul_bw.__int__())
    					EL1_1_UL_BW.append(itemset[i].prim.cell_info[1].ul_bw.__int__())
    					EL1_2_UL_BW.append(itemset[i].prim.cell_info[2].ul_bw.__int__())
    					EL1_3_UL_BW.append(itemset[i].prim.cell_info[3].ul_bw.__int__())    					
    					EL1_0_DL_TPUT.append(itemset[i].prim.dl_info[0].DL_Tput.__int__())
    					EL1_1_DL_TPUT.append(itemset[i].prim.dl_info[1].DL_Tput.__int__())
    					EL1_2_DL_TPUT.append(itemset[i].prim.dl_info[2].DL_Tput.__int__())
    					EL1_3_DL_TPUT.append(itemset[i].prim.dl_info[3].DL_Tput.__int__())

    					#print("dl_rsrp",itemset[i].prim.dl_info[0].dl_rsrp[0].__int__())
    					EL1_0_RSRP0.append(itemset[i].prim.dl_info[0].dl_rsrp[0].__int__())
    					EL1_0_RSRP1.append(itemset[i].prim.dl_info[0].dl_rsrp[1].__int__())
    					EL1_1_RSRP0.append(itemset[i].prim.dl_info[1].dl_rsrp[0].__int__())
    					EL1_1_RSRP1.append(itemset[i].prim.dl_info[1].dl_rsrp[1].__int__())
    					EL1_2_RSRP0.append(itemset[i].prim.dl_info[2].dl_rsrp[0].__int__())
    					EL1_2_RSRP1.append(itemset[i].prim.dl_info[2].dl_rsrp[1].__int__())
    					EL1_3_RSRP0.append(itemset[i].prim.dl_info[3].dl_rsrp[0].__int__())
    					EL1_3_RSRP1.append(itemset[i].prim.dl_info[3].dl_rsrp[1].__int__())

    					#print("dl_rsrp",itemset[i].prim.dl_info[0].dl_sinr[0].__int__())
    					EL1_0_SINR0.append(itemset[i].prim.dl_info[0].dl_sinr[0].__int__())
    					EL1_0_SINR1.append(itemset[i].prim.dl_info[0].dl_sinr[1].__int__())
    					EL1_1_SINR0.append(itemset[i].prim.dl_info[1].dl_sinr[0].__int__())
    					EL1_1_SINR1.append(itemset[i].prim.dl_info[1].dl_sinr[1].__int__())
    					EL1_2_SINR0.append(itemset[i].prim.dl_info[2].dl_sinr[0].__int__())
    					EL1_2_SINR1.append(itemset[i].prim.dl_info[2].dl_sinr[1].__int__())
    					EL1_3_SINR0.append(itemset[i].prim.dl_info[3].dl_sinr[0].__int__())
    					EL1_3_SINR1.append(itemset[i].prim.dl_info[3].dl_sinr[1].__int__())

    					EL1_0_CQI0.append(itemset[i].prim.dl_info[0].cqi_cw0.__int__())
    					EL1_0_CQI1.append(itemset[i].prim.dl_info[0].cqi_cw1.__int__())
    					EL1_1_CQI0.append(itemset[i].prim.dl_info[1].cqi_cw0.__int__())
    					EL1_1_CQI1.append(itemset[i].prim.dl_info[1].cqi_cw1.__int__())
    					EL1_2_CQI0.append(itemset[i].prim.dl_info[2].cqi_cw0.__int__())
    					EL1_2_CQI1.append(itemset[i].prim.dl_info[2].cqi_cw1.__int__())
    					EL1_3_CQI0.append(itemset[i].prim.dl_info[3].cqi_cw0.__int__())
    					EL1_3_CQI1.append(itemset[i].prim.dl_info[3].cqi_cw1.__int__())

    					EL1_0_MCS.append(itemset[i].prim.dl_info[0].DL_Imcs.__int__())
    					EL1_1_MCS.append(itemset[i].prim.dl_info[1].DL_Imcs.__int__())
    					EL1_2_MCS.append(itemset[i].prim.dl_info[2].DL_Imcs.__int__())
    					EL1_3_MCS.append(itemset[i].prim.dl_info[3].DL_Imcs.__int__())

    					EL1_0_BLER.append(itemset[i].prim.dl_info[0].DL_bler.__int__())
    					EL1_1_BLER.append(itemset[i].prim.dl_info[1].DL_bler.__int__())
    					EL1_2_BLER.append(itemset[i].prim.dl_info[2].DL_bler.__int__())
    					EL1_3_BLER.append(itemset[i].prim.dl_info[3].DL_bler.__int__())

    					#print(itemset[i].prim.dl_info[0].avg_dl_grant.__int__())
    					EL1_0_GRANT.append(itemset[i].prim.dl_info[0].DL_rb.__int__())
    					EL1_1_GRANT.append(itemset[i].prim.dl_info[1].DL_rb.__int__())
    					EL1_2_GRANT.append(itemset[i].prim.dl_info[2].DL_rb.__int__())
    					EL1_3_GRANT.append(itemset[i].prim.dl_info[3].DL_rb.__int__())

    					#print("UL_Tput0",itemset[i].prim.ul_info[0].UL_Tput.__int__())
    					#print("UL_Tput1",itemset[i].prim.ul_info[1].UL_Tput.__int__())
    					EL1_0_UL_TPUT.append(itemset[i].prim.ul_info[0].UL_Tput.__int__())
    					EL1_1_UL_TPUT.append(itemset[i].prim.ul_info[1].UL_Tput.__int__())

    					EL1_0_ULMCS.append(itemset[i].prim.ul_info[0].UL_Imcs.__int__())
    					EL1_1_ULMCS.append(itemset[i].prim.ul_info[1].UL_Imcs.__int__())

    					EL1_0_ULRB.append(itemset[i].prim.ul_info[0].UL_rb.__int__())
    					EL1_1_ULRB.append(itemset[i].prim.ul_info[1].UL_rb.__int__())

    					EL1_0_ULBLER.append(itemset[i].prim.ul_info[0].UL_bler.__int__())
    					EL1_1_ULBLER.append(itemset[i].prim.ul_info[1].UL_bler.__int__())

    					EL1_0_ULMOD.append(itemset[i].prim.ul_info[0].UL_Mod.__int__())
    					EL1_1_ULMOD.append(itemset[i].prim.ul_info[1].UL_Mod.__int__())

    					EL1_0_PRACH_PWR.append(itemset[i].prim.ul_info[0].prach_tx_power_ave.__int__())
    					EL1_0_PUCCH_PWR.append(itemset[i].prim.ul_info[0].pucch_tx_power_ave.__int__())
    					EL1_0_PUSCH_PWR.append(itemset[i].prim.ul_info[0].pusch_tx_power_ave.__int__())
    					EL1_0_SRS_PWR.append(itemset[i].prim.ul_info[0].srs_tx_power_ave.__int__())
    					EL1_0_TOT_PWR.append(itemset[i].prim.ul_info[0].total_tx_power_ave.__int__())

    					EL1_1_PRACH_PWR.append(itemset[i].prim.ul_info[1].prach_tx_power_ave.__int__())
    					EL1_1_PUCCH_PWR.append(itemset[i].prim.ul_info[1].pucch_tx_power_ave.__int__())
    					EL1_1_PUSCH_PWR.append(itemset[i].prim.ul_info[1].pusch_tx_power_ave.__int__())
    					EL1_1_SRS_PWR.append(itemset[i].prim.ul_info[1].srs_tx_power_ave.__int__())
    					EL1_1_TOT_PWR.append(itemset[i].prim.ul_info[1].total_tx_power_ave.__int__())

    					EL1_0_PHR.append(itemset[i].prim.ul_info[0].phr.__int__())
    					EL1_1_PHR.append(itemset[i].prim.ul_info[1].phr.__int__())

    					EL1_0_RETX_RATE.append(itemset[i].prim.ul_info[0].UL_retx_rate.__int__())
    					EL1_1_RETX_RATE.append(itemset[i].prim.ul_info[1].UL_retx_rate.__int__())

    					EL1_0_PCMAX.append(itemset[i].prim.ul_info[0].pcmax.__int__())
    					EL1_1_PCMAX.append(itemset[i].prim.ul_info[1].pcmax.__int__())


    				elif search("MSG_ID_EM_RAC_INFO_IND",itemset[i].message):
    					f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)
    					+"\t"+ "ue_mode="+str(itemset[i].prim.ue_mode)
    					+" "+ "ue_usage_setting="+str(itemset[i].prim.ue_usage_setting)
    					+"\t"+ "mcc1="+str(itemset[i].prim.plmn_id.mcc1)
    					+" "+ "mcc2="+str(itemset[i].prim.plmn_id.mcc2)
    					+" "+ "mcc3="+str(itemset[i].prim.plmn_id.mcc3)
    					+" "+ "mnc1="+str(itemset[i].prim.plmn_id.mnc1)
    					+" "+ "mnc2="+str(itemset[i].prim.plmn_id.mnc2)
    					+" "+ "mnc3="+str(itemset[i].prim.plmn_id.mnc3)
    					+"\t"+ "cell_id="+str(itemset[i].prim.cell_id)
    					+"\t"+ "rat="+str(itemset[i].prim.rat)
    					+"\n")

    				elif search("MSG_ID_ERRC_EL1MPC_CARRIER_SEARCH_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "result="+str(itemset[i].prim.result) +"\n")
    				elif search("MSG_ID_ERRC_EL1MPC_CARRIER_SEARCH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "band_idx="+str(itemset[i].prim.band_idx) +"\t"+ "freq_num="+str(itemset[i].prim.freq_num)  +"\n")
    				elif search("MSG_ID_ERRC_EL1_SPECIFIC_CELL_SEARCH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "earfcn="+str(itemset[i].prim.earfcn) +"\t"+ "cell_detected="+str(itemset[i].prim.cell_detected) +"\n")
    				elif search("MSG_ID_ERRC_MOB_CEL_SI_MEAS_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "earfcn="+str(itemset[i].prim.earfcn) +"\t"+ "pci="+str(itemset[i].prim.pci) +"\t"+ "rsrp="+str(itemset[i].prim.rsrp) +"\t"+ "rsrq="+str(itemset[i].prim.rsrq) +"\t"+ "snr="+str(itemset[i].prim.snr) +"\n")
    				elif search("MSG_ID_ERRC_SYS_CEL_BCCH_RCVD_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "rcv_result="+str(itemset[i].prim.rcv_result) +"\t"+ "failure_cause="+str(itemset[i].prim.failure_cause) +"\n")
    				elif search("MSG_ID_ERRC_MOB_CEL_RESEL_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_ERRC_NL1_SFTD_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_ERRC_NL1_SFTD_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_ERRC_NL1_SFTD_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_ERRC_NL1_SFTD_RSP",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_ERRC_EL1_RLF_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "rlf_cause="+str(itemset[i].prim.rlf_cause) +"\n")
    				elif search("MSG_ID_ERRC_ERLC_RLF_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "cause="+str(itemset[i].prim.cause) +"\n")
    				elif search("MSG_ID_ERRC_CHM_CONN_RLF_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "l1_rlf="+str(itemset[i].prim.l1_rlf) +"\t"+ "mac_rlf="+str(itemset[i].prim.mac_rlf) +"\t"+ "rlc_rlf="+str(itemset[i].prim.rlc_rlf) +"\t"+ "rlc_rlf_cause="+str(itemset[i].prim.rlc_rlf_cause) +"\t"+ "l1_rlf_cause="+str(itemset[i].prim.l1_rlf_cause) +"\n")
    				elif search("MSG_ID_ERRC_NRRC_MEAS_REPORT_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("ERRC_CEL_CELL_JUDGE_SUITABLE",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_EMM_ERRC_CELLSELECT_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "cell_status="+str(itemset[i].prim.cell_select_inf.cell_status) +"\n")
    				elif search("MSG_ID_EMM_ERRC_ESTABLISH_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "cause="+str(itemset[i].prim.cause) +"\n")
    				elif search("MSG_ID_EMM_ERRC_ESTABLISH_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "result="+str(itemset[i].prim.result) +"\n")
    				elif search("MSG_ID_ESMREG_PDN_CONN_EST_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "req_reason="+str(itemset[i].prim.req_reason) +"\t"+ "req_type="+str(itemset[i].prim.req_type) +"\t"+ "pdn_type="+str(itemset[i].prim.pdn_type) +"\n")
    				elif search("MSG_ID_ESMREG_PDN_CONN_EST_REJ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "failure_cause="+str(itemset[i].prim.failure_cause) +"\n")
    				elif search("MSG_ID_EMM_CALL_EVALIF_RACH_REJECT_IND|MSG_ID_EVAL_EMM_RACH_REJECT_IND|MSG_ID_L4C_EVAL_RACH_REJECT_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "reject_cause="+str(itemset[i].prim.reject_cause) +"\n")
    				elif search("MSG_ID_IWLAN_L4BNW_ATTACHED_RAT_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "currently_attached_rat="+str(itemset[i].prim.attached_network_info.currently_attached_rat) +"\t"+ "cs_currently_attached_rat="+str(itemset[i].prim.attached_network_info.cs_currently_attached_rat) +"\t"+ "data_speed_support="+str(itemset[i].prim.attached_network_info.data_speed_support) +"\t"+ "cs_data_speed_support="+str(itemset[i].prim.attached_network_info.cs_data_speed_support) +"\n")

    				elif search("MSG_ID_NAS_SV_ANY_RAT_CHANGE_START_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "irat_type="+str(itemset[i].prim.irat_type) +"\t"+ "source_rat="+str(itemset[i].prim.source_rat) +"\t"+ "target_rat="+str(itemset[i].prim.target_rat) +"\n")
    				elif search("MSG_ID_NAS_SV_ANY_RAT_CHANGE_FINISH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "irat_result="+str(itemset[i].prim.irat_result) +"\n")
    				elif search("MSG_ID_NWSEL_NAS_SV_PLMN_SEARCH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "rat="+str(itemset[i].prim.rat) +"\n")
    				elif search("MSG_ID_NWSEL_NAS_SV_PLMN_SEARCH_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "rat="+str(itemset[i].prim.rat) +"\t"+ "result="+str(itemset[i].prim.result) +"\t"+ "is_as_plmn_list_present="+str(itemset[i].prim.is_as_plmn_list_present) +"\n")

    				elif search("MSG_ID_VDM_ATP_CMD_DIAL_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "is_video_call="+str(itemset[i].prim.is_video_call)  +"\n")
    				elif search("MSG_ID_VDM_ATP_CMD_DIAL_RSP",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "result="+str(itemset[i].prim.result) +"\t"+ "err_id="+str(itemset[i].prim.err_id)  +"\n")


    				#elif search("MSG_ID_NL1CSM_NL1MOB_SSB_INTRA_MEAS_RESULT_NTF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				#elif search("MSG_ID_NL1CSM_NL1MOB_SSB_INTER_MEAS_RESULT_NTF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NMAC_NL1_CA_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "is_scell_activated="+str(itemset[i].prim.is_scell_activated) +"\t"+ "num_ca="+str(itemset[i].prim.num_ca) +"\n")
    				elif search("MSG_ID_NRRC_NL1_CONTINUOUS_CARRIER_SEARCH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "detected_cell_list_num="+str(itemset[i].prim.detected_cell_list_num) +"\t"+ "band="+str(itemset[i].prim.detected_cell_list[0].band) +"\t"+ "nrarfcn="+str(itemset[i].prim.detected_cell_list[0].nrarfcn) +"\t"+ "pci="+str(itemset[i].prim.detected_cell_list[0].pci) +"\n")
    				elif search("MSG_ID_NRRC_NL1_BACKGROUND_CONTINUOUS_CARRIER_SEARCH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "detected_cell_list_num="+str(itemset[i].prim.detected_cell_list_num) +"\t"+ "band="+str(itemset[i].prim.detected_cell_list[0].band) +"\t"+ "nrarfcn="+str(itemset[i].prim.detected_cell_list[0].nrarfcn) +"\t"+ "pci="+str(itemset[i].prim.detected_cell_list[0].pci)  +"\n")
    				elif search("MSG_ID_NRRC_IDLE_SEARCH_CELL_SEARCH_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "cell_num="+str(itemset[i].prim.cell_num) +"\t"+ "band="+str(itemset[i].prim.cell_list[0].dl_frequency_band) +"\t"+ "ssb_arfcn="+str(itemset[i].prim.cell_list[0].ssb_arfcn) +"\t"+ "pci="+str(itemset[i].prim.cell_list[0].pci)  +"\n")
    				#elif search("MSG_ID_NRRC_IDLE_SI_COLLECT_SI_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NRRC_MAIN_SCG_IE_CHECK_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "result="+str(itemset[i].prim.result) +"\t"+ "pscell_status="+str(itemset[i].prim.chctrl_param.pscell_status) +"\t"+ "dl_frequency_band="+str(itemset[i].prim.chctrl_param.nr_pscell.dl_frequency_band) +"\t"+ "narfcn="+str(itemset[i].prim.chctrl_param.nr_pscell.narfcn) +"\t"+ "pci="+str(itemset[i].prim.chctrl_param.nr_pscell.pci) +"\n")
    				elif search("MSG_ID_NRRC_NL1_RANDOM_ACCESS_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "type="+str(itemset[i].prim.type)  +"\n")
    				elif search("MSG_ID_NRRC_NL1_CELL_INFO_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "serving_cell_num="+str(itemset[i].prim.serving_cell_num) +"\t"+ "dl_frequency_band="+str(itemset[i].prim.serving_cell_list[0].serving_cell.dl_frequency_band) +"\t"+ "ssb_arfcn="+str(itemset[i].prim.serving_cell_list[0].serving_cell.ssb_arfcn) +"\t"+ "pci="+str(itemset[i].prim.serving_cell_list[0].serving_cell.pci) +"\t"+ "neighbour_cell_num="+str(itemset[i].prim.neighbour_cell_num) +"\t"+ "dl_frequency_band="+str(itemset[i].prim.neighbour_cell_list[0].neighbour_cell.dl_frequency_band)  +"\n")
    				elif search("MSG_ID_NRRC_IDLE_CONFIG_CONFIG_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "q_exlev_min="+str(itemset[i].prim.cell_selection_params.q_rxlev_min) +"\t"+ "q_qual_min="+str(itemset[i].prim.cell_selection_params.q_qual_min) +"\t"+ "q_offset_temp="+str(itemset[i].prim.cell_selection_params.q_offset_temp) +"\t"+ "p_compensation="+str(itemset[i].prim.cell_selection_params.p_compensation) +"\n")
    				elif search("MSG_ID_NRRC_MAIN_CONFIG_ICD_INFO_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "mcg_info.spcell_info.pci="+str(itemset[i].prim.mcg_info.spcell_info.pci) +" "+ "dl_arfcn="+str(itemset[i].prim.mcg_info.spcell_info.dl_arfcn) +" "+ "dl_band="+str(itemset[i].prim.mcg_info.spcell_info.dl_band)  +"\t"+ "mcg_info.scell_info.pci="+str(itemset[i].prim.mcg_info.scell_info[0].pci) +" "+ "dl_arfcn="+str(itemset[i].prim.mcg_info.scell_info[0].dl_arfcn) +" "+ "dl_band="+str(itemset[i].prim.mcg_info.scell_info[0].dl_band)  +"\t\t"+ "scg_info.spcell_info.pci="+str(itemset[i].prim.scg_info.spcell_info.pci) +" "+ "dl_arfcn="+str(itemset[i].prim.scg_info.spcell_info.dl_arfcn) +" "+ "dl_band="+str(itemset[i].prim.scg_info.spcell_info.dl_band)  +"\t"+ "scg_info.scell_info.pci="+str(itemset[i].prim.scg_info.scell_info[0].pci) +" "+ "dl_arfcn="+str(itemset[i].prim.scg_info.scell_info[0].dl_arfcn) +" "+ "dl_band="+str(itemset[i].prim.scg_info.scell_info[0].dl_band) +"\n")
    				elif search("MSG_ID_NRRC_NL1_PAGING_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "ue_identity="+str(itemset[i].prim.ue_identity) +"\n")
    				elif search("MSG_ID_NRRC_MAIN_IDLE_RESELECTION_NEEDED_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NRRC_MAIN_IDLE_RESELECTION_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NRRC_MAIN_IDLE_RESELECTION_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NRRC_NCONN_MEAS_CONFIG_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NRRC_NCONN_MEAS_CONFIG_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("MSG_ID_NRRC_NL1_RLF_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "rlf_event="+str(itemset[i].prim.rlf_event) +"\n")
    				elif search("MSG_ID_NRRC_MAIN_NCONN_RELEASE_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "current_cell_exists="+str(itemset[i].prim.current_cell_exists) +"\t"+ "release_cause="+str(itemset[i].prim.release_cause) +"\n")
    				elif search("MSG_ID_VGMM_NRRC_RELEASE_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "release_cause="+str(itemset[i].prim.release_cause) +"\n")
    				elif search("MSG_ID_VGSM_ESM_CONTEXT_TRANSFER_REQ_NTF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "ebi[0]="+str(itemset[i].prim.ebi[0]) +"\n")
    				elif search("MSG_ID_VGMM_NRRC_ESTABLISH_REQ",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "establish_cause="+str(itemset[i].prim.establish_cause) +"\n")
    				elif search("MSG_ID_VGMM_NRRC_ESTABLISH_CNF",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "establish_result="+str(itemset[i].prim.establish_result) +"\n")
    				elif search("MSG_ID_RAC_VGMM_NW_FEATURE_SUPPORT_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\t"+ "vg_ims_3gpp_ind="+str(itemset[i].prim.vg_nw_feature_support.vg_ims_3gpp_ind) +"\t"+ "vg_emergency_service_ind="+str(itemset[i].prim.vg_nw_feature_support.vg_emergency_service_ind) +"\t"+ "vg_emergency_fallback_ind="+str(itemset[i].prim.vg_nw_feature_support.vg_emergency_fallback_ind) +"\t"+ "iwk_n26_ind="+str(itemset[i].prim.vg_nw_feature_support.iwk_n26_ind) +"\n")
    				elif search("MSG_ID_L4CRAC_REG_STATE_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message)  +"\n") #+"\t"+ "updated_domain="+str(itemset[i].prim.reg_state_ind.updated_domain) +"\t"+ "cs_state="+str(itemset[i].prim.reg_state_ind.cs_state) +"\t"+ "ps_state="+str(itemset[i].prim.reg_state_ind.ps_state) +"\t"+ "rat="+str(itemset[i].prim.reg_state_ind.cell_type.rat) +"\t"+ "reject_cause="+str(itemset[i].prim.reg_state_ind.reject_cause)  +"\n")

    				#sys/ps
    				elif search("Srxlev|cell select|cell failed",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("BW check",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("Serv cell|Serving cell",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("NWSEL Current Camp on|tcm_check_tcm_pdp_activate_req|is_hplmn|SPLMN|Compared PLMN|HPLMN from IMSI|Serving PLMN|AvailPLMN",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("P-Max",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("CA capa supported check|CA combination not supported|NL1 CA band comb",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("RF configuration invalid",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("Add LTE REJ Cell|MOB_REJ_CELL timer",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("Add NR cell|Remove NR cell",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("ENDC cell info|is endc nr|ENDC band combination check result|bad cell|SCG state change",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("RLF_IND|OOS_REQ|OOS due to|OOS_IND",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("LTE_RESEL_JUDGE",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("LFREQ|UFREQ|GFREQ|LCell|UCell|GCell",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("RAR fail|timeout|NL1MOB_TIMER_STATUS_EXPIRE|ERRC_TIMER_CONN_AFR_EXPR",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("report NACK PDU|t-Reordering timer expire",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("attempt count|startT|stopT|timer start|timer stopped|timer expired",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("EMM mainstate",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("pcas_operator",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("\+EAPNACT|\+CFUN|\+EMCS|]\+EREG|]\+EGREG",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    				elif search("FILE_U_FDN_IDX",itemset[i].message): f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")

					#others
    				#elif search("AT_|AT\+|]\+|Internal Processing|All RF calibration|IMC_TASK|Timer|CEL_DI|CELLJ|CJUDGE|CJDG|AvailPLMN|MRM|COM|FSM|MMRF|ETCM|RCM|ERRC|ERLCDL|EMAC|NL1MPC|NCONFIG|PCAS|EMM COMMON|MRS_NRAS|CHM|CREJ|SCG|EMM REG|CAP|PHB|ICD|DHL|RLF",itemset[i].message): s=1
    				#else: f.write(str(itemset[i].index) +"\t"+ str(itemset[i].timestamp.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]) +"\t"+ str(itemset[i].message) +"\n")
    		except:
    			#print("Error! No parsed data!")
    			pass

    f.close()

    """
    if len(LTE_MEAS_TIME)>0 or len(LTE_DCI_TIME)>0 or len(LTE_PDSCH_TPUT_TIME)>0:
        fig=plt.figure(figsize=(13,9))
        fig.suptitle('LTE Analysis', fontsize=16)
        if len(LTE_MEAS_TIME)>0:
            plt.subplot(6,1,1)
            if len(LTE_MEAS_TIME)>100: n=len(LTE_MEAS_TIME)/100
            else: n=1
            rsrp0=[sum(LTE_RSRP0)/len(LTE_RSRP0)]*len(LTE_MEAS_TIME)
            rsrp1=[sum(LTE_RSRP1)/len(LTE_RSRP1)]*len(LTE_MEAS_TIME)
            plt.plot(LTE_MEAS_TIME[::n], LTE_RSRP0[::n], label='RSRP0 (Mean='+str(rsrp0[0])+')')
            plt.plot(LTE_MEAS_TIME[::n], LTE_RSRP1[::n], label='RSRP1 (Mean='+str(rsrp1[0])+')', alpha=0.5)
            #plt.plot(LTE_MEAS_TIME[::n], rsrp0[::n], label='RSRP0 Mean='+str(rsrp0[0]), linestyle='--')
            #plt.plot(LTE_MEAS_TIME[::n], rsrp1[::n], label='RSRP1 Mean='+str(rsrp1[0]), linestyle='--')
            plt.legend()
            plt.subplot(6,1,2)
            rsrq0=[sum(LTE_RSRQ0)/len(LTE_RSRQ0)]*len(LTE_MEAS_TIME)
            rsrq1=[sum(LTE_RSRQ1)/len(LTE_RSRQ1)]*len(LTE_MEAS_TIME)
            plt.plot(LTE_MEAS_TIME[::n], LTE_RSRQ0[::n], label='RSRQ0 (Mean='+str(rsrq0[0])+')')
            plt.plot(LTE_MEAS_TIME[::n], LTE_RSRQ1[::n], label='RSRQ1 (Mean='+str(rsrq1[0])+')', alpha=0.5)
            #plt.plot(LTE_MEAS_TIME[::n], rsrq0[::n], label='RSRQ0 Mean='+str(rsrq0[0]), linestyle='--')
            #plt.plot(LTE_MEAS_TIME[::n], rsrq1[::n], label='RSRQ1 Mean='+str(rsrq1[0]), linestyle='--')
            plt.legend()
            plt.subplot(6,1,3)
            sinr0=[sum(LTE_SINR0)/len(LTE_SINR0)]*len(LTE_MEAS_TIME)
            sinr1=[sum(LTE_SINR1)/len(LTE_SINR1)]*len(LTE_MEAS_TIME)
            plt.plot(LTE_MEAS_TIME[::n], LTE_SINR0[::n], label='SINR0 (Mean='+str(sinr0[0])+')')
            plt.plot(LTE_MEAS_TIME[::n], LTE_SINR1[::n], label='SINR1 (Mean='+str(sinr1[0])+')', alpha=0.5)
            #plt.plot(LTE_MEAS_TIME[::n], sinr0[::n], label='SINR0 Mean='+str(sinr0[0]), linestyle='--')
            #plt.plot(LTE_MEAS_TIME[::n], sinr1[::n], label='SINR1 Mean='+str(sinr1[0]), linestyle='--')
            plt.legend()
    	#plt.show()
    	fig.savefig('LTE_Analysis.png')
   	"""

    #"""
    if len(EL1_STATUS_TIME)>0:
        fig=plt.figure(figsize=(13,9))
        #fig.suptitle('LTE_Cell_Information', fontsize=16)
        if len(EL1_STATUS_TIME)>1000: n=len(EL1_STATUS_TIME)/1000
        else: n=1
        plt.subplot(5,1,1)
        plt.plot(EL1_STATUS_TIME[::n], EL1_DL_CC_COUNT[::n], label='# of DL CC', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_UL_CC_COUNT[::n], label='# of UL CC', color='blue', linestyle='-', alpha=0.6)
        plt.grid()
        plt.ylim([0, 7])
        plt.ylabel('LTE CC#')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(5,1,2)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_BAND[::n], label='CC0_Band', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_BAND[::n], label='CC1_Band', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_BAND[::n], label='CC2_Band', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_BAND[::n], label='CC3_Band', color='cyan', linestyle='-', alpha=0.6)
        plt.grid()
        #plt.ylim([0, 88])
        plt.ylabel('LTE Band')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(5,1,3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_DL_BW[::n], label='CC0_DL_BW', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_DL_BW[::n], label='CC1_DL_BW', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_DL_BW[::n], label='CC2_DL_BW', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_DL_BW[::n], label='CC3_DL_BW', color='cyan', linestyle='-', alpha=0.6)
        plt.grid()
        plt.ylim([0, 105])
        plt.ylabel('LTE BW [RB#]')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(5,1,4)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_PCI[::n], label='CC0_PCI', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_PCI[::n], label='CC1_PCI', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_PCI[::n], label='CC2_PCI', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_PCI[::n], label='CC3_PCI', color='cyan', linestyle='-', alpha=0.6)
        plt.grid()
        plt.ylabel('PCI')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(5,1,5)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_EARFCN[::n], label='CC0_EARFCN', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_EARFCN[::n], label='CC1_EARFCN', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_EARFCN[::n], label='CC2_EARFCN', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_EARFCN[::n], label='CC3_EARFCN', color='cyan', linestyle='-', alpha=0.6)
        plt.grid()
        plt.ylabel('EARFCN')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.xlabel('device time')
        #plt.show()
        fig.savefig('MtkFilter_fig01_LTE_Cell_Information.png')


    if len(EL1_STATUS_TIME)>0:
        fig=plt.figure(figsize=(13,9))
        #fig.suptitle('LTE_Radio_Condition', fontsize=16)
        if len(EL1_STATUS_TIME)>1000: n=len(EL1_STATUS_TIME)/1000
        else: n=1
        plt.subplot(3,1,1)
        cc0RSRP0=[sum(EL1_0_RSRP0)/len(EL1_0_RSRP0)]*len(EL1_STATUS_TIME)
        cc0RSRP1=[sum(EL1_0_RSRP1)/len(EL1_0_RSRP1)]*len(EL1_STATUS_TIME)
        cc1RSRP0=[sum(EL1_1_RSRP0)/len(EL1_1_RSRP0)]*len(EL1_STATUS_TIME)
        cc1RSRP1=[sum(EL1_1_RSRP1)/len(EL1_1_RSRP1)]*len(EL1_STATUS_TIME)
        cc2RSRP0=[sum(EL1_2_RSRP0)/len(EL1_2_RSRP0)]*len(EL1_STATUS_TIME)
        cc2RSRP1=[sum(EL1_2_RSRP1)/len(EL1_2_RSRP1)]*len(EL1_STATUS_TIME)
        cc3RSRP0=[sum(EL1_3_RSRP0)/len(EL1_3_RSRP0)]*len(EL1_STATUS_TIME)
        cc3RSRP1=[sum(EL1_3_RSRP1)/len(EL1_3_RSRP1)]*len(EL1_STATUS_TIME)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_RSRP0[::n], label='CC0_RSRP0 (Mean='+str(cc0RSRP0[0])+')', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_RSRP1[::n], label='CC0_RSRP1 (Mean='+str(cc0RSRP1[0])+')', color='red', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_RSRP0[::n], label='CC1_RSRP0 (Mean='+str(cc1RSRP0[0])+')', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_RSRP1[::n], label='CC1_RSRP1 (Mean='+str(cc1RSRP1[0])+')', color='blue', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_RSRP0[::n], label='CC2_RSRP0 (Mean='+str(cc2RSRP0[0])+')', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_RSRP1[::n], label='CC2_RSRP1 (Mean='+str(cc2RSRP1[0])+')', color='green', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_RSRP0[::n], label='CC3_RSRP0 (Mean='+str(cc3RSRP0[0])+')', color='cyan', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_RSRP1[::n], label='CC3_RSRP1 (Mean='+str(cc3RSRP1[0])+')', color='cyan', linestyle='--', alpha=0.3)
        plt.grid()
        plt.ylabel('LTE RSRP [dBm]')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(3,1,2)
        cc0SINR0=[sum(EL1_0_SINR0)/len(EL1_0_SINR0)]*len(EL1_STATUS_TIME)
        cc0SINR1=[sum(EL1_0_SINR1)/len(EL1_0_SINR1)]*len(EL1_STATUS_TIME)
        cc1SINR0=[sum(EL1_1_SINR0)/len(EL1_1_SINR0)]*len(EL1_STATUS_TIME)
        cc1SINR1=[sum(EL1_1_SINR1)/len(EL1_1_SINR1)]*len(EL1_STATUS_TIME)
        cc2SINR0=[sum(EL1_2_SINR0)/len(EL1_2_SINR0)]*len(EL1_STATUS_TIME)
        cc2SINR1=[sum(EL1_2_SINR1)/len(EL1_2_SINR1)]*len(EL1_STATUS_TIME)
        cc3SINR0=[sum(EL1_3_SINR0)/len(EL1_3_SINR0)]*len(EL1_STATUS_TIME)
        cc3SINR1=[sum(EL1_3_SINR1)/len(EL1_3_SINR1)]*len(EL1_STATUS_TIME)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_SINR0[::n], label='CC0_SINR0 (Mean='+str(cc0SINR0[0])+')', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_SINR1[::n], label='CC0_SINR1 (Mean='+str(cc0SINR1[0])+')', color='red', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_SINR0[::n], label='CC1_SINR0 (Mean='+str(cc1SINR0[0])+')', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_SINR1[::n], label='CC1_SINR1 (Mean='+str(cc1SINR1[0])+')', color='blue', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_SINR0[::n], label='CC2_SINR0 (Mean='+str(cc2SINR0[0])+')', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_SINR1[::n], label='CC2_SINR1 (Mean='+str(cc2SINR1[0])+')', color='green', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_SINR0[::n], label='CC3_SINR0 (Mean='+str(cc3SINR0[0])+')', color='cyan', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_SINR1[::n], label='CC3_SINR1 (Mean='+str(cc3SINR1[0])+')', color='cyan', linestyle='--', alpha=0.3)
        plt.grid()
        plt.ylabel('LTE SINR [dB]')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(3,1,3)
        cc0CQI0=[sum(EL1_0_CQI0)/len(EL1_0_CQI0)]*len(EL1_STATUS_TIME)
        cc0CQI1=[sum(EL1_0_CQI1)/len(EL1_0_CQI1)]*len(EL1_STATUS_TIME)
        cc1CQI0=[sum(EL1_1_CQI0)/len(EL1_1_CQI0)]*len(EL1_STATUS_TIME)
        cc1CQI1=[sum(EL1_1_CQI1)/len(EL1_1_CQI1)]*len(EL1_STATUS_TIME)
        cc2CQI0=[sum(EL1_2_CQI0)/len(EL1_2_CQI0)]*len(EL1_STATUS_TIME)
        cc2CQI1=[sum(EL1_2_CQI1)/len(EL1_2_CQI1)]*len(EL1_STATUS_TIME)
        cc3CQI0=[sum(EL1_3_CQI0)/len(EL1_3_CQI0)]*len(EL1_STATUS_TIME)
        cc3CQI1=[sum(EL1_3_CQI1)/len(EL1_3_CQI1)]*len(EL1_STATUS_TIME)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_CQI0[::n], label='CC0_CQI0 (Mean='+str(cc0CQI0[0])+')', color='red', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_CQI1[::n], label='CC0_CQI1 (Mean='+str(cc0CQI1[0])+')', color='red', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_CQI0[::n], label='CC1_CQI0 (Mean='+str(cc1CQI0[0])+')', color='blue', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_CQI1[::n], label='CC1_CQI1 (Mean='+str(cc1CQI1[0])+')', color='blue', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_CQI0[::n], label='CC2_CQI0 (Mean='+str(cc2CQI0[0])+')', color='green', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_CQI1[::n], label='CC2_CQI1 (Mean='+str(cc2CQI1[0])+')', color='green', linestyle='--', alpha=0.3)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_CQI0[::n], label='CC3_CQI0 (Mean='+str(cc3CQI0[0])+')', color='cyan', linestyle='-', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_CQI1[::n], label='CC3_CQI1 (Mean='+str(cc3CQI1[0])+')', color='cyan', linestyle='--', alpha=0.3)
        plt.grid()
        plt.ylabel('LTE CQI')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.xlabel('device time')
        fig.savefig('MtkFilter_fig02_LTE_Radio_Condition.png')


    if len(EL1_STATUS_TIME)>0:
    	fig=plt.figure(figsize=(13,7))
    	if len(EL1_STATUS_TIME)>1000: n=len(EL1_STATUS_TIME)/1000
    	else: n=1
    	plt.subplot(3,1,1)
    	avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
    	if np.count_nonzero(EL1_0_PCMAX)>0: avg0=sum(EL1_0_PCMAX)/np.count_nonzero(EL1_0_PCMAX)
    	if np.count_nonzero(EL1_1_PCMAX)>0: avg1=sum(EL1_1_PCMAX)/np.count_nonzero(EL1_1_PCMAX)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_PRACH_PWR[::n], label='CC0 PRACH Power', color='red', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_PUCCH_PWR[::n], label='CC0 PUCCH Power', color='blue', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_PUSCH_PWR[::n], label='CC0 PUSCH Power', color='green', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_SRS_PWR[::n], label='CC0 SRS Power', color='cyan', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_TOT_PWR[::n], label='CC0 Total Power (Pcmax='+str(avg0)+')', color='black', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_PRACH_PWR[::n], label='CC1 PRACH Power', color='red', linestyle='--', alpha=0.3)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_PUCCH_PWR[::n], label='CC1 PUCCH Power', color='blue', linestyle='--', alpha=0.3)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_PUSCH_PWR[::n], label='CC1 PUSCH Power', color='green', linestyle='--', alpha=0.3)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_SRS_PWR[::n], label='CC1 SRS Power', color='cyan', linestyle='--', alpha=0.3)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_TOT_PWR[::n], label='CC1 Total Power (Pcmax='+str(avg1)+')', color='black', linestyle='--', alpha=0.3)
    	plt.grid()
    	plt.ylabel('LTE Tx Power [dBm]')
    	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
    	plt.tight_layout()
    	plt.subplot(3,1,2)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_PHR[::n], label='CC0 PHR', color='red', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_PHR[::n], label='CC1 PHR', color='blue', linestyle='-', alpha=0.6)
    	plt.grid()
    	plt.ylabel('LTE PHR')
    	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
    	plt.tight_layout()
    	plt.subplot(3,1,3)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_0_RETX_RATE[::n], label='CC0 ReTx Rate', color='red', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], EL1_1_PHR[::n], label='CC1 ReTx Rate', color='blue', linestyle='-', alpha=0.6)
    	plt.grid()
    	plt.ylabel('LTE ReTx Rate%')
    	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
    	plt.tight_layout()
    	plt.xlabel('device time')
    	fig.savefig('MtkFilter_fig03_LTE_Tx_Power.png')


    if len(EL1_STATUS_TIME)>0:
        fig=plt.figure(figsize=(13,9))
        #fig.suptitle('LTE_DL_Information', fontsize=16)
        #plt.subplots(4,1,gridspec_kw={'height_ratios': [2,1,1,1]})
        if len(EL1_STATUS_TIME)>1000: n=len(EL1_STATUS_TIME)/1000
        else: n=1

        plt.subplot(4,1,1)
        EL1_0_DL_TPUT_BPS = [i*8/1000000 for i in EL1_0_DL_TPUT]
        EL1_1_DL_TPUT_BPS = [i*8/1000000 for i in EL1_1_DL_TPUT]
        EL1_2_DL_TPUT_BPS = [i*8/1000000 for i in EL1_2_DL_TPUT]
        EL1_3_DL_TPUT_BPS = [i*8/1000000 for i in EL1_3_DL_TPUT]
        EL1_DL_TPUT_BPS = np.add(np.add(np.add(EL1_0_DL_TPUT_BPS, EL1_1_DL_TPUT_BPS), EL1_2_DL_TPUT_BPS), EL1_3_DL_TPUT_BPS)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        if np.count_nonzero(EL1_DL_TPUT_BPS)>0: avg=sum(EL1_DL_TPUT_BPS)/np.count_nonzero(EL1_DL_TPUT_BPS)
        if np.count_nonzero(EL1_0_DL_TPUT_BPS)>0: avg0=sum(EL1_0_DL_TPUT_BPS)/np.count_nonzero(EL1_0_DL_TPUT_BPS)
        if np.count_nonzero(EL1_1_DL_TPUT_BPS)>0: avg1=sum(EL1_1_DL_TPUT_BPS)/np.count_nonzero(EL1_1_DL_TPUT_BPS)
        if np.count_nonzero(EL1_2_DL_TPUT_BPS)>0: avg2=sum(EL1_2_DL_TPUT_BPS)/np.count_nonzero(EL1_2_DL_TPUT_BPS)
        if np.count_nonzero(EL1_3_DL_TPUT_BPS)>0: avg3=sum(EL1_3_DL_TPUT_BPS)/np.count_nonzero(EL1_3_DL_TPUT_BPS)
        plt.plot(EL1_STATUS_TIME[::n], EL1_DL_TPUT_BPS[::n], label='LTE DL Agg Tput (Mean='+str(avg)+')', color='black', linestyle='-', alpha=0.9)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_DL_TPUT_BPS[::n], label='CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_DL_TPUT_BPS[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_DL_TPUT_BPS[::n], label='CC2 (Mean='+str(avg2)+')', color='green', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_DL_TPUT_BPS[::n], label='CC3 (Mean='+str(avg3)+')', color='cyan', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE DL Tput [Mbps]')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(4,1,2)
        #EL1_GRANT = np.add(np.add(np.add(EL1_0_GRANT, EL1_1_GRANT), EL1_2_GRANT), EL1_3_GRANT)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        #if np.count_nonzero(EL1_GRANT)>0: avg=sum(EL1_GRANT)/np.count_nonzero(EL1_GRANT)
        if np.count_nonzero(EL1_0_GRANT)>0: avg0=sum(EL1_0_GRANT)/np.count_nonzero(EL1_0_GRANT)
        if np.count_nonzero(EL1_1_GRANT)>0: avg1=sum(EL1_1_GRANT)/np.count_nonzero(EL1_1_GRANT)
        if np.count_nonzero(EL1_2_GRANT)>0: avg2=sum(EL1_2_GRANT)/np.count_nonzero(EL1_2_GRANT)
        if np.count_nonzero(EL1_3_GRANT)>0: avg3=sum(EL1_3_GRANT)/np.count_nonzero(EL1_3_GRANT)
        #plt.plot(EL1_STATUS_TIME[::n], EL1_GRANT[::n], label='DL Agg RB (Mean='+str(avg)+')', color='black', linestyle='-', alpha=0.9)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_GRANT[::n], label='RB CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_GRANT[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_GRANT[::n], label='CC2 (Mean='+str(avg2)+')', color='green', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_GRANT[::n], label='CC3 (Mean='+str(avg3)+')', color='cyan', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE DL RB#')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(4,1,3)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        if np.count_nonzero(EL1_0_MCS)>0: avg0=sum(EL1_0_MCS)/np.count_nonzero(EL1_0_MCS)
        if np.count_nonzero(EL1_1_MCS)>0: avg1=sum(EL1_1_MCS)/np.count_nonzero(EL1_1_MCS)
        if np.count_nonzero(EL1_2_MCS)>0: avg2=sum(EL1_2_MCS)/np.count_nonzero(EL1_2_MCS)
        if np.count_nonzero(EL1_3_MCS)>0: avg3=sum(EL1_3_MCS)/np.count_nonzero(EL1_3_MCS)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_MCS[::n], label='MCS CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_MCS[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_MCS[::n], label='CC2 (Mean='+str(avg2)+')', color='green', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_MCS[::n], label='CC3 (Mean='+str(avg3)+')', color='cyan', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE DL MCS')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(4,1,4)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        if np.count_nonzero(EL1_0_BLER)>0: avg0=sum(EL1_0_BLER)/np.count_nonzero(EL1_0_BLER)
        if np.count_nonzero(EL1_1_BLER)>0: avg1=sum(EL1_1_BLER)/np.count_nonzero(EL1_1_BLER)
        if np.count_nonzero(EL1_2_BLER)>0: avg2=sum(EL1_2_BLER)/np.count_nonzero(EL1_2_BLER)
        if np.count_nonzero(EL1_3_BLER)>0: avg3=sum(EL1_3_BLER)/np.count_nonzero(EL1_3_BLER)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_BLER[::n], label='BLER CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_BLER[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_2_BLER[::n], label='CC2 (Mean='+str(avg2)+')', color='green', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_3_BLER[::n], label='CC3 (Mean='+str(avg3)+')', color='cyan', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE DL BLER%')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.xlabel('device time')
        fig.savefig('MtkFilter_fig04_LTE_DL_Information.png')

    if len(LTE_MAC_TPUT_TIME)>0:
    	fig=plt.figure(figsize=(13,7))
    	n=1
    	EL1_0_DL_TPUT_BPS = [i*8/1000000 for i in EL1_0_DL_TPUT]
    	EL1_1_DL_TPUT_BPS = [i*8/1000000 for i in EL1_1_DL_TPUT]
    	EL1_2_DL_TPUT_BPS = [i*8/1000000 for i in EL1_2_DL_TPUT]
    	EL1_3_DL_TPUT_BPS = [i*8/1000000 for i in EL1_3_DL_TPUT]
    	EL1_DL_TPUT_BPS = np.add(np.add(np.add(EL1_0_DL_TPUT_BPS, EL1_1_DL_TPUT_BPS), EL1_2_DL_TPUT_BPS), EL1_3_DL_TPUT_BPS)
    	LTE_MAC_TPUT_MBPS = [i/1000000 for i in LTE_MAC_TPUT] #Mbps
    	LTE_RLC_TPUT_MBPS = [i/1000000 for i in LTE_RLC_TPUT] #Mbps
    	LTE_PDCP_TPUT_MBPS = [i/1000000 for i in LTE_PDCP_TPUT] #Mbps
    	LTE_IP_TPUT_MBPS = [i/1000000 for i in LTE_IP_TPUT] #Mbps
    	avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
    	mean, mean0, mean1, mean2, mean3 = [],[],[],[],[]
    	if np.count_nonzero(EL1_DL_TPUT_BPS)>0: mean=[sum(EL1_DL_TPUT_BPS)/np.count_nonzero(EL1_DL_TPUT_BPS)]*len(EL1_STATUS_TIME) 
    	else: mean=[0]*len(EL1_STATUS_TIME)
    	if np.count_nonzero(LTE_MAC_TPUT_MBPS)>0: mean0=[sum(LTE_MAC_TPUT_MBPS)/np.count_nonzero(LTE_MAC_TPUT_MBPS)]*len(LTE_MAC_TPUT_TIME) 
    	else: mean0=[0]*len(LTE_MAC_TPUT_TIME)
    	if np.count_nonzero(LTE_RLC_TPUT_MBPS)>0: mean1=[sum(LTE_RLC_TPUT_MBPS)/np.count_nonzero(LTE_RLC_TPUT_MBPS)]*len(LTE_RLC_TPUT_TIME) 
    	else: mean1=[0]*len(LTE_RLC_TPUT_TIME)
    	if np.count_nonzero(LTE_PDCP_TPUT_MBPS)>0: mean2=[sum(LTE_PDCP_TPUT_MBPS)/np.count_nonzero(LTE_PDCP_TPUT_MBPS)]*len(LTE_PDCP_TPUT_TIME) 
    	else: mean2=[0]*len(LTE_PDCP_TPUT_TIME)
    	if np.count_nonzero(LTE_IP_TPUT_MBPS)>0: mean3=[sum(LTE_IP_TPUT_MBPS)/np.count_nonzero(LTE_IP_TPUT_MBPS)]*len(LTE_IP_TPUT_TIME) 
    	else: mean3=[0]*len(LTE_IP_TPUT_TIME)
    	if len(EL1_STATUS_TIME)>0: plt.plot(EL1_STATUS_TIME[::n], EL1_DL_TPUT_BPS[::n], label='LTE PDSCH Tput (Mean='+str(mean[0])+')', color='red', linestyle='-', alpha=0.6)
    	if len(LTE_MAC_TPUT_TIME)>0: plt.plot(LTE_MAC_TPUT_TIME[::n], LTE_MAC_TPUT_MBPS[::n], label='LTE MAC Tput (Mean='+str(mean0[0])+')', color='blue', linestyle='-', alpha=0.6)
    	if len(LTE_RLC_TPUT_TIME)>0: plt.plot(LTE_RLC_TPUT_TIME[::n], LTE_RLC_TPUT_MBPS[::n], label='LTE RLC Tput (Mean='+str(mean1[0])+')', color='green', linestyle='-', alpha=0.6)
    	if len(LTE_PDCP_TPUT_TIME)>0: plt.plot(LTE_PDCP_TPUT_TIME[::n], LTE_PDCP_TPUT_MBPS[::n], label='LTE PDCP Tput (Mean='+str(mean2[0])+')', color='cyan', linestyle='-', alpha=0.6)
    	if len(LTE_IP_TPUT_TIME)>0: plt.plot(LTE_IP_TPUT_TIME[::n], LTE_IP_TPUT_MBPS[::n], label='LTE IP Tput (Mean='+str(mean3[0])+')', color='black', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], mean[::n], label='PDSCH Mean='+str(mean[0]), color='red', linestyle='--', alpha=0.2)
    	plt.plot(LTE_MAC_TPUT_TIME[::n], mean0[::n], label='MAC Mean='+str(mean0[0]), color='blue', linestyle='--', alpha=0.2)
    	plt.plot(LTE_RLC_TPUT_TIME[::n], mean1[::n], label='RLC Mean='+str(mean1[0]), color='green', linestyle='--', alpha=0.2)
    	plt.plot(LTE_PDCP_TPUT_TIME[::n], mean2[::n], label='PDCP Mean='+str(mean2[0]), color='cyan', linestyle='--', alpha=0.2)
    	plt.plot(LTE_IP_TPUT_TIME[::n], mean3[::n], label='IP Mean='+str(mean3[0]), color='black', linestyle='--', alpha=0.2)
    	plt.grid()
    	plt.ylabel('LTE DL Tput [Mbps]')
    	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="small", edgecolor="white")
    	plt.tight_layout()
    	plt.xlabel('device time')
    	fig.savefig('MtkFilter_fig05_LTE_Throughput_DL.png')


    if len(EL1_STATUS_TIME)>0:
        fig=plt.figure(figsize=(13,9))
        #fig.suptitle('LTE_UL_Information', fontsize=16)
        if len(EL1_STATUS_TIME)>1000: n=len(EL1_STATUS_TIME)/1000
        else: n=1

        plt.subplot(4,1,1)
        EL1_0_UL_TPUT_BPS = [i*8/1000000 for i in EL1_0_UL_TPUT]
        EL1_1_UL_TPUT_BPS = [i*8/1000000 for i in EL1_1_UL_TPUT]
        EL1_UL_TPUT_BPS = np.add(EL1_0_UL_TPUT_BPS, EL1_1_UL_TPUT_BPS)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        if np.count_nonzero(EL1_UL_TPUT_BPS)>0: avg=sum(EL1_UL_TPUT_BPS)/np.count_nonzero(EL1_UL_TPUT_BPS)
        if np.count_nonzero(EL1_0_UL_TPUT_BPS)>0: avg0=sum(EL1_0_UL_TPUT_BPS)/np.count_nonzero(EL1_0_UL_TPUT_BPS)
        if np.count_nonzero(EL1_1_UL_TPUT_BPS)>0: avg1=sum(EL1_1_UL_TPUT_BPS)/np.count_nonzero(EL1_1_UL_TPUT_BPS)
        plt.plot(EL1_STATUS_TIME[::n], EL1_UL_TPUT_BPS[::n], label='LTE UL Agg Tput (Mean='+str(avg)+')', color='black', linestyle='-', alpha=0.9)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_UL_TPUT_BPS[::n], label='CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_UL_TPUT_BPS[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE UL Tput [Mbps]')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(4,1,2)
        #EL1_ULRB = np.add(EL1_0_ULRB, EL1_1_ULRB)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        #if np.count_nonzero(EL1_ULRB)>0: avg=sum(EL1_ULRB)/np.count_nonzero(EL1_ULRB)
        if np.count_nonzero(EL1_0_ULRB)>0: avg0=sum(EL1_0_ULRB)/np.count_nonzero(EL1_0_ULRB)
        if np.count_nonzero(EL1_1_ULRB)>0: avg1=sum(EL1_1_ULRB)/np.count_nonzero(EL1_1_ULRB)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_ULRB[::n], label='RB CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_ULRB[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE UL RB#')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(4,1,3)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        if np.count_nonzero(EL1_0_ULMCS)>0: avg0=sum(EL1_0_ULMCS)/np.count_nonzero(EL1_0_ULMCS)
        if np.count_nonzero(EL1_1_ULMCS)>0: avg1=sum(EL1_1_ULMCS)/np.count_nonzero(EL1_1_ULMCS)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_ULMCS[::n], label='MCS CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_ULMCS[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE UL MCS')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.subplot(4,1,4)
        avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
        if np.count_nonzero(EL1_0_ULBLER)>0: avg0=sum(EL1_0_ULBLER)/np.count_nonzero(EL1_0_ULBLER)
        if np.count_nonzero(EL1_1_ULBLER)>0: avg1=sum(EL1_1_ULBLER)/np.count_nonzero(EL1_1_ULBLER)
        plt.plot(EL1_STATUS_TIME[::n], EL1_0_ULBLER[::n], label='BLER CC0 (Mean='+str(avg0)+')', color='red', linestyle='--', alpha=0.6)
        plt.plot(EL1_STATUS_TIME[::n], EL1_1_ULBLER[::n], label='CC1 (Mean='+str(avg1)+')', color='blue', linestyle='--', alpha=0.6)
        plt.grid()
        plt.ylabel('LTE UL BLER%')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
        plt.tight_layout()

        plt.xlabel('device time')
        fig.savefig('MtkFilter_fig06_LTE_UL_Information.png')

    if len(LTE_UL_MAC_TPUT_TIME)>0:
    	fig=plt.figure(figsize=(13,7))
    	n=1
    	EL1_0_UL_TPUT_BPS = [i*8/1000000 for i in EL1_0_UL_TPUT]
    	EL1_1_UL_TPUT_BPS = [i*8/1000000 for i in EL1_1_UL_TPUT]
    	EL1_UL_TPUT_BPS = np.add(EL1_0_UL_TPUT_BPS, EL1_1_UL_TPUT_BPS)
    	LTE_UL_MAC_TPUT_MBPS = [i/1000000 for i in LTE_UL_MAC_TPUT] #Mbps
    	LTE_UL_RLC_TPUT_MBPS = [i/1000000 for i in LTE_UL_RLC_TPUT] #Mbps
    	LTE_UL_PDCP_TPUT_MBPS = [i/1000000 for i in LTE_UL_PDCP_TPUT] #Mbps
    	LTE_UL_IP_TPUT_MBPS = [i/1000000 for i in LTE_UL_IP_TPUT] #Mbps
    	avg, avg0, avg1, avg2, avg3 = 0,0,0,0,0
    	mean, mean0, mean1, mean2, mean3 = [],[],[],[],[]
    	if np.count_nonzero(EL1_UL_TPUT_BPS)>0: mean=[sum(EL1_UL_TPUT_BPS)/np.count_nonzero(EL1_UL_TPUT_BPS)]*len(EL1_STATUS_TIME)
    	else: mean=[0]*len(EL1_STATUS_TIME)
    	if np.count_nonzero(LTE_UL_MAC_TPUT_MBPS)>0: mean0=[sum(LTE_UL_MAC_TPUT_MBPS)/np.count_nonzero(LTE_UL_MAC_TPUT_MBPS)]*len(LTE_UL_MAC_TPUT_TIME)
    	else: mean0=[0]*len(LTE_UL_MAC_TPUT_TIME)
    	if np.count_nonzero(LTE_UL_RLC_TPUT_MBPS)>0: mean1=[sum(LTE_UL_RLC_TPUT_MBPS)/np.count_nonzero(LTE_UL_RLC_TPUT_MBPS)]*len(LTE_UL_RLC_TPUT_TIME)
    	else: mean1=[0]*len(LTE_UL_RLC_TPUT_TIME)
    	if np.count_nonzero(LTE_UL_PDCP_TPUT_MBPS)>0: mean2=[sum(LTE_UL_PDCP_TPUT_MBPS)/np.count_nonzero(LTE_UL_PDCP_TPUT_MBPS)]*len(LTE_UL_PDCP_TPUT_TIME)
    	else: mean2=[0]*len(LTE_UL_PDCP_TPUT_TIME)
    	if np.count_nonzero(LTE_UL_IP_TPUT_MBPS)>0: mean3=[sum(LTE_UL_IP_TPUT_MBPS)/np.count_nonzero(LTE_UL_IP_TPUT_MBPS)]*len(LTE_UL_IP_TPUT_TIME)
    	else: mean3=[0]*len(LTE_UL_IP_TPUT_TIME)
    	if len(EL1_STATUS_TIME)>0: plt.plot(EL1_STATUS_TIME[::n], EL1_UL_TPUT_BPS[::n], label='LTE PUSCH Tput (Mean='+str(mean[0])+')', color='red', linestyle='-', alpha=0.6)
    	if len(LTE_UL_MAC_TPUT_TIME)>0: plt.plot(LTE_UL_MAC_TPUT_TIME[::n], LTE_UL_MAC_TPUT_MBPS[::n], label='LTE MAC Tput (Mean='+str(mean0[0])+')', color='blue', linestyle='-', alpha=0.6)
    	if len(LTE_UL_RLC_TPUT_TIME)>0: plt.plot(LTE_UL_RLC_TPUT_TIME[::n], LTE_UL_RLC_TPUT_MBPS[::n], label='LTE RLC Tput (Mean='+str(mean1[0])+')', color='green', linestyle='-', alpha=0.6)
    	if len(LTE_UL_PDCP_TPUT_TIME)>0: plt.plot(LTE_UL_PDCP_TPUT_TIME[::n], LTE_UL_PDCP_TPUT_MBPS[::n], label='LTE PDCP Tput (Mean='+str(mean2[0])+')', color='cyan', linestyle='-', alpha=0.6)
    	if len(LTE_UL_IP_TPUT_TIME)>0: plt.plot(LTE_UL_IP_TPUT_TIME[::n], LTE_UL_IP_TPUT_MBPS[::n], label='LTE IP Tput (Mean='+str(mean3[0])+')', color='black', linestyle='-', alpha=0.6)
    	plt.plot(EL1_STATUS_TIME[::n], mean[::n], label='PUSCH Mean='+str(mean[0]), color='red', linestyle='--', alpha=0.2)
    	plt.plot(LTE_UL_MAC_TPUT_TIME[::n], mean0[::n], label='MAC Mean='+str(mean0[0]), color='blue', linestyle='--', alpha=0.2)
    	plt.plot(LTE_UL_RLC_TPUT_TIME[::n], mean1[::n], label='RLC Mean='+str(mean1[0]), color='green', linestyle='--', alpha=0.2)
    	plt.plot(LTE_UL_PDCP_TPUT_TIME[::n], mean2[::n], label='PDCP Mean='+str(mean2[0]), color='cyan', linestyle='--', alpha=0.2)
    	plt.plot(LTE_UL_IP_TPUT_TIME[::n], mean3[::n], label='IP Mean='+str(mean3[0]), color='black', linestyle='--', alpha=0.2)
    	plt.grid()
    	plt.ylabel('LTE UL Tput [Mbps]')
    	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="small", edgecolor="white")
    	plt.tight_layout()
    	plt.xlabel('device time')
    	fig.savefig('MtkFilter_fig07_LTE_Throughput_UL.png')


	#NR
    if len(NR_MEAS_TIME)>0 or len(NR_DCI_TIME)>0 or len(NR_PDSCH_TPUT_TIME)>0 :
        fig=plt.figure(figsize=(13,9))
        fig.suptitle('NR Downlink Analysis', fontsize=16)
        if len(NR_MEAS_TIME)>0:
            plt.subplot(6,1,1)
            if len(NR_MEAS_TIME)>100: n=len(NR_MEAS_TIME)/100
            else: n=1
            rsrp0=[sum(NR_RSRP0)/len(NR_RSRP0)]*len(NR_MEAS_TIME)
            rsrp1=[sum(NR_RSRP1)/len(NR_RSRP1)]*len(NR_MEAS_TIME)
            plt.plot(NR_MEAS_TIME[::n], NR_RSRP0[::n], label='RSRP0 (Mean='+str(rsrp0[0])+')')
            plt.plot(NR_MEAS_TIME[::n], NR_RSRP1[::n], label='RSRP1 (Mean='+str(rsrp1[0])+')', alpha=0.5)
            #plt.plot(NR_MEAS_TIME[::n], rsrp0[::n], label='RSRP0 Mean='+str(rsrp0[0]), linestyle='--')
            #plt.plot(NR_MEAS_TIME[::n], rsrp1[::n], label='RSRP1 Mean='+str(rsrp1[0]), linestyle='--')
            plt.legend()
            plt.subplot(6,1,2)
            rsrq0=[sum(NR_RSRQ0)/len(NR_RSRQ0)]*len(NR_MEAS_TIME)
            rsrq1=[sum(NR_RSRQ1)/len(NR_RSRQ1)]*len(NR_MEAS_TIME)
            plt.plot(NR_MEAS_TIME[::n], NR_RSRQ0[::n], label='RSRQ0 (Mean='+str(rsrq0[0])+')')
            plt.plot(NR_MEAS_TIME[::n], NR_RSRQ1[::n], label='RSRQ1 (Mean='+str(rsrq1[0])+')', alpha=0.5)
            #plt.plot(NR_MEAS_TIME[::n], rsrq0[::n], label='RSRQ0 Mean='+str(rsrq0[0]), linestyle='--')
            #plt.plot(NR_MEAS_TIME[::n], rsrq1[::n], label='RSRQ1 Mean='+str(rsrq1[0]), linestyle='--')
            plt.legend()
            plt.subplot(6,1,3)
            sinr0=[sum(NR_SINR0)/len(NR_SINR0)]*len(NR_MEAS_TIME)
            sinr1=[sum(NR_SINR1)/len(NR_SINR1)]*len(NR_MEAS_TIME)
            plt.plot(NR_MEAS_TIME[::n], NR_SINR0[::n], label='SINR0 (Mean='+str(sinr0[0])+')')
            plt.plot(NR_MEAS_TIME[::n], NR_SINR1[::n], label='SINR1 (Mean='+str(sinr1[0])+')', alpha=0.5)
            #plt.plot(NR_MEAS_TIME[::n], sinr0[::n], label='SINR0 Mean='+str(sinr0[0]), linestyle='--')
            #plt.plot(NR_MEAS_TIME[::n], sinr1[::n], label='SINR1 Mean='+str(sinr1[0]), linestyle='--')
            plt.legend()
        if len(NR_DCI_TIME)>0:
            plt.subplot(6,1,4)
            if len(NR_DCI_TIME)>100: n=len(NR_DCI_TIME)/100
            else: n=1
            mcs1=[sum(NR_DL_MCS1)/len(NR_DL_MCS1)]*len(NR_DCI_TIME)
            mcs2=[sum(NR_DL_MCS2)/len(NR_DL_MCS2)]*len(NR_DCI_TIME)
            plt.plot(NR_DCI_TIME[::n], NR_DL_MCS1[::n], label='MCS1 (Mean='+str(mcs1[0])+')')
            plt.plot(NR_DCI_TIME[::n], NR_DL_MCS2[::n], label='MCS2 (Mean='+str(mcs2[0])+')', alpha=0.5)
            #plt.plot(NR_DCI_TIME[::n], mcs1[::n], label='MCS1 Mean='+str(mcs1[0]), linestyle='--')
            #plt.plot(NR_DCI_TIME[::n], mcs2[::n], label='MCS2 Mean='+str(mcs2[0]), linestyle='--')
            plt.legend()
            plt.subplot(6,1,5)
            rb=[sum(NR_DL_RB)/len(NR_DL_RB)]*len(NR_DCI_TIME)
            plt.plot(NR_DCI_TIME[::n], NR_DL_RB[::n], label='RB (Mean='+str(rb[0])+')')
            #plt.plot(NR_DCI_TIME[::n], rb[::n], label='RB Mean='+str(rb[0]), linestyle='--')
            plt.legend()
        if len(NR_PDSCH_TPUT_TIME)>0:
            plt.subplot(6,1,6)
            if len(NR_PDSCH_TPUT_TIME)>100: n=len(NR_PDSCH_TPUT_TIME)/100
            else: n=1
            tput0=[sum(NR_PDSCH_TPUT0)/len(NR_PDSCH_TPUT0)]*len(NR_PDSCH_TPUT_TIME)
            tput1=[sum(NR_PDSCH_TPUT1)/len(NR_PDSCH_TPUT1)]*len(NR_PDSCH_TPUT_TIME)
            tput=[sum(NR_PDSCH_TPUT)/len(NR_PDSCH_TPUT)]*len(NR_PDSCH_TPUT_TIME)
            plt.plot(NR_PDSCH_TPUT_TIME[::n], NR_PDSCH_TPUT[::n], label='TPUT (Mean='+str(tput[0])+')')
            plt.plot(NR_PDSCH_TPUT_TIME[::n], NR_PDSCH_TPUT0[::n], label='TPUT (Mean='+str(tput0[0])+')', alpha=0.5)
            plt.plot(NR_PDSCH_TPUT_TIME[::n], NR_PDSCH_TPUT1[::n], label='TPUT1 (Mean='+str(tput1[0])+')', alpha=0.5)
            #plt.plot(NR_PDSCH_TPUT_TIME[::n], tput[::n], label='TPUT Mean='+str(tput[0]), linestyle='--')
            #plt.plot(NR_PDSCH_TPUT_TIME[::n], tput0[::n], label='TPUT0 Mean='+str(tput0[0]), linestyle='--')
            #plt.plot(NR_PDSCH_TPUT_TIME[::n], tput1[::n], label='TPUT1 Mean='+str(tput1[0]), linestyle='--')
            plt.legend()
            plt.xlabel('device time')
        #plt.show()
        fig.savefig('NR_DL_Analysis.png')
	#"""
	
    #plt.show()

    #raw_input("Finish. Press Enter to continue...")
    sys.exit("Finish.")
