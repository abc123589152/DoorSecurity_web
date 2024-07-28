from flask import Flask, render_template, request, redirect, url_for,jsonify
from model.dbconnect import get_db_connection
from mysql.connector import Error
from model.getdatanowtime import get_now_time
from model.dbconnect_query import dbConnect_query
from model.dbconnect_new import dbConnect_new
from model.dbconnect_noparams import dbConnect_noparams
app = Flask(__name__,template_folder="templates",static_folder='static',static_url_path='/')
dbip = '192.168.1.186'
@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route('/employ')
def employ():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employ")
    employ = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('employ.html', employ=employ)

@app.route('/employinsert',methods=['GET','POST'])
def employinsert():
    door_group_name_list = []
    door_group_remark_list = []
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    get_door_group = conn.cursor(dictionary=True)
    get_door_group_remark = conn.cursor(dictionary=True)
    try:
        #取的目前有設定的door groupname到door_group_name_list裡面
        get_door_group.execute("select groupname from doorgroup")
        get_door_group_name = get_door_group.fetchall()
        for door_group in get_door_group_name:
            door_group_name_list.append(door_group['groupname'])
        #取得目前的門組備註說明
        get_door_group_remark.execute("select remark from doorgroup")
        get_door_group_remark1 = get_door_group_remark.fetchall()
        for door_group_remark in get_door_group_remark1:
            door_group_remark_list.append(door_group_remark['remark'])  
        
    except Error as e:
        return str(f"讀取資料庫發生問題請查看log:{e}")
    if request.method == 'POST':
        try:
            username = request.form['username']
            cardnumber = request.form['cardnumber']
            doorgroup = ','.join(request.form.getlist('doorgroup'))
            # status = request.form['status']
            # activation = request.form['activation']
            # expiration = request.form['expiration']
            remark = request.form['remark']
            creation_time = request.form['creation_time']
            cursor.execute("""
                insert into employ(username,cardnumber,doorgroup,remark,creation_time)
                values(%s,%s,%s,%s,%s)
            """, (username, cardnumber,doorgroup,remark,creation_time))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('employ'))
        except Error as e:
            return str(f"讀取資料庫發生問題請查看log:{e}")
    return render_template('permition/employInsert.html',now_time=get_now_time(),door_group_name_list=door_group_name_list,door_group_remark_list=door_group_remark_list)





@app.route('/employedit/<int:id>', methods=['GET', 'POST'])
def employedit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    get_door_group = conn.cursor(dictionary=True)
    check_door_group_conn = conn.cursor(dictionary=True)
    get_door_group_remark_conn = conn.cursor(dictionary=True)
    door_group_name_list = []
    door_group_remark_list = []
    check_door_group = ''
    try:
        #取得所有employ的資訊
        cursor.execute("SELECT * FROM employ WHERE id = %s", (id,))
        employ = cursor.fetchone()
        get_door_group.execute("select groupname from doorgroup")
        get_door_group_name = get_door_group.fetchall()
        #取得在doorgroup裡面的groupname
        for door_group in get_door_group_name:
            door_group_name_list.append(door_group['groupname'])
        check_door_group_conn.execute("select doorgroup from employ where id = %s",(id,))
        #取得目前在人員資料裡面的doorgroup
        check_door_group_name = check_door_group_conn.fetchall()
        for check_door in check_door_group_name:
            check_door_group = check_door['doorgroup'].split(",")
        #取得doorgrroup裡面的備註項目
        get_door_group_remark_conn.execute("select remark from doorgroup")
        get_door_group_remark = get_door_group_remark_conn.fetchall()
        for get_door_remark in get_door_group_remark:
            door_group_remark_list.append(get_door_remark['remark'])
        
    except Error as e:
        return str(f"讀取資料庫發生問題請查看log:{e}")
    if request.method == 'POST':
        username = request.form['username']
        cardnumber = request.form['cardnumber']
        doorgroup = ','.join(request.form.getlist('doorgroup'))
        # status = request.form['status']
        # activation = request.form['activation']
        # expiration = request.form['expiration']
        remark = request.form['remark']
        creation_time = request.form['creation_time']
        modification_time = request.form['modification_time']
        cursor.execute("""
            UPDATE employ 
            SET username = %s, cardnumber = %s,doorgroup=%s,remark= %s, creation_time = %s ,
            modification_time= %s
            WHERE id = %s
        """, (username, cardnumber,doorgroup,remark,creation_time,modification_time, id))
        conn.commit()
        return redirect(url_for('employ'))

   
    cursor.close()
    conn.close()
    return render_template('employEdit.html', employ=employ,now_time=get_now_time(),door_group_name_list=door_group_name_list,check_door_group=check_door_group,door_group_remark_list=door_group_remark_list)
    #return str(door_group_name_list)

