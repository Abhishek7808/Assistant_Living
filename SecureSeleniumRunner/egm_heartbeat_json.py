import json
import re
import statistics
import sys
import winreg
import os
from configparser import ConfigParser
from datetime import datetime
from datetime import datetime,timezone,timedelta


def json_parse_gateway_profile(json_string):
    """
    Parsing gateway profile json
    :param json_string:
    :return:
    """
    if not json_string:
        return None

    json_string=json_string.replace("'",'"').replace('False','false').replace('True','true').replace('None','null')

    json_string=re.sub(r'/Date\((\d+)\)/',lambda x: str(int(x.group(1))),json_string)

    # Convert the JSON string to a Python dictionary
    print("*****************")
    print(json_string)
    print("********************")
    interval_data=json.loads(json_string)['IntervalData']

    data = json.loads(json_string)
    device_number = data['DeviceNo']

    #interval_data = data
    four_g_count = 0
    two_g_count = 0

    min_rssi,max_rssi,avg_rssi=[],[],[]

    rsrp_min,rsrp_max,rsrp_avg=[],[],[]
    rsrq_min,rsrq_max,rsrq_avg=[],[],[]
    sinr_min,sinr_max,sinr_avg=[],[],[]

    resultant_data = {}

    """with open(file_path,'r') as file:
        interval_data=json.load(file)['IntervalData']
    """
    for data_json in interval_data:
        try:
            print(f"Data json =  {data_json}")
            if data_json['UnregisteredDuration'] == 30:
                min_rssi.append(0)
                max_rssi.append(0)
                avg_rssi.append(0)
                rsrp_min.append(0)
                rsrp_max.append(0)
                rsrp_avg.append(0)
                rsrq_min.append(0)
                rsrq_max.append(0)
                rsrq_avg.append(0)
                sinr_min.append(0)
                sinr_max.append(0)
                sinr_avg.append(0)
            else:

                wan_network_type = data_json['WanNetworkType']

                def extract_numeric(input_str):
                    return ''.join(c for c in input_str if c.isdigit())

                numeric_value_wan_network_type = wan_network_type

                if numeric_value_wan_network_type == 4:
                    four_g_count = four_g_count+1
                elif numeric_value_wan_network_type == 0:
                    two_g_count = two_g_count+1

                rsrp,rsrq,sinr=data_json['RSRP'],data_json['RSRQ'],data_json['SINR']
                rsrp_min.append(rsrp['Min'])
                rsrp_max.append(rsrp['Max'])
                rsrp_avg.append(rsrp['Average'])

                rsrq_min.append(rsrq['Min'])
                rsrq_max.append(rsrq['Max'])
                rsrq_avg.append(rsrq['Average'])

                sinr_min.append(sinr['Min'])
                sinr_max.append(sinr['Max'])
                sinr_avg.append(sinr['Average'])

                min_rssi.append(data_json['MinRssi'])
                max_rssi.append(data_json['MaxRssi'])
                avg_rssi.append(data_json['AvgRssi'])

        except KeyError as e:
            print(f"KeyError: {e} not found in data: {data}")
            exc_type,exc_obj,exc_tb=sys.exc_info()
            fname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type,fname,exc_tb.tb_lineno)

        except Exception as e:
            print(f"Error processing data: {e}")

    def list_average(lst):
        filtered_list=[num for num in lst if num is not None]
        #print(filtered_list)
        return statistics.mean(filtered_list)
    resultant_data['Gateway Number'] = device_number
    resultant_data['Min_RSSI'] = list_average(lst = min_rssi)
    resultant_data['Max_RSSI']=list_average(lst = max_rssi)
    resultant_data['AVG_RSSI']=list_average(lst = avg_rssi)
    resultant_data['RSRP_Min']=list_average(lst = rsrp_min)
    resultant_data['RSRP_Max']=list_average(lst = rsrp_max)
    resultant_data['RSRP_Avg']=list_average(lst = rsrp_avg)
    resultant_data['RSRQ_Min']=list_average(lst = rsrq_min)
    resultant_data['RSRQ_Max']=list_average(lst = rsrq_max)
    resultant_data['RSRQ_Avg']=list_average(lst = rsrq_avg)
    resultant_data['SINR_Min']=list_average(lst = sinr_min)
    resultant_data['SINR_Max']=list_average(lst = sinr_max)
    resultant_data['SINR_Avg']=list_average(lst = sinr_avg)
    resultant_data['4g_count']=four_g_count
    resultant_data['2g_count']=two_g_count


    return resultant_data


#print(json_parse_gateway_profile(file_path = r"C:\Users\44454\Desktop\gross_margin\get_gateway_profile.txt"))

