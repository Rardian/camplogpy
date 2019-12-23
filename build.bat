pyinstaller --noconfirm --log-level=WARN ^
    -w ^
    -i resources\cllogo.ico ^
    -n CamplogAnalyzer ^
    --add-binary="resources/cllogo.ico;resources" ^
    --add-binary="images/*;images" ^
    main.py