@app.route('/employdelete/<int:id>', methods=['GET', 'POST'])
def employdelete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            delete from employ where id = %s
        """, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('employ'))
    except Error as e:
        return str(f'刪除資料失敗請返回後再嘗試：{e}')



@app.route('/doorsetting')
def doorsetting():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doorsetting")
    doorsetting = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('doorsetting.html', doorsetting=doorsetting)

@app.route('/doorsettinginsert',methods=['GET','POST'])
def doorsettinginsert():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
            try:
                control = request.form['control']
                wiegand = request.form['wiegand']
                door = request.form['door']
                # door_sensor = request.form['door_sensor']
                door_lock = request.form['door_lock']
                reset_time = request.form['reset_time']
                remark = request.form['remark']
                creation_time = request.form['creation_time']
                
                cursor.execute("""
                    insert into doorsetting(control,wiegand,door,door_lock,reset_time,remark,creation_time)
                    values(%s,%s,%s,%s,%s,%s,%s)
                """, (control, wiegand,door,door_lock,reset_time,remark,creation_time))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('doorsetting'))
            except Error as e:
                return str(f"讀取資料庫發生問題請查看log:{e}")
    return render_template('doors/doorsettingInsert.html',now_time=get_now_time())

@app.route('/doorsettingedit/<int:id>', methods=['GET', 'POST'])
def doorsettingedit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        control = request.form['control']
        wiegand = request.form['wiegand']
        door = request.form['door']
        # door_sensor = request.form['door_sensor']
        door_lock = request.form['door_lock']
        reset_time = request.form['reset_time']
        remark = request.form['remark']
        creation_time = request.form['creation_time']
        modification_time = request.form['modification_time']
        cursor.execute("""
            UPDATE doorsetting 
            SET control = %s, wiegand = %s, door=%s,door_lock=%s,reset_time=%s,remark= %s,creation_time = %s ,
            modification_time= %s
            WHERE id = %s
        """, (control, wiegand,door,door_lock,reset_time,remark,creation_time,modification_time, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('doorsetting'))
        
    cursor.execute("SELECT * FROM doorsetting WHERE id = %s", (id,))
    doorsetting = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('doorsettingEdit.html', doorsetting=doorsetting,now_time=get_now_time())

@app.route('/doorsettingdelete/<int:id>', methods=['GET', 'POST'])
def doorsettingdelete(id):
    checklist = []
    try:
        #獲取id的門號碼
        select_door_name = dbConnect_new("select door from doorsetting where id = %s",(id,))              
        #update doorgroup裡面有包含此門的訊息
        update_doorgrroup_doornamelist = dbConnect_new("select id,doorname from doorgroup where doorname like %s",('%'+select_door_name[0][0]+'%',))
        #Check是否是空的，如果是則不做下面更新door動作
        if update_doorgrroup_doornamelist != []:
            for get_id_door_name in update_doorgrroup_doornamelist:
                update_doorgroup_doorname = ','.join([door for door in get_id_door_name[1].split(',') if door != 'D532'])
                dbConnect_query("UPDATE doorgroup SET doorname = %s WHERE id = %s",(update_doorgroup_doorname,get_id_door_name[0]))
        #刪除此項目
        dbConnect_query("delete from doorsetting where id = %s",(id,))
        return redirect(url_for('doorsetting'))
    except Error as e:
        return str(f'刪除資料失敗請返回後再嘗試：{e}')
@app.route('/doorgroup')
def doorgroup():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doorgroup")
    doorgroup = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('permition/doorgroup.html', doorgroup=doorgroup)

@app.route('/doorgroupinsert',methods=['GET','POST'])
def doorgroupinsert():
    door_name = []
    door_remark = []
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    get_door = conn.cursor(dictionary=True)
    get_door_name_conn = conn.cursor(dictionary=True)
    try:
        #取的目前doorsetting裡面的door所有門號
        get_door.execute("select *from doorsetting")
        doorname = get_door.fetchall()
        for dname in doorname:
            door_name.append(dname['door'])
            door_remark.append(dname['remark'])
        #取的門的名稱
        
    except Error as e:
        return str(f"讀取資料庫發生問題請查看log:{e}")

    if request.method == 'POST':
            try:
                groupname = request.form['groupname']
                doorname = ','.join(request.form.getlist('doorname'))
                remark = request.form['remark']
                creation_time = request.form['creation_time']
                cursor.execute("""
                    insert into doorgroup(groupname,doorname,remark,creation_time)
                    values(%s,%s,%s,%s)
                """, (groupname, doorname,remark,creation_time))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('doorgroup'))
            except Error as e:
                return str(f"網頁發生錯誤請返回重新嘗試:{e}")
    return render_template('permition/doorgroupinsert.html',now_time=get_now_time(),door_name=door_name,door_remark=door_remark)

@app.route('/doorgroupedit/<int:id>',methods=['GET','POST'])
def doorgroupedit(id):
    door_name = []
    door_remark = []
    check_doornumber_list = ""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    get_door = conn.cursor(dictionary=True)
    check_door_group_permit_doornumber = conn.cursor(dictionary=True)
    try:
        #取的目前doorsetting裡面的door所有門號
        get_door.execute("select *from doorsetting")
        doorname = get_door.fetchall()
        for dname in doorname:
            door_name.append(dname['door'])
            door_remark.append(dname['remark'])
        check_door_group_permit_doornumber.execute("select doorname from doorgroup where id = %s",(id,))
        check_doorname = check_door_group_permit_doornumber.fetchall()
        #從id選擇是哪一個群組授權的doorname全部去出來放到check_doornumber_list裡面
        for ch_dname in check_doorname:
            check_doornumber_list = ch_dname['doorname'].split(',')
        #取得目前id有的doorgroup資料
        get_doorgroup_all_colume = conn.cursor(dictionary=True)
        get_doorgroup_all_colume.execute("Select *from doorgroup where id = %s",(id,))
        get_doorgroup_all = get_doorgroup_all_colume.fetchone()
    except Error as e:
        return str(f"讀取資料庫發生問題請查看log:{e}")

    if request.method == 'POST':
            try:
                groupname = request.form['groupname']
                doorname = ','.join(request.form.getlist('doorname'))
                remark = request.form['remark']
                creation_time = request.form['creation_time']
                modification_time = request.form['modification_time']
                cursor.execute("""
                    update doorgroup set groupname = %s,doorname=%s,remark=%s,creation_time=%s,modification_time=%s
                    where id = %s
                """, (groupname, doorname,remark,creation_time,modification_time,id))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('doorgroup'))
            except Error as e:
                return str(f"網頁發生錯誤請返回重新嘗試:{e}")
    return render_template('permition/doorgroupedit.html',now_time=get_now_time(),door_name=door_name,check_doornumber_list=check_doornumber_list,get_doorgroup_all=get_doorgroup_all,door_remark=door_remark)

@app.route('/doorgroupdelete/<int:id>', methods=['GET', 'POST'])
def doorgroupdelete(id):
    try:
        #獲取id的門群組號碼
        select_door_group_name = dbConnect_new("select groupname from doorgroup where id = %s",(id,))              
        #update employ 裡面有包含此門群組的訊息
        update_employ_doorgrouplist = dbConnect_new("select id,doorgroup from employ where doorgroup like %s",('%'+select_door_group_name[0][0]+'%',))
        #Check是否是空的，如果是則不做下面更新employ doorgroup動作
        if update_employ_doorgrouplist != []:
            for get_id_door_name in update_employ_doorgrouplist:
                 update_doorgroup_employ = ','.join([doorgroup for doorgroup in get_id_door_name[1].split(',') if doorgroup != select_door_group_name[0][0]])
                 dbConnect_query("UPDATE employ SET doorgroup = %s WHERE id = %s",(update_doorgroup_employ,get_id_door_name[0]))
        #刪除此項目
        dbConnect_query("delete from doorgroup where id = %s",(id,))
        return redirect(url_for('doorgroup'))
    except Error as e:
        return str(f'刪除資料失敗請返回後再嘗試：{e}')
    

@app.route('/swipecardlog')
def swipecard():
    swipecardlog = dbConnect_noparams("select *from swipeCardLog order by id desc")
    # conn = get_db_connection()
    # cursor = conn.cursor(dictionary=True)
    # cursor.execute("SELECT * FROM swipeCardLog")
    # swipecardlog = cursor.fetchall()
    # cursor.close()
    # conn.close()
    return render_template('doors/swipecardlog.html', swipecardlog=swipecardlog)
    #return str(swipecardlog)

@app.route('/swipecardlogreturn',methods=['GET'])
def swipecardlogreturn():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM swipeCardLog where DATE(swipetime) = CURDATE() order by id desc")
    swipecardlog = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(swipecardlog)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
