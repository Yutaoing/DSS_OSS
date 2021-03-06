# coding=gbk
import csv
import os, time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QLineEdit, QComboBox,QPushButton
from PyQt5 import QtCore
from Initalize20180706 import *
from soap_all_commands_for_dsc import *
from file_transaction import *
from SendEmail import *
from file_update import *
from Ui_UPD_RMT_ROUTE import *
from Ui_ADD_NEW_REALM import *
from Ui_CONFIRM_WIN import *
from Ui_OPEN_ROUTE import *
from Ui_OP_ONLINE import *
from Ui_SECUIRTY_FILTER import *
from Selenium_login_rmt import *
from Ui_RMTCREDENTIAL import *
import os

from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys 
import time


if not os.path.exists('file'):
	os.mkdir('file')


#current_date=time.strftime("%d/%m/%Y")
current_date=time.strftime("%Y/%m/%d")
login_date_file=r'file\login_date.txt'
if not os.path.exists(login_date_file):
	output = open(login_date_file, 'w')
	output.write(current_date)
	output.close()
	INITIALIZE_DB()
	fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/DecideRoutePloicy.csv','DecideRoutePloicy.csv','.\\file')
	fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv','PeeringPolicy.csv','.\\file')
	fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/security_filter.csv','security_filter.csv','.\\file')

if os.path.exists(login_date_file):
	input=open(login_date_file)
	historical_date=input.read()
	if historical_date<current_date:
		print("initialize historical_date<current_date")
		output = open(login_date_file, 'w')
		output.write(current_date)
		output.close()
		print("outputfile updated")
		INITIALIZE_DB()
		fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/DecideRoutePloicy.csv','DecideRoutePloicy.csv','.\\file')
		fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv','PeeringPolicy.csv','.\\file')
		fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/security_filter.csv','security_filter.csv','.\\file')

if not os.path.exists(r'.\\file\DB.csv'):
	INITIALIZE_DB()
	fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/DecideRoutePloicy.csv','DecideRoutePloicy.csv','.\\file')
	fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/PeeringPolicy.csv','PeeringPolicy.csv','.\\file')
	fileUpdate('http://central.syniverse.com/sites/TECH/io/ipxop/ts/Shared%20Documents/DSS/Tools/file/security_filter.csv','security_filter.csv','.\\file')

def string2list(input_str):
	output_list=[]
	input_str = input_str.lower()
	input_str = input_str.replace(",",";")
	input_str= input_str.replace("\r\n",";")
	input_str = input_str.replace('\n',';')
	if input_str[-1]==';':
		input_str[:-1]
	if input_str[0]==';':
		input_str[1:]
	output_list=SPLIT2LIST(input_str)
	return output_list


def replace_invalid_letter(str):
	invalidlist=". ;:,'`~>>{}[]\|&"
	invalidlist=invalidlist+'"'
	for i in range(len(invalidlist)):
		str=str.replace(invalidlist[i],'_')
	return(str)
	
PEERINGPOLICY=csv2dict('.\\file\PeeringPolicy.csv')
DECIDEROUTEPOLICY=csv2dict('.\\file\DecideRoutePloicy.csv')
#the following 2 variant is used in sync OPA OPB from Open Route to OP ONLINE

global OPAAA
OPAAA=''
global rmt_flag
rmt_flag=-1
global driver
global OPBBB
OPBBB=''
global List_Add_Route_Local
List_Add_Route_Local=[]
RULE_TYPE=['DECIDE_ROUTE','PRE_FORWARD_CONFIGURE','POST_FORWARD_CONFIGURE','BACKWARD_CONFIGURE','REQUEST_FILTER','ANSWER_FILTER','PRE_FORWARD_FORMAT','POST_FORWARD_FORMAT','PRE_BACKWARD_FORMAT','POST_BACKWARD_FORMAT','PRE_FORWARD_TRANSLATE','POST_FORWARD_TRANSLATE','PRE_BACKWARD_TRANSLATE','POST_BACKWARD_TRANSLATE']
EmailTitleHeader='DSS PROVISION RECORD: '

ROUTE_STATUS_LIST=['Agreed','Elected','Electing','Rejecting','Rejected','Provisioned']

def refresh_all():
	INITIALIZE_DB()
	PEERINGPOLICY=csv2dict('.\\file\PeeringPolicy.csv')
	DECIDEROUTEPOLICY=csv2dict('.\\file\DecideRoutePloicy.csv')
	DB_sheet = csv2dict(".\\file\DB.csv")