def json_parse_get_heartbeat(json_string):
    """
    Parsing heartbeats json
    :param json_string:
    :return:
    """
    code_json={23400: "BT",23401: "Vectone Mobile-UK",23402: "O2-UK",23403: "Airtel-Vodafone",23404: "FMS Solutions-UK",
               23405: "Colt Mobile",23406: "Internet Computer Bureau Ltd-UK",23407: "C&W Worldwid-UK",
               23408: "OnePhone-UK",23409: "Tismi BV-UK",23410: "O2-UK",23411: "O2-UK",23412: "Railtrack-UK",
               23413: "Railtrack-UK",23414: "Hay Syestems Ltd-UK",23415: "Vodafone-UK",23416: "TalkTalk-UK",
               23417: "FlexTel-UK",23418: "Cloud9-UK",23419: "PMN-UK",23420: "3 Hutchison-UK",
               23422: "RoutoMessaging-UK",23424: "Greenfone-UK",23425: "Truphone-UK",23426: "Lycamobile-UK",
               23427: "Teleena-UK",23430: "T-Mobile-UK",23431: "Virgin Mobile-UK",23432: "Virgin Mobile-UK",
               23433: "Orange-UK",23434: "Orange-UK",23435: "JSC-UK",23436: "C&W Isle of Man-UK",
               23437: "Synectiv Ltd-UK",23450: "JT-UK",23451: "UK Broadband Ltd-UK",23455: "C&W Guernsey-UK",
               23458: "Manx Telecom-UK",23476: "BT-UK",23478: "Airwave-UK",23500: "Mundio Mobile Ltd-UK",23501: "EE-UK",
               23502: "EE-UK",23577: "BT-UK",23591: "Vodafone-UK",23592: "C&W-UK",23594: "3 Hutchison-UK",
               23595: "Railtrack-UK",40401: "Vodafone-Haryana-IN",40402: "AirTel-Punjab-IN",
               40403: "AirTel-Himachal Pradesh-IN",40404: "IDEA-Delhi & NCR-IN",40405: "Vodafone-Gujarat-IN",
               40407: "IDEA-Andhra Pradesh-IN",40409: "Reliance-Assam-IN",40410: "AirTel-Delhi & NCR-IN",
               40411: "Vodafone-Delhi & NCR-IN",40412: "IDEA-Haryana-IN",40413: "Vodafone-Andhra Pradesh-IN",
               40414: "IDEA-Punjab-IN",40415: "Vodafone-Uttar Pradesh (East)-IN",40416: "Airtel-North East-IN",
               40417: "AIRCEL-West Bengal-IN",40418: "Reliance-Himachal Pradesh-IN",40419: "IDEA-Kerala-IN",
               40420: "Vodafone-Mumbai-IN",40421: "Loop Mobile-Mumbai-IN",40422: "IDEA-Maharashtra & Goa-IN",
               40424: "IDEA-Gujarat-IN",40425: "AIRCEL-Bihar-IN",40427: "Vodafone-Maharashtra & Goa-IN",
               40428: "AIRCEL-Orissa-IN",40429: "AIRCEL-Assam-IN",40430: "Vodafone-Kolkata-IN",
               40431: "AirTel-Kolkata-IN",40434: "CellOne-Haryana-IN",40436: "Reliance-Bihar & Jharkhand-IN",
               40437: "Aircel-Jammu & Kashmir-IN",40438: "CellOne-Assam-IN",40440: "AirTel-Chennai-IN",
               40441: "Aircel-Chennai-IN",40442: "Aircel-Tamil Nadu-IN",40443: "Vodafone-Tamil Nadu-IN",
               40444: "IDEA-Karnataka-IN",40445: "Airtel-Karnataka-IN",40446: "Vodafone-Kerala-IN",
               40448: "Dishnet Wireless-Unknown-IN",40449: "Airtel-Andhra Pradesh-IN",40450: "Reliance-North East-IN",
               40451: "CellOne-Himachal Pradesh-IN",40452: "Reliance-Orissa-IN",40453: "CellOne-Punjab-IN",
               40454: "CellOne-Uttar Pradesh (West)-IN",40455: "CellOne-Uttar Pradesh (East)-IN",
               40456: "IDEA-Uttar Pradesh (West)-IN",40457: "CellOne-Gujarat-IN",
               40458: "CellOne-Madhya Pradesh & Chhattisgarh-IN",40459: "CellOne-Rajasthan-IN",
               40460: "Vodafone-Rajasthan-IN",40462: "CellOne-Jammu & Kashmir-IN",40464: "CellOne-Chennai-IN",
               40466: "CellOne-Maharashtra & Goa-IN",40467: "Reliance-Madhya Pradesh & Chhattisgarh-IN",
               40468: "DOLPHIN-Delhi & NCR-IN",40469: "DOLPHIN-Mumbai-IN",40470: "AirTel-Rajasthan-IN",
               40471: "CellOne-Karnataka (Bangalore)-IN",40472: "CellOne-Kerala-IN",40473: "CellOne-Andhra Pradesh-IN",
               40474: "CellOne-West Bengal-IN",40475: "CellOne-Bihar-IN",40476: "CellOne-Orissa-IN",
               40477: "CellOne-North East-IN",40478: "Idea-Madhya Pradesh & Chattishgarh-IN",
               40479: "CellOne-Andaman Nicobar-IN",40480: "CellOne-Tamil Nadu-IN",40481: "CellOne-Kolkata-IN",
               40482: "IDEA-Himachal Pradesh-IN",40483: "Reliance-Kolkata-IN",40484: "Vodafone-Chennai-IN",
               40485: "Reliance-West Bengal-IN",40486: "Vodafone-Karnataka-IN",40487: "IDEA-Rajasthan-IN",
               40488: "Vodafone-Punjab-IN",40489: "Idea-Uttar Pradesh (East)-IN",40490: "AirTel-Maharashtra-IN",
               40491: "AIRCEL-Kolkata-IN",40492: "AirTel-Mumbai-IN",40493: "AirTel-Madhya Pradesh-IN",
               40494: "AirTel-Tamil Nadu-IN",40495: "AirTel-Kerala-IN",40496: "AirTel-Haryana-IN",
               40497: "AirTel-Uttar Pradesh (West)-IN",40498: "AirTel-Gujarat-IN",40501: "Reliance-Andhra Pradesh-IN",
               40503: "Reliance-Bihar-IN",40504: "Reliance-Chennai-IN",40505: "Reliance-Delhi & NCR-IN",
               40506: "Reliance-Gujarat-IN",40507: "Reliance-Haryana-IN",40508: "Reliance-Himachal Pradesh-IN",
               40509: "Reliance-Jammu & Kashmir-IN",40510: "Reliance-Karnataka-IN",40511: "Reliance-Kerala-IN",
               40512: "Reliance-Kolkata-IN",40513: "Reliance-Maharashtra & Goa-IN",40514: "Reliance-Madhya Pradesh-IN",
               40515: "Reliance-Mumbai-IN",40517: "Reliance-Orissa-IN",40518: "Reliance-Punjab-IN",
               40519: "Reliance-Rajasthan-IN",40520: "Reliance-Tamil Nadu-IN",40521: "Reliance-Uttar Pradesh (East)-IN",
               40522: "Reliance-Uttar Pradesh (West)-IN",40523: "Reliance-West Bengal-IN",
               405025: "TATA DOCOMO-Andhra Pradesh-IN",405026: "TATA DOCOMO-Assam-IN",
               405027: "TATA DOCOMO-Bihar/Jharkhand-IN",405028: "TATA DOCOMO-Chennai-IN",405029: "TATA DOCOMO-Delhi-IN",
               405030: "TATA DOCOMO-Gujarat-IN",405031: "TATA DOCOMO-Haryana-IN",
               405032: "TATA DOCOMO-Himachal Pradesh-IN",405033: "TATA DOCOMO-Jammu & Kashmir-IN",
               405034: "TATA DOCOMO-Karnataka-IN",405035: "TATA DOCOMO-Kerala-IN",405036: "TATA DOCOMO-Kolkata-IN",
               405037: "TATA DOCOMO-Maharashtra & Goa-IN",405038: "TATA DOCOMO-Madhya Pradesh-IN",
               405039: "TATA DOCOMO-Mumbai-IN",405041: "TATA DOCOMO-Orissa-IN",405042: "TATA DOCOMO-Punjab-IN",
               405043: "TATA DOCOMO-Rajasthan-IN",405044: "TATA DOCOMO-Tamil Nadu including Chennai-IN",
               405045: "TATA DOCOMO-[Uttar Pradesh (E)]-IN",405046: "TATA DOCOMO-[Uttar Pradesh (W) & Uttarkhand ]-IN",
               405047: "TATA DOCOMO-[West Bengal]-IN",40551: "AirTel-West Bengal-IN",
               40552: "AirTel-Bihar & Jharkhand-IN",40553: "AirTel-Orissa-IN",40554: "AirTel-Uttar Pradesh (East)-IN",
               40555: "Airtel-Jammu & Kashmir-IN",40556: "AirTel-Assam-IN",40566: "Vodafone-Uttar Pradesh (West)-IN",
               40567: "Vodafone-West Bengal-IN",40570: "IDEA-Bihar & Jharkhand-IN",
               405750: "Vodafone-Jammu & Kashmir-IN",405751: "Vodafone-Assam-IN",
               405752: "Vodafone-Bihar & Jharkhand-IN",405753: "Vodafone-Orissa-IN",
               405754: "Vodafone-Himachal Pradesh-IN",405755: "Vodafone-North East-IN",
               405756: "Vodafone-Madhya Pradesh & Chhattisgarh-IN",405799: "IDEA-Mumbai-IN",
               405800: "AIRCEL-Delhi & NCR-IN",405801: "AIRCEL-Andhra Pradesh-IN",405802: "AIRCEL-Gujarat-IN",
               405803: "AIRCEL-Karnataka-IN",405804: "AIRCEL-Maharashtra & Goa-IN",405805: "AIRCEL-Mumbai-IN",
               405806: "AIRCEL-Rajasthan-IN",405807: "AIRCEL-Haryana-IN",405808: "AIRCEL-Madhya Pradesh-IN",
               405809: "AIRCEL-Kerala-IN",405810: "AIRCEL-Uttar Pradesh (East)-IN",
               405811: "AIRCEL-Uttar Pradesh (West)-IN",405812: "AIRCEL-Punjab-IN",405819: "Uninor-Andhra Pradesh-IN",
               405818: "Uninor-Uttar Pradesh (West)-IN",405820: "Uninor-Karnataka-IN",405821: "Uninor-Kerala-IN",
               405822: "Uninor-Kolkata-IN",405824: "Videocon Datacom-Assam-IN",405827: "Videocon Datacom-Gujarat-IN",
               405834: "Videocon Datacom-Madhya Pradesh-IN",405844: "Uninor-Delhi & NCR-IN",
               405840: "Jio-West Bengal-IN",405845: "IDEA-Assam-IN",405846: "IDEA-Jammu & Kashmir-IN",
               405847: "IDEA-Karnataka-IN",405848: "IDEA-Kolkata-IN",405849: "IDEA-North East-IN",
               405850: "IDEA-Orissa-IN",405851: "IDEA-Punjab-IN",405852: "IDEA-Tamil Nadu-IN",
               405853: "IDEA-West Bengal-IN",405854: "Jio-Andra Pradesh-IN",405855: "Jio-Assam-IN",
               405856: "Jio-Bhiar-IN",405857: "Jio-Gujarat-IN",405858: "Jio-Haryana-IN",
               405859: "Jio-Himachal Pradesh-IN",405860: "Jio-Jammu Kashmir-IN",405861: "Jio-Karnataka-IN",
               405862: "Jio-Kerala-IN",405863: "Jio-Madhyya Pradesh-IN",405864: "Jio-Maharashtra-IN",
               405865: "Jio-North East-IN",405866: "Jio-Orissa-IN",405867: "Jio-Punjab-IN",405868: "Jio-Rajasthan-IN",
               405869: "Jio-Tamil Nadu Chennai-IN",405870: "Jio-Uttar Pradesh West-IN",
               405871: "Jio-Uttar Pradesh East-IN",405872: "Jio-Delhi-IN",405873: "Jio-Kolkatta-IN",
               405874: "Jio-Mumbai-IN",405875: "Uninor-Assam-IN",405880: "Uninor-West Bengal-IN",
               405881: "S Tel-Assam-IN",405908: "IDEA-Andhra Pradesh-IN",405909: "IDEA-Delhi-IN",
               405910: "IDEA-Haryana-IN",405911: "IDEA-Maharashtra-IN",405912: "Etisalat DB-Andhra Pradesh-IN",
               405913: "Etisalat DB-Delhi & NCR-IN",405914: "Etisalat DB-Gujarat-IN",405917: "Etisalat DB-Kerala-IN",
               405927: "Uninor-Gujarat-IN",405929: "Uninor-Maharashtra-IN",27201: "Vodafone-IE",27202: "O2-IE",
               27203: "Meteor-IE",27204: "Access Telecom-IE",27205: "Hutchison-IE",27207: "eMobile-IE",
               27209: "Clever Communications-IE",27211: "Liffey Telecom (Tesco)-IE",27213: "Lycamobile-IE",
               50501: "Telstra-AU",50502: "Optus-AU",50503: "Vodafone-AU",50504: "Department of Defence-AU",
               50505: "Ozitel-AU",50506: "3 Vodafone Hutchison-AU",50507: "Vodafone-AU",50508: "One.Tel-AU",
               50509: "Airnet-AU",50510: "Norfolk Is-AU",50511: "Telstra-AU",50512: "3 Vodafone Hutchison-AU",
               50513: "Railcorp-AU",50514: "AAPT-AU",50515: "3GIS-AU",50516: "VicTrack-AU",50517: "Optus-AU",
               50518: "Pactel-AU",50519: "Lycamobile-AU",50520: "Ausgrid Corporation-AU",50521: "Queensland Rail-AU",
               50522: "iiNet-AU",50523: "Challenge Networks-AU",50524: "Advanced Communications-AU",
               50525: "Pilbara Iron-AU",50526: "Dialogue Communications-AU",50527: "Nexium Telecommunications-AU",
               50528: "RCOM-AU",50530: "Compatel-AU",50531: "BHP Billiton-AU",50532: "Thales Australia",
               50533: "CLX Networks-AU",50534: "Santos Limited-AU",50535: "MessageBird-AU",50536: "Optus-AU",
               50537: "Yancoal-AU",50538: "Truphone-AU",50539: "Telstra-AU",50562: "NBN-AU",50568: "NBN-AU",
               50571: "Telstra-AU",50572: "Telstra-AU",50590: "Optus-AU",50599: "One.Tel-AU"}

    field_trial_df = pd.read_excel("..\\SeleniumAutomation\\DataBase\\Liberty_Gas120_FieldTrialMeter.xlsx")

    """excel_file=r"D:\PythonFrameworkKeyword\grossMargin\SeleniumAutomation\DataBase\Liberty_Gas120_FieldTrialMeter.xlsx"
    df=pd.read_excel(excel_file)"""


    json_string=json_string.replace("'",'"')
    json_string=re.sub(r'/Date\((\d+)\)/',lambda x: str(int(x.group(1))),json_string)

    # Convert the JSON string to a Python dictionary
    heart_beat = json.loads(json_string)['Heartbeats']
    #print(heart_beat)

    # Sort heartbeats by WseLogTime in descending order
    heartbeats_sorted=sorted(heart_beat,key = lambda x: x['WseLogTime'],reverse = True)

    # Get the heartbeat with the latest WseLogTime

    latest_heartbeat=heartbeats_sorted[0]
    #print("*****************")

    print(latest_heartbeat)
    resultant_data = {}

    # Convert Unix timestamp to datetime object
    timestamp=int(latest_heartbeat['WseLogTime'])/1000  # Convert milliseconds to seconds
    dt_object=datetime.fromtimestamp(timestamp,tz = timezone.utc)

    ist=dt_object.astimezone(timezone(timedelta(hours = 5,minutes = 30)))
    ist_str=ist.strftime('%d/%m/%Y_%H:%M:%S')

    #convert gateway time to user reading format
    timestamp_gateway=int(latest_heartbeat['GatewayTime'])/1000  # Convert milliseconds to seconds
    dt_object=datetime.fromtimestamp(timestamp,tz = timezone.utc)

    ist=dt_object.astimezone(timezone(timedelta(hours = 5,minutes = 30)))
    ist_str_gateway=ist.strftime('%d/%m/%Y_%H:%M:%S')

    # Get Meter Location based on Meter Sr. no
    meter_sr_no=latest_heartbeat['ConnectedDevices'][0]['DeviceNo']
    meter_location=field_trial_df.loc[field_trial_df['Meter'] == meter_sr_no,'Meter Location'].values[0]

    #print("Meter Location for Meter Sr. no",meter_sr_no,":",meter_location)


    resultant_data['Product Name']=latest_heartbeat['ConnectedDevices'][0]['DeviceNo']
    resultant_data['Operator Name']=code_json[int(latest_heartbeat['OperatorCode'])]
    resultant_data['Meter Location'] = meter_location
    resultant_data['Rssi'] = latest_heartbeat['Rssi']
    resultant_data['AvgSignalInfo'] = latest_heartbeat['AvgSignalInfo']
    resultant_data['WseLogTime']=str(ist_str)
    resultant_data['Gateway Time']=str(ist_str_gateway)

    json_keys=['TimeZoneOffset',
               'OperatorCode','LastDayWanAttempts',
               'LastDayWanFailedAttempts','LastDayWanTxBytes','LastDayWanRxBytes',

               'LastDayCellChangeCounter','AreaCode','CellId','LastDayEngineSoftResetCounter',
               'LastDayEngineHardResetCounter']

