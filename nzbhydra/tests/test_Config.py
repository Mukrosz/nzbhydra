from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# standard_library.install_aliases()
import json
import unittest
from pprint import pprint

import pytest
from builtins import *
import os
import copy
import shutil

from bunch import Bunch

from nzbhydra import config

print("Loading config from testsettings.cfg")

class TestConfig(unittest.TestCase):
    @pytest.fixture
    def setUp(self):
        if os.path.exists("testsettings.cfg"):
            os.remove("testsettings.cfg")
        shutil.copy("testsettings.cfg.orig", "testsettings.cfg")

    def testMigration3to4(self):
        testCfg = {
            "main":
                {
                    "configVersion": 3,
                    u"baseUrl": u"https://www.somedomain.com/nzbhydra"

                },
            "downloader": {
                "nzbAddingType": "redirect"
            }}

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = testCfg
            cfg["main"]["baseUrl"] = u"https://www.somedomain.com/nzbhydra"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(cfg["main"]["externalUrl"], "https://www.somedomain.com/nzbhydra")
        self.assertEqual(cfg["main"]["urlBase"], "/nzbhydra")

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = testCfg
            cfg["main"]["baseUrl"] = u"https://127.0.0.1/nzbhydra/"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(cfg["main"]["externalUrl"], "https://127.0.0.1/nzbhydra")
        self.assertEqual(cfg["main"]["urlBase"], "/nzbhydra")

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = testCfg
            cfg["main"]["baseUrl"] = u"https://www.somedomain.com/"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(cfg["main"]["externalUrl"], "https://www.somedomain.com")
        self.assertIsNone(cfg["main"]["urlBase"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = testCfg
            cfg["main"]["baseUrl"] = None
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertIsNone(cfg["main"]["externalUrl"])
        self.assertIsNone(cfg["main"]["urlBase"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = testCfg
            cfg["main"]["nzbAddingType"] = "direct"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual("redirect", cfg["downloader"]["nzbAddingType"])

    def testMigration8to9(self):
        testCfg = {
            "main": {
                "adminPassword": None,
                "adminUsername": None,
                "configVersion": 8,
                "enableAdminAuth": False,
                "enableAdminAuthForStats": False,
                "enableAuth": False,
                "password": None,
                "username": None
            }
        }

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(1, len(cfg["auth"]["users"]))
        self.assertIsNone(cfg["auth"]["users"][0]["username"])
        self.assertIsNone(cfg["auth"]["users"][0]["password"])
        self.assertTrue(cfg["auth"]["users"][0]["maySeeStats"])
        self.assertTrue(cfg["auth"]["users"][0]["maySeeAdmin"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            cfg["main"]["enableAuth"] = True
            cfg["main"]["username"] = "u"
            cfg["main"]["password"] = "p"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(1, len(cfg["auth"]["users"]))
        self.assertEqual("u", cfg["auth"]["users"][0]["username"])
        self.assertEqual("p", cfg["auth"]["users"][0]["password"])
        self.assertTrue(cfg["auth"]["users"][0]["maySeeStats"])
        self.assertTrue(cfg["auth"]["users"][0]["maySeeAdmin"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            cfg["main"]["enableAuth"] = True
            cfg["main"]["username"] = "u"
            cfg["main"]["password"] = "p"
            cfg["main"]["enableAdminAuth"] = True
            cfg["main"]["adminUsername"] = "au"
            cfg["main"]["adminPassword"] = "ap"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(2, len(cfg["auth"]["users"]))
        self.assertEqual("u", cfg["auth"]["users"][0]["username"])
        self.assertEqual("p", cfg["auth"]["users"][0]["password"])
        self.assertTrue(cfg["auth"]["users"][0]["maySeeStats"])
        self.assertEqual(False, cfg["auth"]["users"][0]["maySeeAdmin"])
        self.assertEqual("au", cfg["auth"]["users"][1]["username"])
        self.assertEqual("ap", cfg["auth"]["users"][1]["password"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeStats"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeAdmin"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            cfg["main"]["enableAuth"] = True
            cfg["main"]["username"] = "u"
            cfg["main"]["password"] = "p"
            cfg["main"]["enableAdminAuth"] = True
            cfg["main"]["enableAdminAuthForStats"] = True
            cfg["main"]["adminUsername"] = "au"
            cfg["main"]["adminPassword"] = "ap"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(2, len(cfg["auth"]["users"]))
        self.assertEqual("u", cfg["auth"]["users"][0]["username"])
        self.assertEqual("p", cfg["auth"]["users"][0]["password"])
        self.assertEqual(False, cfg["auth"]["users"][0]["maySeeStats"])
        self.assertEqual(False, cfg["auth"]["users"][0]["maySeeAdmin"])
        self.assertEqual("au", cfg["auth"]["users"][1]["username"])
        self.assertEqual("ap", cfg["auth"]["users"][1]["password"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeStats"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeAdmin"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            cfg["main"]["enableAuth"] = False
            cfg["main"]["enableAdminAuthForStats"] = False
            cfg["main"]["enableAdminAuth"] = True
            cfg["main"]["adminUsername"] = "au"
            cfg["main"]["adminPassword"] = "ap"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(2, len(cfg["auth"]["users"]))
        self.assertIsNone(cfg["auth"]["users"][0]["username"])
        self.assertIsNone(cfg["auth"]["users"][0]["password"])
        self.assertTrue(cfg["auth"]["users"][0]["maySeeStats"])
        self.assertFalse(cfg["auth"]["users"][0]["maySeeAdmin"])
        self.assertEqual("au", cfg["auth"]["users"][1]["username"])
        self.assertEqual("ap", cfg["auth"]["users"][1]["password"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeStats"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeAdmin"])

        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            cfg["main"]["enableAuth"] = False
            cfg["main"]["enableAdminAuth"] = True
            cfg["main"]["enableAdminAuthForStats"] = True
            cfg["main"]["adminUsername"] = "au"
            cfg["main"]["adminPassword"] = "ap"
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(2, len(cfg["auth"]["users"]))
        self.assertIsNone(cfg["auth"]["users"][0]["username"])
        self.assertIsNone(cfg["auth"]["users"][0]["password"])
        self.assertFalse(cfg["auth"]["users"][0]["maySeeStats"])
        self.assertFalse(cfg["auth"]["users"][0]["maySeeAdmin"])
        self.assertEqual("au", cfg["auth"]["users"][1]["username"])
        self.assertEqual("ap", cfg["auth"]["users"][1]["password"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeStats"])
        self.assertTrue(cfg["auth"]["users"][1]["maySeeAdmin"])

    def testMigration10to11(self):
        testCfg = {
            "main": {
                "configVersion": 10
            },
            "auth": {
                "users": [
                    {
                        "name": None
                    },
                    {
                        "name": "whatever"
                    }
                ]
            }
        }
        self.assertTrue("name" in testCfg["auth"]["users"][0].keys())
        self.assertTrue("name" in testCfg["auth"]["users"][1].keys())
        
        with open("testsettings.cfg", "wb") as settingsfile:
            cfg = copy.copy(testCfg)
            json.dump(cfg, settingsfile)
        cfg = config.migrate("testsettings.cfg")
        self.assertEqual(2, len(cfg["auth"]["users"]))
        self.assertIsNone(cfg["auth"]["users"][0]["username"])
        self.assertEqual("whatever", cfg["auth"]["users"][1]["username"])
        self.assertFalse("name" in cfg["auth"]["users"][0].keys())
        self.assertFalse("name" in cfg["auth"]["users"][1].keys())
        
        

    def testGetAnonymizedConfig(self):
        config.settings = {
            "downloader": {
                "nzbget": {
                    "host": "3.4.5.6",
                    "password": "nzbgetuser",
                    "username": "nzbgetpassword"
                },
                "sabnzbd": {
                    "apikey": "sabnzbdapikey",
                    "password": "sabnzbdpassword",
                    "url": "http://localhost:8080/sabnzbd/",
                    "username": "sabnzbduser"
                }
            },
            "indexers": {
                "newznab": [
                    {
                        "apikey": "newznabapikey",
                    },
                ],
                "omgwtfnzbs": {
                    "apikey": "omgwtfapikey",
                    "username": "omgwtfusername"
                }
            },
            "main": {
                "apikey": "hydraapikey",
                "externalUrl": "http://www.hydradomain.com/nzbhydra",
                "host": "1.2.3.4"
            },
            "auth": {
                "users": [
                    {
                        "username": "someuser",
                        "password": "somepassword"
                    }
                ]
            }
        }
        ac = config.getAnonymizedConfig()
        ac = Bunch.fromDict(ac)
        self.assertEqual("<OBFUSCATED:3f7ccf2fa729e7329f8d2af3ae5b2d00>", ac.indexers.newznab[0].apikey)
        self.assertEqual("<OBFUSCATED:be1cd7618f0bc25e333d996582c037b2>", ac.indexers.omgwtfnzbs.username)
        self.assertEqual("<OBFUSCATED:680eae14a056ebd0d1c71dbfb6c5ebbc>", ac.indexers.omgwtfnzbs.apikey)
        self.assertEqual("<IPADDRESS:6465ec74397c9126916786bbcd6d7601>", ac.main.host)
        self.assertEqual("<OBFUSCATED:b5f0bb7a7671d14f3d79866bcdfac6b5>", ac.main.apikey)
        self.assertEqual("http://<DOMAIN:ea2cbe92bacf786835b93ff2ca78c459>/nzbhydra", ac.main.externalUrl)
        self.assertEqual("<OBFUSCATED:25adeda6f43bf9adf9781d29d1435986>", ac.auth.users[0].username)
        self.assertEqual("<OBFUSCATED:9c42a1346e333a770904b2a2b37fa7d3>", ac.auth.users[0].password)
        self.assertEqual("<OBFUSCATED:df60a3d2b6cdc05d169e684c0aaa7b20>", ac.downloader.nzbget.username)
        self.assertEqual("<IPADDRESS:c6deeee6bee7ff3d4cc2048843f5678b>", ac.downloader.nzbget.host)
        self.assertEqual("<OBFUSCATED:78afef0fe4ffe1ed97aff6ab577ef5a4>", ac.downloader.nzbget.password)
        self.assertEqual("http://<NOTIPADDRESSORDOMAIN:421aa90e079fa326b6494f812ad13e79>:8080/sabnzbd/", ac.downloader.sabnzbd.url)
        self.assertEqual("<OBFUSCATED:96c4173454468a77d67b2c813ffe307a>", ac.downloader.sabnzbd.username)
        self.assertEqual("<OBFUSCATED:f5095bc1520183e76be64af1c5f9e7e3>", ac.downloader.sabnzbd.apikey)
        self.assertEqual("<OBFUSCATED:4c471a175d85451486af666d7eebe4f8>", ac.downloader.sabnzbd.password)

    