def NEW_EMAIL2PEER(SCENARIO,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
	for row in PEERINGPOLICY:
		if row['SCENARIO']==SCENARIO:
			SVR_PEER=row['SVR_PEER']
			HUB_PEER=row['HUB_PEER']
			SVR_NODE=row['SVR_NODE']
			HUB_NODE=row['HUB_NODE']
			Tolist=row['EMAIL']
	Subject='New Election Request: '+OP_A+' - '+OP_B
	email_body='''<html><body>
	
		<p style='font-family:Arial;font-size:13;color:black'>
		Dear Colleagues,<br/><br/>
		Greeting from Syniverse!<br/>
		We received a request to establish LTE roaming relationship between OP_A and OP_B.<br/><br/>
		Please let us know if you are interested in open this route via Syniverse.<br/><br/>
		<strong><font color="#0066CC">OP_A<br/></font></strong>
		<Strong>Realm         :</Strong>REALM_A<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_A<br><br/>
		<strong><font color="#0066CC">OP_B<br/></font></strong>
		<strong>Realm         :</Strong>REALM_B<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_B<br/><br/> 
		<strong>Peering Point :</Strong><Strong><font color="green">SVR_PEER<==>HUB_PEER</font></Strong><br/><br/>
		<strong>Syniverse Node:</Strong>SVR_NODE<br/><br/>
		<strong>Peering   Node:</Strong>HUB_NODE<br/><br/>
		B.R.<br/><br/>
		<Strong>Syniverse DSS Team<br/></Strong>
		</p>
		</body></html>'''
	email_body=email_body.replace('OP_A',OP_A)
	email_body=email_body.replace('OP_B',OP_B)
	email_body=email_body.replace('REALM_A',REALM_A)
	email_body=email_body.replace('REALM_B',REALM_B)
	email_body=email_body.replace('IMSI_A',IMSI_A)
	email_body=email_body.replace('IMSI_B',IMSI_B)
	email_body=email_body.replace('SVR_PEER',SVR_PEER)
	email_body=email_body.replace('HUB_PEER',HUB_PEER)
	email_body=email_body.replace('SVR_NODE',SVR_NODE)
	email_body=email_body.replace('HUB_NODE',HUB_NODE)
	sendemail(Tolist,'DSS_Route_Provision@syniverse.com',Subject,email_body)

def PROVISIONED_EMAIL2PEER(SCENARIO,OP_A,REALM_A,IMSI_A,OP_B,REALM_B,IMSI_B):
	for row in PEERINGPOLICY:
		if row['SCENARIO']==SCENARIO:
			SVR_PEER=row['SVR_PEER']
			HUB_PEER=row['HUB_PEER']
			SVR_NODE=row['SVR_NODE']
			HUB_NODE=row['HUB_NODE']
			Tolist=row['EMAIL']
	Subject='Provision complete announcement: '+OP_A+' - '+OP_B
	email_body='''<html><body>
	
		<p style='font-family:Arial;font-size:13;color:black'>
		Dear Colleagues,<br/><br/>
		Greeting from Syniverse!<br/><br/>
		Kindly be informed that we have provisioned the LTE route between OP_A and OP_B<br/><br/>
		<strong><font color="#0066CC">OP_A<br/></font></strong>
		<Strong>Realm         :</Strong>REALM_A<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_A<br><br/>
		<strong><font color="#0066CC">OP_B<br/></font></strong>
		<strong>Realm         :</Strong>REALM_B<br/>
		<strong>IMSI Prefix   :</Strong>IMSI_B<br/><br/> 
		<strong>Peering Point :</Strong><Strong><font color="green">SVR_PEER<==>HUB_PEER</font></Strong><br/><br/>
		<strong>Syniverse Node:</Strong>SVR_NODE<br/><br/>
		<strong>Peering   Node:</Strong>HUB_NODE<br/><br/>
		B.R.<br/><br/>
		<Strong>Syniverse DSS Team<br/></Strong>
		</p>
		</body></html>'''
	email_body=email_body.replace('OP_A',OP_A)
	email_body=email_body.replace('OP_B',OP_B)
	email_body=email_body.replace('REALM_A',REALM_A)
	email_body=email_body.replace('REALM_B',REALM_B)
	email_body=email_body.replace('IMSI_A',IMSI_A)
	email_body=email_body.replace('IMSI_B',IMSI_B)
	email_body=email_body.replace('SVR_PEER',SVR_PEER)
	email_body=email_body.replace('HUB_PEER',HUB_PEER)
	email_body=email_body.replace('SVR_NODE',SVR_NODE)
	email_body=email_body.replace('HUB_NODE',HUB_NODE)
	sendemail(Tolist,'DSS_Route_Provision@syniverse.com',Subject,email_body)
	
def MERGE_SUCCESS(BODY):
	content=[]
	result=''
	lines=BODY.split('\n')
	for line in lines:
		if 'success' in line.lower():
			content.append(line+'\n')
	for row in content:
		result=result+row
	return(result)

def ONLINE_EMAIL(OP,BODY):
	Tolist='DSS_Route_Provision@syniverse.com'
	Subject='New OP online on DSC completed : '+OP
	email_body=MERGE_SUCCESS(BODY)			
	sende_plain_mail(Tolist,'',Subject,email_body)

	
def BACKUP_DB():
	file_list=['DB.csv','AMS_LISTCACHE.csv','FRT_LISTCACHE.csv','CHI_LISTCACHE.csv','DAL_LISTCACHE.csv','HKG_LISTCACHE.csv','SNG_LISTCACHE.csv']
	for file in file_list:
		#BackupFile ('hello_world.py','.\\', '.\\backup')
		BackupFile(file,'.\\file\\', '.\\backup')
	
#Read DB from CSV file and initialize variable
def csv2dict(filename):
	new_dict = {}
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		fieldnames = next(reader)
		reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
		new_dict = [row for row in reader]
	return new_dict

DB_sheet = csv2dict(".\\file\DB.csv")

Engineer_set= set()
for row in DB_sheet:
	if row['owner'] not in Engineer_set and row['owner']!='':
		Engineer_set.add(row['owner'])

def realm_to_op_name(realm):
	op_name="n/a"
	for row in DB_sheet:
		if realm.lower() in row['realm_name']:
			op_name=row['name']
			return(op_name)

DRAlist=['HKG','AMS','CHI','SNG','FRT','DAL']
RegionList=['AP','EU','NA']
Local_DSC_List=[]
global SURL1,SURL2,DSC1,DSC2
#This function split strings seperates by ; or , to a LIST and strip spaces in each string
def SPLIT2LIST(items):
	LIST=[]
	items = items.lower()
	items = items.replace(",",";")
	temp =  items.split(";")
	for item in temp:
		LIST.append(item.strip())
	return(LIST)
	
def JOIN_STR(current,new,symble):
	if current=='' and new=='':
		return('')
	if current=='' and new!='':
		return(new)
	if current!='' and new=='':
		return(current)

	string=current+symble+new
	return(string)
	


	


#根据region设置全局共享变量SURL1,SURL2,DSC1,DSC2
def Region2URL_DSC(Region):
		global SURL1,SURL2,DSC1,DSC2,POP
		if Region =="AP":
			SURL1="http://10.162.28.186:8080/DSC_SOAP/query?"
			SURL2="http://10.163.28.131:8080/DSC_SOAP/query?"
			DSC1="HKG"
			DSC2="SNG"
			POP="AP PoP"
		if Region =="EU":
			SURL1="http://10.160.28.32:8080/DSC_SOAP/query?"
			SURL2="http://10.161.28.32:8080/DSC_SOAP/query?"
			DSC1="AMS"
			DSC2="FRT"
			POP="EU PoP"		
		if Region =="NA":
			SURL1="http://10.166.28.200:8080/DSC_SOAP/query?"
			SURL2="http://10.164.28.189:8080/DSC_SOAP/query?"
			DSC1="CHI"
			DSC2="DAL"
			POP="NA PoP"
		if Region =="LAB":
			SURL1="http://10.166.20.125:8080/DSC_SOAP/query?"
			SURL2="http://10.166.20.125:8080/DSC_SOAP/query?"
			DSC1="LAB CHI"
			DSC2="Duplicate"
			POP="LAB PoP"
#DSC OUTPUT 弹窗代码

	
def MESSAGE_OUTPUT(Title,Output_Text):
	dialog=QDialog()
	dialog.resize(400,100)
	MSG = QLabel(Output_Text,dialog)
	MSG.move(50,20)

	dialog.setWindowTitle(Title)
	dialog.setWindowModality(Qt.ApplicationModal)
	dialog.exec_()
	
def BIOUTPUT(Title,Outputlist_1,Outputlist_2):
		dialog=QDialog()
		dialog.resize(1250,600)
		DSC_1 = QLabel(DSC1,dialog)
		DSC_1.move(50,20)
		DSC_2 = QLabel(DSC2,dialog)
		DSC_2.move(650,20)
	
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_1.move(50,50)
		OUTPUT_1.resize(550,500)
		
		OUTPUT_2 = QTextEdit(dialog)
		for row in Outputlist_2:
			OUTPUT_2.append(row)
		OUTPUT_2.move(650,50)
		OUTPUT_2.resize(550,500)

		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
def BIOUTPUT_UPDOWN(Title,Outputlist_1,Outputlist_2):
		dialog=QDialog()
		dialog.resize(1366,740)
		DSC_1 = QLabel(DSC1,dialog)
		DSC_1.move(50,15)
		DSC_2 = QLabel(DSC2,dialog)
		DSC_2.move(50,350)
	
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_1.move(50,30)
		OUTPUT_1.resize(1300,300)
		
		OUTPUT_2 = QTextEdit(dialog)
		for row in Outputlist_2:
			OUTPUT_2.append(row)
		OUTPUT_2.move(50,370)
		OUTPUT_2.resize(1300,300)

		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
def SIXOUTPUT(Title,DSC__1,DSC__2,DSC__3,DSC__4,DSC__5,DSC__6,Outputlist_1,Outputlist_2,Outputlist_3,Outputlist_4,Outputlist_5,Outputlist_6):
		dialog=QDialog()
		dialog.resize(1250,630)

		DSC_1 = QLabel(DSC__1,dialog)
		DSC_2 = QLabel(DSC__2,dialog)
		DSC_3 = QLabel(DSC__3,dialog)
		DSC_4 = QLabel(DSC__4,dialog)
		DSC_5 = QLabel(DSC__5,dialog)
		DSC_6 = QLabel(DSC__6,dialog)
		DSC_1.move(50,0)		
		DSC_2.move(650,0)
		DSC_3.move(50,200)		
		DSC_4.move(650,200)
		DSC_5.move(50,400)		
		DSC_6.move(650,400)
		
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_2 = QTextEdit(dialog)
		for row in Outputlist_2:
			OUTPUT_2.append(row)
		OUTPUT_3 = QTextEdit(dialog)
		for row in Outputlist_3:
			OUTPUT_3.append(row)
		OUTPUT_4 = QTextEdit(dialog)
		for row in Outputlist_4:
			OUTPUT_4.append(row)
		OUTPUT_5 = QTextEdit(dialog)
		for row in Outputlist_5:
			OUTPUT_5.append(row)
		OUTPUT_6 = QTextEdit(dialog)
		for row in Outputlist_6:
			OUTPUT_6.append(row)
			
		OUTPUT_1.move(50,20)
		OUTPUT_2.move(650,20)
		OUTPUT_3.move(50,220)
		OUTPUT_4.move(650,220)
		OUTPUT_5.move(50,420)
		OUTPUT_6.move(650,420)
		
		OUTPUT_1.resize(550,180)
		OUTPUT_2.resize(550,180)
		OUTPUT_3.resize(550,180)
		OUTPUT_4.resize(550,180)
		OUTPUT_5.resize(550,180)
		OUTPUT_6.resize(550,180)

		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
def SINGLE_OUTPUT(Title,Outputlist_1):
		dialog=QDialog()
		dialog.resize(1366,768)
		DSC_1 = QLabel(DSC1,dialog)
		DSC_1.move(50,20)
	
		OUTPUT_1 = QTextEdit(dialog)
		for row in Outputlist_1:
			OUTPUT_1.append(row)
		OUTPUT_1.move(50,50)
		OUTPUT_1.resize(1360,750)
		
		dialog.setWindowTitle(Title)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.exec_()
		
#DSC 组合命令功能执行代码
def Reload_Region_LIST(region):
	if region!='AP' and region!='EU' and region!='NA':
		MESSAGE_OUTPUT("Warning","Please select region")
		return()
	Region2URL_DSC(region)
	Outputlist_1=[]
	Outputlist_2=[]	
	Output1=soap_reload_listcaches(SURL1)
	Output2=soap_reload_listcaches(SURL2)
	Outputlist_1.append(Output1)
	Outputlist_2.append(Output2)
	BIOUTPUT("Reload ListCaches",Outputlist_1,Outputlist_2)
	result='Reload all list cache '+DSC1+':'+Output1+' '+DSC2+':'+Output2
	print('r'+result)
	return(result)

def Reload_Region_RULE(region):
	Region2URL_DSC(region)
	Outputlist_1=[]
	Outputlist_2=[]
	Output1=soap_reload_rule_engine(SURL1)
	Output2=soap_reload_rule_engine(SURL2)
	Outputlist_1.append(Output1)
	Outputlist_2.append(Output2)
	BIOUTPUT("Reload Rule Engine",Outputlist_1,Outputlist_2)
	
def CHECK_DECIDE_ROUTE2OP(region,source_realms,dest_realms):
	Region2URL_DSC(region)
	source_realm_list = []
	dest_realm_list = []
	source_realm_list.insert(0,'*')
	Outputlist_1=[]
	Outputlist_2=[]
	source_realm_list = SPLIT2LIST(source_realms)
	source_realm_list.insert(0,'*')
	dest_realm_list = SPLIT2LIST(dest_realms)
	
	for source_realm in source_realm_list:
		for dest_realm in dest_realm_list:
			print(source_realm+"---->"+dest_realm)
			
			Output1 = soap_check_decide_route(SURL1,'*',source_realm,'*',dest_realm,'*','*')
			for Output in Output1:
				Outputlist_1.append(DSC1+' '+source_realm+"->"+dest_realm)
				if Output==None:
					Output="None"
				Outputlist_1.append(Output)
				
			Output2 = soap_check_decide_route(SURL2,'*',source_realm,'*',dest_realm,'*','*')
			for Output in Output2:
				Outputlist_2.append(DSC2+' '+source_realm+"->"+dest_realm)
				if Output==None:
					Output="None"
				Outputlist_2.append(Output)
			#@将来写成HTML代码带颜色
	BIOUTPUT_UPDOWN("Check Decide Route:*->OP and Source->OP",Outputlist_1,Outputlist_2)
	
	
def CHECK_DECIDE_ROUTE2OP_ALL_REGION(source_realms,dest_realms):
	source_realm_list = []
	dest_realm_list = []
	source_realm_list = SPLIT2LIST(source_realms)
	if source_realms=='':
		source_realm_list = []
	source_realm_list.insert(0,'*')
	dest_realm_list = SPLIT2LIST(dest_realms)
	if dest_realms=='':
		dest_realm_list = []
	Outputlist_1=[]
	Outputlist_2=[]
	Outputlist_3=[]
	Outputlist_4=[]
	Outputlist_5=[]
	Outputlist_6=[]
	OUTPUT_LIST_LIST=[]
	DSC_LIST=[]
	
	Region2URL_DSC('AP')
	DSC__1=DSC1
	DSC__2=DSC2
	for source_realm in source_realm_list:
		for dest_realm in dest_realm_list:
			Output1 = soap_check_decide_route(SURL1,'*',source_realm,'*',dest_realm,'*','*')
			if Output1==None:
				Output1="None"
			for Output in Output1:
				Outputlist_1.append(source_realm+"->"+dest_realm)
				Outputlist_1.append(Output)

			Output2 = soap_check_decide_route(SURL2,'*',source_realm,'*',dest_realm,'*','*')
			if Output2==None:
				Output2="None"
			for Output in Output2:
				Outputlist_2.append(source_realm+"->"+dest_realm)
				Outputlist_2.append(Output)

	Region2URL_DSC('EU')
	DSC__3=DSC1
	DSC__4=DSC2
	for source_realm in source_realm_list:
		for dest_realm in dest_realm_list:
			Output1 = soap_check_decide_route(SURL1,'*',source_realm,'*',dest_realm,'*','*')
			if Output1==None:
				Output1="None"
			for Output in Output1:
				Outputlist_3.append(source_realm+"->"+dest_realm)
				Outputlist_3.append(Output)

			Output2 = soap_check_decide_route(SURL2,'*',source_realm,'*',dest_realm,'*','*')
			if Output2==None:
				Output2="None"
			for Output in Output2:
				Outputlist_4.append(source_realm+"->"+dest_realm)
				Outputlist_4.append(Output)
				
	Region2URL_DSC('NA')
	DSC__5=DSC1
	DSC__6=DSC2
	for source_realm in source_realm_list:
		for dest_realm in dest_realm_list:
			Output1 = soap_check_decide_route(SURL1,'*',source_realm,'*',dest_realm,'*','*')
			if Output1==None:
				Output1="None"
			for Output in Output1:
				Outputlist_5.append(source_realm+"->"+dest_realm)
				Outputlist_5.append(Output)

			Output2 = soap_check_decide_route(SURL2,'*',source_realm,'*',dest_realm,'*','*')
			if Output2==None:
				Output2="None"
			for Output in Output2:
				Outputlist_6.append(source_realm+"->"+dest_realm)
				Outputlist_6.append(Output)

	SIXOUTPUT("Decide Route Check Result",DSC__1,DSC__2,DSC__3,DSC__4,DSC__5,DSC__6,Outputlist_1,Outputlist_2,Outputlist_3,Outputlist_4,Outputlist_5,Outputlist_6)



def CHECK_DECIDE_ROUTE2OP_ALL_REGION_2(source_realms,dest_realms):
	dest_realm_list = []
	dest_realm_list = SPLIT2LIST(dest_realms)
	if dest_realms=='':
		dest_realm_list = []
	Outputlist_1=[]
	Outputlist_2=[]
	Outputlist_3=[]
	Outputlist_4=[]
	Outputlist_5=[]
	Outputlist_6=[]
	OUTPUT_LIST_LIST=[]
	DSC_LIST=[]
	
	Region2URL_DSC('AP')
	DSC__1=DSC1
	DSC__2=DSC2
	for dest_realm in dest_realm_list:
		Output1 = soap_check_decide_route_by_DR(SURL1,source_realms,dest_realm)
		if Output1==None:
			Output1="None"
		for Output in Output1:
			line=Output.split(" ")[1]
			if len(line)>10:
				Output=Output.replace(">","("+realm_to_op_name(line)+")>")
			Outputlist_1.append(Output)

		Output2 = soap_check_decide_route_by_DR(SURL1,source_realms,dest_realm)
		if Output2==None:
			Output2="None"
		for Output in Output2:
			line=Output.split(" ")[1]
			if len(line)>10:
				Output=Output.replace(">","("+realm_to_op_name(line)+")>")
			Outputlist_2.append(Output)

	Region2URL_DSC('EU')
	DSC__3=DSC1
	DSC__4=DSC2
	for dest_realm in dest_realm_list:
		Output1 = soap_check_decide_route_by_DR(SURL1,source_realms,dest_realm)
		if Output1==None:
			Output1="None"
		for Output in Output1:
			line=Output.split(" ")[1]
			if len(line)>10:
				Output=Output.replace(">","("+realm_to_op_name(line)+")>")
			Outputlist_3.append(Output)

		Output2 = soap_check_decide_route_by_DR(SURL1,source_realms,dest_realm)
		if Output2==None:
			Output2="None"
		for Output in Output2:
			line=Output.split(" ")[1]
			if len(line)>10:
				Output=Output.replace(">","("+realm_to_op_name(line)+")>")
			Outputlist_4.append(Output)
				
	Region2URL_DSC('NA')
	DSC__5=DSC1
	DSC__6=DSC2
	for dest_realm in dest_realm_list:
		Output1 = soap_check_decide_route_by_DR(SURL1,source_realms,dest_realm)
		if Output1==None:
			Output1="None"
		for Output in Output1:
			line=Output.split(" ")[1]
			if len(line)>10:
				Output=Output.replace(">","("+realm_to_op_name(line)+")>")
			Outputlist_5.append(Output)

		Output2 = soap_check_decide_route_by_DR(SURL1,source_realms,dest_realm)
		if Output2==None:
			Output2="None"
		for Output in Output2:
			line=Output.split(" ")[1]
			if len(line)>10:
				Output=Output.replace(">","("+realm_to_op_name(line)+")>")
			Outputlist_6.append(Output)

	SIXOUTPUT("Decide Route Check Result",DSC__1,DSC__2,DSC__3,DSC__4,DSC__5,DSC__6,Outputlist_1,Outputlist_2,Outputlist_3,Outputlist_4,Outputlist_5,Outputlist_6)
	
	
#add realms to list on regional DSCs and sent output to popup window
def ADD_REALMS2LIST(Region,Realms,LIST_Name):
	if Region=='':
		MESSAGE_OUTPUT("Error","Empty Region")
	elif Realms=='':
		MESSAGE_OUTPUT("Error","Empty Realm")
	elif LIST_Name=='':
		MESSAGE_OUTPUT("Error","Empty LIST")
	else:	
		Region2URL_DSC(Region)
		Outputlist_1=[]
		Outputlist_2=[]
		Realm_LIST=[]
		Realms = Realms.lower()
		Realms = Realms.replace(",",";")
		temp =  Realms.split(";")
		for realm in temp:
			Realm_LIST.append(realm.strip())
		
		for realm in Realm_LIST:
			response=soap_add_list_cache(LIST_Name,realm,SURL1)
			response="#"+realm+"->"+LIST_Name+'\n#'+response
			Outputlist_1.append(response)
			
			response=soap_add_list_cache(LIST_Name,realm,SURL2)
			response="#"+realm+"->"+LIST_Name+'\n#'+response
			Outputlist_2.append(response)
			
		BIOUTPUT('Add ListCache',Outputlist_1,Outputlist_2)
		
def FTRHUB(Name1,Name2,realms1,realms2):
	Outputlist_1=[]
	Outputlist_2=[]
	Outputlist_3=[]
	Outputlist_4=[]
	Outputlist_5=[]
	Outputlist_6=[]
	if Name1=='':
		MESSAGE_OUTPUT("Error","Empty OP A")
		return()
	if Name2=='':
		MESSAGE_OUTPUT("Error","Empty OP B")
		return()
	if realms1=='':
		MESSAGE_OUTPUT("Error","Empty realm A")
		return()
	if realms2=='':
		MESSAGE_OUTPUT("Error","Empty realm B")
		return()

	REALMLIST1=SPLIT2LIST(realms1)
	REALMLIST2=SPLIT2LIST(realms2)
	suffix='.ftrhub'

#Provision on NA
	Region2URL_DSC('NA')
	DSC__1=DSC1
	DSC__2=DSC2
	if Name1 =='Verizon Wireless' or Name2 =='Verizon Wireless':
		if Name1 =='Verizon Wireless':
			Realms = SPLIT2LIST(realms2)
		if Name2 =='Verizon Wireless':
			Realms = SPLIT2LIST(realms1)
		for realm in Realms:
			response=soap_add_list_cache('LIST_VERIZON_WIRELESS_FTRHUB_RP_REALM',realm,SURL1)
			response='LIST_VERIZON_WIRELESS_FTRHUB_RP_REALM:+'+realm+" "+response
			Outputlist_1.append(response)				
			response=soap_add_list_cache('LIST_VERIZON_WIRELESS_FTRHUB_RP_REALM',realm,SURL2)
			response='LIST_VERIZON_WIRELESS_FTRHUB_RP_REALM:+'+realm+" "+response
			Outputlist_2.append(response)
		MESSAGE_OUTPUT('Notice','Version involved, NA LISTCAHCE need to be reload')

	
	if Name1 !='Verizon Wireless' and Name2 !='Verizon Wireless':
		current_pop_name='NA PoP'
		#DSC A
		for realm1 in REALMLIST1:
			for realm2 in REALMLIST2:
				DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2)
				response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
				Outputlist_1.append(response)

				DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2+suffix)
				response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
				Outputlist_1.append(response)

		for realm2 in REALMLIST2:
			for realm1 in REALMLIST1:
				DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1)
				response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
				Outputlist_1.append(response)

				DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1+suffix)
				response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
				Outputlist_1.append(response)
		#DSC B
		for realm1 in REALMLIST1:
			for realm2 in REALMLIST2:
				DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2)
				response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
				Outputlist_2.append(response)

				DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2+suffix)
				response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
				Outputlist_2.append(response)

		for realm2 in REALMLIST2:
			for realm1 in REALMLIST1:
				DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1)
				response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
				Outputlist_2.append(response)

				DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
				DESC=replace_invalid_letter(DESC)
				response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1+suffix)
				response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
				Outputlist_2.append(response)
# AP PROVISIONING
	Region2URL_DSC('AP')
	DSC__3=DSC1
	DSC__4=DSC2
	current_pop_name='AP PoP'
	#DSC A
	for realm1 in REALMLIST1:
		for realm2 in REALMLIST2:
			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
			Outputlist_3.append(response)

			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2+suffix)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
			Outputlist_3.append(response)

	for realm2 in REALMLIST2:
		for realm1 in REALMLIST1:
			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
			Outputlist_3.append(response)

			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1+suffix)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
			Outputlist_3.append(response)
	#DSC B
	for realm1 in REALMLIST1:
		for realm2 in REALMLIST2:
			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
			Outputlist_4.append(response)

			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2+suffix)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
			Outputlist_4.append(response)

	for realm2 in REALMLIST2:
		for realm1 in REALMLIST1:
			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
			Outputlist_4.append(response)

			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1+suffix)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
			Outputlist_4.append(response)
		
# EU PROVISIONING
	Region2URL_DSC('EU')
	DSC__5=DSC1
	DSC__6=DSC2
	current_pop_name='EU PoP'
	#DSC A
	for realm1 in REALMLIST1:
		for realm2 in REALMLIST2:
			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
			Outputlist_5.append(response)

			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2+suffix)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
			Outputlist_5.append(response)

	for realm2 in REALMLIST2:
		for realm1 in REALMLIST1:
			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
			Outputlist_5.append(response)

			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1+suffix)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
			Outputlist_5.append(response)
	#DSC B
	for realm1 in REALMLIST1:
		for realm2 in REALMLIST2:
			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
			Outputlist_6.append(response)

			DESC='FTRHUB:%request_filter% '+Name1+"-"+Name2
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm1,destrealm=realm2+suffix)
			response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
			Outputlist_6.append(response)

	for realm2 in REALMLIST2:
		for realm1 in REALMLIST1:
			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
			Outputlist_6.append(response)

			DESC='FTRHUB:%request_filter% '+Name2+"-"+Name1
			DESC=replace_invalid_letter(DESC)
			response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name=current_pop_name,origrealm=realm2,destrealm=realm1+suffix)
			response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
			Outputlist_6.append(response)
	
	SIXOUTPUT("FTRHUB Provsion Reslut",DSC__1,DSC__2,DSC__3,DSC__4,DSC__5,DSC__6,Outputlist_1,Outputlist_2,Outputlist_3,Outputlist_4,Outputlist_5,Outputlist_6)
	MESSAGE_OUTPUT('Notice','Please relaod RULE on all region!')
	
