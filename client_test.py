import zeep
from lxml import etree
from dict2xml import dict2xml

# wsdl = 'https://compliance.nemsis.org/nemsisWs.wsdl'
wsdl = 'nemsisWs.xml'
# wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'

client = zeep.Client(wsdl=wsdl)
print(client.get_type('ns0:ServerErrorCodes'))
# print(client.service.Method1('Zeep', 'another parameter'))

factory = client.type_factory('ns0')

# username = factory.username('test_username') # this no work
Error_List = factory.XmlGeneralErrorList('test_username') # this works

## let's see if we can create the types that are required for the WS (ie. NemsisV3WsQueryLimitRequest and some others)
# Limit_Request2 = factory.NemsisV3WsQueryLimitRequest('test_username','test_pw','test_org','test_request') # this does not work for some reason
Limit_Request = factory.NemsisV3WsQueryLimitRequest(username = 'LR_username', password = 'LR_pw', organization = 'LR_org', requestType = 'LR_type') # this works for some reason
Retrieve_Request = factory.NemsisV3WsRetrieveStatusRequest(username = 'RR_username', password = 'RR_pw', organization = 'RR_org', requestType = 'RR_type', requestHandle = 'RR_handle', originalRequestType = 'RR_og_type', additionalInfo = 'RR_info')
Submit_Request = factory.NemsisV3WsSubmitDataRequest(username = 'SR_username', password = 'SR_pw', organization = 'SR_org', requestType = 'SR_type', submitPayload = 'SR_payload', requestDataSchema = 'SR_schema', schemaVersion = 'SR_schema_ver', additionalInfo = 'SR_info')

## can we create the element as an object as well?
# Element_Limit_Request = factory.QueryLimitRequest(NemsisV3WsQueryLimitRequest) # this is the wrong way to create an element object with zeep

## can we print for debug? - yes all of these work
print(Limit_Request.username)
print(Retrieve_Request.organization)
print(Submit_Request.requestType)

print('---')

# # now, can we use the ws functions provided in the WSDL?
# Limit_Response = client.service.QueryLimit(Element_Limit_Request)
# Limit_Response = client.service.QueryLimit(Limit_Request)

# Limit_Response = client.service.QueryLimit('test_username','test_pw','test_org','test_request')
# print('Type: ' + str(Limit_Response.requestType))
# print('Limit: ' + str(Limit_Response.limit))
# print('Status Code: ' + str(Limit_Response.statusCode))
# print('limit query end')

print('---')

# Retrieve_Response = client.service.RetrieveStatus(Retrieve_Request.username,'test_pw','test_org','test_request','test_request_handle','test_original_request_type','test_additional_info')
# print('Type: ' + str(Retrieve_Response.requestType))
# print('Status Code: ' + str(Retrieve_Response.statusCode))
# print('Handle: ' + str(Retrieve_Response.requestHandle))
# print('Type: ' + str(Retrieve_Response.originalRequestType))
# print('Result: ' + str(Retrieve_Response.retrieveResult))
# print('retrieve response end')

print('---')

# Parse the XML file and create an ElementTree
tree = etree.parse('test.xml')

# Get the root element from the ElementTree
root = tree.getroot()

print('here:')
print(root)

staging_payload = factory.PayloadOfXmlElement(root)
# staging_payload = factory.PayloadOfXmlElement(xml_text)
payload = factory.DataPayload(staging_payload)

# print(payload)

Submit_Response = client.service.SubmitData('CadAnly_CADMUS','903484*GATech','CADMUS','SubmitData',payload,61,'3.5.0','info')
print('Type: ' + str(Submit_Response.requestType))
print('Handle: ' + str(Submit_Response.requestHandle))
print('Status Code: ' + str(Submit_Response.statusCode))
print('Reports: ' + str(Submit_Response.reports))
# print('submit response end')

print()
print(type(Submit_Response.reports))

# tree2 = etree.parse(Submit_Response.reports)
# root2 = tree2.getroot()


custom_soap_object = Submit_Response.reports

# Convert custom SOAP object to XML string
xml_dict = zeep.helpers.serialize_object(custom_soap_object)

print()
print(type(xml_dict))
print(xml_dict)

print()
print('Converting to xml:')
xml = dict2xml(xml_dict)
print(xml)

# Parse the XML string to create an etree object
etree_object = etree.fromstring(xml_dict)