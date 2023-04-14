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

clash_direct_domains = {
    '+.satoko.life',
    'yacd.haishan.me',
    'clash.razord.top',
}
surfboard_direct_domains = {
    '.satoko.life',
    'yacd.haishan.me',
    'clash.razord.top',
}

clash_proxy_domains = {
    'immersive-translate.owenyoung.com',
    '+.ea.com',
    'ea-api.arkoselabs.com',
    'origin-a.akamaihd.net',
    'eaassets-a.akamaihd.net',
}
surfboard_proxy_domains = {
    'immersive-translate.owenyoung.com',
    '.ea.com',
    'ea-api.arkoselabs.com',
    'origin-a.akamaihd.net',
    'eaassets-a.akamaihd.net',
}


def generate(name: str,
             urls: List[str],
             clash_domains: Optional[Set[bool]] = None,
             surfboard_domains: Optional[Set[bool]] = None):
    clash_domain_set, surfborad_domain_set, keyword_set = set(), set(), set()
    for url in urls:
        txt = requests.get(url).text
        for line in txt.splitlines():
            if line.startswith('DOMAIN-KEYWORD'):
                keyword_set.add('DOMAIN-KEYWORD,' + line.split(',')[1])
            elif line.startswith('DOMAIN-SUFFIX'):
                clash_domain_set.add('+.' + line.split(',')[1])
                surfborad_domain_set.add('.' + line.split(',')[1])
            elif line.startswith('DOMAIN'):
                clash_domain_set.add(line.split(',')[1])
                surfborad_domain_set.add(line.split(',')[1])

    if clash_domains is not None:
        clash_domain_set |= clash_domains

    if surfboard_domains is not None:
        surfborad_domain_set |= surfboard_domains

    if len(clash_domain_set) > 0:
        with open(f'./providers/{name}-domains.yaml', 'w') as out:
            safe_dump({'payload': list(clash_domain_set)}, out)
        with open(f'./providers/{name}-domains.txt', 'w') as out:
            out.write('\n'.join(list(surfborad_domain_set)))

    if len(keyword_set) > 0:
        with open(f'./providers/{name}-keywords.yaml', 'w') as out:
            safe_dump({'payload': list(keyword_set)}, out)
        with open(f'./providers/{name}-keywords.txt', 'w') as out:
            out.write('\n'.join(list(keyword_set)))


if __name__ == "__main__":
    generate('steam', steam_domain_lists)
    generate('proxy', proxy_domain_lists, clash_proxy_domains, surfboard_proxy_domains)
    generate('direct', direct_domain_sets, clash_direct_domains, surfboard_direct_domains)
