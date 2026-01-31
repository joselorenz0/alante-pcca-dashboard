#!/bin/bash
cd /Users/Jose/Desktop/alante_dashboard_cleaned
rm -rf .git
git init
git remote add origin https://github.com/joselorenz0/alante-dashboard.git
git add -A
git commit -m "Fix dashboard: restore HTML templates, add Benchmark/Variance columns, 50 patients"
git branch -M main
git push -u origin main --force
