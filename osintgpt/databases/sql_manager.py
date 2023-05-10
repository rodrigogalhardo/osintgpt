# -*- coding: utf-8 -*-

# =================================================================================
# osintgpt
#
# Author: @estebanpdl
# 
# File: sql_manager.py
# Description: SQLDatabaseManager provides an abstracted interface for interacting
#   with various SQL databases. The class encapsulates database connection,
#   table creation, and data insertion operations.
# =================================================================================

# import modules
import os
import sqlite3

# import submodules
from sqlite3 import Error

# type hints
from typing import List, Optional

# import exceptions
from osintgpt.exceptions.errors import MissingEnvironmentVariableError

# SQLDatabaseManager class
class SQLDatabaseManager(object):
    '''
    SQLDatabaseManager class

    This class provides an abstracted interface for interacting with various SQL
    databases
    '''
    # constructor
    def __init__(self, env_file_path: str):
        '''
        constructor
        '''
        # set database file path
        self.db_file = os.getenv('SQL_DB_FILE_PATH')
        if not self.db_file:
            raise MissingEnvironmentVariableError('SQL_DB_FILE_PATH')
        
        # set database connection
        self.conn = self.create_connection(self.db_file)

        # create main chat gpt index table
        self._create_chat_gpt_index_table()

        # create chat gpt conversations table
        self._create_chat_gpt_conversations_table()
    
    # create connection
    def create_connection(self, db_file: str):
        '''
        create connection

        Args:
            db_file (str): database file path

        Returns:
            conn (sqlite3.Connection): database connection
        '''
        # set connection
        conn = None

        # try to connect to database
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print (e)
        
        # return connection
        return conn

    # get connection'
    def get_connection(self):
        '''
        get connection

        Returns:
            conn (sqlite3.Connection): database connection
        '''
        # return connection
        return self.conn
    
    # create main chat gpt index table
    def _create_chat_gpt_index_table(self):
        '''
        create table
        '''
        # set cursor
        cursor = self.conn.cursor()

        # try to create table
        try:
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS chat_gpt_index (
                    id text NOT NULL PRIMARY KEY,
                    created_at VARCHAR (20) NOT NULL
                );
                '''
            )

            # commit changes
            self.conn.commit()
        
        except Error as e:
            print (f"The error '{e}' occurred")
    
    # create chat gpt conversations table
    def _create_chat_gpt_conversations_table(self):
        '''
        create chat gpt conversations table
        '''
        # set cursor
        cursor = self.conn.cursor()

        # try to create table
        try:
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS chat_gpt_conversations (
                    id text PRIMARY KEY,
                    chat_id text NOT NULL,
                    role text NOT NULL,
                    message text NOT NULL
                );
                '''
            )

            # commit changes
            self.conn.commit()
        
        except Error as e:
            print (f"The error '{e}' occurred")
    
    # insert chat gpt data
    def insert_data_to_chat_gpt_index(self, id: str, created_at: str):
        '''
        insert data to chat gpt index table

        Args:
            id (str): conversation id
            created_at (str): created at
        '''
        # set cursor
        cursor = self.conn.cursor()

        # try to insert data
        try:
            cursor.execute(
                '''
                INSERT INTO chat_gpt_index (id, created_at)
                VALUES (?, ?)
                ''',
                (id, created_at)
            )

            # commit changes
            self.conn.commit()
        
        except Error as e:
            print (f"The error '{e}' occurred")
            self.conn.rollback()
    
    # insert chat gpt conversations
    def insert_data_to_chat_gpt_conversations(self, id: str, chat_id: str,
        role: str, message: str):
        '''
        insert data to chat gpt conversations table

        Args:
            id (str): conversation id
            chat_id (str): chat id
            role (str): role
            message (str): message
        '''
        # set cursor
        cursor = self.conn.cursor()

        # try to insert data
        try:
            cursor.execute(
                '''
                INSERT INTO chat_gpt_conversations (id, chat_id, role, message)
                VALUES (?, ?, ?, ?)
                ''',
                (id, chat_id, role, message)
            )

            # commit changes
            self.conn.commit()
        
        except Error as e:
            print (f"The error '{e}' occurred")
            self.conn.rollback()
