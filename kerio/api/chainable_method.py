import importlib
import kerio.api
from pprint import pprint

class ChainableMethod(object):
    def next_method(self, **params):

        names = params['names']

        try:
            # import the module
            module_name = '.'.join(['kerio.api.method'] + names[:-1]).lower()
            importlib.import_module(module_name)

            # get method's module
            module_names = ['api', 'method'] + map(str.lower, names[:-1])

            module = globals()['kerio']

            for name in module_names:
                module = getattr(module, name)

            # instantiate method's class
            class_name = names[-1].capitalize()

#            pprint(module)
#            pprint(class_name)

            method = getattr(module, class_name)(**params)

        except (ImportError, AttributeError) as e:
#            pprint(e)
            importlib.import_module('kerio.api.method')
            method = kerio.api.method.Generic(**params)

        return method
