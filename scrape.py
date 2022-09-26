import requests
from bs4 import BeautifulSoup
import json
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
session = FuturesSession(max_workers=1000)
def writeline(filename,data):
	with open(filename,'a') as f:
		f.write('\n' + data)
		f.close()
def scrape():
	invites = []
	def scrp(session,amount,skip):
		domains = ['discord.gg/','discord.com/invite/']
		url = f'https://search.discordservers.com/?term=&size={amount}&from={skip}&keyword='
		servers = session.get(url).result().json()['results']
		for server in servers:
			invite = server['customInvite']
			if invite != None and len(invite) > 0 and invite not in invites:
				print(f'Invite: {invite} |')
				invites.append(invite)
				writeline('invites.txt',f"https://discord.gg/{invite}")

		url = f'https://top.gg/api/client/entities/search?list=top&platform=discord&entityType=server&amount={amount}&skip={skip}'
		servers = session.get(url).result().json()['results']
		for server in servers:
			server_id = server['id']
			invite_url = f'https://top.gg/servers/{server_id}/join'
			invite = session.get(invite_url,allow_redirects=True).result().url
			for domain in domains:
				if domain in invite.lower():
					invite = invite.split(domain)[1]
					if invite not in invites and len(invite) > 0:
						print(f'Invite: {invite} |')
						invites.append(invite)
						writeline('invites.txt',f"https://discord.gg/{invite}")
	with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
		skip = 0
		skip_interval = 50
		futures = []
		amount = 50
		while True:
			futures.append(executor.submit(scrp,session,amount,skip))
			skip += skip_interval
			print(f'Total Invites Scraped: {len(invites)}')

amount = input("Press ENTER to start scraping..")
scrape()