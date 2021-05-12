import json
import boto3
import time

# getting time (originally in GMT)
current_time = time.localtime()

# getting current hour (will be in military time)
current_hour=time.strftime('%H',current_time)
hour=int(current_hour)
#setting am or pm
setting='AM'
# the GMT is 4 hours ahead of cville time, so  had to adjust the hour accordingly
# base case: if GMT to is 4 (4am) then set current_hours to 12 (12am est)
if(hour==4):
    current_hours=12
# if Gmt is anytime from (12am-3:59am) it will be 0-3 so if that is the case we want to be 4 hours behind
# so we will be in the night before so set setting to PM and set current hours to 12-hours so ex:
# if GMT is 2 (2am, we want it to be 10pm), so 12-2=10 and set setting to PM so 10pm
elif(hour<4):
	current_hours=12-hour	
	setting='PM'
# if GMT is past noon, we want to convert military time to normal time, and back 4 hours
# we want to make sure if the time is 13 for example, we only subtract 4
elif(hour>12 and hour<=16):
    current_hours=hour-4
    if(current_hours==12):
        setting='PM'
# if past noon in est time, it is 16 in gmt so adjust the military time and go back 4 hours
elif(hour>16):
	hour-=12
	current_hours=hour-4
	setting='PM'
else:
	current_hours=hour-4
	
# formatting time
now_time=time.strftime('%m/%d/%Y '+str(current_hours)+':%M '+setting, current_time)
print('Loading function')

# initializing s3
s3=boto3.resource('s3')


def lambda_handler(event, context):
    # set input to value variable
    value=event['key1']
    #printing out value for logs
    print("value1 = " + value)
    
    #if input is Open, then office hours is ON!
    if(value=='Open'):
        office_hours='ON!'
    else:
        #if input is Close, then office hours is OFF!
        office_hours='OFF!'
    
    # Creating simple html script, I have two headings. the second heading concatnates the time and office hours vairables
    web_body="""<html>
                    <head>
                        
                    </head>
                    <body>
                        <h1>Office Hours Page.</h1>
                        <h2>Welcome to Prof. Smith's Office Hours... last generated: """+now_time+"""... office hours are currently: """+office_hours+"""</h2>
                    </body>
                </html>"""
    # encode so we can make it an actual html file
    web_body=web_body.encode("utf-8")
    # put in bucket, which will be used for the static website. Add to adjust IAM for this
    s3.Bucket("ejh9qz-cs4740-pa6").put_object(ACL='public-read', Key='index.html', Body=web_body, ContentType='text/html')
    # printing for the logs
    print('completed!!')
    return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')