#'LastDayWakeupDuration','LastDayNetworkReedinessDuration','LastDayFirstDataRoundTripDuration','LastDayPSMEnableDuration',
#'LastDayPSMUnregisterCumulativeCount',
    for keys in json_keys:
        resultant_data[keys]=latest_heartbeat[keys]
        # print(f"{keys} = {json_value[keys]}")

    print(resultant_data)


    """resultant_data['Device No'] = latest_heartbeat['ConnectedDevices'][0]['DeviceNo']
    resultant_data['WSE Log Time'] = str(ist_str)
    resultant_data['Gateway Time'] = str(ist_str_gateway)
    resultant_data['Time Zone Offset'] = latest_heartbeat['TimeZoneOffset']
    resultant_data['Last day wan attempts'] = latest_heartbeat['LastDayWanAttempts']
    resultant_data['last_day_tls_fail_attempts'] = latest_heartbeat['LastDayTLSFailAttempts']
    resultant_data['last_day_tcp_fail_attempts']=latest_heartbeat['LastDayTcpFailAttempts']
    resultant_data['last_day_udp_fail_attempts']=latest_heartbeat['LastDayUdpFailAttempts']
    resultant_data['last_day_engine_soft_reset_counts']=latest_heartbeat['LastDayEngineSoftResetCounter']
    resultant_data['last_day_engine_hard_reset_counts']=latest_heartbeat['LastDayEngineHardResetCounter']
    resultant_data['last_day_unregistered_duration']=latest_heartbeat['LastDayUnregisteredDuration']"""

    return resultant_data


