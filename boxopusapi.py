#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pickle
import os
from lxml import etree
import json

BASE_URL = 'https://boxopus.com'

class Boxopus:

    session = requests.Session()

    headers = {
        'Origin': BASE_URL,
        'Refer': BASE_URL,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._initiate()

    def _save_cookies(self):
        cookies_file = '.{0}.cookies'.format(self.username)
        with open(cookies_file, 'w') as f:
            pickle.dump(
                requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def _load_cookies(self):
        cookies_file = '.{0}.cookies'.format(self.username)
        if os.path.exists(cookies_file):
            with open(cookies_file) as cookies_file:
                cookies = requests.utils.cookiejar_from_dict(
                    pickle.load(cookies_file))
                self.session.cookies = cookies
                return True
        else:
            return False

    def _initiate(self):
        if not self._load_cookies():
            self.session.get(BASE_URL, headers=self.headers)
            self._login()

    def _login(self):
        params = {
            '_username': self.username,
            '_password': self.password,
            '_remember_me': 'on',
            '_submit': 'Sign in'
        }
        ret = self.session.post('https://boxopus.com/login_check', headers=self.headers, data=params)
        doc = etree.HTML(ret.content)
        try:
            sign_title = doc.xpath('//title')[0].text
            if cmp(sign_title, 'Sign') == 0:
                print('登录失败')
            else:
                print('登录成功')
                self._save_cookies()
        except Exception, e:
            print(e)

    def _request(self, path, data=None, files=None, retries=3):
        try:
            url = BASE_URL + path
            if data is not None:
                return self.session.post(url, data=data, headers=self.headers)
            elif files is not None:
                return self.session.post(url, files=files, headers=self.headers)
            else:
                return self.session.get(url, headers=self.headers)
        except Exception, e:
            print(e)
            if retries > 0:
                return self._request(path, data, files, retries-1)
            else:
                print '请求失败', url

    def getTask(self):
        ret = self._request('/tasks')
        doc = etree.HTML(ret.content)
        items = doc.xpath('//div[@class="container pt"]//div[contains(@class,"torrent-item")]')
        downloaded = []
        downloading = []
        results = {'downloaded': downloaded, 'downloading': downloading}
        for item in items:
            try:
                name = item.xpath('.//h4[@class="name"]')[0].xpath('string(.)').strip()
                file_count = item.xpath('.//small//a/text()')[0].strip()
                status = item.xpath('.//small/text()')[2].strip()
                tid = item.xpath('.//div[@class="panel-footer"]/div/@id')[0]
                if 'progress' in tid:
                    link = item.xpath('.//div[@class="panel-footer"]/a/@href')[0]
            except Exception, e:
                print '解析出错, ' + str(e)
            finally:
                data = {'name': name,
                        'file_count': file_count,
                        'status': status}
                if 'progress' in tid:
                    data['link'] = link
                    downloaded.append(data)
                else:
                    data['hash'] = tid
                    downloading.append(data)
        return results

    def getTorrent(self, tpath):
        ret = self._request(tpath)
        doc = etree.HTML(ret.content)
        items = doc.xpath('//div[@class="file type-file"]')
        results = []
        for item in items:
            try:
                size = item.xpath('./span[@class="size"]/text()')[0]
                downlink = item.xpath('./span[@class="controls"]/a/@href')[0]
                name = item.xpath('./a/text()')[0]
            except Exception, e:
                print e
            finally:
                results.append({
                        'name': name,
                        'downlink': downlink,
                        'size': size
                    })
        return results

    def updateTaskInfo(self, items):
        params = {'hashes[]': [item['hash'] for item in items]}
        ret = self._request('/tasks/info', data=params)
        for info in json.loads(ret.content):
            for item in items:
                if cmp(info['hash'], item['hash']) == 0:
                    item['percentDone'] = info['percentDone']

    def uploadTorrent(self, name):
        files = {'form[file]': open(name, 'rb')}
        ret = self._request('/tasks', files=files)
        doc = etree.HTML(ret.content)
        return doc.xpath('//form[contains(@id,"torrent_form")]/@action')[0]

    def createTask(self, creatPath):
        self._request(creatPath, data={'storageId': 0, 'remoteBaseDir': 'Boxopus'})
