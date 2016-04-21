def attack(target):
    # write your code here
    print target

def exploit(target):
    if isinstance(target, str):
        attack(target)
    else:
        while target.isReady():
            if not target.queue.empty():
                host = target.queue.get()
                if host.has_key('ip'):
                    attack(host['ip'])
                elif host.has_key('site'):
                    attack(host['site'])
                else:
                    print "[!] can not find a ip or site in your target!"