#print(json_parse_get_heartbeat(file_path = r"C:\Users\44454\Desktop\gross_margin\get_heartbeat.txt"))

def json_parse_get_diagnostic_data(json_str):
    """
    Parsing diagnostic data
    :param json_str:
    :return:
    """

    json_str = json_str.replace("'", '"')
    json_data = json.loads(json_str)
    resultant_data = {}
    counters = json_data['Counters']
    VoltageAfterLastGasp = json_data['VoltageAfterLastGasp']
    wan_network_type = json_data['WanNetworkType']
    nb_signal_info = json_data['CurrentNBSignalInformation']
    module_temperature = json_data['ModuleTemperature']
    rssi = json_data['Rssi']
    """with open(file_path,'r') as file:
        counters = json.load(file)['Counters']"""

    """with open(file_path,'r') as file:
        VoltageAfterLastGasp=json.load(file)['VoltageAfterLastGasp']"""

        #VoltageAfterLastGasp = json.load(file)['VoltageAfterLastGasp']
        #print(counters)
    resultant_data['Gateway number'] = json_data['DeviceNo']
    resultant_data['gsm_reset_count'] = counters[1]['Value']
    resultant_data['processor_reset_count']=counters[0]['Value']
    resultant_data['pdd_count']=counters[3]['Value']
    resultant_data['SmsSendFailedCount']=counters[8]['Value']
    resultant_data['ModuleOpen']=counters[10]['Value']
    resultant_data['Voltage_after_last_gasp']=VoltageAfterLastGasp
    resultant_data['Wan_Network_type'] = wan_network_type
    resultant_data['NB_Signal_Information'] = nb_signal_info
    resultant_data['Module_Temperature'] = module_temperature
    resultant_data['RSSI'] = rssi
    #resultant_data['Last_gasp_notification']=''

    return resultant_data


