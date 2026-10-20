import json
import os
import pwinput
from prettytable import PrettyTable

FILE_KAMAR = "kamar.json"
FILE_RESERVASI = "reservasi.json"
FILE_AKUN = "akun.json"


def muat_data_akun():
    """Memuat data akun, jika gagal buat default sementara."""
    try:
        with open(FILE_AKUN, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_awal = {
            "admin": {"Admin1": "iniadmin"},
            "user": {}
        }
        with open(FILE_AKUN, "w", encoding="utf-8") as file:
            json.dump(data_awal, file, indent=4)
        return data_awal

def simpan_data_akun(data):
    with open(FILE_AKUN, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def muat_data_kamar():
    try:
        with open(FILE_KAMAR, "r", encoding="utf-8") as file:
            data = json.load(file)
            for hotel in ["Aston", "Mercure", "Harris"]:
                if hotel not in data:
                    data[hotel] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        data_awal = {"Aston": [], "Mercure": [], "Harris": []}
        simpan_data_kamar(data_awal)
        return data_awal

def simpan_data_kamar(data):
    with open(FILE_KAMAR, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def pilih_hotel():
    """Fungsi bantu untuk memilih hotel."""
    while True:
        print("\n=== PILIH HOTEL ===")
        print("1. Hotel Aston")
        print("2. Hotel Mercure")
        print("3. Hotel Harris")
        pilihan = input("Masukkan pilihan (1-3): ").strip()

        if not pilihan:
            print("[!] Pilihan tidak boleh kosong.")
            continue
            
        if pilihan == "1": return "Aston"
        elif pilihan == "2": return "Mercure"
        elif pilihan == "3": return "Harris"
        else: print("[!] Pilihan tidak valid. Harap masukkan angka 1 sampai 3.")

def registrasi():
    print("=" * 40)
    print("            REGISTRASI AKUN")
    print("=" * 40)
    akun = muat_data_akun()
    
    while True:
        print("Pilih Role:")
        print("1. User")
        print("2. Admin")
        role_pilihan = input("Masukkan pilihan (1/2): ").strip()
        
        if role_pilihan == "1":
            role = "user"
            break
        elif role_pilihan == "2":
            role = "admin"
            break
        else:
            print("[!] Pilihan role tidak valid. Masukkan 1 atau 2.")

    while True:
        username = input("Masukkan Username Baru: ").strip()
        if not username:
            print("[!] Username tidak boleh kosong.")
            continue
        if username in akun[role]:
            print("[!] Username sudah terdaftar! Silakan gunakan username lain.")
            return
        break

    while True:
        password = pwinput.pwinput("Masukkan Password Baru: ")
        if not password.strip():
            print("[!] Password tidak boleh kosong.")
            continue
        break
        
    akun[role][username] = password
    simpan_data_akun(akun)
    print(f"\n[Sukses] Akun {role.capitalize()} '{username}' berhasil didaftarkan!")

def login():
    akun = muat_data_akun()
    while True:
        print("=" * 40)
        print("             SILAHKAN LOGIN")
        print("=" * 40)
        username = input("Masukkan Username : ").strip()
        if not username:
            print("[!] Username tidak boleh kosong.")
            continue
            
        password = pwinput.pwinput("Masukkan Password : ")
        if not password:
            print("[!] Password tidak boleh kosong.")
            continue

        if username in akun["admin"] and akun["admin"][username] == password:
            print("\nLogin Berhasil sebagai Admin")
            return "admin", username
        elif username in akun["user"] and akun["user"][username] == password:
            print("\nLogin Berhasil sebagai User")
            return "user", username
        else:
            print("\n[!] Username atau Password salah. Silakan coba lagi.")

def tampilkan_kamar():
    data = muat_data_kamar()
    hotel = pilih_hotel()
    
    print("\n" + "="*50)
    print(f"            DAFTAR KAMAR HOTEL {hotel.upper()}            ")
    print("="*50)
    
    if not data[hotel]:
        print("[Info] Belum ada kamar di hotel ini.")
        return hotel, False

    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Kamar", "Tipe Kamar", "Harga", "Status"]
    
    for index, kamar in enumerate(data[hotel], start=1):
        tabel.add_row([index, kamar['nama'], kamar['tipe'], f"Rp {kamar['harga']:,}", kamar['status']])
    
    print(tabel)
    return hotel, True

def tambah_tipe_kamar():
    print("\n=== TAMBAH TIPE KAMAR BARU ===")
    data = muat_data_kamar()
    hotel = pilih_hotel()
    
    while True:
        nama_kamar = input("Masukkan Nama Kamar (Contoh: A1): ").strip()
        if not nama_kamar:
            print("[!] Nama kamar tidak boleh kosong.")
            continue
        break
        
    while True:
        tipe_kamar = input("Masukkan Tipe Kamar (Contoh: Exclusive): ").strip()
        if not tipe_kamar:
            print("[!] Tipe kamar tidak boleh kosong.")
            continue
        break
    
    while True:
        try:
            harga_kamar = int(input("Masukkan Harga Kamar : "))
            if harga_kamar < 0:
                print("[!] Harga kamar tidak boleh bernilai negatif.")
                continue
            break
        except ValueError:
            print("[!] INPUT HARUS BERUPA ANGKA")

    kamar_baru = {
        "nama": nama_kamar,
        "tipe": tipe_kamar,
        "harga": harga_kamar,
        "status": "Tersedia"
    }
    
    data[hotel].append(kamar_baru)
    simpan_data_kamar(data)
    print(f"\n[Sukses] Kamar '{nama_kamar}' berhasil ditambahkan ke Hotel {hotel}!")

def ubah_kamar():
    print("\n=== UBAH HARGA & STATUS KAMAR ===")
    data = muat_data_kamar()
    hotel, ada_data = tampilkan_kamar()
    
    if not ada_data: return

    try:
        pilihan = int(input("Masukkan NOMOR kamar yang ingin diubah (berdasarkan tabel): "))
        indeks = pilihan - 1 
        
        if 0 <= indeks < len(data[hotel]):
            kamar_terpilih = data[hotel][indeks]
            print(f"\nMengubah data untuk {kamar_terpilih['nama']}")
            
            harga_baru = input(f"Masukkan harga baru (tekan Enter jika tetap {kamar_terpilih['harga']}): ").strip()
            if harga_baru:
                if harga_baru.isdigit():
                    harga_val = int(harga_baru)
                    if harga_val >= 0:
                        kamar_terpilih['harga'] = harga_val
                        print("--> Harga berhasil diperbarui.")
                    else:
                        print("[!] Harga tidak boleh negatif. Harga diabaikan.")
                else:
                    print("[!] Input harga harus berupa angka. Harga diabaikan.")
            
            print(f"Status saat ini: {kamar_terpilih['status']}")
            print("Pilih Status Baru (1. Tersedia / 2. Tidak Tersedia)")
            status_pilihan = input("Masukkan pilihan (1/2 atau tekan Enter jika tetap): ").strip()
            
            if status_pilihan == "1":
                kamar_terpilih['status'] = "Tersedia"
                print("--> Status berhasil diubah menjadi Tersedia.")
            elif status_pilihan == "2":
                kamar_terpilih['status'] = "Tidak Tersedia"
                print("--> Status berhasil diubah menjadi Tidak Tersedia.")
            elif status_pilihan == "":
                pass
            else:
                print("[!] Pilihan status tidak valid. Status tidak diubah.")
                
            simpan_data_kamar(data)
            print("\n[Sukses] Data kamar berhasil diperbarui!")
        else:
            print("\n[!] Nomor kamar tidak valid.")
    except ValueError:
        print("\n[!] Harap masukkan angka yang valid.")

def hapus_kamar():
    print("\n=== HAPUS KAMAR ===")
    data = muat_data_kamar()
    hotel, ada_data = tampilkan_kamar()
    
    if not ada_data: return

    try:
        pilihan = int(input("Masukkan NOMOR kamar yang ingin dihapus (0 untuk batal): "))
        if pilihan == 0: return
        
        indeks = pilihan - 1
        
        if 0 <= indeks < len(data[hotel]):
            kamar_dihapus = data[hotel].pop(indeks) 
            simpan_data_kamar(data)
            print(f"\n[Sukses] Kamar '{kamar_dihapus['nama']}' berhasil dihapus dari Hotel {hotel}!")
        else:
            print("\n[!] Nomor kamar tidak valid.")
    except ValueError:
        print("\n[!] Harap masukkan angka yang valid.")

def lihatreservasi():
    print("\n" + "=" * 60)
    print("                        DATA RESERVASI CUSTOMER")
    print("=" * 60)
    
    try:
        with open(FILE_RESERVASI, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[Info] Belum ada data reservasi atau file tidak ditemukan.")
        return

    if not data:
        print("[Info] Belum ada reservasi.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Customer", "Hotel", "Kamar", "Tipe"]
    
    for idx, i in enumerate(data, start=1):
        nama_hotel = i.get('hotel', 'Tidak Diketahui') 
        tabel.add_row([idx, i.get('nama', '-'), nama_hotel, i.get('kamar', '-'), i.get('tipe', '-')])
        
    print(tabel)

def lihat_kamar_tersedia():
    """1. Lihat daftar kamar yang statusnya Tersedia beserta harga."""
    data = muat_data_kamar()
    hotel = pilih_hotel()
    
    print("\n" + "=" * 55)
    print(f"       DAFTAR KAMAR TERSEDIA DI HOTEL {hotel.upper()}       ")
    print("=" * 55)
    
    kamar_tersedia = [k for k in data[hotel] if k.get('status', '').lower() == 'tersedia']
    
    if not kamar_tersedia:
        print(f"[Info] Mohon maaf, saat ini belum ada kamar yang tersedia di Hotel {hotel}.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Kamar", "Tipe Kamar", "Harga", "Status"]
    
    for index, kamar in enumerate(kamar_tersedia, start=1):
        tabel.add_row([index, kamar['nama'], kamar['tipe'], f"Rp {kamar['harga']:,}", kamar['status']])
    
    print(tabel)

def pesan_kamar(username_login):
    """2. Memesan kamar (menambah data reservasi ke json & mengubah status kamar)."""
    print("\n=== PEMESANAN KAMAR HOTEL ===")
    data_kamar = muat_data_kamar()
    hotel = pilih_hotel()
    
    kamar_tersedia = [k for k in data_kamar[hotel] if k.get('status', '').lower() == 'tersedia']
    
    if not kamar_tersedia:
        print(f"[Info] Tidak ada kamar yang tersedia di Hotel {hotel} untuk dipesan.")
        return

    print(f"\n--- DAFTAR KAMAR TERSEDIA DI {hotel.upper()} ---")
    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Kamar", "Tipe Kamar", "Harga"]
    for idx, k in enumerate(kamar_tersedia, start=1):
        tabel.add_row([idx, k['nama'], k['tipe'], f"Rp {k['harga']:,}"])
    print(tabel)

    try:
        pilihan = int(input("Masukkan NOMOR kamar yang ingin dipesan (0 untuk batal): "))
        if pilihan == 0:
            return
        
        indeks = pilihan - 1
        if 0 <= indeks < len(kamar_tersedia):
            kamar_dipilih = kamar_tersedia[indeks]
            
            while True:
                konfirmasi = input(f"Yakin ingin memesan kamar {kamar_dipilih['nama']} ({kamar_dipilih['tipe']})? (y/t): ").strip().lower()
                if konfirmasi in ['y', 't']:
                    break
                print("[!] Masukkan pilihan yang valid ('y' atau 't').")
                
            if konfirmasi != 'y':
                print("[Info] Pemesanan dibatalkan.")
                return

            data_baru_reservasi = {
                "username": username_login,
                "nama": username_login,
                "hotel": hotel,
                "kamar": kamar_dipilih['nama'],
                "tipe": kamar_dipilih['tipe'],
                "harga": kamar_dipilih['harga']
            }

            try:
                with open(FILE_RESERVASI, "r", encoding="utf-8") as f:
                    data_reservasi = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data_reservasi = []

            data_reservasi.append(data_baru_reservasi)

            with open(FILE_RESERVASI, "w", encoding="utf-8") as f:
                json.dump(data_reservasi, f, indent=4, ensure_ascii=False)

            for k in data_kamar[hotel]:
                if k['nama'] == kamar_dipilih['nama']:
                    k['status'] = "Tidak Tersedia"
                    break
            
            simpan_data_kamar(data_kamar)
            print(f"\n[Sukses] Kamar {kamar_dipilih['nama']} di Hotel {hotel} berhasil dipesan!")
        else:
            print("[!] Nomor kamar tidak valid.")
    except ValueError:
        print("[!] Harap masukkan angka yang valid.")

def lihat_reservasi_sendiri(username_login):
    """3. Melihat reservasi milik user yang sedang login."""
    print("\n" + "=" * 60)
    print(f"            RIWAYAT RESERVASI ATAS NAMA: {username_login}            ")
    print("=" * 60)
    
    try:
        with open(FILE_RESERVASI, "r", encoding="utf-8") as f:
            data_reservasi = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[Info] Belum ada data reservasi.")
        return

    reservasi_user = [r for r in data_reservasi if r.get('username') == username_login]

    if not reservasi_user:
        print("[Info] Anda belum memiliki riwayat reservasi kamar.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["No", "Hotel", "Nama Kamar", "Tipe Kamar", "Harga"]
    
    for idx, r in enumerate(reservasi_user, start=1):
        tabel.add_row([idx, r.get('hotel', '-'), r.get('kamar', '-'), r.get('tipe', '-'), f"Rp {r.get('harga', 0):,}"])
        
    print(tabel)

def batalkan_reservasi(username_login):
    """4. Membatalkan reservasi (hapus dari json & kembalikan status kamar jadi Tersedia)."""
    print("\n=== BATALKAN RESERVASI KAMAR ===")
    
    try:
        with open(FILE_RESERVASI, "r", encoding="utf-8") as f:
            data_reservasi = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[Info] Belum ada data reservasi.")
        return

    reservasi_user = [r for r in data_reservasi if r.get('username') == username_login]

    if not reservasi_user:
        print("[Info] Anda tidak memiliki reservasi untuk dibatalkan.")
        return

    print("Daftar Reservasi Anda:")
    tabel = PrettyTable()
    tabel.field_names = ["No", "Hotel", "Nama Kamar", "Tipe Kamar"]
    for idx, r in enumerate(reservasi_user, start=1):
        tabel.add_row([idx, r.get('hotel', '-'), r.get('kamar', '-'), r.get('tipe', '-')])
    print(tabel)

    try:
        pilihan = int(input("Masukkan NOMOR reservasi yang ingin dibatalkan (0 untuk batal): "))
        if pilihan == 0:
            return

        indeks = pilihan - 1
        if 0 <= indeks < len(reservasi_user):
            target_batal = reservasi_user[indeks]
            
            while True:
                konfirmasi = input(f"Yakin ingin membatalkan reservasi kamar {target_batal['kamar']} di {target_batal['hotel']}? (y/t): ").strip().lower()
                if konfirmasi in ['y', 't']:
                    break
                print("[!] Masukkan pilihan yang valid ('y' atau 't').")
                
            if konfirmasi != 'y':
                print("[Info] Pembatalan dibatalkan.")
                return

            data_reservasi.remove(target_batal)
            with open(FILE_RESERVASI, "w", encoding="utf-8") as f:
                json.dump(data_reservasi, f, indent=4, ensure_ascii=False)

            data_kamar = muat_data_kamar()
            hotel_target = target_batal['hotel']
            nama_kamar_target = target_batal['kamar']

            if hotel_target in data_kamar:
                for k in data_kamar[hotel_target]:
                    if k['nama'] == nama_kamar_target:
                        k['status'] = "Tersedia"
                        break
                simpan_data_kamar(data_kamar)

            print(f"\n[Sukses] Reservasi kamar {nama_kamar_target} berhasil dibatalkan!")
        else:
            print("[!] Nomor reservasi tidak valid.")
    except ValueError:
        print("[!] Harap masukkan angka yang valid.")

def user_menu(username_login):
    """Menu Utama khusus User."""
    while True:
        print("\n" + "=" * 35)
        print(f"       MENU USER ({username_login})")
        print("=" * 35)
        print("1. Lihat Daftar Kamar Tersedia & Harga")
        print("2. Memesan Kamar")
        print("3. Melihat Reservasi Sendiri")
        print("4. Membatalkan Reservasi")
        print("0. Logout")

        try:
            pilihan = int(input("Pilih menu: "))
            if pilihan == 1:
                lihat_kamar_tersedia()
            elif pilihan == 2:
                pesan_kamar(username_login)
            elif pilihan == 3:
                lihat_reservasi_sendiri(username_login)
            elif pilihan == 4:
                batalkan_reservasi(username_login)
            elif pilihan == 0:
                print("\nKeluar dari menu user...")
                break
            else:
                print("[!] Pilihan tidak valid.")
        except ValueError:
            print("[!] INPUT HARUS BERUPA ANGKA")
        except KeyboardInterrupt:
            print("\n[!] Jangan menekan CTRL + C!")

def admin():
    while True:
        print("\n" + "="*30)
        print("        MENU ADMIN")
        print("="*30)
        print("1. Tambah Kamar Baru")
        print("2. Lihat Semua Kamar")
        print("3. Lihat Daftar Reservasi")
        print("4. Ubah Harga dan Status Kamar")
        print("5. Hapus Data Kamar")
        print("0. Logout")

        try:
            pilihan = int(input("Pilih menu : "))
            if pilihan == 1: tambah_tipe_kamar()
            elif pilihan == 2: tampilkan_kamar()
            elif pilihan == 3: lihatreservasi()
            elif pilihan == 4: ubah_kamar()
            elif pilihan == 5: hapus_kamar()
            elif pilihan == 0:
                print("\nKeluar dari menu admin...")
                break
            else:
                print("[!] Pilihan tidak valid.")
        except ValueError:
            print("[!] INPUT HARUS BERUPA ANGKA")
        except KeyboardInterrupt:
            print("\n[!] Jangan menekan CTRL + C!")

def menu_awal():
    while True:
        print("\n" + "="*40)
        print("    SISTEM RESERVASI HOTEL MULTI")
        print("="*40)
        print("1. Login")
        print("2. Registrasi Akun")
        print("0. Keluar Aplikasi")
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            role, username = login()
            if role == "admin":
                admin()
            elif role == "user":
                user_menu(username)
        elif pilihan == "2":
            registrasi()
        elif pilihan == "0":
            print("\nTERIMA KASIH TELAH MENGGUNAKAN APLIKASI INI.")
            break
        else:
            print("[!] Pilihan tidak valid.")

if __name__ == "__main__":
    menu_awal()