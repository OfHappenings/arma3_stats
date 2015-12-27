import datetime
import argparse

import valve.source.a2s
from elasticsearch import Elasticsearch

#SERVER_ADDRESS = ('72.5.195.137', 2303)

#server = valve.source.a2s.ServerQuerier(SERVER_ADDRESS)
#info = server.get_info()
#players = server.get_players()

#print "{player_count}/{max_players} {server_name}".format(**info)
#for player in sorted(players["players"],
#                             key=lambda p: p["score"], reverse=True):
#        print "{score} {name}".format(**player)


class Stats():
    def __init__(self):
        self.es = Elasticsearch()


    def get_current_players(self, ip, port):
        server_addr = (ip, port)
        now = datetime.datetime.utcnow()
        server  = valve.source.a2s.ServerQuerier(server_addr)
        players = server.get_players()
        info    = server.get_info()
   
        print(players.keys())

        body = {'timestamp':now, 'player_count':players['player_count'], 
                'server_name':info['server_name'], 'ip_addr':ip}

        self.es.index(index='arma3', doc_type='catalog', body=body) 



if __name__ == '__main__':
    stats = Stats()

    parser = argparse.ArgumentParser(description='Arma 3 stats to Elasticsearch')
    parser.add_argument('--get-players', action='store_true')
    parser.add_argument('--port',        action='store', type=int, required=True)
    parser.add_argument('--ip',      action='store', required=True)

    args = parser.parse_args()

    if args.get_players:
        stats.get_current_players(args.ip, args.port)