#read data from the result file

import pandas as pd

#identify file in the latest 2 min timeframe
import os
import time

def find_latest_file(folder_path, file_name, time_frame=60000):
    time.sleep(10)
    latest_file = None
    latest_modification_time = 0

    # Get current time
    current_time = time.time()

    # Iterate through files in the folder
    for file in os.listdir(folder_path):
        if file.startswith(file_name):
            file_path = os.path.join(folder_path, file)
            # Get the modification time of the file
            modification_time = os.path.getmtime(file_path)
            # Check if the file modification time is within the time frame
            if current_time - modification_time <= time_frame:
                # Update latest file if modification time is later
                if modification_time > latest_modification_time:
                    latest_file = file_path
                    latest_modification_time = modification_time

    return latest_file

# Read the relative path of the frameworksettings .ini
#Read system variable
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_READ)
var_value, _ = winreg.QueryValueEx(key, 'SECURE_SELENIUM_RUNNER')
winreg.CloseKey(key)

print("[Info]: Framework Execution Started")
config = ConfigParser()
#config.read('frameworksettings.ini')
config.read(var_value)
relative_path = config.get('DEFAULT', 'project_hirarchy')
reports_path = relative_path+'Reports\\Final Report Folder\\API_Reports'
print("[Info]: Reports path = " +str(reports_path))


