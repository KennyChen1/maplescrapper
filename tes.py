import requests
import datetime
import time

URL = 'https://maplelegends.com/api/character?name='
from datetime import date

# scrap and write files locally
LOCAL = True
# add to database
ONLINE = True	#10-29  false because I do not want to add to db without adding sumexp
MISSED = False
DIV = 500  #how often to insert
count = 0;
count2 = 0;

hours = 0


###############https://mapleroyals.com/forum/threads/xp-table.16611/
sumexp = [0,
	15,
	49,
	106,
	198,
	333,
	705,
	1265,
	2105,
	3347,
	5063,##2321
	7423,
	10639,
	14839,
	20299,
	27349,
	36189,
	47229,
	60945,
	77625,
	97841,
	122243,
	151223,
	185543,
	226055,
	273271,
	328171,
	391837,
	464917,
	548637,
	644337,
	752817,
	875577,
	1014243,
	1169783,
	1343999,
	1538831,
	1755431,
	1995931,
	2262613,
	2556829,
	2881069,
	3237985,
	3629145,
	4057425,
	4525875,
	5036295,
	5591975,
	6196391,
	6851591,
	7561307,
	8309915,
	9099546,
	9932448,
	10810993,
	11737682,
	12715153,
	13746189,
	14833725,
	15980757,
	17190751,
	18467052,
	19813294,
	21233310,
	22731142,
	24311055,
	25977547,
	27735362,
	29589505,
	31545255,
	33608180,
	35784153,
	38079369,
	40500362,
	43054025,
	45747628,
	48588840,
	51585750,
	54746890,
	58081260,
	61598353,
	65308182,
	69221309,
	73348875,
	77702631,
	82294972,
	87138973,
	92248425,
	97637874,
	103322664,
	109318980,
	115643894,
	122315413,
	129352531,
	136775283,
	144604801,
	152863376,
	161574520,
	170763034,
	180455078,
	190678246,
	201461643,
	212835970,
	224833610,
	237488720,
	250837330,
	264917443,
	279769146,
	295434722,
	311958771,
	329388337,
	347773043,
	367165230,
	387620108,
	409195913,
	431954072,
	455959378,
	481280174,
	507988549,
	536160542,
	565876360,
	597220604,
	630282512,
	665156212,
	701940990,
	740741573,
	781668427,
	824838072,
	870373413,
	918404090,
	969066848,
	1022505925,
	1078873463,
	1138329942,
	1201044636,
	1267196095,
	1336972653,
	1410572966,
	1488206576,
	1570094507,
	1656469896,
	1747578656,
	1843680176,
	1945048059,
	2052040901,
	2164823114,
	2283785792,
	2409267624,
	2541625860,
	2681237327,
	2828499502,
	2983831644,
	3147675987,
	3320498999,
	3502792712,
	3695076120, 
	3897896658,
	4111831761,
	4337490507,
	4575515352,
	4826583958,
	5091411123,
	5370750762,
	5665398270,
	5976192461,
	6304018173,
	6649808734,
	7014548617,
	7399276245,
	7805086947,
	8233136075,
	8684642295,
	9160891055,
	9663238247,
	10193114065,
	10752027077,
	11341568522,
	11963416838,
	12619342441,
	13311212767,
	14040997586,#180
	14810774613,
	15622735421,
	16479191681,
	17382581744,
	18335477582,
	19340592111,
	20400786916,
	21519080396,
	22698656358,
	23942873082,#190
	25255272882,
	26639592191,
	28099772198,
	29639970069,
	31264570783,
	32978199616,
	34785735309,
	36692293957,
	38703363662,
	40824639986]    #200
###############


today = (date.today()+ datetime.timedelta(days=1)).strftime("%#m-%d-%y")
fname = "F:/Users/Kenny/Desktop/MTrack/datadump/data_" + today + ".txt"

#print(datetime.datetime.now() - datetime.timedelta(hours = 7))


if(LOCAL == True or ONLINE == True):
	from google.cloud import bigquery
	# Construct a BigQuery client object.	
	client = bigquery.Client()
	
	query = """
		SELECT name
		FROM `mtrack1337.MLData.username`
	"""
	query_job = client.query(query)  # Make an API request.

	#print("starting...")
	for row in query_job:
		
		if(MISSED == True):
			if(count2 < 5):
				count2 = count2 +1
				continue
				
			
		# Row values can be accessed by field name or index.
		line = "{}".format(row[0])
			
		# checks if the name is on ranking or valid
		# returns empty if not on ranking/valid
		try:
			data = requests.get(URL+line).json()
		except ValueError:
			#nothing return?
			print("decode json error", line)

			#i think i need this continue 10-19
			continue
		if(not bool(data)):	
			print("no json found", count, line)	
			continue
		
		#add timestamp to json
		#data.update(date = str(datetime.datetime.now()))
		data.update(date = str(datetime.datetime.now() - datetime.timedelta(hours = hours)))
		
		#UNTESTED BUT PROBABLY WORKS 
		if(data["level"] != 200):
			exptnl = sumexp[data["level"]] -sumexp[data["level"]-1]
			percent = float(data["exp"].strip('%'))/100
			#print(int(sumexp[data["level"]]+exptnl*percent))
			data.update(sumexp = int(sumexp[data["level"]]+exptnl*percent))
		else:
			data.update(sumexp = sumexp[data["level"]])
		#UNTESTED BUT PROBABLY WORKS 
		
		if LOCAL == True:
			try:
				if(count >= 0):

					dataStr = str(data)+'\n'
					dataStr = dataStr.replace('\'', '"')
					dataStr = dataStr.replace(': True, ', ': true, ')
					dataStr = dataStr.replace(': False, ', ': false, ')


					fd  = open(fname , "a") 
					fd.write(dataStr)
					fd.close()
					#print(dataStr)				
								
			except(JSONDecodeError) as e :
				print(e, line, count)
		if ONLINE == True:
			# 19,977
			# 22,458
			# 109,611
			try:
				if(count%DIV == 0):
					print("creating new query")
					queryInsert = "INSERT INTO `mtrack1337.MLData.datadump` (" + ", ".join(data.keys()) + ") VALUES "
				queryInsert = queryInsert +  "(" + str(data.values())[13:-2] + "), "
				if(count%DIV == DIV-1):
					print(count, "ending and sending query")
					queryInsert = queryInsert[:-2] + ";"
					query_insert_job = client.query(queryInsert)  # Make an API request.
			except Exception as e:
				ename = "F:/Users/Kenny/Desktop/MTrack/logs/log_" + today + ".txt"
				fd  = open(fname , "a") 
				fd.write(e)
				fd.write("\nbreaker\n")
				fd.close()


		if count%(DIV/10) == 0:
			print(count)
		count=count+1
		
		time.sleep(.6)

	# this should occur when the loop ends and it's not a multiple of DIV
	if ONLINE == True:
		print("processing query: out of loop")
		if count%DIV != 0 and count%DIV != DIV-1:
			queryInsert = queryInsert[:-2] + ";"
			query_insert_job = client.query(queryInsert)  # Make an API request.

print("done", count)