def K2R(Region,Realms2,List1,Realms1,Name1,Name2):
	REALMLIST1=SPLIT2LIST(Realms1)
	REALMLIST2=SPLIT2LIST(Realms2)
	suffix='.key2roam.comfone.com'
	if Region=='':
		MESSAGE_OUTPUT("Error","Empty Region")
		return()
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Realms2")
		return()
	if List1=='':
		MESSAGE_OUTPUT("Error","Empty List1")
		return()
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Name1")
		return()
	if Realms2=='':
		MESSAGE_OUTPUT("Error","Empty Name2")
		return()
	if Region=='NA':
		MESSAGE_OUTPUT("Notice","If OP is not Vzw,reloadRULE on NA instead of LIST")
	Region2URL_DSC(Region)
	Outputlist_1=[]
	Outputlist_2=[]
	
	if Region =='NA':
		#Verison K2R route on NA DSC
		if Name1 =='Verizon Wireless' or Name2 =='Verizon Wireless':
			if Name1 =='Verizon Wireless':
				Realms = SPLIT2LIST(Realms2)
			if Name2 =='Verizon Wireless':
				Realms = SPLIT2LIST(Realms1)
			for realm in Realms:
				response=soap_add_list_cache('LIST_VERIZON_WIRELESS_K2R_RP_REALM',realm,SURL1)
				response='LIST_VERIZON_WIRELESS_K2R_RP_REALM:+'+realm+" "+response
				Outputlist_1.append(response)
				
				response=soap_add_list_cache('LIST_VERIZON_WIRELESS_K2R_RP_REALM',realm,SURL2)
				response='LIST_VERIZON_WIRELESS_K2R_RP_REALM:+'+realm+" "+response
				Outputlist_2.append(response)
				
			BIOUTPUT('Add ListCache LIST_VERIZON_WIRELESS_K2R_RP_REALM',Outputlist_1,Outputlist_2)
		else:
			#NA none Vzw K2R create RF for all realms
			for realm1 in REALMLIST1:
				for realm2 in REALMLIST2:
					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
					Outputlist_1.append(response)

					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2+suffix)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
					Outputlist_1.append(response)

			for realm2 in REALMLIST2:
				for realm1 in REALMLIST1:
					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
					Outputlist_1.append(response)

					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1+suffix)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
					Outputlist_1.append(response)					

			for realm1 in REALMLIST1:
				for realm2 in REALMLIST2:
					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+' RequestFilter\n#'+response
					Outputlist_2.append(response)

					DESC='K2R:%request_filter% '+Name1+"-"+Name2
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm1,destrealm=realm2+suffix)
					response='#'+Name1+':'+realm1+'->'+Name2+':'+realm2+suffix+' RequestFilter\n#'+response
					Outputlist_2.append(response)

			for realm2 in REALMLIST2:
				for realm1 in REALMLIST1:
					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+' RequestFilter\n#'+response					
					Outputlist_2.append(response)

					DESC='K2R:%request_filter% '+Name2+"-"+Name1
					DESC=replace_invalid_letter(DESC)
					response=soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=DESC,pop_name='NA PoP',origrealm=realm2,destrealm=realm1+suffix)
					response='#'+Name2+':'+realm2+'->'+Name1+':'+realm1+suffix+' RequestFilter\n#'+response
					Outputlist_2.append(response)
					
			BIOUTPUT('Add K2R Filter on NA DSC',Outputlist_1,Outputlist_2)

	elif Region == 'AP' or Region == 'EU':
		KKK=''
		for realm in REALMLIST2:
			KKK=KKK+realm+','+realm+suffix+','
		KKK=KKK[:-1]
		ADD_REALMS2LIST(Region,KKK,List1)		
				

#soap_check_decide_route(dsc_url,source_host,source_realm,dest_host,dest_realm,adjacent_source_peer,adjacent_source_realm)
		


#open route window layout


		
class OPEN_ROUTE(QMainWindow, Ui_Ui_OPEN_ROUTE_WIN):
	signal_opa_change = QtCore.pyqtSignal(str)
	

	def __init__(self,parent=None):
		super(OPEN_ROUTE,self).__init__(parent)
		self.setupUi(self)
		self.Full_list=['']
		for row in DB_sheet:
			self.Full_list.append(row["name"])
		self.ROUTE_LIST.hide()
		self.OWNER.addItem('All')
		for i in Engineer_set:
			self.OWNER.addItem(i)
			
		for i in ROUTE_STATUS_LIST:
			self.ROUTE_STATUS.addItem(i)
			
		self.LIST_ROUTE.clicked.connect(lambda:self.route_filter())
		self.ROUTE_LIST.currentIndexChanged.connect(self.fill_OPAB)
		self.HIDE_LIST_ROUTE.clicked.connect(self.hide_route_filter)
		#self.Button_FTRUB.clicked.connect(lambda: FTRHUB(self.OP_A.text(),self.OP_B.text(),self.realm_A.text(),self.realm_B.text()))
		self.Button_FTRUB.clicked.connect(lambda: self.ftrhub_initial())

		self.IMSI_A.activated.connect(self.update_IMSI_A)
		self.IMSI_B.activated.connect(self.update_IMSI_B)
		
		self.TADIG_A.activated.connect(self.update_TADIG_A)
		self.TADIG_B.activated.connect(self.update_TADIG_B)
		
#COMMAND BUTTONS ON RIGHT		
		self.CALL_RMT.clicked.connect(self.call_rmt)
		self.UPD_DB.clicked.connect(lambda:refresh_all())
		self.BKP_DB.clicked.connect(lambda:BACKUP_DB())
		self.RST_DB.clicked.connect(lambda:RestoreFile(".\\backup",".\\file"))

		self.Re_AP_LIST.clicked.connect(lambda: Reload_Region_LIST("AP"))
		self.Re_EU_LIST.clicked.connect(lambda: Reload_Region_LIST("EU"))
		self.Re_NA_LIST.clicked.connect(lambda: Reload_Region_LIST("NA"))
		self.Re_AP_RULE.clicked.connect(lambda: Reload_Region_RULE("AP"))
		self.Re_EU_RULE.clicked.connect(lambda: Reload_Region_RULE("EU"))
		self.Re_NA_RULE.clicked.connect(lambda: Reload_Region_RULE("NA"))


		self.New_Election.clicked.connect(lambda: NEW_EMAIL2PEER(self.Combo_SCENARIO.currentText(),self.OP_A.text(),self.realm_A.text(),self.IMSI_A.currentText(),self.OP_B.text(),self.realm_B.text(),self.IMSI_B.currentText()))
		self.Provisoned.clicked.connect(lambda: PROVISIONED_EMAIL2PEER(self.Combo_SCENARIO.currentText(),self.OP_A.text(),self.realm_A.text(),self.IMSI_A.currentText(),self.OP_B.text(),self.realm_B.text(),self.IMSI_B.currentText()))

		SCENARIO=[]
		for row in PEERINGPOLICY:
			SCENARIO.append(row['SCENARIO'])

		for i in SCENARIO:
			self.Combo_SCENARIO.addItem(i)
		self.Combo_SCENARIO.setMaxVisibleItems (10)
		self.Combo_SCENARIO.currentIndexChanged.connect(self.update_POLICY)


		self.TECH_COMMENT_A.LineWrapMode


#BUILD COMBO LIST_A WITH DROP DOWN SELECTION
		Combo_LIST_A=self.Full_list
		for i in Combo_LIST_A:
			self.Combo_Select_A.addItem(i)
		self.Combo_Select_A.setMaxVisibleItems (10)
		self.Combo_Select_A.currentIndexChanged.connect(self.update_A)
		self.OP_A.returnPressed.connect(self.rebuild_A_list)

#Add LISTCACHE FUNCTION_A
		self.Combo_Region_A.addItem('')
		for i in RegionList:
			self.Combo_Region_A.addItem(i)
		
		self.Combo_Region_A.setMaxVisibleItems (4)
	

		self.B_Reams2A_LIST.clicked.connect(lambda: ADD_REALMS2LIST(self.Combo_Region_A.currentText(),self.realm_B.displayText(),self.LIST_A.displayText()))

#Check DECIDE ROUTE	FUNCTION_A
		self.Check_TO_A_Route.clicked.connect(lambda: CHECK_DECIDE_ROUTE2OP_ALL_REGION_2(self.realm_B.displayText(),self.realm_A.displayText()))
		
#Add K2R FUNCTION_A

		self.K2R_B_Reams2A_LIST.clicked.connect(lambda: K2R(self.Combo_Region_A.currentText(),self.realm_B.displayText(),self.LIST_A.displayText(),self.realm_A.displayText(),self.OP_A.displayText(),self.OP_B.displayText()))

		

## code for OPB only start

		

		self.TECH_COMMENT_B.LineWrapMode

#COMBO LIST_B WITH DROP DOWN SELECTION
		Combo_LIST_B=self.Full_list
		for i in Combo_LIST_B:
			self.Combo_Select_B.addItem(i)
		self.Combo_Select_B.setMaxVisibleItems (10)
		self.Combo_Select_B.currentIndexChanged.connect(self.update_B)
		self.OP_B.returnPressed.connect(self.rebuild_B_list)

#Add LISTCACHE FUNCTION_B
		self.Combo_Region_B.addItem('')
		for i in RegionList:
			self.Combo_Region_B.addItem(i)

		self.A_Reams2B_LIST.clicked.connect(lambda: ADD_REALMS2LIST(self.Combo_Region_B.currentText(),self.realm_A.displayText(),self.LIST_B.displayText()))
		
#Check DECIDE ROUTE	FUNCTION_B
		self.Check_TO_B_Route.clicked.connect(lambda: CHECK_DECIDE_ROUTE2OP_ALL_REGION_2(self.realm_A.displayText(),self.realm_B.displayText()))
		
#Add K2R FUNCTION_B
		self.K2R_A_Reams2B_LIST.clicked.connect(lambda: K2R(self.Combo_Region_B.currentText(),self.realm_A.displayText(),self.LIST_B.displayText(),self.realm_B.displayText(),self.OP_B.displayText(),self.OP_A.displayText()))


	def ftrhub_initial(self):
		reply=QMessageBox.information(self,'Provision FTRUB Route','Will Provison Request filter for A->B,A->B.ftrhub,B->A,B-A.ftrub on all region\nOn NA DSC,if Verizon,will only insert RP realm into LIST_VERIZON_WIRELESS_FTRHUB_RP_REALM', QMessageBox.Yes | QMessageBox.No)
		
		if reply==QMessageBox.Yes:
			FTRHUB(self.OP_A.text(),self.OP_B.text(),self.realm_A.text(),self.realm_B.text())
		if reply==QMessageBox.No:
			return()
		
	def fill_OPAB(self):
		if self.ROUTE_LIST.currentText()=='':
			return()
		AB=self.ROUTE_LIST.currentText().split('<>')
		self.OP_A.setText(AB[0])
		self.OP_B.setText(AB[-2])
		self.update_AB()
		
	def route_filter(self):
		FILTERED_ROUTE=[]
		self.ROUTE_LIST.clear()
		self.ROUTE_LIST.show()

		results=READ_RMT_ROUTE_BY_STATUS(self.ROUTE_STATUS.currentText())

		#Insert o_owner into result
		for result in results:
			result['o_owner']=''
			for entry in DB_sheet:
				if entry['name']==result['o_name']:
					result['o_owner']=entry['owner']

		#filter by owner
		filtered_route_owner=[]
		if self.OWNER.currentText()=='All':
			filtered_route_owner=results[:]
		if self.OWNER.currentText()!='All':
			for result in results:
				if result['o_owner']==self.OWNER.currentText():
					filtered_route_owner.append(result)

		

		for route in filtered_route_owner:
			if route['dra1']==None:
				route['dra1']=''
			if route['dra2']==None:
				route['dra2']=''
			if route['dra3']==None:
				route['dra3']=''
			if route['o_real_hub']==None:
				route['o_real_hub']=''
			if route['r_real_hub']==None:
				route['r_real_hub']=''
				

			route_info=route['o_name']+'<>'+route['o_real_hub']+'<>'+route['dra1']+'<>'+route['dra2']+'<>'+route['dra3']+'<>'+route['r_real_hub']+'<>'+route['r_name']+'<>---'+route['o_owner']+'-----'+str(route['electing_date'])+'-----'+route['status']
			self.ROUTE_LIST.addItem(route_info)
			

			
	def hide_route_filter(self):
		self.ROUTE_LIST.hide()
		self.OP_A.setText('')
		self.OP_B.setText('')
		self.update_AB()			
					
	def update_POLICY(self):
		for row in PEERINGPOLICY:
			if row['SCENARIO']==self.Combo_SCENARIO.currentText():
				self.POLICY.setText(row['SVR_PEER']+'-'+row['HUB_PEER'])
			
	def update_AB(self):
		OPA_Name = self.OP_A.text()
		OPB_Name = self.OP_B.text()

		global OPAAA
		OPAAA=OPA_Name
		self.SSID_A.setText('')
		self.IMSI_A.clear()
		self.Country_A.setText('')
		self.realm_A.setText('')
		self.LIST_A.setText('')
		self.LISTREGION_A.setText('')
		self.Owner_A.setText('')
		self.RMT_A.setText('')
		self.DRA_A.setText('')
		self.HUB_POLICY_A.setText('')
		self.TECH_COMMENT_A.setText('')
		self.TADIG_A.clear()
		self.Combo_Region_A.setCurrentIndex(0)

		self.SSID_B.setText('')
		self.IMSI_B.clear()
		self.Country_B.setText('')
		self.realm_B.setText('')
		self.LIST_B.setText('')
		self.LISTREGION_B.setText('')
		self.Owner_B.setText('')
		self.RMT_B.setText('')
		self.DRA_B.setText('')
		self.HUB_POLICY_B.setText('')
		self.TECH_COMMENT_B.setText('')
		self.TADIG_B.clear()
		self.Combo_Region_B.setCurrentIndex(0)
		
		for row in DB_sheet:
			if row["name"] == OPA_Name:
				self.SSID_A.setText(row["ssid"])
				self.IMSI_A.clear()
				self.IMSI_A.addItem(row["imsi_prefix"])
				self.Country_A.setText(row["country"])
				self.realm_A.setText(row["realm_name"])
				self.LIST_A.setText(row["LIST"])
				self.LISTREGION_A.setText(row["LISTREGION"])
				self.Owner_A.setText(row["owner"])
				self.RMT_A.setText(row["status"])
				self.DRA_A.setText(row["dra"])
				self.HUB_POLICY_A.setText(row["hub_policy"])
				self.TECH_COMMENT_A.setText(row["technicalcomment"])
				self.TADIG_A.addItem(row["tagid"])
				self.Combo_Region_A.setCurrentIndex(0)
			if row["name"] == OPB_Name:
				self.SSID_B.setText(row["ssid"])
				self.IMSI_B.clear()
				self.IMSI_B.addItem(row["imsi_prefix"])
				self.Country_B.setText(row["country"])
				self.realm_B.setText(row["realm_name"])
				self.LIST_B.setText(row["LIST"])
				self.LISTREGION_B.setText(row["LISTREGION"])
				self.Owner_B.setText(row["owner"])
				self.RMT_B.setText(row["status"])
				self.DRA_B.setText(row["dra"])
				self.HUB_POLICY_B.setText(row["hub_policy"])
				self.TECH_COMMENT_B.setText(row["technicalcomment"])
				self.TADIG_B.addItem(row["tagid"])
				self.Combo_Region_B.setCurrentIndex(0)

	def update_A(self,ii):
		OPA_Name = self.Combo_Select_A.currentText()
		self.OP_A.setText(OPA_Name)
		global OPAAA
		OPAAA=OPA_Name
		for row in DB_sheet:
			if row["name"] == OPA_Name:
				self.SSID_A.setText(row["ssid"])
				self.IMSI_A.clear()
				self.IMSI_A.addItem(row["imsi_prefix"])
				self.Country_A.setText(row["country"])
				self.realm_A.setText(row["realm_name"])
				self.LIST_A.setText(row["LIST"])
				self.LISTREGION_A.setText(row["LISTREGION"])
				self.Owner_A.setText(row["owner"])
				self.RMT_A.setText(row["status"])
				self.DRA_A.setText(row["dra"])
				self.HUB_POLICY_A.setText(row["hub_policy"])
				self.TECH_COMMENT_A.setText(row["technicalcomment"])
				self.TADIG_A.clear()
				self.TADIG_A.addItem(row["tagid"])
				self.Combo_Region_A.setCurrentIndex(0)


				
	def update_B(self,ii):
		OPB_Name = self.Combo_Select_B.currentText()
		global OPBBB
		OPBBB=OPB_Name
		self.OP_B.setText(OPB_Name)

		for row in DB_sheet:
			if row["name"] == OPB_Name:
				self.SSID_B.setText(row["ssid"])
				self.IMSI_B.clear()
				self.IMSI_B.addItem(row["imsi_prefix"])
				self.Country_B.setText(row["country"])
				self.realm_B.setText(row["realm_name"])
				self.LIST_B.setText(row["LIST"])
				self.LISTREGION_B.setText(row["LISTREGION"])
				self.Owner_B.setText(row["owner"])
				self.RMT_B.setText(row["status"])
				self.DRA_B.setText(row["dra"])
				self.HUB_POLICY_B.setText(row["hub_policy"])
				self.TECH_COMMENT_B.setText(row["technicalcomment"])
				self.TADIG_B.clear()
				self.TADIG_B.addItem(row["tagid"])
				self.Combo_Region_B.setCurrentIndex(0)

