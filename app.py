from flask import Flask, render_template
from flask import request, redirect, url_for
from mysql import connector

app = Flask(__name__)

db = connector.connect(
    host="wf01-b.h.filess.io",
    port=3306,
    user="db_akademik_processhas",
    passwd="0f89d9f5f67b3e3ebe6e617310683a030033ba19",
    database="db_akademik_processhas"
)

if db.is_connected():
    print("Berhasil Terhubung ke Database")


# READ - Menampilkan semua data
@app.route('/')
def halaman_awal():
    cur = db.cursor()
    cur.execute("SELECT * FROM mahasiswa")
    res = cur.fetchall()
    cur.close()
    return render_template('index.html', hasil=res)


# FORM TAMBAH
@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')


# PROSES TAMBAH
@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']

    cur = db.cursor()
    sql = "INSERT INTO mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)"
    cur.execute(sql, (nim, nama, asal))
    db.commit()
    cur.close()

    return redirect(url_for('halaman_awal'))


# FORM UBAH
@app.route('/ubah/<nim>')
def ubah_data(nim):
    cur = db.cursor()
    cur.execute("SELECT * FROM mahasiswa WHERE nim=%s", (nim,))
    res = cur.fetchone()
    cur.close()

    return render_template('ubah.html', hasil=res)


# PROSES UBAH
@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    nim_lama = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']

    cur = db.cursor()
    sql = "UPDATE mahasiswa SET nim=%s, nama=%s, asal=%s WHERE nim=%s"
    value = (nim, nama, asal, nim_lama)
    cur.execute(sql, value)
    db.commit()
    cur.close()

    return redirect(url_for('halaman_awal'))


# HAPUS DATA
@app.route('/hapus/<nim>')
def hapus_data(nim):
    cur = db.cursor()
    cur.execute("DELETE FROM mahasiswa WHERE nim=%s", (nim,))
    db.commit()
    cur.close()

    return redirect(url_for('halaman_awal'))


if __name__ == '__main__':
    app.run(debug=True)