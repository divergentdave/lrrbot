#!/usr/bin/python3
FINAL = False # Whether to delete the game data from the data.json when we're done

import json
import psycopg2

with open("data.json") as fp:
	data = json.load(fp)

conn = psycopg2.connect(database="lrrbot")
cur = conn.cursor()

cur.execute("DELETE FROM game_votes;");
cur.execute("DELETE FROM game_stats;");
cur.execute("DELETE FROM stats;");
cur.execute("DELETE FROM games;");
cur.execute("DELETE FROM shows;");
conn.commit()

statmap = {}
for statkey, stat in sorted(data['stats'].items()):
	cur.execute("INSERT INTO stats(statkey, displayname, displayplural, emote) VALUES (%s, %s, %s, %s) RETURNING statid", (
		statkey,
		stat.get('singular'),
		stat.get('plural'),
		stat.get('emote'),
	))
	statmap[statkey], = cur.fetchone()
conn.commit()

for showkey, show in sorted(data['shows'].items()):
	cur.execute("INSERT INTO shows(showkey, displayname) VALUES (%s, %s) RETURNING showid", (
		showkey,
		show['name'],
	));
	showid, = cur.fetchone()
	for gamekey, game in sorted(show['games'].items()):
		try:
			twitchid = int(gamekey)
		except ValueError:
			twitchid = None
		cur.execute("INSERT INTO games(showid, twitchid, name, displayname, status) VALUES (%s, %s, %s, %s, 'unverified') RETURNING gameid", (
			showid,
			twitchid,
			game.get('name', gamekey),
			game.get('display'),
		))
		gameid, = cur.fetchone()
		for username, vote in game['votes'].items():
			cur.execute("INSERT INTO game_votes(gameid, username, vote) VALUES (%s, %s, %s)", (
				gameid,
				username,
				vote,
			))
		for statkey, count in game['stats'].items():
			cur.execute("INSERT INTO game_stats(gameid, statid, statcount) VALUES (%s, %s, %s)", (
				gameid,
				statmap[statkey],
				count,
			))
	conn.commit()

if FINAL:
	del data['stats']
	del data['shows']
	with open("data.json", "w") as fp:
		json.dump(data, fp, indent=2)