## code for OPB only end

	def rebuild_A_list(self):
		list=[]
		key= self.OP_A.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_A.clear()
		for i in list:
			self.Combo_Select_A.addItem(i)

	def rebuild_B_list(self):
		list=[]
		key= self.OP_B.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_B.clear()
		for i in list:
			self.Combo_Select_B.addItem(i)
			
	def call_rmt(self):
		global rmt_flag
		global rmt_user
		global rmt_pwd
		rmt_flag=rmt_flag+1
		url="https://dssrmt.syniverse.com/rmt/route?oSsid="+self.SSID_A.text()+"&oCountry=&oRealHub=&rSsid="+self.SSID_B.text()+"&rCountry=&rRealHub=&priority=&status="
		rmt_route_edit(url,rmt_flag,rmt_user,rmt_pwd)

	def update_IMSI_A(self):
		self.ROUTE_LIST.hide()
		self.Combo_Select_A.setCurrentIndex(0)
		self.Combo_Select_B.setCurrentIndex(0)
		self.ROUTE_LIST.setCurrentIndex(0)
		IMSI_A=self.IMSI_A.currentText()
		self.IMSI_A.clear()
		for row in DB_sheet:
			if IMSI_A in row["imsi_prefix"]:
				self.IMSI_A.addItem(row["imsi_prefix"])
		for row in DB_sheet:
			if row["imsi_prefix"] == IMSI_A:
				self.OP_A.setText(row["name"])
				self.SSID_A.setText(row["ssid"])
				self.Country_A.setText(row["country"])
				self.realm_A.setText(row["realm_name"])
				self.LIST_A.setText(row["LIST"])
				self.LISTREGION_A.setText(row["LISTREGION"])
				self.Owner_A.setText(row["owner"])
				self.RMT_A.setText(row["status"])
				self.DRA_A.setText(row["dra"])
				self.HUB_POLICY_A.setText(row["hub_policy"])
				self.TECH_COMMENT_A.setText(row["technicalcomment"])
				self.TADIG_A.clear()
				self.TADIG_A.addItem(row["tagid"])
				self.Combo_Region_A.setCurrentIndex(0)

	def update_IMSI_B(self):
		self.ROUTE_LIST.hide()
		self.Combo_Select_A.setCurrentIndex(0)
		self.Combo_Select_B.setCurrentIndex(0)
		self.ROUTE_LIST.setCurrentIndex(0)
		IMSI_B=self.IMSI_B.currentText()
		self.IMSI_B.clear()
		for row in DB_sheet:
			if IMSI_B in row["imsi_prefix"]:
				self.IMSI_B.addItem(row["imsi_prefix"])
		for row in DB_sheet:
			if row["imsi_prefix"] == IMSI_B:
				self.OP_B.setText(row["name"])
				self.SSID_B.setText(row["ssid"])
				self.Country_B.setText(row["country"])
				self.realm_B.setText(row["realm_name"])
				self.LIST_B.setText(row["LIST"])
				self.LISTREGION_B.setText(row["LISTREGION"])
				self.Owner_B.setText(row["owner"])
				self.RMT_B.setText(row["status"])
				self.DRA_B.setText(row["dra"])
				self.HUB_POLICY_B.setText(row["hub_policy"])
				self.TECH_COMMENT_B.setText(row["technicalcomment"])
				self.TADIG_B.clear()
				self.TADIG_B.addItem(row["tagid"])
				self.Combo_Region_B.setCurrentIndex(0)
				
	def update_TADIG_A(self):
		self.ROUTE_LIST.hide()
		self.Combo_Select_A.setCurrentIndex(0)
		self.Combo_Select_B.setCurrentIndex(0)
		self.ROUTE_LIST.setCurrentIndex(0)
		TADIG_A=self.TADIG_A.currentText()
		self.TADIG_A.clear()
		for row in DB_sheet:
			if TADIG_A.lower() in row["tagid"].lower():
				self.TADIG_A.addItem(row["tagid"])
		for row in DB_sheet:
			if row["tagid"].lower() == TADIG_A.lower():
				self.OP_A.setText(row["name"])
				self.SSID_A.setText(row["ssid"])
				self.Country_A.setText(row["country"])
				self.realm_A.setText(row["realm_name"])
				self.LIST_A.setText(row["LIST"])
				self.LISTREGION_A.setText(row["LISTREGION"])
				self.Owner_A.setText(row["owner"])
				self.RMT_A.setText(row["status"])
				self.DRA_A.setText(row["dra"])
				self.HUB_POLICY_A.setText(row["hub_policy"])
				self.TECH_COMMENT_A.setText(row["technicalcomment"])
				self.IMSI_A.clear()
				self.IMSI_A.addItem(row["imsi_prefix"])
				self.Combo_Region_A.setCurrentIndex(0)
	
	def update_TADIG_B(self):
		self.ROUTE_LIST.hide()
		self.Combo_Select_A.setCurrentIndex(0)
		self.Combo_Select_B.setCurrentIndex(0)
		self.ROUTE_LIST.setCurrentIndex(0)
		TADIG_B=self.TADIG_B.currentText()
		self.TADIG_B.clear()
		for row in DB_sheet:
			if TADIG_B.lower() in row["tagid"].lower():
				self.TADIG_B.addItem(row["tagid"])
		for row in DB_sheet:
			if row["tagid"].lower() == TADIG_B.lower():
				self.OP_B.setText(row["name"])
				self.SSID_B.setText(row["ssid"])
				self.Country_B.setText(row["country"])
				self.realm_B.setText(row["realm_name"])
				self.LIST_B.setText(row["LIST"])
				self.LISTREGION_B.setText(row["LISTREGION"])
				self.Owner_B.setText(row["owner"])
				self.RMT_B.setText(row["status"])
				self.DRA_B.setText(row["dra"])
				self.HUB_POLICY_B.setText(row["hub_policy"])
				self.TECH_COMMENT_B.setText(row["technicalcomment"])
				self.IMSI_B.clear()
				self.IMSI_B.addItem(row["imsi_prefix"])
				self.Combo_Region_B.setCurrentIndex(0)
	
	
class OthersWidget(QDialog):
	def __init__(self, parent=None):
		super(OthersWidget, self).__init__(parent)
		#self.setStyleSheet("background:lightgrey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)

class OthersWidget2(QDialog):
	def __init__(self, parent=None):
		super(OthersWidget2, self).__init__(parent)
		self.setStyleSheet("background:lightgrey")
		self.Lable_TADIG_A = QLabel("TADIG_TEST",self)

class OP_Online(QMainWindow, Ui_Ui_OP_ONLINE):
	def __init__(self,parent=None):
		super(OP_Online,self).__init__(parent)
		self.setupUi(self)

		self.sync.clicked.connect(lambda:self.OPERATOR.setText(OPAAA))
		self.sync.clicked.connect(lambda:self.update_online_info(self.OPERATOR.text()))
		self.sync.clicked.connect(lambda:self.check_list_name())
		
		self.btn_direct.setChecked(False)
		self.btn_direct.toggled.connect(lambda:self.tuggle())
		

		self.btn_indirect.setChecked(True)

		

		self.Lable_VIRTUAL_REALM.hide()
		self.VIRTUAL_REALM.hide()

		self.Local_DSC_AP.stateChanged.connect(lambda:self.toggle_local_dsc(self.Local_DSC_AP.checkState(),"AP"))
		self.Local_DSC_EU.stateChanged.connect(lambda:self.toggle_local_dsc(self.Local_DSC_EU.checkState(),"EU"))
		self.Local_DSC_NA.stateChanged.connect(lambda:self.toggle_local_dsc(self.Local_DSC_AP.checkState(),"NA"))

		#Add test entry in listcache

		self.Combo_LIST_REGION.addItem('Select Region')
		for row in Local_DSC_List:
			self.Combo_LIST_REGION.addItem(row)
		self.Combo_LIST_REGION.setMaxVisibleItems (4)
		
		self.ADD_TEST_ENTRY.clicked.connect(lambda:self.add_test_entry_listcache(self.Combo_LIST_REGION.currentText(),self.LISTNAME.text()))

		self.RELOADLIST.clicked.connect(lambda:self.RELOAD_LISTCACHES_ALLDSC(self.Combo_LIST_REGION.currentText()))	
		
		#Add request filter

		self.Combo_RF_REGION.addItem('Select Region')
		for row in RegionList:
			self.Combo_RF_REGION.addItem(row)
		self.Combo_RF_REGION.setMaxVisibleItems (4)

		self.C_RequestFilter.clicked.connect(lambda:self.create_request_filter(self.Combo_RF_REGION.currentText(),self.DRACustomerRealmName.text(),self.DRACustomerRealmNameBeforeTranslation.text(),self.LISTNAME.text(),self.SSID.text()))
		
		self.C_RequestFilter_reload.clicked.connect(lambda:self.reload_rule_engine_op_online(self.Combo_RF_REGION.currentText()))
		

		#Add Decide Route

		self.Combo_DR_REGION.addItem('Select Region')
		for row in RegionList:
			self.Combo_DR_REGION.addItem(row)
		self.Combo_DR_REGION.setMaxVisibleItems (4)
		self.Combo_DR_REGION.currentIndexChanged.connect(self.update_DR_Region)		
		

		self.Combo_DR_TYPE.addItem('Select Rule Type')
		self.Combo_DR_TYPE.setMaxVisibleItems (10)
		self.Combo_DR_TYPE.currentIndexChanged.connect(self.update_Online_CondCons)
		
		self.C_Route.clicked.connect(lambda:self.add_decide_route2op(self.Combo_DR_REGION.currentText(),self.DRACustomerRealmName.text(),self.DRACustomerRealmNameBeforeTranslation.text(),self.CONDITION.toPlainText(),self.CONSEQUENCE.toPlainText(),self.PRIORITY.text(),self.Combo_DR_TYPE.currentText()))

		self.RELOAD_DECIDE_ROUTE_ON_REGION.clicked.connect(lambda:self.reload_rule_engine_op_online(self.Combo_DR_REGION.currentText()))

		self.IMSI2REALM.clicked.connect(lambda:self.MAP_IMSI2REALM(self.DRACustomerRealmName.text(),self.IMSI.text()))
		
		self.IMSI_TO_K2RREALM.clicked.connect(lambda:self.MAP_IMSI_TO_K2RREALM(self.DRACustomerRealmName.text(),self.IMSI.text()))	

		self.RELOADMAP.clicked.connect(lambda:self.RELOAD_MAPCACHES())
		#REALM2OP
		self.ADDREAL2OP.clicked.connect(lambda:self.ADD_REALM2OP(self.DRACustomerRealmName.text(),self.DRACustomerNodeName.text(),self.DRACustomerRealmNameBeforeTranslation.text(),self.R2OP_NAME.text()))

		self.RELOADREALM2OP.clicked.connect(lambda:self.RELOAD_REALM2OP_ALLDSC())
		#SEND EMAIL
		self.EMAIL.clicked.connect(lambda:ONLINE_EMAIL(self.OPERATOR.text(),self.LOG.toPlainText()))
	



	def toggle_local_dsc(self,state,region):
		global List_Add_Route_Local
		Local_DSC_List=[]
		if self.Local_DSC_AP.checkState()==2:
			Local_DSC_List.append("AP")
		if self.Local_DSC_EU.checkState()==2:
			Local_DSC_List.append("EU")
		if self.Local_DSC_NA.checkState()==2:
			Local_DSC_List.append("NA")
		List_Add_Route_Local=[]
		self.Combo_LIST_REGION.clear()
		self.Combo_RF_REGION.clear()

		self.Combo_LIST_REGION.addItem('Select Region')
		self.Combo_RF_REGION.addItem('Select Region')
		self.Combo_DR_REGION.addItem('Select Region')
		for row in Local_DSC_List:
			self.Combo_LIST_REGION.addItem(row)
			self.Combo_RF_REGION.addItem(row)
			List_Add_Route_Local.append(row)

			

			
	def check_list_name(self):
		for row in DB_sheet:
			if row['name']==OPAAA:
				self.Exisisting_LISTNAME.setText(row['LIST'])
		if self.Exisisting_LISTNAME.text()=='':
			self.Exisisting_LISTNAME.setText('Not Exist')

	def update_DR_Region(self):
		if self.Local_DSC_AP.checkState()==0 and self.Local_DSC_EU.checkState()==0 and self.Local_DSC_NA.checkState()==0:
			MESSAGE_OUTPUT("WRONG","No Local DSC Checked!")
			return()
		self.CONSEQUENCE.setText("")
		self.CONDITION.setText("")
		self.Combo_DR_TYPE.clear()
		self.Combo_DR_TYPE.addItem('Select Rule Type')
		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_DR_REGION.currentText():
				self.Combo_DR_TYPE.addItem(row['TYPE'])
		
		
	def update_Online_CondCons(self):
		self.PRIORITY.setText('10')
		if 'MME/HSS' in self.Combo_DR_TYPE.currentText():
			self.PRIORITY.setText('9')
		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_DR_REGION.currentText():
				if row['TYPE']==self.Combo_DR_TYPE.currentText():
					self.CONSEQUENCE.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VIRTUAL_REALM.text()))
					self.CONDITION.setText(row['CONDITION'])
					

