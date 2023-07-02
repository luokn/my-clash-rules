from typing import List, Optional, Set

import requests
from yaml import safe_dump

steam_domain_lists = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/SteamCN.list'
]
proxy_domain_lists = [
    # Apple
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Apple.list',
    # Google
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Google.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleFCM.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleCN.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleCNProxyIP.list',
    # Microsoft/OneDrive/Github
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Microsoft.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/OneDrive.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Github.list',
    # Xbox/Sony/Epic/Origin
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Xbox.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Sony.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Epic.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Origin.list',
    # Twitter/Telegram
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Twitter.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Telegram.list',
    # Media
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyMedia.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/YouTube.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Netflix.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Spotify.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Hulu.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Porn.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Instagram.list',
    # GFW
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.list'
]
direct_domain_lists = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaMedia.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list',
]

proxy_domains = {
    'immersive-translate.owenyoung.com',
    '+.ea.com',
    'ea-api.arkoselabs.com',
    'origin-a.akamaihd.net',
    'eaassets-a.akamaihd.net',
}
direct_domains = {
    '+.satoko.life',
    '+.yukako.live',
    'yacd.haishan.me',
    'clash.razord.top',
}


def generate(name: str, list_urls: List[str], additions: Optional[Set[str]] = None):
    domains, keywords = set(), set()
    for url in list_urls:
        content = requests.get(url).text
        for line in content.splitlines():
            if line.startswith('DOMAIN-KEYWORD'):
                keywords.add('DOMAIN-KEYWORD,' + line.split(',')[1])
            elif line.startswith('DOMAIN-SUFFIX'):
                domains.add('+.' + line.split(',')[1])
            elif line.startswith('DOMAIN'):
                domains.add(line.split(',')[1])

    if additions is not None:
        domains |= additions

    if len(domains) > 0:
        with open(f'./providers/{name}-domains.yaml', 'w') as out:
            safe_dump({'payload': sorted(domains)}, out)

    if len(keywords) > 0:
        with open(f'./providers/{name}-keywords.yaml', 'w') as out:
            safe_dump({'payload': sorted(keywords)}, out)


if __name__ == "__main__":
    generate('steam', steam_domain_lists)
    generate('proxy', proxy_domain_lists, proxy_domains)
    generate('direct', direct_domain_lists, direct_domains)
