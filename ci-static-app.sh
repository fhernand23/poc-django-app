echo "==============================="
echo "CI STATIC ANALYSIS: APP0"
echo "==============================="
code=0
# export MYPYPATH=plugins/platform-auth/src:app0-admin/src/ && python3 -m mypy --install-types --namespace-packages --non-interactive -p app0.admin
# export MYPYPATH=plugins/platform-auth/src:app0-admin/src/ && python3 -m mypy --namespace-packages -p app0.admin
code+=$?
python3 -m flake8 --max-line-length=120 django_project/
python3 -m flake8 --max-line-length=120 accounts/
python3 -m flake8 --max-line-length=120 pages/
python3 -m flake8 --max-line-length=120 products/
code+=$?
python3 -m pylint django_project
python3 -m pylint accounts
python3 -m pylint pages
python3 -m pylint products
code+=$?
if [ $code -gt 0 ]
then
  echo "[FAILED] CI STATIC ANALYSIS: APP0"
fi
echo "========================================================================================================"
exit $code
