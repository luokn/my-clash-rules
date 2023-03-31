import requests
from yaml import safe_dump

steam_urls = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Steam.list',
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/SteamCN.list'
]

proxy_rules = [
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
proxy_domains = {
    'immersive-translate.owenyoung.com',
    '+.ea.com',
    'ea-api.arkoselabs.com',
    'origin-a.akamaihd.net',
    'eaassets-a.akamaihd.net',
}

direct_rules = [
    'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.list',
]
direct_domains = [
    '+.satoko.life',
    'yacd.haishan.me',
    'clash.razord.top',
]


def compile(name, urls, domains=[]):
    domain_list, keyword_list = [], []
    for url in urls:
        txt = requests.get(url).text
        for line in txt.splitlines():
            if line.startswith('DOMAIN-KEYWORD'):
                keyword_list.append('DOMAIN-KEYWORD,' + line.split(',')[1])
            elif line.startswith('DOMAIN-SUFFIX'):
                domain_list.append('+.' + line.split(',')[1])
            elif line.startswith('DOMAIN'):
                domain_list.append(line.split(',')[1])

    domain_list += domains
    with open(f'./providers/{name}-domains.yaml', 'w') as out:
        safe_dump({'payload': domain_list}, out)

    if len(keyword_list) > 0:
        with open(f'./providers/{name}-keywords.yaml', 'w') as out:
            safe_dump({'payload': keyword_list}, out)


if __name__ == "__main__":
    compile('steam', steam_urls)
    compile('proxy', proxy_rules, proxy_domains)
    compile('direct', direct_rules, direct_domains)
