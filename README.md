# creating environment via cli
python -m venv env
source env/bin/activate

# uploading all required packages
pip install -r requirements.txt

# setting migrations
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb

# launching server
python manage.py runserver

(It's better to create products in advance)

POST for request, id must be the existing one
{
    "external_id": "PR-123-321-123",
    "details": [{
        "product": {"id": 4},
        "amount": 10,
        "price": "12.00"
    }]
}

accept and fail are used with speific order {id} 
then you can request POST with click and status will change