#def soap_add_list_cache(list_cache_name,realm_to_add,dsc_url):
	def add_test_entry_listcache(self,region,listcachename):
		if region== 'AP' or region== 'EU' or region== 'NA':
			if listcachename!='':
				Region2URL_DSC(region)
				Outputlist_1=[]
				Outputlist_2=[]
				Output1=DSC1+':'+'add test entry to '+listcachename+':'+soap_add_list_cache(listcachename,'test',SURL1)
				Output2=DSC2+':'+'add test entry to '+listcachename+':'+soap_add_list_cache(listcachename,'test',SURL2)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				BIOUTPUT("Add Test Entry in Listcache",Outputlist_1,Outputlist_2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			else:
				MESSAGE_OUTPUT('Prompt','empty listcache name')
		else:
			MESSAGE_OUTPUT('Prompt','Wrong region when add listcache')

#. soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0")
	def create_request_filter(self,region,realm_names,private_realm_names,listname,SSID):
		all_realms=JOIN_STR(realm_names,private_realm_names,',')
		if region!= 'AP' and region!= 'EU' and region!= 'NA':
			MESSAGE_OUTPUT('Wrong','Wrong Region Name')
			return
		if all_realms== '':
			MESSAGE_OUTPUT('Wrong','Empty realmName')
			return
		if listname== '':
			MESSAGE_OUTPUT('Wrong','Empty listname')
			return
		if SSID== '':
			MESSAGE_OUTPUT('Wrong','Empty SSID')
			return
		Outputlist_1=[]
		Outputlist_2=[]	
		Region2URL_DSC(region)
		desc_from_op=self.OPERATOR.text()+' SSID '+SSID+' %request filter% if dest realm in LISTCACHE,let pass'
		desc_to_op  =self.OPERATOR.text()+' SSID '+SSID+' %request filter% if origin realm in LISTCACHE,let pass'
		realms=SPLIT2LIST(all_realms)
		#283-destination realm 296-oringinal realm
		condition_from_op='''(IsExist(#AVP283)&amp;&amp;InList(ToLower(AVP283),"'''+listname+'''"))'''
		condition_to_op='''(IsExist(#AVP296)&amp;&amp;InList(ToLower(AVP296),"'''+listname+'''"))'''
		for realm in realms:
			Output1=DSC1+' RF from OP:orig realm='+realm+' con:'+condition_from_op+':'
			Output1=Output1+soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=desc_from_op,pop_name=POP,origrealm=realm,condition=condition_from_op)
			Output1=Output1+'\n'
			Output1=Output1+DSC1+' RF to OP:dest realm='+realm+' con:'+condition_to_op+':'
			Output1=Output1+soap_add_rule(dsc_url=SURL1,ruletype='REQUEST_FILTER',description=desc_to_op,pop_name=POP,destrealm=realm,condition=condition_to_op)
			
			Output2=DSC2+' RF from OP:orig realm='+realm+' con:'+condition_from_op+':'
			Output2=Output2+soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=desc_from_op,pop_name=POP,origrealm=realm,condition=condition_from_op)
			Output2=Output2+'\n'
			Output2=Output2+DSC2+' RF to OP:dest realm='+realm+' con:'+condition_to_op+':'
			Output2=Output2+soap_add_rule(dsc_url=SURL2,ruletype='REQUEST_FILTER',description=desc_to_op,pop_name=POP,destrealm=realm,condition=condition_to_op)

			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)			
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
		BIOUTPUT("Add request filter",Outputlist_1,Outputlist_2)


	def add_decide_route2op(self,region,realm_names,private_realm_names,condi,cons,prio,Combo_DR_TYPE):
		# List_Add_Route_Local is the list contains the regions of local DSC
		global List_Add_Route_Local
		global DSC1,DSC2,SURL1,SURL2

		SSID=self.SSID.text()
		Local=0
		for row in List_Add_Route_Local:
			if region in row:
				Local=1
		if Local ==1:
			all_realms=JOIN_STR(realm_names,private_realm_names,',')
		else:
			all_realms=realm_names
		Outputlist_1=[]
		Outputlist_2=[]
		if region!= 'AP' and region!= 'EU' and region!= 'NA':
			MESSAGE_OUTPUT('Wrong','Wrong Region Name')
			return
		if all_realms== '':
			MESSAGE_OUTPUT('Wrong','Empty Region Name')
			return
		if condi== '':
			MESSAGE_OUTPUT('Wrong','Empty condition')
			return
		if cons== '':
			MESSAGE_OUTPUT('Wrong','Empty consequence')
			return
		if prio== '':
			MESSAGE_OUTPUT('Wrong','Empty priority')
			return
		Region2URL_DSC(region)
		desc=self.OPERATOR.text()+' SSID '+SSID+' %decide route% * to OP'
		desc=replace_invalid_letter(desc)
		realms=SPLIT2LIST(all_realms)
		if Combo_DR_TYPE=='MME/HSS on HKG':
			DSC2=DSC1
			SURL1="http://10.162.28.186:8080/DSC_SOAP/query?"
			SURL2=SURL1
		if Combo_DR_TYPE=='MME/HSS on SNG':
			DSC1=DSC2
			SURL2="http://10.163.28.131:8080/DSC_SOAP/query?"
			SURL1=SURL2
		if Combo_DR_TYPE=='MME/HSS on AMS':
			DSC2=DSC1
			SURL1="http://10.160.28.32:8080/DSC_SOAP/query?"
			SURL2=SURL1
		if Combo_DR_TYPE=='MME/HSS on FRT':
			DSC1=DSC2
			SURL2="http://10.161.28.32:8080/DSC_SOAP/query?"
			SURL1=SURL2
		if Combo_DR_TYPE=='MME/HSS on CHI':
			DSC2=DSC1
			SURL1="http://10.166.28.200:8080/DSC_SOAP/query?"
			SURL2=SURL1
		if Combo_DR_TYPE=='MME/HSS on DAL':
			DSC1=DSC2
			SURL2="http://10.164.28.189:8080/DSC_SOAP/query?"
			SURL1=SURL2
			
		for realm in realms:
			Output1= DSC1+' DecideRoute to OP:* to '+realm+' condi:'+condi+' cons:'+cons+':'
			Output1= Output1+soap_add_rule(dsc_url=SURL1,ruletype='DECIDE_ROUTE',description=desc,pop_name=POP,destrealm=realm,condition=condi,consequence=cons,priority=prio)
			Output2= DSC2+' DecideRoute to OP:* to '+realm+' condi:'+condi+' cons:'+cons+':'
			Output2= Output2+soap_add_rule(dsc_url=SURL2,ruletype='DECIDE_ROUTE',description=desc,pop_name=POP,destrealm=realm,condition=condi,consequence=cons,priority=prio)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
		BIOUTPUT("Add Decide route to OP",Outputlist_1,Outputlist_2)
		
	def MAP_IMSI2REALM(self,realms,IMSIs):
		if realms=='':
			MESSAGE_OUTPUT('Wrong','Empty DRACustomerRealmName')
			return
		if IMSIs=='':
			MESSAGE_OUTPUT('Wrong','Empty IMSI Prefix')
			return
		MESSAGE_OUTPUT('Warning','All IMSI will be mapped to \nthe 1st realm in DRACustomerRealmName ')
		realm_list=SPLIT2LIST(realms)
		first_realm=realm_list[0].strip()
		imsi_list=SPLIT2LIST(IMSIs)
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		for re in region_list:
			Region2URL_DSC(re)
			for imsi in imsi_list:
				imsi=imsi.strip()
				Output1=DSC1+' '+imsi+'->'+first_realm+'->MAP_IMSITOREALM '
				Output1=Output1+soap_add_mapcache(SURL1,'MAP_IMSITOREALM',imsi,first_realm)
				Output2=DSC2+' '+imsi+'->'+first_realm+'->MAP_IMSITOREALM '
				Output2=Output2+soap_add_mapcache(SURL2,'MAP_IMSITOREALM',imsi,first_realm)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add  MAP_IMSITOREALM",Outputlist_1,Outputlist_2)

	def MAP_IMSI_TO_K2RREALM(self,realms,IMSIs):
		if realms=='':
			MESSAGE_OUTPUT('Wrong','Empty DRACustomerRealmName')
			return
		if IMSIs=='':
			MESSAGE_OUTPUT('Wrong','Empty IMSI Prefix')
			return
		MESSAGE_OUTPUT('Warning','All IMSI will be mapped to \nthe 1st realm in DRACustomerRealmName ')
		realm_list=SPLIT2LIST(realms)
		first_realm=realm_list[0].strip()
		first_realm=first_realm+'.key2roam.comfone.com'
		imsi_list=SPLIT2LIST(IMSIs)
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		for re in region_list:
			Region2URL_DSC(re)
			for imsi in imsi_list:
				imsi=imsi.strip()
				Output1=DSC1+' '+imsi+'->'+first_realm+'->MAP_IMSI_TO_K2RREALM '
				Output1=Output1+soap_add_mapcache(SURL1,'MAP_IMSI_TO_K2RREALM',imsi,first_realm)
				Output2=DSC2+' '+imsi+'->'+first_realm+'->MAP_IMSI_TO_K2RREALM '
				Output2=Output2+soap_add_mapcache(SURL2,'MAP_IMSI_TO_K2RREALM',imsi,first_realm)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add  MAP_IMSI2K2R REALM",Outputlist_1,Outputlist_2)

	def RELOAD_MAPCACHES(self,reg=''):
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		if reg=='AP' or reg=='EU' or reg=='NA':
			region_list=[reg]
		for re in region_list:
			Region2URL_DSC(re)
			Output1=DSC1+':reload all MAPCACHE:'
			Output1=Output1+soap_reload_mapcache(SURL1)
			Output2=DSC2+':reload all MAPCACHE:'
			Output2=Output2+soap_reload_mapcache(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
		BIOUTPUT("Reload LISTCACHES",Outputlist_1,Outputlist_2)
			
	def RELOAD_LISTCACHES_ALLDSC(self,reg=''):
		region_list=['AP','EU','NA']
		if reg=='AP' or reg=='EU' or reg=='NA':
			region_list=[reg]
		for re in region_list:
			Outputlist_1=[]
			Outputlist_2=[]
			Region2URL_DSC(re)
			Output1=DSC1+':reload all LISTCACHE:'
			Output1=Output1+soap_reload_listcaches(SURL1)
			Output2=DSC2+':reload all LISTCACHE:'
			Output2=Output2+soap_reload_listcaches(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Reload LISTCACHES",Outputlist_1,Outputlist_2)
			
	def RELOAD_REALM2OP_ALLDSC(self):
		region_list=['AP','EU','NA']
		for re in region_list:
			Outputlist_1=[]
			Outputlist_2=[]
			Region2URL_DSC(re)
			Output1=DSC1+':reload REALM2OP:'
			Output1=Output1+soap_reload_realm2op(SURL1)
			Output2=DSC2+':reload REALM2OP:'
			Output2=Output2+soap_reload_realm2op(SURL2)
			LOGTEXT=self.LOG.toPlainText()
			LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
			self.LOG.setPlainText(LOGTEXT)
			Outputlist_1.append(Output1)
			Outputlist_2.append(Output2)
			BIOUTPUT("Reload REALM2OP",Outputlist_1,Outputlist_2)

	def ADD_REALM2OP(self,realms,node_realms,private_realms,R2OP_NAME):
		realms=JOIN_STR(realms,node_realms,',')
		realms=JOIN_STR(realms,private_realms,',')
		if realms=='':
			MESSAGE_OUTPUT('Wrong','Empty Realm')
			return
		if R2OP_NAME=='':
			MESSAGE_OUTPUT('Wrong','Empty Realm2OP name')
			return

		realm_list=SPLIT2LIST(realms)
		
		Outputlist_1=[]
		Outputlist_2=[]
		region_list=['AP','EU','NA']
		for re in region_list:
			Region2URL_DSC(re)
			for realm in realm_list:
				Output1=DSC1+' Realm2OP '+realm+'->'+R2OP_NAME
				Output1=Output1+soap_add_realm2op(SURL1,realm,R2OP_NAME)
				Output2=DSC2+' Realm2OP '+realm+'->'+R2OP_NAME
				Output2=Output2+soap_add_realm2op(SURL2,realm,R2OP_NAME)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add  Realm2OP",Outputlist_1,Outputlist_2)

	def reload_rule_engine_op_online(self,region):
		if region!= 'AP' and region!= 'EU' and region!= 'NA':
			MESSAGE_OUTPUT('Wrong','Wrong Region Name')
			return
		Region2URL_DSC(region)
		Outputlist_1=[]
		Outputlist_2=[]
		Output1= DSC1+' reload rule engine '
		Output1= Output1+soap_reload_rule_engine(dsc_url=SURL1)
		Output2= DSC2+' reload rule engine '
		Output2= Output2+soap_reload_rule_engine(dsc_url=SURL1)
		Outputlist_1.append(Output1)
		Outputlist_2.append(Output2)
		LOGTEXT=self.LOG.toPlainText()
		LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
		self.LOG.setPlainText(LOGTEXT)
		BIOUTPUT("Add Decide route to OP",Outputlist_1,Outputlist_2)



	def update_online_info(self,OP):
		RealmName1=''
		NodeRealm1=''
		RealmNameBeforeTranslation1=''
		DRAIMSIPrefix1=''
		result=CCB_ONLINE2CSV()
		ssid="n/a"
		#print(OP)
		for row in result:
			if row['name']==OP:
				ssid=row['id']
				if row['item']=='DRACustomerRealmName':
					RealmName1=JOIN_STR(RealmName1,row['value'],',')
				if row['item']=='CustomerNodeRealm':
					NodeRealm1=JOIN_STR(NodeRealm1,row['value'],',')
				if row['item']=='DRACustomerRealmNameBeforeTranslation':
					RealmNameBeforeTranslation1=JOIN_STR(RealmNameBeforeTranslation1,row['value'],',')
				if row['item']=='DRAIMSIPrefix':
					DRAIMSIPrefix1=JOIN_STR(DRAIMSIPrefix1,row['value'],',')
					
					

		self.SSID.setText(str(ssid))	
		self.DRACustomerRealmName.setText(RealmName1)
		self.DRACustomerNodeName.setText(NodeRealm1)		
		self.DRACustomerRealmNameBeforeTranslation.setText(RealmNameBeforeTranslation1)
		self.IMSI.setText(DRAIMSIPrefix1)
		temp=OP.replace(' ','_').upper()
		LISTNAME='LIST_'+str(ssid)+'_'+temp
		self.LISTNAME.setText(LISTNAME)
		temp=OP.replace(' ','-')
		R2OP_NAME=str(ssid)+'#'+temp
		self.R2OP_NAME.setText(R2OP_NAME)
	def tuggle(self):
		if self.btn_direct.isChecked()==True:
			self.VIRTUAL_REALM.show()
			self.Lable_VIRTUAL_REALM.show()
			MESSAGE_OUTPUT('Prompt','Please input Virtual_Realm name!')
		else:
			self.VIRTUAL_REALM.hide()
			self.VIRTUAL_REALM.setText("")	
					

class ADD_RULE(QWidget):
	def __init__(self,parent=None):
		super(ADD_RULE,self).__init__(parent)
		
		self.Full_list=[]
		for row in DB_sheet:
			self.Full_list.append(row["name"])
			
		QE_length = 400
		QE_hight = 20
		Y_start = 40
		Y_step = 30
		X10 =1080
		X11 = 1160
		X12 = 1240
		X13 = 1240
		distance=550

		
## OPA and OPB
		Y_start=40	
## code for OPA only start
		X1 = 10 #OPA lable start
		X2 = 100#OPA text start
		X3 = 200#labe2 start
		X4 = 250#text2 start

		
		X11 = distance+X1 #OPB start
		X12 = distance+X2

		


		self.Lable_SSID_A = QLabel("SSID_A",self)
		self.Lable_SSID_A.move (X1,Y_start-Y_step)		
		self.SSID_A = QLineEdit(self)
		self.SSID_A.setText("NULL")
		self.SSID_A.setGeometry(QtCore.QRect(X2, Y_start-Y_step, QE_length/4, QE_hight))

		self.Lable_OP_A = QLabel("OP_A",self)
		self.Lable_OP_A.move (X1,Y_start)		
		self.OP_A = QLineEdit(self)
		self.OP_A.setText("*")
		self.OP_A.setGeometry(QtCore.QRect(X2, Y_start, QE_length, QE_hight))

		
		Combo_LIST_A=self.Full_list[:]
		Combo_LIST_A.insert(0,'*')
		self.Combo_Select_A = QComboBox(self)
		for i in Combo_LIST_A:
			self.Combo_Select_A.addItem(i)
		self.Combo_Select_A.move(X2,Y_start+Y_step*1)
		self.Combo_Select_A.setMaxVisibleItems (10)
		self.Combo_Select_A.currentIndexChanged.connect(self.update_A)
		self.OP_A.returnPressed.connect(self.rebuild_A_list)
			
		self.Lable_Realm_A = QLabel("SourceRealm(A)",self)
		self.Lable_Realm_A.move (X1,Y_start+Y_step*2)				
		self.realm_A = QLineEdit(self)
		self.realm_A.setText("*")
		self.realm_A.setGeometry(QtCore.QRect(X2,Y_start+Y_step*2, QE_length, QE_hight))
		
		self.Lable_SSID_B = QLabel("SSID_B",self)
		self.Lable_SSID_B.move (X11,Y_start-Y_step)		
		self.SSID_B = QLineEdit(self)
		self.SSID_B.setText("")
		self.SSID_B.setGeometry(QtCore.QRect(X12, Y_start-Y_step, QE_length/4, QE_hight))

		self.Lable_OP_B = QLabel("OP_B",self)
		self.Lable_OP_B.move (X11,Y_start)		
		self.OP_B = QLineEdit(self)
		self.OP_B.setText("")
		self.OP_B.setGeometry(QtCore.QRect(X12, Y_start, QE_length, QE_hight))
		
		Combo_LIST_B=self.Full_list[:]
		self.Combo_Select_B = QComboBox(self)
		for i in Combo_LIST_B:
			self.Combo_Select_B.addItem(i)
		self.Combo_Select_B.move(X12,Y_start+Y_step*1)
		self.Combo_Select_B.setMaxVisibleItems (10)
		self.Combo_Select_B.currentIndexChanged.connect(self.update_B)
		self.OP_B.returnPressed.connect(self.rebuild_B_list)
			
		self.Lable_Realm_B = QLabel("DestRealm(B)",self)
		self.Lable_Realm_B.move (X11,Y_start+Y_step*2)				
		self.realm_B = QLineEdit(self)
		self.realm_B.setText("")
		self.realm_B.setGeometry(QtCore.QRect(X12,Y_start+Y_step*2, QE_length, QE_hight))
		
		self.Lable_Region = QLabel("Region",self)
		self.Lable_Region.move (X1,Y_start+Y_step*3)
		
		self.Combo_Region = QComboBox(self)
		self.Combo_Region.addItem('')
		for i in RegionList:
			self.Combo_Region.addItem(i)
		self.Combo_Region.setCurrentIndex(0)
		self.Combo_Region.move(X2,Y_start+Y_step*3)
		self.Combo_Region.setMaxVisibleItems (4)
		self.Combo_Region.currentIndexChanged.connect(self.update_Scenario)
		self.Combo_Region.currentIndexChanged.connect(self.update_CondCons)


		self.Lable_Scenario = QLabel("Scenario",self)
		self.Lable_Scenario.move (X3,Y_start+Y_step*3)
		
		self.Combo_Scenario = QComboBox(self)
		self.Combo_Scenario.setMaxVisibleItems (4)
		self.Combo_Scenario.addItem('Please Select Scenario')		
		self.Combo_Scenario.move(X4,Y_start+Y_step*3)
		self.Combo_Scenario.setMaxVisibleItems (10)
		self.Combo_Scenario.currentIndexChanged.connect(self.update_CondCons)	
		
		self.Lable_VRB = QLabel("Virtual Realm B",self)
		self.Lable_VRB.move (X11,Y_start+Y_step*3)
		self.VRB = QLineEdit(self)
		self.VRB.setText("")
		self.VRB.setGeometry(QtCore.QRect(X12, Y_start+Y_step*3, QE_length, QE_hight))
		self.VRB.returnPressed.connect(self.update_VRB)

		self.Lable_Condition = QLabel("Condition",self)
		self.Lable_Condition.move(X1,Y_start+Y_step*4)		
		self.Condition = QTextEdit(self)
		self.Condition.setText("")
		self.Condition.setGeometry(QtCore.QRect(X2,Y_start+Y_step*4, QE_length, QE_hight*4))
		
		self.Lable_Consequence = QLabel("Consequence",self)
		self.Lable_Consequence.move(X1,Y_start+Y_step*7)		
		self.Consequence = QTextEdit(self)
		self.Consequence.setText("")
		self.Consequence.setGeometry(QtCore.QRect(X2,Y_start+Y_step*7, QE_length, QE_hight*4))
		
		self.Lable_Origin_Host = QLabel("Origin_Host",self)
		self.Lable_Origin_Host.move (X1,Y_start+Y_step*10)				
		self.Origin_Host = QLineEdit(self)
		self.Origin_Host.setText("*")
		self.Origin_Host.setGeometry(QtCore.QRect(X2,Y_start+Y_step*10, QE_length, QE_hight))
		
		self.Lable_Dest_Host = QLabel("Dest_Host",self)
		self.Lable_Dest_Host.move (X1,Y_start+Y_step*11)				
		self.Dest_Host = QLineEdit(self)
		self.Dest_Host.setText("*")
		self.Dest_Host.setGeometry(QtCore.QRect(X2,Y_start+Y_step*11, QE_length, QE_hight))
		
		self.Lable_SRC_Peer = QLabel("SRC_Peer",self)
		self.Lable_SRC_Peer.move (X1,Y_start+Y_step*12)				
		self.SRC_Peer = QLineEdit(self)
		self.SRC_Peer.setText("*")
		self.SRC_Peer.setGeometry(QtCore.QRect(X2,Y_start+Y_step*12, QE_length, QE_hight))
		
		self.Lable_SRC_Realm = QLabel("SRC_Realm",self)
		self.Lable_SRC_Realm.move (X1,Y_start+Y_step*13)				
		self.SRC_Realm = QLineEdit(self)
		self.SRC_Realm.setText("*")
		self.SRC_Realm.setGeometry(QtCore.QRect(X2,Y_start+Y_step*13, QE_length, QE_hight))

		self.Lable_Type = QLabel("Type",self)
		self.Lable_Type.move (X1,Y_start+Y_step*14)				
		self.Type = QComboBox(self)
		self.Type.setGeometry(QtCore.QRect(X2,Y_start+Y_step*14, QE_length, QE_hight))
		for row in RULE_TYPE:
			self.Type.addItem(row)
		
		self.Lable_Appid = QLabel("Appid",self)
		self.Lable_Appid.move (X1,Y_start+Y_step*15)				
		self.Appid = QLineEdit(self)
		self.Appid.setText("16777251")
		self.Appid.setGeometry(QtCore.QRect(X2,Y_start+Y_step*15, QE_length, QE_hight))
		
		self.Lable_Priority = QLabel("Priority",self)
		self.Lable_Priority.move (X1,Y_start+Y_step*16)				
		self.Priority = QLineEdit(self)
		self.Priority.setText("10")
		self.Priority.setGeometry(QtCore.QRect(X2,Y_start+Y_step*16, QE_length, QE_hight))
		
	
		self.Description = QTextEdit(self)
		self.Description.setText("")
		self.Description.setGeometry(QtCore.QRect(X2,Y_start+Y_step*17, QE_length, QE_hight*4))
		
		self.Build_Description = QPushButton('Build_Description',self)
		self.Build_Description.move(X1,Y_start+Y_step*17)
		self.Build_Description.clicked.connect(self.BD_Description)
		
		self.Provision = QPushButton('Provision',self)
		self.Provision.move(X1,Y_start+Y_step*20)
		self.Provision.clicked.connect(lambda:self.provsion())
		
		self.Reload = QPushButton('Reload Rule Engine',self)
		self.Reload.move(X2,Y_start+Y_step*20)
		self.Reload.clicked.connect(lambda:self.reload_rule_engine())
		
		self.Lable_LOG = QLabel("LOG",self)
		self.Lable_LOG.move (X11,Y_start+Y_step*4)		
		self.LOG = QTextEdit(self)
		self.LOG.setGeometry(QtCore.QRect(X12, Y_start+Y_step*4, QE_length*1.5, QE_hight*25))
		
		self.rule_email = QPushButton('Email',self)
		self.rule_email.move(X11,Y_start+Y_step*5)
		self.rule_email.clicked.connect(lambda:self.email())
		
	def email(self):
		Tolist='DSS_Route_Provision@syniverse.com'
		Subject=EmailTitleHeader+'Add Rule '+self.OP_A.text()+'-'+self.OP_B.text()
		email_body=MERGE_SUCCESS(self.LOG.toPlainText())
		sende_plain_mail(Tolist,'',Subject,email_body)

	def provsion(self):
		
		if self.Combo_Region.currentText()!='AP' and self.Combo_Region.currentText()!='EU' and self.Combo_Region.currentText()!='NA':
			MESSAGE_OUTPUT("ERROR","NO REGION Selected!")
			return
		if self.realm_A.text()=='':
			MESSAGE_OUTPUT("ERROR","SOURCE REALM(A) EMPTY!")
			return
		if self.realm_B.text()=='':
			MESSAGE_OUTPUT("ERROR","SOURCE REALM(B) EMPTY!")
			return
		if self.Description.toPlainText()=='':
			MESSAGE_OUTPUT("ERROR","description EMPTY!")
			return
		if self.Condition.toPlainText()=='':
			MESSAGE_OUTPUT("ERROR","Condition EMPTY!")
		if self.Consequence.toPlainText()=='':
			MESSAGE_OUTPUT("ERROR","Consequence EMPTY!")
			return
		
		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(self.Combo_Region.currentText())
		realm_a_list=SPLIT2LIST(self.realm_A.text())
		realm_b_list=SPLIT2LIST(self.realm_B.text())
		for realm_a in realm_a_list:
			for realm_b in realm_b_list:
#V=def soap_add_rule(dsc_url,ruletype,description,pop_name,orighost="*",origrealm="*",desthost="*",destrealm="*",srchost="*",srcrealm="*",priority="10",condition="1",consequence="RET := 0"):
				temp_cons=self.Consequence.toPlainText()
				Output1=DSC1+' '+self.Type.currentText()+' from '+self.OP_A.text()+' '+realm_a+' to '+self.OP_B.text()+' '+realm_b+' cond: '+self.Condition.toPlainText()+' cons '+ self.Consequence.toPlainText()
				Output1=Output1+' : '+soap_add_rule(dsc_url=SURL1,ruletype=self.Type.currentText(),description=self.Description.toPlainText()\
,pop_name=POP,orighost=self.Origin_Host.text(),origrealm=realm_a,desthost=self.Dest_Host.text(),destrealm=realm_b,\
srchost=self.Origin_Host.text(),srcrealm=self.SRC_Realm.text(),priority=self.Priority.text(),condition=self.Condition.toPlainText(),consequence=self.Consequence.toPlainText())

				Output2=DSC2+' '+self.Type.currentText()+' from '+self.OP_A.text()+' '+realm_a+' to '+self.OP_B.text()+' '+realm_b+' cond: '+self.Condition.toPlainText()+' cons '+ self.Consequence.toPlainText()
				Output2=Output2+' : '+soap_add_rule(dsc_url=SURL2,ruletype=self.Type.currentText(),description=self.Description.toPlainText()\
,pop_name=POP,orighost=self.Origin_Host.text(),origrealm=realm_a,desthost=self.Dest_Host.text(),destrealm=realm_b,\
srchost=self.Origin_Host.text(),srcrealm=self.SRC_Realm.text(),priority=self.Priority.text(),condition=self.Condition.toPlainText(),\
consequence=self.Consequence.toPlainText())

				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)		
				
		BIOUTPUT("Add Rule",Outputlist_1,Outputlist_2)

		
	def reload_rule_engine(self):
		
		if self.Combo_Region.currentText()!='AP' and self.Combo_Region.currentText()!='EU' and self.Combo_Region.currentText()!='NA':
			MESSAGE_OUTPUT("ERROR","NO REGION Selected!")
			return

		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(self.Combo_Region.currentText())
		Output1=DSC1+' reload rule engine '
		Output1=Output1+soap_reload_rule_engine(SURL1)
		Output2=DSC2+' reload rule engine '
		Output2=Output2+soap_reload_rule_engine(SURL2)

		Outputlist_1.append(Output1)
		Outputlist_2.append(Output2)
		LOGTEXT=self.LOG.toPlainText()
		LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
		self.LOG.setPlainText(LOGTEXT)		
				
		BIOUTPUT("Reload Rule engine",Outputlist_1,Outputlist_2)

		
	def BD_Description(self):
		DESC_A = self.OP_A.text()+' SSID '+self.SSID_A.text()
		if self.SSID_A.text()== 'NULL':
			DESC_A=' any '
		DESC_B = self.OP_B.text()+' SSID '+self.SSID_B.text()
		DESC='%'+self.Type.currentText()+'% from '+DESC_A+' to '+DESC_B
		DESC=replace_invalid_letter(DESC)
		self.Description.setPlainText(DESC)



	def update_CondCons(self):
		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_Region.currentText():
				if row['TYPE']==self.Combo_Scenario.currentText():
					self.Consequence.setText(row['CONSEQUENCE'])
					if self.VRB.text()=='' and '#REPLACEME#' in self.Consequence.toPlainText():
						MESSAGE_OUTPUT('Wrong Parameter','Virtual RealmB is empty!')
					else:
						self.Consequence.setText(row['CONSEQUENCE'].replace('#REPLACEME#',self.VRB.text()))
					self.Condition.setText(row['CONDITION'])

	
	def update_VRB(self):
		if '#REPLACEME#' in self.Consequence.toPlainText() and self.VRB.text()!='':
			self.Consequence.setText(self.Consequence.toPlainText().replace('#REPLACEME#',self.VRB.text()))
			
	def update_Scenario(self):
		self.Combo_Scenario.clear()
		self.Combo_Scenario.addItem('Please Select Scenario')

		for row in DECIDEROUTEPOLICY:
			if row['REGION']==self.Combo_Region.currentText():
				self.Combo_Scenario.addItem(row['TYPE'])
				
	def update_A(self,ii):
		OPA_Name = self.Combo_Select_A.currentText()
		self.OP_A.setText(OPA_Name)
		for row in DB_sheet:
			if row["name"] == OPA_Name:
				self.SSID_A.setText(row["ssid"])
				self.realm_A.setText(row["realm_name"])
			if OPA_Name == '*':
				self.SSID_A.setText('NULL')
				self.realm_A.setText('*')
		self.BD_Description()				
	def update_B(self,ii):
		OPB_Name = self.Combo_Select_B.currentText()
		self.OP_B.setText(OPB_Name)

		for row in DB_sheet:
			if row["name"] == OPB_Name:
				self.SSID_B.setText(row["ssid"])
				self.realm_B.setText(row["realm_name"])
		self.BD_Description()


	def rebuild_A_list(self):
		list=[]
		self.Full_list2=[]
		self.Full_list2=self.Full_list[:]
		self.Full_list2.insert(0,"*")
		key= self.OP_A.text()
		for OP in self.Full_list2:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_A.clear()
		#list.insert(0,'*')
		for i in list:
			self.Combo_Select_A.addItem(i)

	def rebuild_B_list(self):
		list=[]
		key= self.OP_B.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.Combo_Select_B.clear()
		for i in list:
			self.Combo_Select_B.addItem(i)


class UPD_RMT_ROUTE(QMainWindow, Ui_UPD_RMT_ROUTE):

	def __init__(self, parent=None):    
		super(UPD_RMT_ROUTE, self).__init__(parent)
		self.setupUi(self)
		
		self.tableWidget.setColumnWidth(0,30)
		self.tableWidget.setColumnWidth(1,200)
		self.tableWidget.setColumnWidth(2,30)
		self.tableWidget.setColumnWidth(3,200)
		self.tableWidget.setColumnWidth(4,300)
		self.tableWidget.setColumnWidth(5,50)
		self.tableWidget.setColumnWidth(6,180)
		self.tableWidget.setColumnWidth(7,180)
		self.EMAIL_2.hide()
		self.PROVISION.clicked.connect(lambda:self.pro())
		self.EMAIL.clicked.connect(lambda:self.eml())
		self.RELOAD_LIST.clicked.connect(lambda:Reload_Region_LIST(self.REGION_SELECT.currentText()))
		self.INPUT.clicked.connect(lambda:self.input_entry())
		self.EMAIL_2.clicked.connect(lambda:self.eml2())
#inital self.OP_SELECT
		self.Full_list=[]
		for row in DB_sheet:
			self.Full_list.append(row["name"])
		for i in self.Full_list:
			self.OP_SELECT.addItem(i)
#select OP function
		self.OP_SELECT.currentIndexChanged.connect(self.update_A)
		self.OP.returnPressed.connect(self.rebuild_A_list)
		self.BUILD.clicked.connect(self.build_table)

	def input_entry(self):
		self.tableWidget.hide()
		self.EMAIL.hide()
		self.EMAIL_2.show()
		global function
		function='FREE'
#build table
	def build_table(self):
		self.EMAIL_2.hide()
		self.EMAIL.show()
		global function
		function='RMT'
		self.tableWidget.show()
		results=READ_RMT_ROUTE(self.OP.text())
		item = QTableWidgetItem("1,1")
		#self.tableWidget.setItem(1,1,item)
		rowindex=0
		dra=''
		hub=''
		info=''
		for row in results:
			for record in DB_sheet:
				if record["name"] == row['r_name']:
					dra = record["dra"]
					hub = record["hub_policy"]
					realms=record["realm_name"]
			info=dra
			if dra=="":
				info=hub
					
			item0=QTableWidgetItem('Y')
			item1=QTableWidgetItem(row['r_name'])
			item3=QTableWidgetItem(info)
			item4=QTableWidgetItem(realms)
			
			self.tableWidget.setItem(rowindex,0,item0)
			self.tableWidget.setItem(rowindex,1,item1)
			self.tableWidget.setItem(rowindex,3,item3)
			self.tableWidget.setItem(rowindex,4,item4)
			self.btn=QPushButton(str(rowindex))
			self.btn.clicked.connect(lambda:self.showpos())
			self.tableWidget.setCellWidget(rowindex,2,self.btn)
			#https://www.cnblogs.com/yuanlipu/p/7492260.html
			rowindex=rowindex+1
		self.tableWidget.setRowCount(rowindex)
		
	def pro(self):
		if self.REGION_SELECT.currentText()!='AP' and self.REGION_SELECT.currentText()!='EU' and self.REGION_SELECT.currentText()!='NA':
			QMessageBox.information(self,"Warning","Please select region",QMessageBox.Ok)
			return()
		if self.OP_LIST.text()=='':
			QMessageBox.information(self,"Warning","Empty LIST name",QMessageBox.Ok)
			return()

		if function=='RMT':
			try:
				c=self.tableWidget.item(0,0).text()
				realm_list=[]

				Region2URL_DSC(self.REGION_SELECT.currentText())
				for task in range(self.tableWidget.rowCount()):
					c=self.tableWidget.item(task,0).text()
					if c=='Y':
						result1=''
						result2=''
						realms=self.tableWidget.item(task,4).text()
						realm_list = SPLIT2LIST(realms)
						for realm in realm_list:
							result=soap_add_list_cache(self.OP_LIST.text(),realm,SURL1)
							result=result[0]
							result1=result1+result
							result=soap_add_list_cache(self.OP_LIST.text(),realm,SURL2)
							result=result[0]
							result2=result2+result
						itemA=QTableWidgetItem(result1)
						itemB=QTableWidgetItem(result2)
						itemRegion=QTableWidgetItem(self.REGION_SELECT.currentText())
						self.tableWidget.setItem(task,5,itemRegion)
						self.tableWidget.setItem(task,6,itemA)
						self.tableWidget.setItem(task,7,itemB)
			except AttributeError:
				pass
		if function=='FREE':
			Outputlist_1=[]
			Outputlist_2=[]
			Region2URL_DSC(self.REGION_SELECT.currentText())
			entry=[]
			raw=self.INPUT_EDIT.toPlainText()
			raw = raw.lower()
			raw = raw.replace(",",";")
			raw = raw.replace("\r\n",";")
			raw = raw.replace('\n',';')
			if raw[-1]==';':
				raw=raw[:-1]
			if raw[0]==';':
				raw=raw[1:]
			raw_entry=SPLIT2LIST(raw)
			for row in raw_entry:
				if row.strip()!='':
					entry.append(row)
			for row in entry:
				Output1=DSC1+':'+row+'-->'+self.OP_LIST.text()+':'+soap_add_list_cache(self.OP_LIST.text(),row,SURL1)
				Output2=DSC2+':'+row+'-->'+self.OP_LIST.text()+':'+soap_add_list_cache(self.OP_LIST.text(),row,SURL2)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)
				LOGTEXT=self.LOG.toPlainText()
				LOGTEXT=LOGTEXT+'\n'+Output1+'\n'+Output2
				self.LOG.setPlainText(LOGTEXT)
			BIOUTPUT("Add Entry to Listcache",Outputlist_1,Outputlist_2)
				
	def reload_list(self):
		if self.REGION_SELECT.currentText()!='AP' and self.REGION_SELECT.currentText()!='EU' and self.REGION_SELECT.currentText()!='NA':
			QMessageBox.information(self,"Warning","Please select region",QMessageBox.Ok)
			return()
		result=Reload_Region_LIST(self.REGION_SELECT.currentText())
		print(result)
		LOGTEXT=self.LOG.toPlainText()
		LOGTEXT=LOGTEXT+'\n'+result
		self.LOG.setPlainText(LOGTEXT)

	def eml(self):
		body=''
		for task in range(self.tableWidget.rowCount()):
			output=''
			c=self.tableWidget.item(task,0).text()

			if c=='Y':
				output=self.tableWidget.item(task,1).text()+'|'+self.tableWidget.item(task,3).text()+'|'+self.tableWidget.item(task,5).text()+'|'+self.tableWidget.item(task,6).text()+'|'+self.tableWidget.item(task,7).text()+'\n'
				body=body+output
				
		Tolist='DSS_Route_Provision@syniverse.com'
		Subject=EmailTitleHeader+'UPD RMT ROUTE for '+self.OP.text()
		email_body=body
		sende_plain_mail(Tolist,'',Subject,email_body)
		
	def eml2(self):
		Tolist='DSS_Route_Provision@syniverse.com'
		Subject=EmailTitleHeader+'update listcache'+self.OP_LIST.text()
		email_body=MERGE_SUCCESS(self.LOG.toPlainText())
		sende_plain_mail(Tolist,'',Subject,email_body)

	def showpos(self):
		row=(self.sender().text())
		row_num=int(row)
		print(row_num)
		c=self.tableWidget.item(row_num,0).text()
		if c=="Y":
			mark="N"
		if c=="N":
			mark="Y"
		
		item=QTableWidgetItem(mark)
		self.tableWidget.setItem(row_num,0,item)

	def update_A(self,ii):
		OP_Name = self.OP_SELECT.currentText()
		self.OP.setText(OP_Name)
		for row in DB_sheet:
			if row["name"] == OP_Name:
				self.OP_LIST.setText(row["LIST"])
				self.LISTREGION.setText(row["LISTREGION"])
				self.HUB_POLICY.setText(row["hub_policy"])



	def rebuild_A_list(self):
		list=[]
		key= self.OP.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.OP_SELECT.clear()
		for i in list:
			self.OP_SELECT.addItem(i)


		
