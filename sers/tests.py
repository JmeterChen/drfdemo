from django.test import TestCase

# Create your tests here.


import requests
from threading import Thread
from queue import Queue, Empty
import time

THREAD_POOL_SIZE = 8

dpa_ids = [
    7079099461481301765,
    7079099367050790662,
    7079099180286887685,
    7079099461481285381,
    7079099367050774278,
    7079099180286871301,
    7079099461481268997,
    7079099367050757894,
    7079099162368820998,
    7079099367050741510,
    7079099180286854917,
    7079099180286838533,
    7079099162368804614,
    7079099367050725126,
    7079099180286822149,
    7079099162368788230,
    7079099367050708742,
    7079099162368771846,
    7079099146476603142,
    7079099180286805765,
    7079099162368755462,
    7079099180286789381,
    7079099162368739078,
    7079099146476586758,
    7079099180286772997,
    7079099146476570374,
    7079099162368722694,
    7079099146476553990,
    7079099180286756613,
    7079099162368706310,
    7079099146476537606,
    7079099180286740229,
    7079099162368689926,
    7079099146476521222,
    7078954101479982854,
    7079099162368673542,
    7078954101479966470,
    7078872212882736901,
    7079099146476504838,
    7078954101479950086,
    7078872212882720517,
    7079099146476488454,
    7078954101479933702,
    7078872212882704133,
    7079099146476472070,
    7078954101479917318,
    7078871627777197830,
    7078871627777181446,
    7078871352844896005,
    7078871288130946821,
]

cookies = {
    "passport_csrf_token": "3ef5c1f84a7c04cc70751c24cedcfa84",
    "passport_csrf_token_default": "3ef5c1f84a7c04cc70751c24cedcfa84",
    "lang_type": "en",
    "tt_webid": "7075200271135966725",
    "tta_attr_id": "0.1647325739.7075210174415241221",
    "tta_attr_id_mirror": "0.1647325739.7075210174415241221",
    "gftoken": "NjkxOTI4MDA4fDE2NDczMjU1NDAzMnx8MAcHBwcHBwc",
    "pre_country": "US",
    "s_v_web_id": "verify_l12y3upb_wv0ityJb_UQY7_4cQG_B2do_8gwFkF2wxQvn",
    "MONITOR_WEB_ID": "3511f2af-06ea-4447-9257-59b70d05b1f3",
    "shop_tiktok_oauth_state": "5af3356d58e5d7637ee7e5707dae8fe0bed08ae3a4b9892d",
    "csrftoken": "TNlXKVMVfJb34rSTWFqrFfohcPFHZSxN",
    "gfsitesid": "NjkxOTI4MDA4fDE2NDczMjU1NDAzMnx8MAcHBwcHBwc",
    "ac_csrftoken": "7584a378cb2645198c8ad892f6cf7463",
    "ttwid": "1%7CLTY93OS9qNluQ19cNYyiWbrGt2CO2j0zH6g_LR0_a3A%7C1649233063%7C6e47a8ff637debfcff2f6d22f15f5a6fcd4777fc4f5ddad6ea1ea68ed044b77b",
    "odin_tt": "d9b8ce590b840e6ab495d4ddb8fbb630f3b8b4e9cff72425e9a8e110e7966c4834895faa0218dde0504237299d1507642ead66949a048b7e9b056ece19aa599a",
    "sid_guard_ads": "ab60edc787260388deabddead30c91d5%7C1649233065%7C3870887%7CSat%2C+21-May-2022+03%3A32%3A32+GMT",
    "uid_tt_ads": "c15976d362d1a3cc72d243bceec48248d025c80a9c600bc09c2ee0b5a634d94f",
    "uid_tt_ss_ads": "c15976d362d1a3cc72d243bceec48248d025c80a9c600bc09c2ee0b5a634d94f",
    "sid_tt_ads": "ab60edc787260388deabddead30c91d5",
    "sessionid_ads": "ab60edc787260388deabddead30c91d5",
    "sessionid_ss_ads": "ab60edc787260388deabddead30c91d5",
    "sid_ucp_v1_ads": "1.0.0-KDMyZjQyMDIyMTVlY2U1YWIyNzY4YWNkMjY0ZmYyMjYzMGUzMDJkMDUKGgiGiKWKoujGtmAQqZm1kgYYrwwgDDgBQOsHEH4aB2JvZWkxOG4iIGFiNjBlZGM3ODcyNjAzODhkZWFiZGRlYWQzMGM5MWQ1",
    "ssid_ucp_v1_ads": "1.0.0-KDMyZjQyMDIyMTVlY2U1YWIyNzY4YWNkMjY0ZmYyMjYzMGUzMDJkMDUKGgiGiKWKoujGtmAQqZm1kgYYrwwgDDgBQOsHEH4aB2JvZWkxOG4iIGFiNjBlZGM3ODcyNjAzODhkZWFiZGRlYWQzMGM5MWQ1",
}

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    "Accept": "application/json, text/plain, */*",
    "X-CSRFToken": "TNlXKVMVfJb34rSTWFqrFfohcPFHZSxN",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
    "sec-ch-ua-platform": '"macOS"',
    "Origin": "https://boei18n-ads.byteoversea.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://boei18n-ads.byteoversea.net/catalogs/list",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

params = {
    "bc_id": "6954233589097562118",
}


def delete_dpa(dpa_id):
    try:
        res = requests.delete(
            f"https://boei18n-ads.byteoversea.net/api/v2/dpa/ec/platform/{dpa_id}/",
            headers=headers,
            params=params,
            cookies=cookies,
        )
        if res.ok:
            return True
        else:
            print("dpa_id id delete fail!")
            return False
    except Exception:
        print("dpa_id id delete fail!")
        return False


def worker(work_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            delete_dpa(item)
            work_queue.task_done()


def main():
    work_queue = Queue()
    for i in dpa_ids:
        work_queue.put(i)
    threads = [
        Thread(target=worker, args=(work_queue,)) for _ in range(THREAD_POOL_SIZE)
    ]
    for thread in threads:
        thread.start()
    work_queue.join()
    while threads:
        threads.pop().join()


if __name__ == "__main__":
    # for i in dpa_ids:
    #     response = requests.delete(f'https://boei18n-ads.byteoversea.net/api/v2/dpa/ec/platform/{i}/',
    #                                headers=headers, params=params, cookies=cookies)
    started = time.time()
    main()
    elapsed = time.time() - started
    print("Time elapsed: {:.2f}s".format(elapsed))