# Example usage
#folder_path = r"D:\PythonFrameworkKeyword\Reports\Final Report Folder"
folder_path = reports_path
file_name = "API_Final_Report"
latest_file = find_latest_file(folder_path, file_name)

#if latest_file:
print("Latest file found:", latest_file)
df = pd.read_excel(latest_file)

filtered_df_diag_data_json = df[(df["Test Scenario (Control File)"] == "Get Gateway Diagnostic Data Reply")
                                ]['Actual Value'].values
filtered_df_profile_json = df[(df["Test Scenario (Control File)"] == "Get Gateway Profile Reply"
                               )]['Actual Value'].values
filtered_df_heartbeats_json = df[(df["Test Scenario (Control File)"] == "Get Heartbeats"
                                  )]['Actual Value'].values

#print(filtered_df_diag_data_json)

diagnostic_data = []
profile_data = []
heartbeat_data = []
print(filtered_df_diag_data_json)
for meter_data_diagnostic in filtered_df_diag_data_json:
    #print(meter_data_diagnostic)
    try:
        print("----"*50)
        print(meter_data_diagnostic)
        print(json_parse_get_diagnostic_data(meter_data_diagnostic))
        print("----"*50)
        diagnostic_data.append(json_parse_get_diagnostic_data(meter_data_diagnostic))
    except Exception as e:
        print(str(e))


