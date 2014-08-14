#! /usr/bin/env python
import MySQLdb as db
import math
import sys
import time
import threading
import mysql.connector
import MySQLdb
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter,con,query):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.query = query
        self.con =con
        self.error_mes = None
        self.dataObj = dataEncaptulation()
    def run(self):
        threadLock.acquire()
        print "Starting " + self.name
        # Get lock to synchronize threads
        operator = self.con.cursor()
    
#    try:
        try:
            operator.execute(self.query)
            data = operator.fetchall()
            success = 1
            print('execution done')
        except mysql.connector.Error as err:
            self.error_mes = "Something went wrong: {}".format(err)
            success = 0
            #self.con.rollback()
            #self.con.close()
            operator.close()
            del operator
            threadLock.release()
            return 
        except MySQLdb.Error, e:
            #self.con.rollback()
            #self.con.close()
            operator.close()
            del operator
            self.error_mes = "MySQL Error: %s" + str(e)
            threadLock.release()
            #print "MySQL Error: %s" % str(e)
            return
        
        for row in data:
            tempList= []
            for col in row:
                tempList.append(col)
            self.dataObj.data.append(tempList)
        operator.close()
        del operator
        del data
        #return self.dataObj
       
        #print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

threadLock = threading.Lock()
threads = []

# Create new threads

class dataEncaptulation(object):
    #data = []
    dict_data = {}
    #userName=None
    #passwd =None
    def __init__(self):
        self.data = []
        self.userName=None
        self.passwd =None
        return
def start_processing_thread(con,query):
    thread1 = myThread(1, "Thread-1", 1,con,query[0])
    thread2 = myThread(2, "Thread-2", 2,con,query[1])
    thread3 = myThread(3, 'Thread-3', 3,con,query[2])
    thread4 = myThread(4, 'Thread-4', 4,con,query[3])

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    con.close()
    if(len(thread2.dataObj.data) != 0):
        thread1.dataObj.data.extend(thread2.dataObj.data)
    if(len(thread3.dataObj.data) != 0):
        thread1.dataObj.data.extend(thread3.dataObj.data)
    if(len(thread4.dataObj.data) != 0):
        thread1.dataObj.data.extend(thread4.dataObj.data)
    for thread_com in threads:
        if(thread_com.error_mes != None):
            return thread_com.error_mes
        else:
            print(thread_com)
            print(thread_com.dataObj.data)
  
    print "Exiting main Thread"
    
    if(len(thread1.dataObj.data) == 0):
        return None
    return thread1.dataObj
def creatingTable(table_name,number_of_attrib,attribList,operator):
    operator.execute('DROP TABLE IF EXISTS '+ table_name)
    string_To_execute = 'create table '+ table_name+' ('
    for elem in range(0,len(attribList)):
        if(elem == 0):
            string_To_execute += attribList[elem][0]+' '+attribList[elem][1] +' not null auto_increment'
        else:
            string_To_execute += attribList[elem][0] + ' '+ attribList[elem][1]
        if(elem == len(attribList)-1):
            string_To_execute += ', primary key ('+attribList[0][0]+'))'
        else:
            string_To_execute +=', '
#    operator.execute('create table '+table_name+' ('+ attribList[0][0] +' '+ attribList[0][1]+', '+attribList[1][0]+' '+ attribList[1][1]+')')
    operator.execute(string_To_execute)
    return
def showColumns(table_name,con):
    operator = con.cursor()
    string_To_execute = 'show columns from ' + table_name
    operator.execute(string_To_execute)
    data = operator.fetchall()
    for datum in data:
        print('attribute name = %s, attribute type = %s, attribute other info =%s, attribute4 info=%s, attribute info =%s \n' % (datum[0],datum[1],datum[2],datum[3],datum[4]))
    return
def showTable(table_name,con):
    try:
        operator = con.cursor()
        string_To_execute = 'select count(*) from ' + table_name
        result    = operator.execute(string_To_execute)
        data = operator.fetchall()
        for datum in data:
            print('No of records in the table are: '+str(datum[0]))
    except:
        print('cursor has not been opened')
    
    return
def getConnector(username= None,passwd = None,machine='localhost',databaseName = None,port=None):
    con = db.connect(machine,username,passwd,databaseName)
    return con
def other_query_execution(query,conn):
    cur_ = conn.cursor()
    try:
        cur_.execute(query)
        conn.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        success = 0
        conn.rollback()
        conn.close()
        return "Something went wrong: {}".format(err)
    except MySQLdb.Error, e:
        print "MySQL Error: %s" % str(e)
        conn.rollback()
        conn.close()
        return "Something went wrong: {}".format(e) 
    return 1
