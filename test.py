

if __name__ == "__main__":

    a = dict()
    if not a:
        print("aa")
    else:
        print("bb")

    a["0"] = 2
    if not a:
        print("aa")
    else:
        print("bb")
    a["1"] = 1


    sql_template = "UPDATE information SET {} = %s WHERE id = {}"
    sql = sql_template.format(', '.join(a.keys()), 2)
    print(sql)

    params = list(a.values())[0]
    print(len(a.values()))


