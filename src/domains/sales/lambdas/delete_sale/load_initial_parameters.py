import json


def load_initial_parameters(event):
    print(f'Begin load_initial_parameters')
    print(f'Event: {event}')

    path_parameters = event.get('pathParameters', None)
    if path_parameters is None or 'id' not in path_parameters:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Se debe proporcionar el ID de la cotización en la ruta"
            })
        }

    id_sale = path_parameters['id']
    if not id_sale or id_sale.strip() == '':
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "El ID de la cotización no puede estar vacío"
            })
        }

    return id_sale