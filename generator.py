from typing import List, Optional, Set

import requests
from yaml import safe_dump

steam_domain_lists = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/SteamCN.list'
]
proxy_domain_lists = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Google.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleFCM.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleCN.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/GoogleCNProxyIP.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/YouTube.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Microsoft.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Github.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/OneDrive.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Xbox.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Epic.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Twitter.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Telegram.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Porn.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.list'
]
direct_domain_sets = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list',
]

direct_domains = {
    '+.satoko.life',
    'yacd.haishan.me',
    'clash.razord.top',
}
proxy_domains = {
    'immersive-translate.owenyoung.com',
    '+.ea.com',
    'ea-api.arkoselabs.com',
    'origin-a.akamaihd.net',
    'eaassets-a.akamaihd.net',
}


def generate(name: str, urls: List[str], domains: Optional[Set[bool]] = None):
    domain_set, keyword_set = set(), set()
    for url in urls:
        txt = requests.get(url).text
        for line in txt.splitlines():
            if line.startswith('DOMAIN-KEYWORD'):
                keyword_set.add('DOMAIN-KEYWORD,' + line.split(',')[1])
            elif line.startswith('DOMAIN-SUFFIX'):
                domain_set.add('+.' + line.split(',')[1])
            elif line.startswith('DOMAIN'):
                domain_set.add(line.split(',')[1])

    if domains is not None:
        domain_set |= domains

    if len(domain_set) > 0:
        with open(f'./providers/{name}-domains.yaml', 'w') as out:
            safe_dump({'payload': list(domain_set)}, out)

    if len(keyword_set) > 0:
        with open(f'./providers/{name}-keywords.yaml', 'w') as out:
            safe_dump({'payload': list(keyword_set)}, out)


if __name__ == "__main__":
    generate('steam', steam_domain_lists)
    generate('proxy', proxy_domain_lists, proxy_domains)
    generate('direct', direct_domain_sets, direct_domains)