for meter_data_profile in filtered_df_profile_json:
    #print(meter_data_profile)
    try:
        #print(json_parse_gateway_profile(meter_data_profile))
        profile_data.append(json_parse_gateway_profile(meter_data_profile))
    except Exception as e:
        print(str(e))

for heartbeats in filtered_df_heartbeats_json:
    #print(heartbeats)
    try:
        #print(json_parse_get_heartbeat(heartbeats))
        heartbeat_data.append(json_parse_get_heartbeat(heartbeats))
    except Exception as e:
        print(str(e))

# Create DataFrame for diagnostic data
diagnostic_df = pd.DataFrame(diagnostic_data)

# Create DataFrame for profile data
profile_df = pd.DataFrame(profile_data)

heartbeats_df = pd.DataFrame(heartbeat_data)

now=datetime.now()
dt_string=now.strftime("%d_%m_%Y_%H_%M_%S")

#Check if folder exists


folder_path = "..\\..\\Reports\\Raw_Output"

try:
    os.makedirs(folder_path)
    print("Folder created successfully.")
except FileExistsError:
    print("Folder already exists. Skipping creation.")

# Write the DataFrames to an Excel file with each dataset in a separate sheet
with pd.ExcelWriter('..\\..\\Reports\\Raw_Output\\output_' +dt_string + '.xlsx', engine='openpyxl') as writer:
    #diagnostic_df.to_excel(writer, sheet_name='Diagnostic Data', index=False)
    #profile_df.to_excel(writer, sheet_name='Profile Data', index=False)
    heartbeats_df.to_excel(writer, sheet_name='Heartbeats', index=False)

    """# Access the worksheet
    worksheet=writer.sheets['Diagnostic Data']

    # Adjust column widths
    for column in diagnostic_df:
        column_length=max(diagnostic_df[column].astype(str).map(len).max(),len(column))
        col_idx=diagnostic_df.columns.get_loc(column)
        worksheet.column_dimensions[worksheet.cell(row = 1,column = col_idx + 1).column_letter].width=column_length + 2

        # Access the worksheet
    worksheet=writer.sheets['Profile Data']

    # Adjust column widths
    for column in profile_df:
        column_length=max(profile_df[column].astype(str).map(len).max(),len(column))
        col_idx=profile_df.columns.get_loc(column)
        worksheet.column_dimensions[
            worksheet.cell(row = 1,column = col_idx + 1).column_letter].width=column_length + 2
"""
    # Access the worksheet
    worksheet=writer.sheets['Heartbeats']

    # Adjust column widths
    for column in heartbeats_df:
        column_length=max(heartbeats_df[column].astype(str).map(len).max(),len(column))
        col_idx=heartbeats_df.columns.get_loc(column)
        worksheet.column_dimensions[worksheet.cell(row = 1,column = col_idx + 1).column_letter].width=column_length + 2




#print(filtered_df_profile_json)
#print(filtered_df_heartbeats_json)



#else:
#    print("No file found within the time frame.")





#print(json_parse_get_diagnostic_data(file_path = r"C:\Users\44454\Desktop\gross_margin\get_diagnostic_data.txt"))

















#var = json_parse_gateway_profile(file_path = r"C:\Users\44454\Desktop\gross_margin_json.txt")


#file_path = r"C:\Users\44454\Desktop\gross_margin_json.txt"
"""min_rssi, max_rssi, avg_rssi = [], [], []
rsrp_min, rsrp_max, rsrp_avg = [], [], []
rsrq_min, rsrq_max, rsrq_avg = [], [], []
sinr_min, sinr_max, sinr_avg = [], [], []

with open(file_path, 'r') as file:
    interval_data = json.load(file)['IntervalData']

for data in interval_data:
    try:
        rsrp, rsrq, sinr = data['RSRP'], data['RSRQ'], data['SINR']
        rsrp_min.append(rsrp['Min'])
        rsrp_max.append(rsrp['Max'])
        rsrp_avg.append(rsrp['Average'])

        rsrq_min.append(rsrq['Min'])
        rsrq_max.append(rsrq['Max'])
        rsrq_avg.append(rsrq['Average'])

        sinr_min.append(sinr['Min'])
        sinr_max.append(sinr['Max'])
        sinr_avg.append(sinr['Average'])

        #print(f"RSRP = {rsrp}\nRSRQ = {rsrq}\nSINR = {sinr}")
        min_rssi.append(data['MinRssi'])
        max_rssi.append(data['MaxRssi'])
        avg_rssi.append(data['AvgRssi'])

    except KeyError as e:
        print(f"KeyError: {e} not found in data: {data}")

    except Exception as e:
        print(f"Error processing data: {e}")

average_min_rssi = sum(min_rssi) / len(min_rssi)
average_max_rssi = sum(max_rssi) / len(max_rssi)
average_avg_rssi = sum(avg_rssi) / len(avg_rssi)

print(f"Average Min RSSI: {average_min_rssi}")
print(f"Average Max RSSI: {average_max_rssi}")
print(f"Average Avg RSSI: {average_avg_rssi}")

filtered_numbers = [num for num in rsrp_min if num is not None]

"""
#print(f"RSRP Min: {statistics.mean(filtered_numbers)}\nRSRP Max: {rsrp_max}\nRSRP Avg: {rsrp_avg}")
#print(f"RSRQ Min: {rsrq_min}\nRSRQ Max: {rsrq_max}\nRSRQ Avg: {rsrq_avg}")
#print(f"SINR Min: {sinr_min}\nSINR Max: {sinr_max}\nSINR Avg: {sinr_avg}")
"""
def list_average(lst):
    filtered_list = [num for num in lst if num is not None]
    return statistics.mean(filtered_list)


print(list_average(lst = rsrp_min ))
#print((json_data['IntervalData'][0]))
"""

