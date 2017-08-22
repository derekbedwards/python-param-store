__all__ = [
    'EC2ParameterStore'
]


class BaseStore(object):

    def load_values(self, items):
        raise NotImplementedError()


class EC2ParameterStore(BaseStore):

    def __init__(self):
        import boto3
        import json
        import urllib2

        document = json.loads(urllib2.urlopen("http://169.254.169.254/latest/dynamic/instance-identity/document").read())
        self.client = boto3.client('ssm', region_name=document['region'])

    def load_values(self, items):
        """Load the parameters from the AWS Parameter Store

        :parameter items: dict with target as key and parameter name as value
        :rtype: dict

        """
        if not items:
            return {}

        data = self.client.get_parameters(
            Names=items,
            WithDecryption=True)

        result = {}
        for parameter in data['Parameters']:
            key = parameter['Name']
            value = parameter['Value']
            result[key] = value
        return result
