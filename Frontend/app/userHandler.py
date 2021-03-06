from app import sql
from app import emailer
from app import passHandler
from app import eventHandler
import datetime


def createUser(email, fName, lName, rawPass):
    exists = getUser(email)
    if exists == ():
        hashedPass = passHandler.getHash(rawPass)
        query = "insert into Users(userID,FName,LName,Pass) values (%s,%s,%s,%s)"
        values = (email, fName, lName, hashedPass)
        sql.createQuery(query, values)
        return True
    else:
        return False


def getUser(userID):
    query = "select FName, LName, userID from Users where userID = %s"
    values = (userID,)
    return sql.getQueryResults(query, values)


def editFirstName(fName, email):
    query = "update Users set FName = %s where userID = %s"
    values = (fName, email)
    sql.createQuery(query, values)


def getFirstName(userID):
    query = "select FName from Users where userID = %s"
    values = (userID,)
    return sql.getQueryResults(query, values)


def editLastName(lName, email):
    query = "update Users set LName = %s where userID = %s"
    values = (lName, email)
    sql.createQuery(query, values)


def getLastName(userID):
    query = "select LName from Users where userID = %s"
    values = (userID,)
    return sql.getQueryResults(query, values)


def getName(userID):
    return getFirstName(userID)[0][0] + ' ' + getLastName(userID)[0][0]


def editName(fName, lName, email):
    query = "update Users set FName = %s, LName = %s where userID = %s"
    values = (fName, lName, email)
    sql.createQuery(query, values)


def updatePassword(email, oldPass, newPass):
    if(passHandler.confirmPass(email, oldPass)):
        pwd = passHandler.getHash(newPass)
        query = "update Users set Pass = %s where userID = %s"
        values = (email, pwd)
        sql.createQuery(query, values)


def requestReset(email):
    emailer.emailRecovery(email)


def checkForReset(key, email):
    query = "select validator, date from passReset where userID = %s"
    values = (email,)
    result = sql.getQueryResults(query, values)
    validator = result[0]
    date = result[1]
    if(key == validator):
        if ((date - datetime.datetime.now()).getseconds() < 3600):
            return True
        else:
            return False
    else:
        return False


def resetPassword(key, email, newPass):
    if(checkForReset(key, email)):
        query = "delete from passReset where validator = %s"
        values = (key,)
        sql.createQuery(query, values)
        pwd = passHandler.getHash(newPass)
        query = "update Users set Pass = %s where userID = %s"
        values = (email, pwd)
        sql.createQuery(query, values)
        return True
    return False


def deleteUser(userID):
    eventHandler.deleteEventByCreator(userID)
    query = "delete from Users where userID=%s"
    values = (userID, )
    sql.createQuery(query, values)