def insertData(table_name,con,_data):#tableName,con,list_data):
    operator = con.cursor()
    #print('Enter the employee name: ')
    #name = sys.stdin.readline()
    #print('Enter the age of employee: ')
    #age = sys.stdin.readline()
    #print('Enter the experience of employee(can be fraction): ')
    #experience = sys.stdin.readline()
    #print('Enter type of employee: ')
    #Type = sys.stdin.readline()
    success = 0
    #print(list_data)
    #print(list_data[9]+' '+list_data[0]+' '+list_data[1]+' '+ list_data[2]+' '+str(list_data[3])+' '+list_data[4]+' '+str(list_data[5])+' '+str(list_data[6])+' '+str(list_data[7])+' '+str(list_data[8]))
    for each in _data:
        if(len(each) == 0):
            break
        list_data = each.strip().split('\t')
        if(table_name == 'branch'):
            string_To_execute = 'insert into '+ table_name +' (branchID,name_state,zip) values ( '+list_data[0] +', "'+ list_data[1]+'", "'+ list_data[2]+'")'
        elif(table_name == 'customer'):
            string_To_execute = 'insert into '+ table_name +' (customerID,branchID,acctype,balance) values ( '+list_data[0] +', '+ list_data[1]+', "'+ list_data[2]+'", '+list_data[3]+')'
        else:
            string_To_execute = 'insert into '+ table_name +' (employeeID,branchID,emplname,empfname,salary) values ( '+list_data[0] +', '+ list_data[1]+', "'+ list_data[2]+'", "'+list_data[3]+'", '+list_data[4] +')'
        # + str(list_data[2]) +', '+ str(list_data[3])+', "'+list_data[4]+'", '+ str(list_data[5])+', '+str(list_data[6])+', '+str(list_data[7])+', '+str(list_data[8])+')'
    
        try:
            operator.execute(string_To_execute)
            success = 1
            print('execution done')
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            success = 0
            con.rollback()
            con.close()
            return "Something went wrong: {}".format(err)
        except MySQLdb.Error, e:
            print "MySQL Error: %s" % str(e)
            con.rollback()
            con.close()
            return "Something went wrong: {}".format(e)
    con.commit()
    operator.close()
    con.close()
    return success
def fetchData(con,sqlquery):
    operator = con.cursor()
    dataObj = dataEncaptulation()
    print(sqlquery)
    stringElem=""
    print(sqlquery)
    try:
        operator.execute(sqlquery)
        success = 1
        print('execution done')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        success = 0
        #con.rollback()
        #con.close()
        return "Something went wrong: {}".format(err)
    except MySQLdb.Error, e:
        #con.rollback()
        #con.close()
        print "MySQL Error: %s" % str(e)
        return "Something went wrong: {}".format(e)
    data = operator.fetchall()
    print(data)
    if(len(data) == 0):
        return None
    for row in data:
        tempList= []
        for col in row:
            tempList.append(col)
        dataObj.data.append(tempList)
        # name = row[0]
        # password = row[1]
        # dept1 = row[2]
        # dept2 = row[3]
        # dept3 = row[4]
        # dept4 = row[5]
        # dept5 = row[6]
        # print('name = %s password = %s dept1 = %s dept2=%s dept3=%s dept4=%s dept5=%s type[1 means Regular and 0 means Temporary]' % (name,password,dept1,dept2,dept3,dept4,dept5))
    #print(dataObj.data)
    operator.close()
    del operator
    del data
    print(dataObj.data)
    con.close()
    return dataObj
#    except Exception:
#        print(Exception.message)
    

def __main1__():
    print('enter the tableName: ')
    table_name = sys.stdin.readline()
    number_of_attrib = input('Enter the number of attrib: ')
    attribList = []
    attribTypeList = []
    for i in range(0,number_of_attrib):
        print('Enter the attrib name: ')
        attrib = sys.stdin.readline()
        attribList.append(attrib.rstrip())
        print('Enter the attrib data type: ')
        attrib_type = sys.stdin.readline()
        attribTypeList.append(attrib_type.rstrip())
    zipped = zip(attribList,attribTypeList)
    con = getConnector(machine = '10.10.10.101',username = 'sabbir',passwd = '33C_JNh',databaseName='sabbir')
    operator = con.cursor()
    creatingTable(table_name.rstrip(),number_of_attrib,zipped,operator)
    con.close()
    return table_name

def __main__():
    #global tableName
    tableName = 'employee'
#    con = getConnector(username ='sabbir',passwd='33C_JNh',databaseName='sabbir')
    while(True):
        option = input('choose option \n, [1 for table creation \n, 2 for getting number of records \n, 3 for data insertion \n, 4 for fetching all data \n, 5 for displaying table attribute]')
        con = getConnector(machine = '10.10.10.101',username='sabbir',passwd='33C_JNh',databaseName='sabbir')
        if(option == 1 ):
            tableName = __main1__()
        elif(option == 2):
            showTable(tableName,con.cursor())
        elif(option == 3):
            insertData(tableName,con)
        elif(option == 4):
            fetchData(tableName,con)
        elif(option ==5):
            showColumns(tableName,con)
        else:
            break
    return
#__main__()
