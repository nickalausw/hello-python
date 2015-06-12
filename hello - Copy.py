import os
import uuid
import urlparse
import redis
import json
import newrelic.agent
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
ORANGE = "#FF9900"
GREEN = "#33CC33"

COLOR = ORANGE

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
r.set("hit_counter", 1)

newrelic.agent.initialize('newrelic.ini')

@app.route('/')
def hello():
	r.incr("hit_counter")

	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Hi, I'm GUID:<br/>
	{}
	<center><h1><font color="black">Hit Counter:<br/>
	{}

	</center>

	</body>
	</html>
	""".format(COLOR,my_uuid,r.get("hit_counter"))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
