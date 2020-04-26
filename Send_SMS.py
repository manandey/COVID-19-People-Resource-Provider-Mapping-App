from twilio.rest import Client
#harshit
# account_sid = 'AC8da042ddf0308e13c3b9527f8bfa9ca7'
# auth_token = 'b540856d495d6b003ec52c9ccf7f6cff'
#manan
# auth_token = 'c31fafd25562448d54fb5c0c90352175'
# account_sid = 'ACe1c35813f18119dc8e165df79de857cf'
#shashi
account_sid="ACf807961c8c8b19765668cfbda0c26fde"
auth_token = '24bf455d7cf1926ce0f7bf523ca60d7a'

client = Client(account_sid, auth_token)
numbers_to_message = ['+919837549167','+919663557785','+919368940246']
for number in numbers_to_message:
    client.messages.create(
                     body="Hello World From Twilio",
                     # from_='+12056277965',
                     from_='+18634501750',
                     to=number
                 )
