setlocal

echo Shutting down MongoDB...

.\mongo.lnk --eval "db.adminCommand({shutdown: 1})"

endlocal