class ADD_NEW_REALM(QMainWindow, Ui_ADD_NEW_REALM):

	def __init__(self, parent=None):    
		super(ADD_NEW_REALM, self).__init__(parent)
		self.setupUi(self)
		
		self.tableWidget.setColumnWidth(0,200)
		self.tableWidget.setColumnWidth(1,200)
		self.tableWidget.setColumnWidth(2,300)
		self.tableWidget.setColumnWidth(3,50)
		self.tableWidget.setColumnWidth(4,50)
		self.tableWidget.setColumnWidth(5,50)
		self.tableWidget.setColumnWidth(6,60)
		self.tableWidget.setColumnWidth(7,60)
		self.tableWidget.setColumnWidth(8,60)
		self.tableWidget.setColumnWidth(9,60)
		self.tableWidget.setColumnWidth(10,60)
		self.tableWidget.setColumnWidth(11,60)


		self.PROVISION.clicked.connect(lambda:self.pro())
		self.EMAIL.clicked.connect(lambda:self.eml())
		self.RE_AP_LIST.clicked.connect(lambda:Reload_Region_LIST('AP'))
		self.RE_EU_LIST.clicked.connect(lambda:Reload_Region_LIST('EU'))
		self.RE_NA_LIST.clicked.connect(lambda:Reload_Region_LIST('NA'))


