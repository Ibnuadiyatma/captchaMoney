import os
from Session.login import clear_session_files, perform_login_prompt

def switch_account(session):
    print('\n=== GANTI AKUN ===')
    ok = input('Yakin ingin logout? (y/n): ').strip().lower()
    if ok not in ('y', 'yes'):
        print('Batal')
        return
    clear_session_files()
    print('Logout Berhasil, Silakan login ulang.')
    perform_login_prompt(session)
