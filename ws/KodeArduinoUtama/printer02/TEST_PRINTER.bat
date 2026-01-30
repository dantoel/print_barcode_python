@echo off
echo ====================================================================
echo PRINTER DIAGNOSTIC TOOL
echo ====================================================================
echo.
echo Akan mengecek:
echo 1. DLL file exists
echo 2. DLL bisa dimuat
echo 3. Printer bisa diinisialisasi
echo 4. Status printer (harus 1, bukan 8)
echo 5. Test print
echo.
pause
echo.

python test_printer_diagnostic.py
