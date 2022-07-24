import mysql.connector 
from mysql.connector import Error
import pandas as pd
from IPython.display import display

def create_server_connection(host_name, user_name, user_password):
    connection = None
    
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print("MySQL connection successful")
    except Error as err:
        print(f"Error: {err}")
    return connection


# Fungsi membuat database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database berhasil dibuat")
    except Error as err:
        print(f"Error: {err}")


# Fungsi Koneksi ke database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
        print("MySQL database connection successfull")
    except Error as err:
        print(f"Error: {err}")
    return connection
        
# Fungsi untuk Eksekusi Query, Create, Update, Delete, Insert table and data
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query berhasil dieksekusi")
    except Error as err:
        print(f"Error: {err}")

# FUngsi Read Query
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result)
    except Error as err:
        print(f"Error: {err}")

user = 'root'
pw = "428o3545"
host = "localhost"
db = "library"
#connecting to our local sql server
connection =create_server_connection(host_name=host,
                                     user_name=user,
                                     user_password=pw)
#connecting to library database

connection = create_db_connection(host_name=host, 
                                  user_name=user, 
                                  user_password=pw, 
                                  db_name=db)

def pendaftaran_user():
    nama=input("Masukan nama user:")
    tgl_lahir=input("Masukan tanggal lahir(YYYY-MM-DD):")
    pekerjaan=input("Pekerjaan:")
    alamat=input("Masukan Alamat:")
    sql_query="insert into anggota (nama_user, tanggal_lahir, pekerjaan, alamat) values ('{}','{}','{}','{}')".format(nama,tgl_lahir,pekerjaan,alamat)
    execute_query(connection, sql_query)
       
    
def pendaftaran_buku():
    kode_buku=input("Masukan kode buku:")
    name=input("Enter book name:")
    kategori=input("Masukan kategori buku:")
    stok=input("Stok Buku:")
    sql_query="insert into buku values ({},'{}','{}',{})".format(kode_buku,
                                                             name,
                                                             kategori,
                                                             stok)
    execute_query(connection, sql_query)
    
def daftar_buku():
    sql_query="select * from buku;"
    df=read_query(connection, sql_query)
    df.rename(
    columns={0:"id buku",
             1:"Nama Buku",
             2:"genre",
             3:"stok"
            }
          ,inplace=True)
    display(df)
    print("\n")
    print("\n")
    
    
    
def daftar_user():
    sql_query="select * from anggota;"
    df=read_query(connection, sql_query)
    df.rename(
    columns={0:"id anggota",
             1:"Nama Member",
             2:"tanggal lahir",
             3:"pekerjaan",
             4:"asal"
            }
          ,inplace=True)
    display(df)
    print("\n")
    print("\n")

def peminjaman():
    id_peminjam=input("Masukan id peminjam:")
    id_buku=input("Masukan id buku:")
    #call nama peminjam
    sql_query="select nama_user from anggota where id_anggota={};".format(id_peminjam)
    nama_peminjam=read_query(connection, sql_query)[0].iloc[0]
    #call nama buku
    sql_query="select nama_buku from buku where id_buku={};".format(id_buku)
    nama_buku= read_query(connection, sql_query)[0].iloc[0]
    sql_query="insert into pinjaman (id_peminjam, id_buku, tanggal_pinjaman, tanggal_pengembalian) value ({}, {}, curdate(), date_add(curdate(), interval 1 week));".format(id_peminjam, id_buku)
    execute_query(connection, sql_query)
    print("Nama peminjam: {}".format(nama_peminjam))
    print("Nama buku: {}".format(nama_buku))
    print("............................................")
    print("Buku dipinjamkan ke : {}".format(nama_peminjam))
    print("............................................")
    sql_query="select stok_buku-1 from buku where id_buku={};".format(id_buku)
    sisa_stok=read_query(connection, sql_query)[0].iloc[0]
    sql_query="update buku set stok_buku={} where id_buku={};".format(sisa_stok, id_buku)
    execute_query(connection, sql_query)
    
def daftar_peminjaman():
    sql_query="select p.id_peminjam, p.id_buku, a.nama_user, b.nama_buku, p.tanggal_pinjaman, p.tanggal_pengembalian from pinjaman p left join buku b on p.id_buku=b.id_buku left join anggota a on p.id_peminjam=a.id_anggota;"
    df=read_query(connection, sql_query)
    df.rename(
    columns={0:"id anggota",
             1:"id buku",
             2:"Nama Anggota",
             3:"judul buku",
             4:"tanggal pinjaman",
             5:"tanggal pengembalian"
            }
          ,inplace=True)
    display(df)
    print("\n")
    print("\n")
    
def cari_buku():
    nama_buku=input("Masukan nama buku:")
    sql_query="select * from buku where nama_buku={};".format(nama_buku)
    try: 
        df=read_query(connection, sql_query)
        df.rename(
        columns={0:"id buku",
                 1:"Nama Buku",
                 2:"genre",
                 3:"stok"
                }
              ,inplace=True)
        display(df)
    except:
        print("Buku yang anda cari tidak ada")
    print("\n")
    print("\n")
    
def pengembalian():
    id_anggota=input("Masukan id peminjam:")
    id_buku=input("Masukan id buku:")
    sql_query="delete from pinjaman where id_peminjam={} and id_buku={}".format(id_anggota,id_buku)
    execute_query(connection, sql_query)
    sql_query="select stok_buku+1 from buku where id_buku={};".format(id_buku)
    tambahan_stok=read_query(connection, sql_query)[0].iloc[0]
    sql_query="update buku set stok_buku={} where id_buku={};".format(tambahan_stok, id_buku)
    execute_query(connection, sql_query)
    
def exit():
    print("terimakasih telah menggunakan LMS")
    
    
stored_func={1:pendaftaran_user, 
             2:pendaftaran_buku, 
             3:peminjaman,
             4:daftar_buku,
             5:daftar_user,
             6:daftar_peminjaman,
             7:cari_buku,
             8:pengembalian,
             9:exit
            }
_input =0
while _input != 9:
    print("----------- Library Management System -----------")
    print("     1. Pendaftaran User Baru")
    print("     2. Pendaftaran Buku Baru")
    print("     3. Peminjaman")
    print("     4. Tampilkan Daftar Buku")
    print("     5. Tampilkan Daftar User")
    print("     6. Tampilkan Daftar Peminjaman")
    print("     7. Cari buku")
    print("     8. Pengembalian")
    print("     9. Exit")
    
    _input=int(input("Masukan Nomor Tugas:"))
    assert _input>0 and _input<10, "Nomor tugas hanya 1-9"
    stored_func[_input]()
        