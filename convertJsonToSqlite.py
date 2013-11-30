import sqlite3
import json

def main():
    allShopInfo = json.load(open('all_shop.json'))

    con = sqlite3.connect('all_shop.sqlite')
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS `info`''')
    cur.execute('''CREATE TABLE `info` (`version` TEXT)''')
    cur.execute('''INSERT INTO `info` (`version`) VALUES (?)''', (allShopInfo['version'],))
    fieldnames = allShopInfo['shopList'][0].keys()
    shopTableCreateStatement = []
    shopTableCreateStatement.append('CREATE TABLE `shops` (')
    typeMapping = {'px': 'REAL', 'py': 'REAL'}
    prefix = ""
    for fieldname in fieldnames:
        if fieldname[0].isalpha() and fieldname.isalnum():
            shopTableCreateStatement.append(prefix + '`' + fieldname + '` ' + typeMapping.get(fieldname, 'TEXT'))
            prefix = ", "
    shopTableCreateStatement.append(')')
    cur.execute('DROP TABLE IF EXISTS `shops`')
    cur.execute(''.join(shopTableCreateStatement))

    shopInsertData = []
    for shop in allShopInfo['shopList']:
        shopData = []
        for fieldname in fieldnames:
            shopData.append(shop.get(fieldname, ''))
        shopInsertData.append(tuple(shopData))

    shopTableInsertStatement = []
    shopTableInsertStatement.append('INSERT INTO `shops` (')
    prefix = ""
    for fieldname in fieldnames:
        shopTableInsertStatement.append(prefix + '`' + fieldname + '`')
        prefix = ", "
    shopTableInsertStatement.append(') VALUES (')
    shopTableInsertStatement.append('?' + ' ,?' * (len(fieldnames) - 1))
    shopTableInsertStatement.append(')')

    cur.executemany(''.join(shopTableInsertStatement), shopInsertData)

    cur.close()
    con.commit()
    con.close()

if __name__ == '__main__':
    main()