"""import json

# Your JSON data
json_data = '''
{
  "SupplyType": "0 (Electricity)",
  "ServicePointNo": "0000000004251",
  "DeviceNo": "96154418",
  "IntervalPeriod": 30,
  "IntervalData": [
    {
      "Time": "2024-03-07T00:00:00Z",
      "UnregisteredDuration": 0,
      "MinRssi": -113,
      "MaxRssi": -113,
      "AvgRssi": -113,
      "EMeterCommStatus": true,
      "GMeterCommStatus": false,
      "HMeterCommStatus": false,
      "IhdCommStatus": false,
      "WanAttemptCount": 1,
      "PppFailCount": 0,
      "TcpFailCount": 0,
      "UdpFailCount": 0,
      "CellIdChangeCount": 0,
      "ValidSmsReceived": 0,
      "AreaCode": "2841",
      "CellId": "0ABA1052",
      "OperatorChangeCount": 0,
      "OperatorCode": "40470",
      "WanNetworkType": "4 (CatNB)",
      "RSRP": {
        "Min": -75,
        "Max": -75,
        "Average": -75
      },
      "RSRQ": {
        "Min": -3,
        "Max": -1,
        "Average": -1
      },
      "SINR": {
        "Min": 13,
        "Max": 24,
        "Average": 14
      }
    },
    {
      "Time": "2024-03-07T00:30:00Z",
      "UnregisteredDuration": 0,
      "MinRssi": -113,
      "MaxRssi": -113,
      "AvgRssi": -113,
      "EMeterCommStatus": true,
      "GMeterCommStatus": false,
      "HMeterCommStatus": false,
      "IhdCommStatus": false,
      "WanAttemptCount": 2,
      "PppFailCount": 0,
      "TcpFailCount": 0,
      "UdpFailCount": 0,
      "CellIdChangeCount": 0,
      "ValidSmsReceived": 0,
      "AreaCode": "2841",
      "CellId": "0ABA1052",
      "OperatorChangeCount": 0,
      "OperatorCode": "40470",
      "WanNetworkType": "4 (CatNB)",
      "RSRP": {
        "Min": -75,
        "Max": -75,
        "Average": -75
      },
      "RSRQ": {
        "Min": -2,
        "Max": -1,
        "Average": -1
      },
      "SINR": {
        "Min": 13,
        "Max": 22,
        "Average": 14
      }
    }
  ]
}
'''

# Parse JSON data
data = json.loads(json_data)

# Extract values from "IntervalData"
avg_rssi_values = [entry["AvgRssi"] for entry in data["IntervalData"]]
min_rssi_values = [entry["MinRssi"] for entry in data["IntervalData"]]
max_rssi_values = [entry["MaxRssi"] for entry in data["IntervalData"]]

sinr_values = [entry["SINR"]["Average"] for entry in data["IntervalData"]]
rsrq_values = [entry["RSRQ"]["Average"] for entry in data["IntervalData"]]
rsrp_values = [entry["RSRP"]["Average"] for entry in data["IntervalData"]]

# Calculate averages
avg_avg_rssi = sum(avg_rssi_values) / len(avg_rssi_values)
avg_min_rssi = min(min_rssi_values)
avg_max_rssi = max(max_rssi_values)

avg_sinr = sum(sinr_values) / len(sinr_values)
avg_rsrq = sum(rsrq_values) / len(rsrq_values)
avg_rsrp = sum(rsrp_values) / len(rsrp_values)

# Display results
print("Average AvgRssi:", avg_avg_rssi)
print("Min AvgRssi:", avg_min_rssi)
print("Max AvgRssi:", avg_max_rssi)

print("\nAverage SINR:", avg_sinr)
print("Average RSRQ:", avg_rsrq)
print("Average RSRP:", avg_rsrp)
"""