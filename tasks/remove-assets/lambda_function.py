#!/usr/bin/env python
from cirrus.lib.process_payload import ProcessPayload
from cirrus.lib.logging import get_task_logger
from cirrus.lib.transfer import get_s3_session


LAMBDA_TYPE = 'task'


def lambda_handler(event, context={}):
    payload = ProcessPayload.from_event(event)
    logger = get_task_logger(f'{LAMBDA_TYPE}.remove-assets', payload=payload)

    item = payload['features'][0]

    # configuration options
    config = payload.get_task('remove-assets', {})
    #outopts = payload.process.get('output_options', {})

    # asset config
    assets = config.get('assets', [])

    s3_session = get_s3_session()

    # drop specified assets
    for asset in [a for a in assets if a in item['assets'].keys()]:
        logger.debug(f'Removing asset {asset}')
        url = item['assets'][asset]['href']
        item['assets'].pop(asset)
        s3_session.delete(url)

    return payload
