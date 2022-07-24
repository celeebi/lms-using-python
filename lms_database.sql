show schemas;
create schema library;
use library;

show tables;
drop table anggota;
drop table buku;
drop table pinjaman;

create table anggota (
	id_anggota int not null auto_increment primary key,
	nama_user varchar(50),
    tanggal_lahir date,
    pekerjaan varchar(50),
    alamat varchar(50)
);
create table buku (
	id_buku int primary key,
    nama_buku varchar(50),
    kategori_buku varchar(50),
    stok_buku int
);


create table pinjaman (
	id_peminjam int,
	id_buku int
);

ALTER TABLE pinjaman ADD FOREIGN KEY (id_peminjam) REFERENCES anggota (id_anggota);
ALTER TABLE pinjaman ADD FOREIGN KEY (id_buku) REFERENCES buku (id_buku);
alter table pinjaman add column tanggal_pinjaman date;
alter table pinjaman add column tanggal_pengembalian date;
insert into buku values 
(1001, "pipti sades of grey", "blue", 200),
(1002, "cara membuat rakitan", "misc", 5);
						;


insert into anggota (nama_user, tanggal_lahir, pekerjaan, alamat)
values 
('doni', '2000-05-05', 'pengangguran', 'jakarta'),
("farhan", '2000-03-05', 'pengangguran', 'jakarta');


-- below unessential to the db, just scratch
select * from buku where nama_buku='cara membuat rakitan';
select nama_user from anggota where id_anggota=1;
select * from buku;
select stok_buku-5 from buku where id_buku=1001;
select nama_buku from buku where id_buku=1001;
select * from buku;
update buku set stok_buku= where id_buku=1001; 

select * from anggota;
insert into pinjaman (id_peminjam, id_buku, tanggal_pinjaman, tanggal_pengembalian) 
value (2, 1002,curdate(), date_add(curdate(), interval 1 week)); -- pinjaman
select * from pinjaman;
delete from pinjaman where id_peminjam=1 and id_buku=1002; -- pengembalian

select p.id_peminjam, p.id_buku, a.nama_user, b.nama_buku, p.tanggal_pinjaman, p.tanggal_pengembalian 
from pinjaman p
left join buku b
on p.id_buku=b.id_buku
left join anggota a
on p.id_peminjam=a.id_anggota;
select * from anggota;
delete from buku where id_buku=1001;