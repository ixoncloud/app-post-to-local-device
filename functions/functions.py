import requests
from ixoncdkingress.cbc.context import CbcContext

@CbcContext.expose
def execute(context: CbcContext,  httpServerName: str,
            plcCommand: str,
            value: str):
    if context.agent is None:
        return {'error': 'No agent found'}
    session, url = _connectToHttpService(context, httpServerName)
    return _postToHttpService(session, url, plcCommand, value)


def _connectToHttpService(context: CbcContext, webServerName: str):
    agentServer = _getSelectedAgentServer(context, webServerName)
    if agentServer is None:
        return {'error': 'No server found'}
    webAccessUrl = _getWebAccessUrl(context, agentServer['publicId'])
    if webAccessUrl is None or webAccessUrl == 'No server found':
        return {'error': 'Error retrieving web access url'}
    landingPage = _getLandingPage(
        context, agentServer['publicId'])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()

    session.cookies.clear()

    connectedToRscServer = session.get(webAccessUrl, headers=headers)
    if connectedToRscServer.status_code == 200:

        baseUrl = webAccessUrl.split("/?")[0]
        url = baseUrl + landingPage

        return [session, url]


def _postToHttpService(
        session, url: str, plc_command: str, value: str):
    properties = [{'key': plc_command, 'value': value}]

    formBody = '&'.join([f"{property['key']}={property['value']}"
                        for property in properties])

    response = session.post(
        url, data=formBody,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    if response.status_code == 200:
        return {'message': 'done'}
    return {'error': 'Error posting to http service'}


def _getSelectedAgentServer(context: CbcContext, webServerName: str):
    agentServers = _getAgentServers(context)
    for x in agentServers:
        if x['name'] == webServerName and x['type'] == 'http':
            return x
    return None


def _getWebAccessUrl(context: CbcContext, publicId: str):
    response = context.api_client.post(
        'WebAccess', {'server': {'publicId': publicId}})
    return response['data']['url']


def _getLandingPage(context: CbcContext, serverId: str):
    response = context.api_client.get(
        'AgentServer',
        url_args={'agentId': context.agent.public_id, 'publicId': serverId})
    return response['data']['landingPage']


def _getAgentServers(context: CbcContext):
    agent = context.api_client.get(
        'Agent', url_args={'publicId': context.agent.public_id},
        query={"fields": "publicId,servers.publicId,servers.type,servers.name"})['data']
    return agent['servers']
