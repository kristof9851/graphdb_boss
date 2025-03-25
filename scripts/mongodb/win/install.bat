@echo off
setlocal

set "MONGODB_ZIP_URL=https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-8.0.5.zip"
set "MONGODB_ZIP_FILENAME=mongodb-windows-x86_64-8.0.5.zip"
set "MONGODB_EXTRACT_DIR=mongodb-win32-x86_64-windows-8.0.5"
set "MONGOD_BINARY=mongod.exe"
set "MONGOD_SHORTCUT=.\mongod.lnk"

set "MONGO_SHELL_ZIP_URL=https://downloads.mongodb.com/compass/mongosh-2.4.0-win32-x64.zip"
set "MONGO_SHELL_ZIP_FILENAME=mongosh-2.4.0-win32-x64.zip"
set "MONGO_SHELL_BINARY=mongosh.exe"
set "MONGO_SHELL_EXTRACT_DIR=mongosh-2.4.0-win32-x64"
set "MONGO_SHELL_SHORTCUT=.\mongosh.lnk"


echo Checking if MongoDB is already downloaded...

:: Check if the MongoDB zip file already exists
if exist %MONGODB_ZIP_FILENAME% (
    echo MongoDB archive already exists.
) else (
    echo MongoDB archive not found. Downloading MongoDB...

    :: Download the MongoDB zip file
    powershell -Command "Invoke-WebRequest -Uri %MONGODB_ZIP_URL% -OutFile %MONGODB_ZIP_FILENAME%"
    if %errorlevel% neq 0 (
        echo Failed to download MongoDB.
        del %MONGODB_ZIP_FILENAME%
        exit /b 1
    )
)



echo Checking if MongoDB is already extracted...

:: Check if the MongoDB directory already exists
if exist %MONGODB_EXTRACT_DIR% (
    echo MongoDB is already extracted.
) else (
    echo Extracting MongoDB...

    :: Extract the zip file
    tar -xf "%MONGODB_ZIP_FILENAME%" -C "."
    @REM if %errorlevel% neq 0 (
    @REM     echo Failed to extract MongoDB.
    @REM     rmdir /S /Q "%MONGODB_EXTRACT_DIR%"
    @REM     exit /b 1
    @REM )
)



echo Checking if symlink already exists...

:: Check if the shortcut already exists
if exist %MONGOD_SHORTCUT% (
    echo MongoDB Shortcut already exists.
) else (
    echo Creating shortcut...

    :: Create the shortcut using PowerShell
    powershell -Command ^
        "$WScriptShell = New-Object -ComObject WScript.Shell;" ^
        "$Shortcut = $WScriptShell.CreateShortcut('%MONGOD_SHORTCUT%');" ^
        "$Shortcut.TargetPath = '%cd%\%MONGODB_EXTRACT_DIR%\bin\%MONGOD_BINARY%';" ^
        "$Shortcut.WorkingDirectory = '%cd%';" ^
        "$Shortcut.Save()"
    if %errorlevel% neq 0 (
        echo Failed to create shortcut.
        exit /b 1
    )
)



echo Checking if data directory exists...

:: Check if the data directory already exists
if exist data (
    echo Data directory already exists.
) else (
    echo Creating data directory...
    mkdir data
    if %errorlevel% neq 0 (
        echo Failed to create data directory.
        exit /b 1
    )
)



echo Checking if Mongo Shell is already downloaded...

:: Check if the Mongo Shell zip file already exists
if exist %MONGO_SHELL_ZIP_FILENAME% (
    echo Mongo Shell archive already exists.
) else (
    echo Mongo Shell archive not found. Downloading Mongo Shell...

    :: Download the Mongo Shell zip file
    powershell -Command "Invoke-WebRequest -Uri %MONGO_SHELL_ZIP_URL% -OutFile %MONGO_SHELL_ZIP_FILENAME%"
    if %errorlevel% neq 0 (
        echo Failed to download Mongo Shell.
        del %MONGO_SHELL_ZIP_FILENAME%
        exit /b 1
    )
)



echo Checking if Mongo Shell is already extracted...

:: Check if the Mongo Shell directory already exists
if exist %MONGO_SHELL_EXTRACT_DIR% (
    echo Mongo Shell is already extracted.
) else (
    echo Extracting Mongo Shell...

    :: Extract the zip file
    tar -xf "%MONGO_SHELL_ZIP_FILENAME%" -C "."
    @REM if %errorlevel% neq 0 (
    @REM     echo Failed to extract Mongo Shell.
    @REM     rmdir /S /Q "%MONGO_SHELL_EXTRACT_DIR%"
    @REM     exit /b 1
    @REM )
)



echo Checking if Mongo Shell shortcut already exists...

:: Check if the shortcut already exists
if exist %MONGO_SHELL_SHORTCUT% (
    echo Mongo Shell shortcut already exists.
) else (
    echo Creating Mongo Shell shortcut...

    :: Create the shortcut using PowerShell
    powershell -Command ^
        "$WScriptShell = New-Object -ComObject WScript.Shell;" ^
        "$Shortcut = $WScriptShell.CreateShortcut('%MONGO_SHELL_SHORTCUT%');" ^
        "$Shortcut.TargetPath = '%cd%\%MONGO_SHELL_EXTRACT_DIR%\bin\%MONGO_SHELL_BINARY%';" ^
        "$Shortcut.WorkingDirectory = '%cd%';" ^
        "$Shortcut.Save()"
    if %errorlevel% neq 0 (
        echo Failed to create Mongo Shell shortcut.
        exit /b 1
    )
)



echo MongoDB installed successfully.
endlocal
exit /b 0