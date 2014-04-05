#! /usr/bin/env python
"""
Copyright (C) 2014 CompleteDB LLC.

This program is free software: you can redistribute it and/or modify
it under the terms of the Apache License Version 2.0 http://www.apache.org/licenses.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

"""

import unittest
import time
from pubsubsql import Client

class TestClient(unittest.TestCase):
    """MAKE SURE TO RUN PUBSUBSQL SERVER!"""

    def __ADDRESS(self):
        return "localhost:7777"

    def __generateTableName(self):
        return "T" + str(int(round(time.time() * 1000)))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnectDisconnect(self):
        client = Client()
        #
        client.connect(self.__ADDRESS())
        self.assertTrue(client.isConnected())
        client.disconnect()
        #
        with self.assertRaises(Exception):
            client.connect("addresswithnoport")
        self.assertFalse(client.isConnected())
        client.disconnect()
        #
        with self.assertRaises(Exception):
            client.connect("addresswithnoport:")
        self.assertFalse(client.isConnected())
        client.disconnect()
        #
        with self.assertRaises(Exception):
            client.connect("localhost:7778")
        self.assertFalse(client.isConnected())
        client.disconnect()

    def testExecuteStatus(self):
        client = Client()
        client.connect(self.__ADDRESS())
        #
        client.execute("status")
        self.assertEqual("status", client.getAction())
        client.disconnect()

    def testExecuteInvalidCommand(self):
        client = Client()
        client.connect(self.__ADDRESS())
        #
        with self.assertRaises(Exception):
            client.execute("blablabla")

    def testInsertOneRow(self):
        client = Client()
        client.connect(self.__ADDRESS())
        tableName = self.__generateTableName()
        command = "insert into {} (col1, col2, col3) values (1:col1, 1:col2, 1:col3) returning *".format(tableName)
        client.execute(command)
        self.assertEqual("insert", client.getAction())
        self.assertEqual(1, client.getRowCount())
        self.assertTrue(client.nextRow())
        #
        self.assertFalse(client.nextRow())
        client.disconnect()

if __name__ == "__main__":
    unittest.main()
