import zeep

# wsdl = 'https://compliance.nemsis.org/nemsisWs.wsdl'
wsdl = 'nemsisWs.xml'
# wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'

client = zeep.Client(wsdl=wsdl)
print(client.get_type('ns0:ServerErrorCodes'))
# print(client.service.Method1('Zeep', 'another parameter'))

factory = client.type_factory('ns0')

# username = factory.username('test_username') # this no work
Error_List = factory.XmlGeneralErrorList('test_username') # this work

# let's see if we can create the types that are required for the WS (ie. NemsisV3WsQueryLimitRequest and some others)
Limit_Request = factory.NemsisV3WsQueryLimitRequest(username = 'test_username', password = 'test_pw', organization = 'test_org', requestType = 'test_request') # this works for some reason
# Limit_Request2 = factory.NemsisV3WsQueryLimitRequest('test_username','test_pw','test_org','test_request') # this works for some reason

# can we create the element as an object as well?
# Element_Limit_Request = factory.QueryLimitRequest(NemsisV3WsQueryLimitRequest) # this is the wrong way to create an element object with zeep

# can we print for debug? - yes all of these work
print(Limit_Request.username)
print(Limit_Request.organization)
print(Limit_Request.requestType)
print(Limit_Request.password)

# now, can we use the ws function provided in the WSDL
# Limit_Response = client.service.QueryLimit(Element_Limit_Request)
# Limit_Response = client.service.QueryLimit(Limit_Request)
Limit_Response = client.service.QueryLimit('test_username','test_pw','test_org','test_request')
print(Limit_Response.limit)
print(Limit_Response.limit)
print(Limit_Response.limit)
print('hmmm')