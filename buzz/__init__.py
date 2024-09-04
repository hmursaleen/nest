default_app_config = 'buzz.apps.BuzzConfig'

'''
Setting the default_app_config in the __init__.py ensures that the BuzzConfig is 
used, which in turn ensures that the signal is connected when the app starts.
'''