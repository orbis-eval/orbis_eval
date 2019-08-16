def get_config_yaml(data):

    config_data = {
        'aggregation': {
            'service': {
                'name': data['aggregation__service__name'],
                'location': data['aggregation__service__location']
            },
            'input': {
                'data_set': {
                    'name': data['aggregation__input__data_set__name']
                }
            }
        },
        'evaluation': {
            'name': data['evaluation__name']
        },
        'scoring': {
            'name': data['scoring__name'],
            'condition': 'overlap',
            'ignore_empty': False
        },
        'metrics': {
            'name': data['metrics__name'],

        },
        'storage': [data['storage__name']]
    }

    return config_data
