#!/bin/bash
mongosh --eval "db.adminCommand({shutdown: 1})"
