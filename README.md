## Welcome!
This is **Jeff's Flask Starter App**.

###### Features:

- Authentication and RBAC using Flask-user
- User management, sign-up, login, change password, forgot password
- Admin interface using Flask-admin
- Error logging; error mailing
- Cosmetics using Flask-Bootstrap
- Modular using Blueprints
- Database migrations with SQLAlchemy/Alembic

###### Steps:
1. python manage.py init_db
2. flask db init
3. flask db migrate
4. flask db upgrade
5. edit config.py; set USER_APP_NAME