#inital self.OP_SELECT
		self.Full_list=[]
		for row in DB_sheet:
			self.Full_list.append(row["name"])
		for i in self.Full_list:
			self.OP_SELECT.addItem(i)
#select OP function
		self.OP_SELECT.currentIndexChanged.connect(self.update_A)
		self.OP.returnPressed.connect(self.rebuild_A_list)
		self.BUILD.clicked.connect(self.build_table)


#build table
	def build_table(self):
		self.tableWidget.show()
		global function

		results=READ_RMT_ROUTE(self.OP.text())
		OP=self.OP.text()
		rowindex=0
		dra=''
		hub=''
		info=''
		for row in results:
			for record in DB_sheet:
				if record["name"] == row['r_name']:
					dra = record["dra"]
					hub = record["hub_policy"]
					LIST=record["LIST"]
					LISTREGION=record['LISTREGION']
			info=dra
			if dra=="":
				info=hub
			item0=QTableWidgetItem(row['r_name'])
			item1=QTableWidgetItem(info)
			item2=QTableWidgetItem(LIST)
			
			self.tableWidget.setItem(rowindex,0,item0)
			self.tableWidget.setItem(rowindex,1,item1)
			self.tableWidget.setItem(rowindex,2,item2)

			self.RG1=QComboBox(self)
			if 'AP' in LISTREGION:
				self.RG1.addItem('AP')
			self.RG2=QComboBox(self)
			if 'EU' in LISTREGION:
				self.RG2.addItem('EU')
			self.RG3=QComboBox(self)
			if 'NA' in LISTREGION:
				self.RG3.addItem('NA')

			self.RG1.addItem('-')
			self.RG2.addItem('-')
			self.RG3.addItem('-')

			self.tableWidget.setCellWidget(rowindex,3,self.RG1)
			self.tableWidget.setCellWidget(rowindex,4,self.RG2)
			self.tableWidget.setCellWidget(rowindex,5,self.RG3)
			#https://www.cnblogs.com/yuanlipu/p/7492260.html
			rowindex=rowindex+1
		self.tableWidget.setRowCount(rowindex)
		
	def pro(self):
		realm_list=[]
		realms=self.NEW_REALMS.text().strip()
		realm_list=SPLIT2LIST(realms)

		try:
			c=self.tableWidget.item(0,0).text()

			for task in range(self.tableWidget.rowCount()):
				listcachename=self.tableWidget.item(task,2).text().strip()
				if self.tableWidget.cellWidget(task,3).currentText()=='AP':
					Result1=''
					Result2=''
					Region2URL_DSC("AP")
					for realm in realm_list:
						response1=soap_add_list_cache(listcachename,realm,SURL1)
						if 'success' in response1.lower():
							Result1=Result1+'S'
						if 'fail' in response1.lower():
							Result1=Result1+'F'
						response2=soap_add_list_cache(listcachename,realm,SURL2)
						if 'success' in response1.lower():
							Result2=Result2+'S'
						if 'fail' in response1.lower():
							Result2=Result2+'F'
						itemA=QTableWidgetItem(Result1)
						itemB=QTableWidgetItem(Result2)
						self.tableWidget.setItem(task,6,itemA)
						self.tableWidget.setItem(task,7,itemB)

				if self.tableWidget.cellWidget(task,4).currentText()=='EU':
					Result1=''
					Result2=''
					Region2URL_DSC("EU")
					for realm in realm_list:
						response1=soap_add_list_cache(listcachename,realm,SURL1)
						if 'success' in response1.lower():
							Result1=Result1+'S'
						if 'fail' in response1.lower():
							Result1=Result1+'F'
						response2=soap_add_list_cache(listcachename,realm,SURL2)
						if 'success' in response1.lower():
							Result2=Result2+'S'
						if 'fail' in response1.lower():
							Result2=Result2+'F'
						itemA=QTableWidgetItem(Result1)
						itemB=QTableWidgetItem(Result2)
						self.tableWidget.setItem(task,8,itemA)
						self.tableWidget.setItem(task,9,itemB)
						
				if self.tableWidget.cellWidget(task,5).currentText()=='NA':
					Result1=''
					Result2=''
					Region2URL_DSC("NA")
					for realm in realm_list:
						response1=soap_add_list_cache(listcachename,realm,SURL1)
						if 'success' in response1.lower():
							Result1=Result1+'S'
						if 'fail' in response1.lower():
							Result1=Result1+'F'
						response2=soap_add_list_cache(listcachename,realm,SURL2)
						if 'success' in response1.lower():
							Result2=Result2+'S'
						if 'fail' in response1.lower():
							Result2=Result2+'F'
						itemA=QTableWidgetItem(Result1)
						itemB=QTableWidgetItem(Result2)
						self.tableWidget.setItem(task,10,itemA)
						self.tableWidget.setItem(task,11,itemB)

		except AttributeError:
			pass

			
	def reload_list(self):
		if self.REGION_SELECT.currentText()!='AP' and self.REGION_SELECT.currentText()!='EU' and self.REGION_SELECT.currentText()!='NA':
			QMessageBox.information(self,"Warning","Please select region",QMessageBox.Ok)
			return()
		Reload_Region_LIST(self.REGION_SELECT.currentText())

	def eml(self):
		body=''
		for task in range(self.tableWidget.rowCount()):
			output=''
			c=self.tableWidget.item(task,0).text()

			if c=='Y':
				output=self.tableWidget.item(task,1).text()+'|'+self.tableWidget.item(task,3).text()+'|'+self.tableWidget.item(task,5).text()+'|'+self.tableWidget.item(task,6).text()+'|'+self.tableWidget.item(task,7).text()+'\n'
				body=body+output
				
		Tolist='DSS_Route_Provision@syniverse.com'
		Subject=EmailTitleHeader+'ADD NEW REALM for '+self.OP.text()
		email_body=body
		sende_plain_mail(Tolist,'',Subject,email_body)

	def showpos(self):
		row=(self.sender().text())
		row_num=int(row)
		print(row_num)
		c=self.tableWidget.item(row_num,0).text()
		if c=="Y":
			mark="N"
		if c=="N":
			mark="Y"
		
		item=QTableWidgetItem(mark)
		self.tableWidget.setItem(row_num,0,item)

	def update_A(self,ii):
		OP_Name = self.OP_SELECT.currentText()
		self.OP.setText(OP_Name)
		for row in DB_sheet:
			if row["name"] == OP_Name:
				self.OP_LIST.setText(row["LIST"])
				self.REALMS.setText(row["realm_name"])

	def rebuild_A_list(self):
		list=[]
		key= self.OP.text()
		for OP in self.Full_list:
			if key.lower() in OP.lower():
				list.append(OP)
		self.OP_SELECT.clear()
		for i in list:
			self.OP_SELECT.addItem(i)


