import json


class Encoder:

    @staticmethod
    def encode(**kwargs):
        """
        Take in any number of key arguments and return a json string

        :param **kwargs: Any number of key arguments
        :returns: document containing the kwargs
        :return type: json
        """
        _dict = dict()
        for item, value in kwargs.items():
            _dict[item] = value
        return json.dumps(_dict)



































