import os
import uuid
import urlparse
import redis
import json
import newrelic.agent
import logging
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = BLUE

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
r.set("hit_counter", 1)

newrelic.agent.initialize('newrelic.ini')

logging.basicConfig(filename='Animal.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

@app.route('/')
def hello():
	r.incr("hit_counter")

	return """
	<html>
	<body bgcolor="{}">
	<center><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkDKEiHNerWOD-sfpKodevDksLQQQ1O0ef-CGXzatMuubCWXOKrg" alt="encrypted-tbn0.gstatic.com">
	<center><h1><font color="white">Hi, Welcome to EMC MidMarket Central Div Solutions Summit,<br/>
	<center><h1><font color="white">Here's your GUID:<br/>
	{}
	<center><h1><font color="black">HIT COUNTER:<br/>
	{}

	</center>

	</body>
	</html>
	""".format(COLOR,my_uuid,r.get("hit_counter"))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
