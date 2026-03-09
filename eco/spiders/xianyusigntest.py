import requests


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.goofish.com",
    "priority": "u=1, i",
    "referer": "https://www.goofish.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
cookies = {
    "cna": "3LKTICSXsjgBASQIgiCsWUn8",
    "cookie2": "1f7c10e4298b190a6f465d0c945a6171",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "c6dff575a401ee4923ee85fd45b913a3_1766485417037",
    "_m_h5_tk_enc": "91cf968a56eed9de0962f5c03e3ccf0d",
    "xlly_s": "1",
    "tfstk": "gdFsQEYbRhxs4g7ODh7eA-YQhahf8w5yGEgYrrdwkfh9DnU-YloZ_ZfjDlmU_czZ6F234zda_Oc2GfcmMgSPa_zQSjcAKNkSfhDKS4C2BIHtsX3x4zdPa_zgWFuOzyCzQ9Yn4qoxMAHv9pnnWVpYDApKvD0mkh3v6waKxD3vDxdvJy3jkK3YDjQQJD0xMVExBwaKxqhxDxwk4q_qfP_P_iocTt-4RDOvMWgdm0U6WC3u9VOKvPiCmiVBZAi8WDOAXSTBMmi3wMWQ-JeTb2qfNMG0x-ExlkKd0A4Ydkg_bgtm054aGcz1BMUItcZtCJ_JI2aU1rwxdNCTRfisUSE9kdG_HlVjIRTcryhTx8moB9jnR5Prh0DBvGUURcH7hlSHMcy7JkMzTHRrik2YDqZpfgzea09NXKTIEIgI4w_BnKDBjom0VnotcA3n5X_CRhGKB20I4w_BnKDt-2JCRwts9"
}
url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlehome.home.webpc.feed/1.0/"
params = {
    "jsv": "2.7.2",
    "appKey": "34839810",
    "t": "1766475813310",
    "sign": "1b7b084d1616b45e27aa4b11f01a06f7",
    "v": "1.0",
    "type": "originaljson",
    "accountSite": "xianyu",
    "dataType": "json",
    "timeout": "20000",
    "api": "mtop.taobao.idlehome.home.webpc.feed",
    "sessionOption": "AutoLoginOnly",
    "spm_cnt": "a21ybx.home.0.0"
}
data = {
    "data": "{\"itemId\":\"\",\"pageSize\":30,\"pageNumber\":1,\"machId\":\"168395_1\"}"
}
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

print(response.text)
print(response)