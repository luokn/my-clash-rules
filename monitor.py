#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : main.py
# @Data   : 2023/03/29
# @Author : Luo Kun
# @Contact: luokun485@gmail.com

import asyncio
import json

import websockets as ws


async def async_main():

    async with ws.connect('ws://127.0.0.1:55555/connections?token=666666', ping_interval=None) as client:

        prev_connections = {}
        while True:
            obj = json.loads(await client.recv())

            connections, new_connections = {}, {}
            for conn in obj['connections']:
                connections[conn['id']] = conn
                if conn['id'] not in prev_connections:
                    new_connections[conn['id']] = conn

            for conn in new_connections.values():
                proc_path = conn['metadata']['processPath']
                if '\\' not in proc_path:
                    continue

                proc_name = proc_path.split('\\')[-1]
                rule, rule_payload, chains = conn['rule'], conn['rulePayload'], '/'.join(conn['chains'])

                line = f'{rule}\t{rule_payload}\t{chains}\t{proc_path}'
                with open(f'./logs/{proc_name}.csv', 'a', encoding='utf-8') as out:
                    out.write(line)
                    out.write('\n')

            prev_connections = connections


asyncio.get_event_loop().run_until_complete(async_main())
