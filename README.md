# environment-variables-action

## env vars

    DB_DATABASE=driveshare
    DB_ENGINE=django.db.backends.mysql
    DB_USER=root
    DB_PASS=root
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_AUTH_PLUGIN=mysql_native_password

    SITE_ID=10

    URL_SUCCESS_SIGNIN=http://127.0.0.1:5173
    LOGIN_REDIRECT_URL=/social-signin

    ALLOWED_ORIGINS=http://127.0.0.1:5173,http://127.0.0.1:8000,http://127.0.0.1:4000

## definition

    DB_DATABASE=<database-name>
    DB_ENGINE=django.db.backends.mysql
    DB_USER=<database-user>
    DB_PASS=<database-password>
    DB_HOST=<database-host>
    DB_PORT=<database-port>
    DB_AUTH_PLUGIN=mysql_native_password

    SITE_ID=<site-id-for-django-social-auth!>

    URL_SUCCESS_SIGNIN=<url-home-redirect-after-login>
    LOGIN_REDIRECT_URL=/social-signin

    ALLOWED_ORIGINS=<coma-separated-list-of-allowed-origins>