class SECURITY_FILTER(QMainWindow, Ui_SECURITY_FILTER):

	def __init__(self, parent=None):    
		super(SECURITY_FILTER, self).__init__(parent)
		self.setupUi(self)
		global SDB
		SDB=csv2dict('.\\file\security_filter.csv')
		
		self.OP_NAME.activated.connect(self.update_OP)
		self.OP_NAME.activated.connect(self.update_filter)
		
		self.MAP_ADD.clicked.connect(lambda:self.ADD_MAPCACHE(self.MAP_REGION.currentText(),self.MAPCAHCE.text(),self.MAPCACHE_KEY.toPlainText(),self.MAPCACHE_VALUE.toPlainText()))
		self.TWO_D_LIST_ADD.clicked.connect(lambda:self.ADD_2D_LISTCACHE(self.TWO_D_LIST_REGION.currentText(),self.TWO_D_LISTCACHE.text(),self.TWO_D_LIST_VALUE1.toPlainText(),self.TWO_D_LIST_VALUE2.toPlainText()))
		self.TWO_D_MAP_ADD.clicked.connect(lambda:self.ADD_2D_MAPCACHE(self.TWO_D_MAP_REGION.currentText(),self.TWO_D_MAPCACHE.text(),self.TWO_D_MAP_KEY1.toPlainText(),self.TWO_D_MAP_KEY2.toPlainText(),self.TWO_D_MAP_VALUE.text()))
		self.LIST_ADD.clicked.connect(lambda:self.ADD_REALMS2LIST(self.LIST_REGION.currentText(),self.LIST_VALUE.toPlainText(),self.LISTCACHE.text()))
		
		self.MAP_CHECK.clicked.connect(lambda:(self.CHECK_MAPCACHE(self.MAP_REGION.currentText(),self.MAPCAHCE.text(),self.MAPCACHE_KEY.toPlainText(),'.\\file\mapcache.csv')))
		self.TWO_D_LIST_CHECK.clicked.connect(lambda:(self.CHECK_2D_LISTCACHE(self.TWO_D_LIST_REGION.currentText(),self.TWO_D_LISTCACHE.text(),self.TWO_D_LIST_VALUE1.toPlainText())))
		self.LIST_CHECK.clicked.connect(lambda:(self.CHECK_LISTCACHE(self.LIST_REGION.currentText(),self.LISTCACHE.text(),self.LIST_VALUE.toPlainText())))
		self.TWO_D_MAP_CHECK.clicked.connect(lambda:(self.CHECK_2D_MAPCACHE(self.TWO_D_MAP_REGION.currentText(),self.TWO_D_MAPCACHE.text(),self.TWO_D_MAP_KEY1.toPlainText())))

		self.RMT_FILTER_NAME.currentIndexChanged.connect(self.update_filter)
		self.RMT_FILTER_NAME.addItem("")
		for row in SDB:
			if "Mandantary" not in row['Type']:
				self.RMT_FILTER_NAME.addItem(row["Filter Name in RMT"])
		region_list=['LAB','AP','EU','NA']
		for region in region_list:
			self.MAP_REGION.addItem(region)
			self.TWO_D_LIST_REGION.addItem(region)
			self.TWO_D_MAP_REGION.addItem(region)
			self.LIST_REGION.addItem(region)
	def update_OP(self):
		OP_name=self.OP_NAME.currentText()
		self.OP_NAME.clear()
		for row in DB_sheet:
			if OP_name.lower() in row["name"].lower():
				self.OP_NAME.addItem(row["name"])
		for row in DB_sheet:
			if row["name"].lower() == OP_name.lower():
				self.REALMS.setText(row["realm_name"])
				self.IMSIS.setText(row["imsi_prefix"])
				
				self.MAP_REGION.setCurrentIndex(0)
				self.TWO_D_LIST_REGION.setCurrentIndex(0)
				self.TWO_D_MAP_REGION.setCurrentIndex(0)
				self.LIST_REGION.setCurrentIndex(0)

	def update_filter(self):
		if self.RMT_FILTER_NAME.currentText()=='':
			return
		global SDB
		for row in SDB:
			if row['Filter Name in RMT']==self.RMT_FILTER_NAME.currentText():
				self.FILTER_TYPE.setText(row['Type'])
				self.FILTER_DIRECTION.setText(row['Filter Direction'])
				self.FILTER_DESCRIPTION.setPlainText(row['Description'])
				self.TABLE_NAME_A.setText(row['Table Name A'])
				self.TABLE_TYPE_A.setText(row['Table Type A'])
				self.KEY1_ALIAS_A.setText(row['Key1 Alias A'])
				self.VALUE_ALIAS_A.setText(row['Value Alias A'])
				self.KEY2_ALIAS_A.setText(row['Key2 Alias A'])
				
				self.TABLE_NAME_B.setText(row['Table Name B'])
				self.TABLE_TYPE_B.setText(row['Table Type B'])
				self.KEY1_ALIAS_B.setText(row['Key1 Alias B'])
				self.VALUE_ALIAS_B.setText(row['Value Alias B'])
				self.KEY2_ALIAS_B.setText(row['Key2 Alias B'])

				self.MAP_REGION.setCurrentIndex(0)
				self.TWO_D_LIST_REGION.setCurrentIndex(0)
				self.TWO_D_MAP_REGION.setCurrentIndex(0)
				self.LIST_REGION.setCurrentIndex(0)
				
				self.MAPCACHE_KEY.setPlainText("")
				self.MAPCACHE_VALUE.setPlainText("")
				self.TWO_D_LIST_VALUE1.setPlainText("")
				self.TWO_D_LIST_VALUE2.setPlainText("")
				self.TWO_D_MAP_KEY1.setPlainText("")
				self.TWO_D_MAP_KEY2.setPlainText("")
				self.TWO_D_MAP_VALUE.setText("")
				self.LIST_VALUE.setPlainText("")
				
				self.MAPCAHCE.setText("")
				self.TWO_D_LISTCACHE.setText("")
				self.TWO_D_MAPCACHE.setText("")
				self.TWO_D_MAPCACHE.setText("")
				#below is a simple logic based on phase1 security filters
				if self.TABLE_NAME_A.text().startswith("MAP"):
					self.MAPCAHCE.setText(self.TABLE_NAME_A.text())
					self.TWO_D_LISTCACHE.setText(self.TABLE_NAME_B.text())
					self.MAPCACHE_KEY.setText(self.REALMS.text())
					self.MAPCACHE_VALUE.setText("WILL_LOG = 1, RET:5003")

				if self.TABLE_NAME_A.text().startswith("DUALPREFIXMAP"):
					self.TWO_D_MAPCACHE.setText(self.TABLE_NAME_A.text())
					self.TWO_D_MAP_KEY1.setText(self.REALMS.text())
					self.TWO_D_MAP_KEY2.setText(self.IMSIS.text())
					self.TWO_D_MAP_VALUE.setText("WILL_LOG = 1, RET:5003")
					
				if self.TWO_D_LISTCACHE.text()=='DUALPREFIXLIST_SRC_ORIGIN_REALM_WL':
					self.TWO_D_LIST_VALUE1.setText(self.REALMS.text())
					self.TWO_D_LIST_VALUE2.setText(self.REALMS.text())
					MESSAGE_OUTPUT("Warning","This config may lead to message from OP peer rejected.\
					\nmake sure to check 1 weeks TDR to ensure\
					\nno other realm from the peer in addtion to default value2s\
					\nPrivate realm modified by request filter can be ignored\
					\nThis config must double reviewed by team leader")

				
	def ADD_MAPCACHE(self,region,mapcache_name,keys,values):
		value_list=[]
		key_list=[]
		if keys=='':
			MESSAGE_OUTPUT('Wrong','No Key')
			return
		if values=='':
			MESSAGE_OUTPUT('Wrong','No Value')
			return
		
		if "WILL_LOG" in values:
			value_list.append(values)
		else:
			value_list=string2list(values)
		
		key_list=string2list(keys)

		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		entry=[]


		for key in key_list:
			for value in value_list:
				Output1=DSC1+' '+key+'->'+value+'->'+mapcache_name+'\n'
				Output1=Output1+soap_add_mapcache(SURL1,mapcache_name,key,value)
				Output2=DSC2+' '+key+'->'+value+'->'+mapcache_name+'\n'
				Output2=Output2+soap_add_mapcache(SURL2,mapcache_name,key,value)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)

		BIOUTPUT(mapcache_name,Outputlist_1,Outputlist_2)
		
	def ADD_2D_LISTCACHE(self,region,listcache_name,value1s,value2s):
		value1_list=[]
		value2_list=[]
		if value1s=='':
			MESSAGE_OUTPUT('Wrong','No value1s')
			return
		if value2s=='':
			MESSAGE_OUTPUT('Wrong','No value2s')
			return
		
		if "WILL_LOG" in value1s:
			value1_list.append(value1s)
		else:
			value1_list=string2list(value1s)

		value2_list=string2list(value2s)

		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		entry=[]
		for value1 in value1_list:
			for value2 in value2_list:
				Output1=DSC1+' '+value1+'->'+value2+'->'+listcache_name+'\n'
				Output1=Output1+soap_add_2d_listcache(SURL1,listcache_name,value1,value2)
				Output2=DSC2+' '+value1+'->'+value2+'->'+listcache_name+'\n'
				Output2=Output2+soap_add_2d_listcache(SURL2,listcache_name,value1,value2)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)

		BIOUTPUT(listcache_name,Outputlist_1,Outputlist_2)
		
	def ADD_2D_MAPCACHE(self,region,name,key1s,key2s,value):
		key1_list=[]
		key2_list=[]
		if key1s=='':
			MESSAGE_OUTPUT('Wrong','No key1s')
			return
		if key2s=='':
			MESSAGE_OUTPUT('Wrong','No key2s')
			return
		
		key1_list=string2list(key1s)		
		key2_list=string2list(key2s)

		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		entry=[]
		for key1 in key1_list:
			for key2 in key2_list:
				Output1=DSC1+' '+key1+'-'+key2+'->'+name+'\n'
				Output1=Output1+soap_add_2d_mapcache(SURL1,name,key1,key2,value)
				Output2=DSC2+' '+key1+'-'+key2+'->'+name+'\n'
				Output2=Output2+soap_add_2d_mapcache(SURL2,name,key1,key2,value)
				Outputlist_1.append(Output1)
				Outputlist_2.append(Output2)

		BIOUTPUT(name,Outputlist_1,Outputlist_2)
		
	def CHECK_LISTCACHE(self,region,listcache_name,values_to_check=''):
		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		result_list_1=soap_query_listcache(SURL1,listcache_name)
		result_list_2=soap_query_listcache(SURL1,listcache_name)
		if values_to_check=='':
			for row in result_list_1:
				Output1=DSC1+" "+row
				Outputlist_1.append(Output1)
			for row in result_list_2:
				Output2=DSC2+" "+row
				Outputlist_2.append(Output1)
			BIOUTPUT(listcache_name,Outputlist_1,Outputlist_2)
					
			
		else:
			check_list=SPLIT2LIST(values_to_check)
			for check_item in check_list:
				found=0
				for row in result_list_1:
					if row.lower()==check_item.lower():
						found=1
				if found==1:
					Output1=DSC1+" "+check_item+" Y"
				else:
					Output1=DSC1+" "+check_item+" N"
				Outputlist_1.append(Output1)

			for check_item in check_list:
				found=0
				for row in result_list_2:
					if row.lower()==check_item.lower():
						found=1
				if found==1:
					Output1=DSC2+" "+check_item+" Y"
				else:
					Output1=DSC2+" "+check_item+" N"
				Outputlist_2.append(Output1)
				
			BIOUTPUT(listcache_name,Outputlist_1,Outputlist_2)
		
	def CHECK_MAPCACHE(self,region,mapcache_name,keys,filename):
		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		result_list_1=soap_query_mapcache(SURL1,mapcache_name,filename)
		for row in result_list_1:
			if row['key'].lower() in keys.lower() or keys=='':
				Output1=DSC1+" "+row['key']+" "+row['value']
				Outputlist_1.append(Output1)
				
		result_list_2=soap_query_mapcache(SURL2,mapcache_name,filename)
		for row in result_list_2:
			if row['key'].lower() in keys.lower():
				Output2=DSC1+" "+row['key']+" "+row['value']
				Outputlist_2.append(Output2)
				
		BIOUTPUT(mapcache_name,Outputlist_1,Outputlist_2)
		
	def CHECK_2D_LISTCACHE(self,region,listcache_name,key1s):
		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		result_list_1=soap_query_2d_listcache(SURL1,listcache_name)
		for row in result_list_1:
			if row['key1'].lower() in key1s.lower() or key1s=='':
				Output1=DSC1+" "+row['key1']+" "+row['key2']
				Outputlist_1.append(Output1)
				
		result_list_2=soap_query_2d_listcache(SURL2,listcache_name)
		for row in result_list_2:
			if row['key1'].lower() in key1s.lower() or key1s=='':
				Output2=DSC1+" "+row['key1']+" "+row['key2']
				Outputlist_2.append(Output2)
				
		BIOUTPUT(listcache_name,Outputlist_1,Outputlist_2)
		

	def CHECK_2D_MAPCACHE(self,region,mapcache_name,key1s):
		Outputlist_1=[]
		Outputlist_2=[]
		Region2URL_DSC(region)
		result_list_1=soap_query_2d_mapcache(SURL1,mapcache_name)
		for row in result_list_1:
			if row['key1'].lower() in key1s.lower() or key1s=='':
				Output1=DSC1+" "+row['key1']+" "+row['key2']+row['value']
				Outputlist_1.append(Output1)
				
		result_list_2=soap_query_2d_mapcache(SURL2,mapcache_name)
		for row in result_list_2:
			if row['key1'].lower() in key1s.lower() or key1s=='':
				Output1=DSC2+" "+row['key1']+" "+row['key2']+row['value']
				Outputlist_2.append(Output1)
				
		BIOUTPUT(mapcache_name,Outputlist_1,Outputlist_2)
		

class Confirm_Win(QMainWindow, Ui_Confirm_Window):

	alarms_inputed_signal = pyqtSignal(str)

	def __init__(self, parent=None):    
		super(Confirm_Win, self).__init__(parent)
		self.setupUi(self)

		self.PROCEED.clicked.connect(self.close)
		self.CANCEL.clicked.connect(self.alarms_inputed)

	def alarms_inputed(self):
		self.alarms_inputed_signal.emit(self.textEdit_alarm_content.toPlainText())
		self.close()
	

class RMT_CREDENTIAL(QMainWindow, Ui_RMT_CREDENTIAL):

	def __init__(self, parent=None):    
		super(RMT_CREDENTIAL, self).__init__(parent)
		self.setupUi(self)
		self.confirm.clicked.connect(self.save)

	def save(self):
		global rmt_user
		global rmt_pwd
		rmt_user=self.RMT_USER.text()
		rmt_pwd=self.RMT_PWD.text()
		userinfodirectory=r'file\rmtcredential.txt'
		output = open(userinfodirectory, 'w')
		output.write(rmt_user+' '+rmt_pwd)
		output.close()
		self.close()



class Main_TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(Main_TabWidget, self).__init__(parent)
        self.setWindowTitle("DSS OSS 201800706")
        #self.setStyleSheet("background:lightgrey")
        self.resize(1366, 768)
        self.mContent = OPEN_ROUTE()
        self.mContent2 = OP_Online()
        self.mContent3 = ADD_RULE()
        self.mContent4 = UPD_RMT_ROUTE()
        self.mContent5 = ADD_NEW_REALM()
        self.mContent6 = SECURITY_FILTER()
        self.mIndex = OthersWidget()
        self.mIndex2 = OthersWidget2()
        self.addTab(self.mContent, u"Open Route")
        self.addTab(self.mContent2, u"OP_Online")
        self.addTab(self.mContent3, u"ADD_RULE")
        self.addTab(self.mContent4, u"UPD_RMT_ROUTE")
        self.addTab(self.mContent5, u"ADD_NEW_REALM")
        self.addTab(self.mContent6, u"SECURITY_FILTER")
        self.addTab(self.mIndex, u"Other")
        self.addTab(self.mIndex2, u"Others2")




if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	t = Main_TabWidget()
	t.show()
	rmt_window=RMT_CREDENTIAL()
	# read rmt user and pwd
	if not os.path.exists(r'.\\file\rmtcredential.txt'):
		rmt_window.show()

	if os.path.exists(r'.\\file\rmtcredential.txt'):
		input=open(r'.\\file\rmtcredential.txt')
		info=input.read().split(' ')
		global rmt_user
		global rmt_pwd
		rmt_user= info[0]
		rmt_pwd=info[1]
		input.close()

	app.exec_()



